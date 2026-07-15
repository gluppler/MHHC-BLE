#!/usr/bin/env python3
"""Inspect ESP-IDF images and partition tables without external packages."""

from __future__ import annotations

import argparse
import hashlib
import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path


IMAGE_MAGIC = 0xE9
APP_DESC_MAGIC = 0xABCD5432
PARTITION_MAGIC = 0x50AA
PARTITION_MD5_MAGIC = 0xEBEB

SPI_MODES = {
    0: "QIO",
    1: "QOUT",
    2: "DIO",
    3: "DOUT",
    4: "FAST_READ",
    5: "SLOW_READ",
}
SPI_SPEEDS = {0x0: "40 MHz", 0x1: "26.7 MHz", 0x2: "20 MHz", 0xF: "80 MHz"}
FLASH_SIZES = {
    0x0: "1 MB",
    0x1: "2 MB",
    0x2: "4 MB",
    0x3: "8 MB",
    0x4: "16 MB",
    0x5: "32 MB",
    0x6: "64 MB",
    0x7: "128 MB",
}
CHIP_IDS = {
    0: "ESP32",
    2: "ESP32-S2",
    4: "ESP32-C3",
    5: "ESP32-S3",
    9: "ESP32-C2",
    12: "ESP32-C6",
    13: "ESP32-H2",
    16: "ESP32-P4",
    18: "ESP32-C5",
    20: "ESP32-C61",
}


class FormatError(ValueError):
    """Raised when an input is not a structurally valid supported image."""


@dataclass(frozen=True)
class Segment:
    index: int
    file_offset: int
    load_address: int
    size: int

    @property
    def file_end(self) -> int:
        return self.file_offset + self.size


@dataclass(frozen=True)
class Image:
    data: bytes
    segments: tuple[Segment, ...]
    entry_address: int
    spi_mode: int
    spi_speed_size: int
    chip_id: int
    min_revision: int
    max_revision: int
    checksum_offset: int
    stored_checksum: int
    calculated_checksum: int
    hash_appended: bool
    stored_digest: bytes | None
    calculated_digest: bytes | None

    def address_for_offset(self, offset: int) -> int | None:
        for segment in self.segments:
            if segment.file_offset <= offset < segment.file_end:
                return segment.load_address + offset - segment.file_offset
        return None


def _align_up(value: int, alignment: int) -> int:
    return (value + alignment - 1) & ~(alignment - 1)


def _cstring(field: bytes) -> str:
    return field.split(b"\0", 1)[0].decode("utf-8", errors="replace")


def parse_image(data: bytes) -> Image:
    if len(data) < 24:
        raise FormatError("image is smaller than the 24-byte ESP image header")
    if data[0] != IMAGE_MAGIC:
        raise FormatError(f"bad ESP image magic: expected 0xe9, got {data[0]:#04x}")

    segment_count = data[1]
    if not 1 <= segment_count <= 16:
        raise FormatError(f"implausible segment count: {segment_count}")

    entry_address = struct.unpack_from("<I", data, 4)[0]
    chip_id = struct.unpack_from("<H", data, 12)[0]
    min_revision = struct.unpack_from("<H", data, 15)[0]
    max_revision = struct.unpack_from("<H", data, 17)[0]
    segments: list[Segment] = []
    offset = 24
    checksum = 0xEF

    for index in range(segment_count):
        if offset + 8 > len(data):
            raise FormatError(f"segment {index} header extends past end of image")
        load_address, size = struct.unpack_from("<II", data, offset)
        file_offset = offset + 8
        file_end = file_offset + size
        if file_end > len(data):
            raise FormatError(f"segment {index} data extends past end of image")
        segment = Segment(index, file_offset, load_address, size)
        segments.append(segment)
        for value in data[file_offset:file_end]:
            checksum ^= value
        offset = file_end

    # The checksum occupies the last byte of the next 16-byte block. If the
    # segment data ends on a boundary, a fresh block is still added.
    checksum_end = _align_up(offset + 1, 16)
    checksum_offset = checksum_end - 1
    if checksum_offset >= len(data):
        raise FormatError("image ends before its XOR checksum")

    hash_appended = bool(data[23])
    stored_digest = None
    calculated_digest = None
    if hash_appended:
        digest_end = checksum_end + 32
        if digest_end > len(data):
            raise FormatError("header requests an appended SHA-256, but it is truncated")
        stored_digest = data[checksum_end:digest_end]
        calculated_digest = hashlib.sha256(data[:checksum_end]).digest()

    return Image(
        data=data,
        segments=tuple(segments),
        entry_address=entry_address,
        spi_mode=data[2],
        spi_speed_size=data[3],
        chip_id=chip_id,
        min_revision=min_revision,
        max_revision=max_revision,
        checksum_offset=checksum_offset,
        stored_checksum=data[checksum_offset],
        calculated_checksum=checksum,
        hash_appended=hash_appended,
        stored_digest=stored_digest,
        calculated_digest=calculated_digest,
    )


def print_image(path: Path, image: Image) -> None:
    speed_code = image.spi_speed_size & 0x0F
    size_code = image.spi_speed_size >> 4
    chip = CHIP_IDS.get(image.chip_id, "unknown")
    mode = SPI_MODES.get(image.spi_mode, "unknown")
    speed = SPI_SPEEDS.get(speed_code, "unknown")
    flash_size = FLASH_SIZES.get(size_code, "unknown")

    print(f"Image: {path}")
    print(f"  size:             {len(image.data):#x} ({len(image.data)} bytes)")
    print(f"  file SHA-256:     {hashlib.sha256(image.data).hexdigest()}")
    print(f"  chip:             {chip} (ID {image.chip_id})")
    print(f"  entry address:    {image.entry_address:#010x}")
    print(f"  flash parameters: {mode}, {speed}, {flash_size}")
    print(f"  chip revisions:   {image.min_revision}..{image.max_revision}")
    print(f"  segments:         {len(image.segments)}")
    for segment in image.segments:
        print(
            f"    [{segment.index}] file {segment.file_offset:#08x}.."
            f"{segment.file_end:#08x} -> {segment.load_address:#010x}, "
            f"size {segment.size:#x}"
        )

    checksum_ok = image.stored_checksum == image.calculated_checksum
    print(
        f"  XOR checksum:     stored {image.stored_checksum:#04x}, "
        f"calculated {image.calculated_checksum:#04x} "
        f"({'OK' if checksum_ok else 'MISMATCH'})"
    )
    if image.hash_appended:
        assert image.stored_digest is not None
        assert image.calculated_digest is not None
        digest_ok = image.stored_digest == image.calculated_digest
        print(f"  appended SHA-256: {image.stored_digest.hex()} ({'OK' if digest_ok else 'MISMATCH'})")
    else:
        print("  appended SHA-256: absent")

    first = image.segments[0]
    if first.size >= 176 and struct.unpack_from("<I", image.data, first.file_offset)[0] == APP_DESC_MAGIC:
        base = first.file_offset
        secure_version = struct.unpack_from("<I", image.data, base + 4)[0]
        version = _cstring(image.data[base + 16 : base + 48])
        project = _cstring(image.data[base + 48 : base + 80])
        compile_time = _cstring(image.data[base + 80 : base + 96])
        compile_date = _cstring(image.data[base + 96 : base + 112])
        idf_version = _cstring(image.data[base + 112 : base + 144])
        elf_digest = image.data[base + 144 : base + 176].hex()
        print("  application descriptor:")
        print(f"    project:          {project}")
        print(f"    version:          {version}")
        print(f"    built:            {compile_date} {compile_time}")
        print(f"    ESP-IDF:          {idf_version}")
        print(f"    secure version:   {secure_version}")
        print(f"    ELF SHA-256:      {elf_digest}")


def print_matches(image: Image, needle: bytes, label: str) -> None:
    offset = 0
    found = False
    while True:
        offset = image.data.find(needle, offset)
        if offset < 0:
            break
        address = image.address_for_offset(offset)
        mapped = f"{address:#010x}" if address is not None else "unmapped"
        print(f"  {offset:#08x}  {mapped}  {label}")
        offset += 1
        found = True
    if not found:
        print(f"  not found: {label}")


def print_hex20_candidates(image: Image) -> None:
    pattern = re.compile(rb"(?<![0-9a-f])[0-9a-f]{20}(?![0-9a-f])")
    print("20-character lowercase-hex candidates:")
    for match in pattern.finditer(image.data):
        address = image.address_for_offset(match.start())
        mapped = f"{address:#010x}" if address is not None else "unmapped"
        print(f"  {match.start():#08x}  {mapped}  {match.group().decode('ascii')}")


def print_partition_table(path: Path, data: bytes) -> None:
    print(f"Partition table: {path}")
    md5_input_end = None
    stored_md5 = None
    for offset in range(0, len(data) - 31, 32):
        entry = data[offset : offset + 32]
        if entry == b"\xff" * 32:
            break
        magic = struct.unpack_from("<H", entry)[0]
        if magic == PARTITION_MAGIC:
            _, part_type, subtype, flash_offset, size, raw_label, flags = struct.unpack(
                "<HBBII16sI", entry
            )
            label = _cstring(raw_label)
            print(
                f"  {label:<16} type {part_type:#04x}/{subtype:#04x}, "
                f"flash {flash_offset:#010x}..{flash_offset + size:#010x}, "
                f"size {size:#x}, flags {flags:#x}"
            )
        elif magic == PARTITION_MD5_MAGIC:
            md5_input_end = offset
            stored_md5 = entry[16:32]
            break
        else:
            raise FormatError(f"unknown partition-table magic {magic:#06x} at {offset:#x}")

    if md5_input_end is not None and stored_md5 is not None:
        calculated = hashlib.md5(data[:md5_input_end]).digest()
        print(
            f"  table MD5:       {stored_md5.hex()} "
            f"({'OK' if stored_md5 == calculated else 'MISMATCH'})"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="ESP bootloader or application .bin")
    parser.add_argument(
        "--partition-table", type=Path, help="optional ESP-IDF partition-table .bin"
    )
    parser.add_argument(
        "--find",
        action="append",
        default=[],
        metavar="TEXT",
        help="find UTF-8 text and report file offsets and mapped addresses; repeatable",
    )
    parser.add_argument(
        "--hex20",
        action="store_true",
        help="list standalone 20-character lowercase-hex strings (the BLE CTF flag format)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        image = parse_image(args.image.read_bytes())
        print_image(args.image, image)
        if args.partition_table:
            print()
            print_partition_table(args.partition_table, args.partition_table.read_bytes())
        for value in args.find:
            print()
            print(f"Matches for {value!r}:")
            print_matches(image, value.encode("utf-8"), repr(value))
        if args.hex20:
            print()
            print_hex20_candidates(image)
    except (OSError, FormatError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
