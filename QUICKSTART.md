# M0DUL0-CTF quick start

This is the shortest path from a GitHub clone to a working original ESP32.
Use a USB data cable and replace `/dev/ttyUSB0` with the board's serial port.

## Clone

```bash
git clone https://github.com/gluppler/M0DUL0-CTF.git
cd M0DUL0-CTF
```

## Option 1: flash the checked-in M0DUL0CTF release

Install esptool in an isolated environment:

```bash
python3 -m venv .venv-esptool
. .venv-esptool/bin/activate
python -m pip install --upgrade esptool
```

Verify the images and flash all three at their required offsets:

```bash
(cd firmware/m0dul0 && sha256sum -c SHA256SUMS)

PORT=/dev/ttyUSB0
python -m esptool --chip esp32 --port "$PORT" --baud 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 2MB --flash_freq 40m \
  0x1000 firmware/m0dul0/bootloader.bin \
  0x8000 firmware/m0dul0/partition-table.bin \
  0x10000 firmware/m0dul0/ble_ctf.bin
```

This command flashes the bootloader, partition table, and application. Flashing
only `ble_ctf.bin` is not a complete first-time installation.

## Option 2: build the source with Docker, then flash it

The following command creates the deliberately named, ignored
`build-m0dul0/` directory:

```bash
docker run --rm \
  -v "$PWD":/project -w /project \
  -u "$(id -u):$(id -g)" -e HOME=/tmp \
  espressif/idf:release-v5.5 \
  idf.py -B build-m0dul0 set-target esp32 build
```

Flash that fresh build from the host:

```bash
PORT=/dev/ttyUSB0
python -m esptool --chip esp32 --port "$PORT" --baud 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 2MB --flash_freq 40m \
  0x1000 build-m0dul0/bootloader/bootloader.bin \
  0x8000 build-m0dul0/partition_table/partition-table.bin \
  0x10000 build-m0dul0/ble_ctf.bin
```

On Linux, Docker can instead access the serial device directly:

```bash
PORT=/dev/ttyUSB0
docker run --rm --device="$PORT:$PORT" \
  -v "$PWD":/project -w /project \
  espressif/idf:release-v5.5 \
  idf.py -B build-m0dul0 -p "$PORT" flash
```

Docker Desktop on macOS and Windows does not normally pass USB serial devices
through this way. Build in Docker and run host-side esptool there.

## Confirm BLE operation

From a Linux machine with BlueZ and
[gratttool](https://github.com/hackgnar/gratttool):

```bash
gratttool --scan
gratttool -b <M0DUL0CTF_ADDRESS> --enumerate
```

The scan should show `M0DUL0CTF`, and enumeration should show the complete GATT
table. Continue with [`ble_ctf_commands.txt`](ble_ctf_commands.txt) or the
organizer guide in [`SETUP_GUIDE.md`](SETUP_GUIDE.md).

## Modify and rebuild

Challenge behavior, prompts, accepted values, and the advertising name live in
`main/gatts_table_creat_demo.c`. After editing, rerun the Docker build command.
Keep dependent challenge values synchronized as described in
[`SETUP_GUIDE.md`](SETUP_GUIDE.md), especially the device-name hash challenge.
