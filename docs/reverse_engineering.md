# BLE CTF firmware reverse-engineering notes

> This document records the supplied stock `BLECTF` artifact. For the current
> `M0DUL0CTF` source, live handles, and modified flag values, use the
> [customized organizer flag map](customized_flag_map.md).

## Scope

This report covers the self-hosted educational firmware checked into this
repository. The application binary is treated as the artifact of record; the
checked-in source and Git history are used as matching provenance and to name
the recovered logic.

## Executive summary

- `firmware/stock/ble_ctf.bin` is a plain ESP-IDF application image for the original
  ESP32 (Xtensa), built with ESP-IDF 5.5.3 on March 13, 2026.
- The image implements one Bluedroid GATT server with custom service UUID
  `0x00ff` and characteristic UUIDs `0xff01` through `0xff17`.
- The advertised local name is `BLECTF`. The Generic Access device name is a
  separate value: `2b00042f7481c7b056c4b410d28f33cf`.
- All challenge outputs are fixed 20-byte ASCII values. They are present in
  plaintext in the DROM segment and are accepted by direct `strcmp` calls;
  the device does not calculate or authenticate flags at runtime.
- Score and challenge state are global RAM variables. They are shared by all
  connected clients and reset on reboot.
- Rebuilding from source is the reliable way to customize the CTF. Direct
  binary edits must preserve data layout and repair both the ESP XOR checksum
  and appended SHA-256.
- The documentation's hard-coded handles become inconsistent after the first
  Client Characteristic Configuration descriptor. Use UUID discovery and
  verify handles on the flashed target.

## Artifact identity and provenance

| Artifact | SHA-256 |
| --- | --- |
| `firmware/stock/ble_ctf.bin` | `91ca127349ff48b7b85729ca9c642807e9446be5284ff3899f47944d21f8b901` |
| `firmware/stock/bootloader.bin` | `2bd0770283fd4c895603bd0e0a3b08af65c571e08cc09aac57a41a18c83cd587` |
| `firmware/stock/partition-table.bin` | `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820` |

The application descriptor contains:

| Field | Value |
| --- | --- |
| Project | `ble_ctf` |
| Version | `v1.0-7-g4f4ba0d-dirty` |
| Build time | `Mar 13 2026 19:48:33` |
| ESP-IDF | `v5.5.3` |
| Entry address | `0x400813e8` |
| ELF SHA-256 | `7aae5c384a2239b78f341b11cf3c8e3293cfe4809f692d6c4144342ec9af776b` |
| Appended image SHA-256 | `e0c0d32c870aee6787479668a5e4257778feb746fb4b6a20778425ba11baf69e` |

The version string is expected even though the binary was committed later as
`7caeb72`: it was compiled one minute before that commit, while the working
tree was based on `4f4ba0d`. Between `4f4ba0d` and `7caeb72`, the only change
to the application source was the additional
`ESP_ERR_NVS_NEW_VERSION_FOUND` recovery condition. The challenge constants
and event logic in the present source match the binary's DROM literals. This
gives high confidence that the present source is the source used for the
checked-in image.

## Flash and image layout

The image header requests DIO mode, 40 MHz flash, and a 2 MB flash device. The
partition table places the three supplied images as follows:

| Flash address | Size | Purpose |
| --- | ---: | --- |
| `0x00001000` | `0x6630` bytes | Second-stage bootloader |
| `0x00008000` | `0x0c00` bytes | Partition table |
| `0x00009000` | `0x6000` | NVS partition |
| `0x0000f000` | `0x1000` | PHY initialization data |
| `0x00010000` | `0x100000` | `factory` application partition |

There are no OTA application slots. The application image is `0xa6b60` bytes
and fits in the 1 MB factory partition.

Application segments:

| Segment | File range | Load/mapped address | Size | Likely role |
| ---: | --- | --- | ---: | --- |
| 0 | `0x000020..0x01e2cc` | `0x3f400020` | `0x1e2ac` | Flash-mapped DROM/constants |
| 1 | `0x01e2d4..0x020018` | `0x3ffbdb60` | `0x1d44` | Initialized DRAM |
| 2 | `0x020020..0x08bebc` | `0x400d0020` | `0x6be9c` | Flash-mapped IROM/code |
| 3 | `0x08bec4..0x08eec0` | `0x3ffbf8a4` | `0x2ffc` | Initialized DRAM |
| 4 | `0x08eec8..0x0a6b10` | `0x40080000` | `0x17c48` | IRAM/code |
| 5 | `0x0a6b18..0x0a6b38` | `0x50000000` | `0x20` | RTC fast memory |

Both the application and bootloader XOR checksums and appended SHA-256 values
validate. The image is visibly not encrypted. It has a normal hash trailer and
no secure-boot signature block; this does not reveal the eFuse state of any
particular board.

Use the dependency-free inspector to reproduce these results:

```bash
python3 tools/firmware_inspector.py \
  firmware/stock/ble_ctf.bin \
  --partition-table firmware/stock/partition-table.bin \
  --hex20
```

## Runtime architecture

The server uses ESP-IDF's Bluedroid stack and a single application profile:

1. `app_main()` initializes NVS, releases Classic Bluetooth memory, enables the
   controller in BLE-only mode, enables Bluedroid, registers GAP/GATTS
   callbacks, registers application ID `0x55`, and sets the local maximum MTU
   to 500.
2. `ESP_GATTS_REG_EVT` sets the Generic Access device name, configures raw
   advertising data, and creates the attribute table.
3. `ESP_GATTS_CREAT_ATTR_TAB_EVT` stores the dynamically assigned handles and
   starts service `0x00ff`.
4. One GATTS event switch handles all reads, writes, MTU changes, connections,
   notifications, indications, and score submissions.
5. `flag_state[20]` uses `F` for unsolved, `H` for a challenge whose output has
   been exposed, and `T` for an output submitted to UUID `0xff02`.

Important names are split deliberately:

- Raw advertising contains complete local name `BLECTF`, service UUID
  `0x00ff`, and TX power byte `0xeb`.
- `esp_ble_gap_set_device_name()` sets Generic Access name
  `2b00042f7481c7b056c4b410d28f33cf`.

That distinction explains why flag 3 hashes `BLECTF`, while flag 4 is the first
20 characters of the longer Generic Access device name.

## GATT and challenge map

The canonical identifiers are the UUIDs. Handles are allocated at runtime. The
"derived handle" column assumes the application service begins at `0x0028`, as
the supplied score (`0x002a`) and submission (`0x002c`) documentation states,
and counts every attribute-table entry, including CCC descriptors.

| # | UUID / derived value handle | Recovered condition | Accepted 20-byte value |
| ---: | --- | --- | --- |
| 1 | Submit at `ff02` / `0x002c` | Gift value from the hint/source | `12345678901234567890` |
| 2 | `ff03` / `0x002e` | Read the value directly | `d205303e099ceff44835` |
| 3 | `ff04` / `0x0030` | MD5 of advertised name `BLECTF`, then truncate | `5cd56d74049ae40f442e` |
| 4 | GAP Device Name `2a00` | Read the 32-byte name and submit its first 20 bytes | `2b00042f7481c7b056c4` |
| 5 | `ff05` / `0x0032` | Write anything, then read | `3873c0270763568cf7aa` |
| 6 | `ff06` / `0x0034` | Write ASCII `yo`, then read | `c55c6314b3db0a6128af` |
| 7 | `ff07` / `0x0036` | Write little-endian value `0x0007`, then read | `1179080b29f8da16ad66` |
| 8 | `ff08` / `0x0038`; target `ff09` / `0x003a` | Write little-endian `0x00c9` to `ff09`, then read `ff08` | `f8b136d937fad6a2be9f` |
| 9 | `ff0a` / `0x003c` | Write/fuzz until little-endian `0x00d1`, then read | `933c1fcfa8ed52d2ec05` |
| 10 | `ff0b` / `0x003e` | Cause the global read count to exceed 1000, then read | `6ffcd214ffebdc0d069e` |
| 11 | `ff0c` / `0x0040`; CCC `0x0041` | Listen and write to trigger one notification | `5ec3772bcd00cf06d8eb` |
| 12 | helper `ff0d` / `0x0043`; indication `ff0e` / `0x0045`; CCC `0x0046` | Enable/listen and write to the indication characteristic | `c7b86dd121848c77c113` |
| 13 | `ff0f` / `0x0048`; CCC `0x0049` | Receive the decoy and subsequent notification | `c9457de5fd8cafe349fd` |
| 14 | helper `ff10` / `0x004b`; indication `ff11` / `0x004d`; CCC `0x004e` | Confirm the decoy and receive the subsequent indication | `b6f3a47f207d38e16ffa` |
| 15 | `ff12` / `0x0050` | Connect from client address `11:22:33:44:55:66`, then read | `aca16920583e42bdcf5f` |
| 16 | `ff13` / `0x0052` | Negotiate ATT MTU exactly 444, then read | `b1e409e5a4eaf9fe5158` |
| 17 | `ff14` / `0x0054` | Use a write request for ASCII `hello`, receive its response, then read | `d41d8cd98f00b204e980` |
| 18 | `ff15` / `0x0056` | Listen and write despite the missing Notify property | `fc920c68b6006169477b` |
| 19 | `ff16` / `0x0058` | After a write, combine read half `fbb966958f` with notification half `07e4a0cc48` | `fbb966958f07e4a0cc48` |
| 20 | `ff17` / `0x005a` | MD5 of `@hackgnar`, then truncate | `d953bfb9846acc2e15ee` |

Every value is submitted as ASCII to UUID `0xff02`. `set_score()` counts only
`T` entries and rewrites UUID `0xff01` as `Score: n/20`.

### Hard-coded handle drift

The README and embedded prompts appear to calculate handles while omitting the
four CCC descriptor attributes. CCC descriptors do consume GATT handles. This
causes the intended/documented sequence after `0x0040` to diverge from the
attribute table:

| Purpose | Documented/embedded | Source-derived with CCC entries |
| --- | ---: | ---: |
| Single-indication helper | `0x0042` | `0x0043` |
| Single-indication value | `0x0044` | `0x0045` |
| Multi-notification value | `0x0046` | `0x0048` |
| Multi-indication helper | `0x0048` | `0x004b` |
| Multi-indication value | `0x004a` | `0x004d` |
| MAC challenge | `0x004c` | `0x0050` |
| MTU challenge | `0x004e` | `0x0052` |
| Write-response challenge | `0x0050` | `0x0054` |
| Hidden notification | `0x0052` | `0x0056` |
| Multi-property challenge | `0x0054` | `0x0058` |
| Final challenge | `0x0056` | `0x005a` |

The exact service start can also change with the ESP-IDF version or target.
Enumerate UUIDs on the actual board instead of treating either handle column as
an API contract. This should be corrected before publishing a customized
workshop.

## Plaintext locations in the application image

The first image segment maps file offset `0x20` to `0x3f400020`, so these file
offsets and virtual addresses differ only by the `0x3f400000` prefix.

| # | File offset | DROM address | Value |
| ---: | ---: | ---: | --- |
| 1 | `0x0039b0` | `0x3f4039b0` | `12345678901234567890` |
| 2 | `0x0039e0` | `0x3f4039e0` | `d205303e099ceff44835` |
| 3 | `0x0039f8` | `0x3f4039f8` | `5cd56d74049ae40f442e` |
| 4 | `0x0039c8` | `0x3f4039c8` | `2b00042f7481c7b056c4` |
| 5 | `0x003920` | `0x3f403920` | `3873c0270763568cf7aa` |
| 6 | `0x00393c` | `0x3f40393c` | `c55c6314b3db0a6128af` |
| 7 | `0x003954` | `0x3f403954` | `1179080b29f8da16ad66` |
| 8 | `0x003984` | `0x3f403984` | `f8b136d937fad6a2be9f` |
| 9 | `0x00396c` | `0x3f40396c` | `933c1fcfa8ed52d2ec05` |
| 10 | `0x0038a0` | `0x3f4038a0` | `6ffcd214ffebdc0d069e` |
| 11 | `0x003a10` | `0x3f403a10` | `5ec3772bcd00cf06d8eb` |
| 12 | `0x003a28` | `0x3f403a28` | `c7b86dd121848c77c113` |
| 13 | `0x003a40` | `0x3f403a40` | `c9457de5fd8cafe349fd` |
| 14 | `0x003a58` | `0x3f403a58` | `b6f3a47f207d38e16ffa` |
| 15 | `0x003a70` | `0x3f403a70` | `aca16920583e42bdcf5f` |
| 16 | `0x003a88` | `0x3f403a88` | `b1e409e5a4eaf9fe5158` |
| 17 | `0x003aa0` | `0x3f403aa0` | `d41d8cd98f00b204e980` |
| 18 | `0x003ab8` | `0x3f403ab8` | `fc920c68b6006169477b` |
| 19 | `0x003ad0` | `0x3f403ad0` | `fbb966958f07e4a0cc48` |
| 20 | `0x003ae8` | `0x3f403ae8` | `d953bfb9846acc2e15ee` |

The 32-byte Generic Access name begins at file offset `0x003770` (DROM
`0x3f403770`).

## Source modification map

Most customization belongs in
[`main/gatts_table_creat_demo.c`](../main/gatts_table_creat_demo.c):

- Lines 36 and 60-78: Generic Access name and raw advertising payload.
- Lines 158-181: service and characteristic UUIDs.
- Lines 195-225: global state and user-facing challenge prompts.
- Lines 227-488: GATT attribute database, properties, permissions, and initial
  values.
- Lines 490-509: score calculation and rendering.
- Lines 670-698: read-triggered behavior.
- Lines 699-825: challenge write handlers and notification/indication output.
- Lines 827-917: accepted flag list and score transitions.
- Lines 935-970: MTU and client-MAC checks.
- Lines 941-955: follow-up multi-notification and multi-indication output.

The table order is declared separately in
[`main/gatts_table_creat_demo.h`](../main/gatts_table_creat_demo.h). Add, remove,
or reorder an attribute in both files.

For each customized challenge, update all of the following together:

1. The prompt/initial attribute value.
2. The trigger condition in the event handler.
3. The output value exposed by the challenge.
4. The matching accepted value in the `ff02` submission block.
5. The workshop hint and solution material.

If the challenge count changes, also update `flag_state`, the score loop bound,
the `/20` display, and any client-side material. Keep 20-byte values if legacy
clients must operate at the default ATT MTU; otherwise negotiate a larger MTU
and make all length handling explicit.

## Engineering issues to fix before extending it

These are implementation defects or workshop reliability problems, not hidden
security mechanisms:

1. Every normal write copies 20 bytes from `param->write.value` regardless of
   `param->write.len`. Short writes can cause an out-of-bounds read.
2. The numeric challenges read bytes 0 and 1 without first requiring a length
   of at least two. Require two bytes and decode them explicitly.
3. `flag_state` has no terminating NUL but is logged with `%s`, which can read
   beyond the array.
4. The flag-10 counter increments for every attribute read, not only reads of
   `ff0b`, and the condition is `> 1000` rather than `>= 1000`.
5. All state is global, shared across clients, and non-persistent. One student
   can expose a challenge for another student.
6. Many characteristic values have `ESP_GATT_PERM_WRITE` even when their
   declaration omits the Write property. A client writing by raw handle may
   overwrite supposedly read-only prompts or score data.
7. CCC descriptors declare a maximum length of two bytes but initialize their
   current length from long prompt strings. Initialize them with a two-byte
   zero value.
8. The app-managed read response for flag 17 is allocated without clearing all
   fields, is not freed, and sends the flag's terminating NUL as a 21st byte.
9. The confirmation handler accesses `param->write.conn_id` during a
   confirmation event; use the confirmation member of the event union.
10. Multi-message state is not cleared after the final message, so later
    confirmations can repeat output until disconnect.
11. The source and workshop material embed numeric handles that do not account
    for CCC descriptors and can vary between targets.
12. All accepted values are plaintext static literals. If preventing trivial
    extraction matters, generate per-event/per-device values or score outside
    the firmware; obfuscating literals alone will not make them secret from a
    determined firmware analyst.

## Build and validation workflow

The repository targets ESP-IDF 5.5 and supports `esp32`, `esp32s3`, and
`esp32c6`. The checked-in binary is for `esp32` only.

With an ESP-IDF shell:

```bash
idf.py -B build-m0dul0 set-target esp32 build
idf.py -B build-m0dul0 -p /dev/ttyUSB0 flash
```

Or use the provided Dockerfile and run the same `idf.py` commands from a
container with this repository mounted at `/project`.

After each customized build:

1. Run `tools/firmware_inspector.py` and confirm both integrity checks pass.
2. Enumerate the live GATT database and record UUID-to-handle mappings.
3. Test every property type: read, write command, write request, notification,
   indication, MTU event, and reconnect.
4. Complete all challenges from a fresh boot and from two simultaneous clients
   if the event will be multi-user.
5. Update workshop docs from the observed UUID map. Prefer UUIDs over handles.

The customized source has been rebuilt from a source-only copy with the
`espressif/idf:release-v5.5` container. The resulting firmware was flashed to an
original ESP32, enumerated with `gratttool`, and validated through the final
`Score:20/20` state. This document's offsets and stock hashes still describe
the preserved stock artifact unless explicitly labeled otherwise.

## Direct binary modification

Source rebuilds are strongly preferred. For equal-length string-only edits,
the DROM offsets above identify the relevant data. A binary edit still needs:

1. All code and data references to remain valid.
2. Attribute lengths to continue matching the actual data.
3. The ESP image XOR checksum to be recomputed over every segment.
4. The appended SHA-256 to be recomputed over the image through the checksum
   block.

Longer strings, changed table layouts, changed numeric conditions, or added
challenges require a rebuild (or architecture-aware Xtensa code relocation),
not a simple byte replacement.
