# M0DUL0-BLE-CTF

Forked from @hackgnar's ble ctf and modified by @gluppler

Device Name : M0DUL0CTF (Addresses may vary on each machine)
Equipment needed for setup :
- ESP32 CP2102 - [Link](https://my.shp.ee/KG9cLYti)
- MicroUSB to USB Adapter (DATA Cable) - [Link](https://my.shp.ee/qXq6PAB4)
- Transparent Case (ESP32 Specific) - [Link](https://my.shp.ee/8pSbBDnH)

Steps needed for setup :

Test the ESP32 by plugging the cable into it.
After confirming it powers on, run the commands in quickstart.md to flash firmware.
After flashing firmware, make sure to follow the exact commands to unblock bluetooth and run gratttool.
After it works without any issues, unplug it and assemble the case.
Yes the two buttons will pop off during assembly.
THE END.

M0DUL0-BLE-CTF is a customized, self-hosted Bluetooth Low Energy capture-the-flag
for teaching BLE discovery, GATT reads and writes, notifications, indications,
MTU behavior, and client/device attributes. It advertises as `M0DUL0CTF` and
contains 20 challenges.

The checked-in ESP32 release has been flashed to hardware and solved end to end
with `gratttool`; the device reported `Score:20/20`. A clean source-only clone
also builds successfully with the pinned ESP-IDF 5.5 Docker image.

> **Organizer note:** this full repository intentionally contains firmware
> source, accepted values, command sheets, and intended solutions. Keep the
> repository private—or publish a separate participant-only bundle—while those
> values are active in a scored event.

## Start here

- [Clone, build, and flash quick start](QUICKSTART.md)
- [Complete organizer setup and customization guide](SETUP_GUIDE.md)
- [Bare-bones commands for all 20 flags](ble_ctf_commands.txt)
- [Organizer-only intended solutions](docs/writeups/README.md)
- [CTFd challenge descriptions](docs/challenges/README.md)
- [Organizer-only accepted-value map](docs/customized_flag_map.md)

## Hardware and tools

- An original ESP32 development board for the supplied binaries.
- A USB data cable.
- Docker or a native ESP-IDF 5.5 installation when rebuilding.
- Linux, BlueZ, and
  [gratttool](https://github.com/hackgnar/gratttool) for participant interaction.

ESP32-S3 and ESP32-C6 defaults are included, but their images must be built and
hardware-tested separately. Do not flash the supplied original-ESP32 binaries
to those targets.

## Firmware layout

| Directory | Contents |
| --- | --- |
| `firmware/m0dul0/` | Tested custom `M0DUL0CTF` bootloader, partition table, app, and checksums |
| `firmware/stock/` | Preserved upstream-supplied ESP32 images and checksums |
| `build-m0dul0/` | Ignored local output created when you build the custom source |

All three images in a set are required for a complete first flash. See the
[quick start](QUICKSTART.md) for the exact offsets and commands.

As a convenience, `make docker-build` runs the documented container build.
Native ESP-IDF users can run `make set-target build`, and then
`make flash PORT=/dev/ttyUSB0`.

## Player submission format

Each recovered device value is exactly 20 lowercase hexadecimal characters.
Submit the raw value as ASCII to GATT UUID `0xff02` (observed handle `0x002c`),
then submit the wrapped value to CTFd:

```text
M0DUL0CTF{<20-character-raw-value>}
```

Use UUIDs as the stable interface and enumerate the actual device after every
attribute-table change; numeric handles can drift between target and ESP-IDF
versions.

## Attribution

This project is derived from
[hackgnar/ble_ctf](https://github.com/hackgnar/ble_ctf). Read
[`NOTICE.md`](NOTICE.md) before public redistribution; this package preserves
the available source notices and intentionally does not invent a missing
repository-wide license.
