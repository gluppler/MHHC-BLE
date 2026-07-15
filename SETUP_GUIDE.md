# M0DUL0-CTF complete setup guide

This guide covers the organizer workflow from source customization through
building, flashing, testing, and resetting the BLE CTF. It targets the original
ESP32 and the ESP-IDF 5.5 toolchain used by the supplied firmware.

## Choose a workflow

Use one of these paths:

1. **Flash the supplied image:** fastest way to confirm a board and USB cable
   work. No compiler is required.
2. **Modify and build with Docker:** recommended for reproducible community CTF
   builds. The repository pins the `espressif/idf:release-v5.5` image.
3. **Modify and build with native ESP-IDF 5.5.3:** best for frequent development
   and serial debugging.

The supplied binaries are for the original ESP32 only. ESP32-S3 and ESP32-C6
configuration defaults exist, but those targets require a fresh build and full
hardware testing.

## Hardware and software

Organizer/programming station:

- An original ESP32 development board with Bluetooth Low Energy support.
- A USB **data** cable that matches the board. Charge-only cables will not work.
- A Windows, Linux, or macOS computer.
- Either Docker or ESP-IDF 5.5.3.
- `esptool` or the copy bundled with ESP-IDF.
- A text editor.

Participant/test station:

- A Linux computer or Linux VM.
- A BLE-capable adapter visible inside Linux.
- BlueZ with `bluetoothd` running.
- `gratttool` installed and on `PATH`.
- For flag 15, an adapter whose chipset supports changing its Bluetooth address.

Official references:

- [ESP-IDF 5.5.3 Get Started](https://docs.espressif.com/projects/esp-idf/en/v5.5.3/esp32/get-started/index.html)
- [ESP-IDF 5.5.3 Linux/macOS installation](https://docs.espressif.com/projects/esp-idf/en/v5.5.3/esp32/get-started/linux-macos-setup.html)
- [ESP-IDF 5.5.3 Windows installation](https://docs.espressif.com/projects/esp-idf/en/v5.5.3/esp32/get-started/windows-setup.html)
- [Official ESP-IDF Docker image guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/tools/idf-docker-image.html)
- [Official esptool installation guide](https://docs.espressif.com/projects/esptool/en/latest/esp32/installation.html)
- [Official esptool flashing guide](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/flashing-firmware.html)

## Repository map

| Path | Purpose |
| --- | --- |
| `main/gatts_table_creat_demo.c` | BLE service, challenge prompts, triggers, outputs, accepted flags, and score logic |
| `main/gatts_table_creat_demo.h` | Attribute-table ordering and indexes |
| `sdkconfig.defaults` | ESP32 BLE defaults |
| `sdkconfig.defaults.esp32s3` | ESP32-S3 target defaults |
| `sdkconfig.defaults.esp32c6` | ESP32-C6 target defaults |
| `Dockerfile` | ESP-IDF `release-v5.5` build environment |
| `firmware/m0dul0/` | Versioned, tested custom ESP32 release images and checksums |
| `firmware/stock/` | Preserved stock ESP32 images and checksums |
| `build-m0dul0/` | Ignored local output from custom source builds |
| `docs/hints/` | Participant hints for flags 1 through 20 |
| `ble_ctf_commands.txt` | Organizer solution commands using `gratttool` |
| `tools/firmware_inspector.py` | Dependency-free ESP image and partition-table validator |

## Step 1: enter the project and verify the release firmware

After cloning the repository:

```bash
cd M0DUL0-CTF
```

The custom and stock releases are already separated from generated build output.
Verify both sets before flashing:

```bash
(cd firmware/m0dul0 && sha256sum -c SHA256SUMS)
(cd firmware/stock && sha256sum -c SHA256SUMS)
```

Expected stock SHA-256 values:

```text
91ca127349ff48b7b85729ca9c642807e9446be5284ff3899f47944d21f8b901  ble_ctf.bin
2bd0770283fd4c895603bd0e0a3b08af65c571e08cc09aac57a41a18c83cd587  bootloader.bin
7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820  partition-table.bin
```

`build-m0dul0/` is generated and ignored by Git. Running `fullclean` against it
does not touch either versioned set under `firmware/`.

## Step 2A: flash the supplied stock image

Use this path to prove the board, cable, serial driver, and BLE radio work before
customizing anything.

### Install standalone esptool

ESP-IDF already includes esptool. If ESP-IDF is not installed, create a Python
virtual environment:

```bash
python3 -m venv .venv-esptool
. .venv-esptool/bin/activate
python -m pip install --upgrade pip esptool
python -m esptool version
```

Current standalone esptool releases require Python 3.10 or newer. Depending on
the installed version, the executable may also be named `esptool.py`; the
remaining arguments are the same.

### Find the serial port

Connect the ESP32 and compare the output before and after plugging it in:

```bash
# Linux
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null

# macOS
ls /dev/cu.*
```

On Windows, use Device Manager and note the board's `COM` number.

On Linux, serial devices commonly belong to `dialout`. If access is denied:

```bash
sudo usermod -aG dialout "$USER"
```

Log out and back in after changing group membership. Do not work around serial
permissions by making the device world-writable.

Set the port for the current shell:

```bash
# Linux example
PORT=/dev/ttyUSB0

# macOS example
# PORT=/dev/cu.usbserial-0001

# Windows PowerShell/cmd example: substitute COM5 directly in each command
```

### Flash all three stock images

```bash
python -m esptool --chip esp32 --port "$PORT" --baud 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 2MB --flash_freq 40m \
  0x1000 firmware/stock/bootloader.bin \
  0x8000 firmware/stock/partition-table.bin \
  0x10000 firmware/stock/ble_ctf.bin
```

The flash layout is:

| Address | Image |
| ---: | --- |
| `0x1000` | Second-stage bootloader |
| `0x8000` | Partition table |
| `0x10000` | BLE CTF application |

If the board remains at `Connecting...`, hold its **BOOT** button, briefly press
**EN/RESET**, release **BOOT** when writing begins, and try again. Many DevKit
boards enter the bootloader automatically, so only do this if automatic reset
fails.

## Step 2B: customize the CTF

The project intentionally keeps the challenges in one C file. Read
`docs/reverse_engineering.md` before changing table layout or notification
behavior.

### Device and project identity

Application/project name:

- Root `CMakeLists.txt` contains `project(ble_ctf)`.
- Keeping this name produces `build-m0dul0/ble_ctf.bin` when the documented
  `-B build-m0dul0` option is used.
- Changing it to `project(M0DUL0_CTF)` changes the generated application binary
  name. Update flash commands and documentation if you do this.

BLE names in `main/gatts_table_creat_demo.c`:

- `SAMPLE_DEVICE_NAME` is the Generic Access Device Name used by flag 4.
- `raw_adv_data` contains the local name shown during scanning (`M0DUL0CTF` in
  this customized source) and
  used by flag 3.

The two names are deliberately different. Changing either without updating the
associated flag will break that challenge.

The raw advertising field for the current `M0DUL0CTF` test name is:

```c
/* AD length is one type byte plus nine name bytes: 10 == 0x0A */
0x0A, 0x09, 'M', '0', 'D', 'U', 'L', '0', 'C', 'T', 'F'
```

BLE advertising data is limited to 31 bytes. Whenever the name length changes,
update the leading AD length byte and recount the entire advertising payload.

### Generate replacement flag values

Legacy clients expect 20-byte ASCII flags. One simple organizer convention is
to truncate a deterministic MD5 string:

```bash
printf %s 'M0DUL0-flag-05-v1' | md5sum | cut -c1-20
```

This is a CTF identifier, not a password or security boundary. All accepted
values are present in plaintext in the firmware.

Maintain exactly one organizer-only mapping containing:

- Flag number.
- Prompt.
- Trigger input or event.
- Output flag.
- Accepted submission value.
- Hint file.
- UUID and observed handle after flashing.

### Update each challenge consistently

Most challenge changes require edits in several places in
`main/gatts_table_creat_demo.c`:

1. Update the user-facing prompt or initial GATT value near lines 195-217.
2. Update the trigger condition in the GATTS read/write/MTU/connect handlers,
   beginning near line 670.
3. Update the value returned, notified, or indicated by that trigger.
4. Update the accepted `strcmp` value in the submission handler near lines
   834-912.
5. Update `docs/hints/flagN.md` and the organizer command sheet.

If the trigger emits one value but the submission handler accepts another, the
challenge can be solved but will never score.

Special dependencies:

| Challenge | Dependency to keep synchronized |
| ---: | --- |
| 3 | MD5/truncation of the raw advertised local name |
| 4 | First 20 bytes of the Generic Access Device Name |
| 7-9 | Raw numeric byte values expected by the write handler |
| 10 | Global read threshold and counter behavior |
| 11-14, 18-19 | Notification/indication payloads and characteristic properties |
| 15 | Required connecting client Bluetooth address |
| 16 | Exact MTU event value and local maximum MTU |
| 17 | Required write-with-response text and follow-up read response |
| 19 | Order of the read half and notification half |
| 20 | Input string used to derive the final truncated hash |

### Change service structure only when necessary

The custom service and characteristic UUIDs are declared near lines 158-181.
The GATT database follows near lines 227-488, while its index order is defined
in `main/gatts_table_creat_demo.h`.

If you add, remove, or reorder an attribute:

1. Update the enum in the header.
2. Update the GATT database in the C file.
3. Update every index reference in the event handler.
4. Rebuild and enumerate the live device.
5. Replace numeric handles in hints and organizer material.

Handles are runtime allocations, not stable identifiers. Treat UUIDs as the
canonical interface and use `gratttool --enumerate` after every table change.

### Change the number of flags

The value 20 is coupled to several locations:

- `flag_state[20]`.
- The score loop bound.
- `score_read_value`, including `/20`.
- The accepted submission checks.
- Workshop hints and command material.

Update all of them together. The current code also contains reliability and
memory-safety defects listed in `docs/reverse_engineering.md`; fix those before
expanding the server or using it with many simultaneous participants.

## Step 3A: build with Docker (recommended)

Docker keeps the organizer build independent from system compiler versions.
The repository pins ESP-IDF's `release-v5.5` branch.

### Build using the official image directly

On Linux, from the project root:

```bash
docker pull espressif/idf:release-v5.5

docker run --rm \
  -v "$PWD":/project \
  -w /project \
  -u "$(id -u):$(id -g)" \
  -e HOME=/tmp \
  espressif/idf:release-v5.5 \
  idf.py -B build-m0dul0 set-target esp32 build
```

The explicit user ID prevents Docker from leaving root-owned build files. The
first run downloads the image and toolchain and can take several minutes.

For later source-only changes, keep the existing target/configuration and run:

```bash
docker run --rm \
  -v "$PWD":/project \
  -w /project \
  -u "$(id -u):$(id -g)" \
  -e HOME=/tmp \
  espressif/idf:release-v5.5 \
  idf.py -B build-m0dul0 build
```

### Build using the repository Dockerfile

The included Dockerfile is a small wrapper around the same official image:

```bash
docker build -t m0dul0-ctf-idf .
docker run --rm -it -v "$PWD":/project -w /project m0dul0-ctf-idf
```

Inside the container:

```bash
idf.py -B build-m0dul0 set-target esp32 build
exit
```

This interactive form normally runs as the container's default user and may
leave root-owned files on Linux. Prefer the direct-image command above for a
repeatable organizer workflow.

## Step 3B: build with native ESP-IDF 5.5.3

Follow Espressif's OS-specific installation page for prerequisites. A minimal
Linux/macOS installation is:

```bash
mkdir -p "$HOME/esp"
cd "$HOME/esp"
git clone -b v5.5.3 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh esp32
. "$HOME/esp/esp-idf/export.sh"
```

The export step is required in every new development shell. Return to the CTF
project and build:

```bash
cd M0DUL0-CTF
idf.py -B build-m0dul0 set-target esp32 build
```

Successful builds produce at least:

```text
build-m0dul0/bootloader/bootloader.bin
build-m0dul0/partition_table/partition-table.bin
build-m0dul0/ble_ctf.bin
```

If you renamed `project(ble_ctf)`, substitute the new application filename.

## Step 4: inspect the new images

Run the included parser before flashing:

```bash
python3 tools/firmware_inspector.py \
  build-m0dul0/ble_ctf.bin \
  --partition-table build-m0dul0/partition_table/partition-table.bin \
  --hex20
```

Confirm:

- Chip is `ESP32`.
- XOR checksum is `OK`.
- Appended SHA-256 is `OK`.
- Partition-table MD5 is `OK`.
- Project/version and build timestamp are the expected new values.
- Every intended 20-character lowercase-hex flag appears if that remains your
  flag format.

The `--hex20` check only finds standalone lowercase hexadecimal strings. It will
not list flags using another alphabet or length.

## Step 5: flash the customized build

### Native ESP-IDF

```bash
PORT=/dev/ttyUSB0
idf.py -B build-m0dul0 -p "$PORT" flash
idf.py -B build-m0dul0 -p "$PORT" monitor
```

`flash` automatically rebuilds when necessary. Exit the serial monitor with
`Ctrl+]`.

### Host esptool after a Docker build

Use the same three-image command as the stock image, now pointing at the newly
generated `build-m0dul0/` files:

```bash
PORT=/dev/ttyUSB0
python -m esptool --chip esp32 --port "$PORT" --baud 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 2MB --flash_freq 40m \
  0x1000 build-m0dul0/bootloader/bootloader.bin \
  0x8000 build-m0dul0/partition_table/partition-table.bin \
  0x10000 build-m0dul0/ble_ctf.bin
```

### Flash from Docker on Linux

Passing the serial device into Docker is optional; host esptool is usually
simpler. If desired:

```bash
PORT=/dev/ttyUSB0
SERIAL_GID=$(stat -c '%g' "$PORT")

docker run --rm -it \
  --device "$PORT":"$PORT" \
  --group-add "$SERIAL_GID" \
  -v "$PWD":/project \
  -w /project \
  -u "$(id -u):$(id -g)" \
  -e HOME=/tmp \
  espressif/idf:release-v5.5 \
  idf.py -B build-m0dul0 -p "$PORT" flash monitor
```

Docker Desktop on Windows and macOS does not provide ordinary Linux serial
device pass-through in the same way. Build in Docker and flash from the host on
those systems.

## Step 6: verify the running CTF

### Check serial logs

At 115200 baud, a healthy startup should progress through controller and
Bluedroid initialization, GATTS registration, attribute-table creation, service
start, and advertising. Repeated resets or an attribute-table error indicate a
source/configuration problem.

### Prepare the Linux BLE client

`gratttool` uses BlueZ D-Bus, so `bluetoothd` must remain running:

```bash
sudo rfkill unblock bluetooth
sudo systemctl start bluetooth
bluetoothctl power on
```

Scan and enumerate:

```bash
gratttool --scan
gratttool -b <ESP32_BLE_ADDRESS> --enumerate
```

Confirm the custom service UUID `0x00ff`, score UUID `0xff01`, submission UUID
`0xff02`, and the remaining challenge UUIDs appear. Record the live handle map;
do not assume it is identical after an IDF upgrade or table edit.

Read the initial score:

```bash
gratttool -b <ESP32_BLE_ADDRESS> --char-read -a 0x002a \
  | awk -F: '{print $2}' | tr -d ' ' | xxd -r -p
```

Smoke-test flag 1:

```bash
gratttool -b <ESP32_BLE_ADDRESS> --char-write-req -a 0x002c \
  -n $(printf %s '12345678901234567890' | xxd -ps)
```

Read the score again and confirm it increased. If you changed flag 1 or the
handle allocation, substitute the customized value/observed handle.

Use `ble_ctf_commands.txt` for the complete organizer acceptance test. For
notification challenges, run `--listen` under `sudo` when BlueZ suppresses a
notification that is intentionally absent from the declared properties.

## Step 7: prepare a community event

Keep organizer and participant material separate.

Organizer-only material:

- Firmware source.
- `docs/reverse_engineering.md`.
- `docs/customized_flag_map.md`.
- `ble_ctf_commands.txt`.
- The final flag/trigger mapping.
- Stock and customized build backups.

Participant material:

- A flashed ESP32.
- `docs/workshop_setup.md`.
- The 20 files in `docs/challenges/`.
- Selected files from `docs/hints/`.
- Rules, scope, and a reset/help procedure.

The source and organizer command sheet reveal every accepted value. Do not put
them in the participant bundle if discovering the challenges is part of the
event.

### Configure CTFd

Create 20 CTFd challenges and use `docs/challenges/flag1.md` through
`docs/challenges/flag20.md` as the participant-facing descriptions. Configure
each challenge with the exact wrapped static value shown in its organizer
solution under `docs/writeups/`.

Every raw device value matches `[0-9a-f]{20}`: exactly 20 lowercase hexadecimal
characters. Instruct players to submit that raw value first to the ESP32 at
UUID `0xff02` / handle `0x002c`, then submit
`M0DUL0CTF{<raw-device-value>}` to CTFd. The device advances its local score;
CTFd records the official event solve.

Do not attach `docs/customized_flag_map.md`, `docs/writeups/`, or
`ble_ctf_commands.txt` to a CTFd challenge because they reveal the accepted
values.

Before opening the CTF:

1. Flash every board from the same validated build.
2. Power-cycle every board and confirm the score starts at zero.
3. Label each board and its USB cable.
4. Scan the room and confirm boards can be distinguished. If several boards use
   the same advertised name, record their hardware BLE addresses or give them
   unique names at build time.
5. Complete all 20 flags on at least one board using the exact participant tool
   version.
6. Test notifications, indications, MTU 444, and client-address changes on the
   adapters available at the event.
7. Test two clients if boards will be shared.

The current score and exposed-challenge state are global RAM state, shared by
all clients, and lost on reboot. Allocate one board per participant/team when
possible. Otherwise, power-cycle between teams and expect participants to
affect one another's state.

## Restore the stock image

To return a board to the supplied firmware, flash the versioned stock set:

```bash
PORT=/dev/ttyUSB0
python -m esptool --chip esp32 --port "$PORT" --baud 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 2MB --flash_freq 40m \
  0x1000 firmware/stock/bootloader.bin \
  0x8000 firmware/stock/partition-table.bin \
  0x10000 firmware/stock/ble_ctf.bin
```

An erase is normally unnecessary because writing all three images replaces the
used application layout. If stale NVS/configuration causes persistent problems,
the following erases the **entire** ESP32 flash before reflashing:

```bash
python -m esptool --chip esp32 --port "$PORT" erase_flash
```

Only run the erase command on a CTF board whose entire contents may be deleted.

## Troubleshooting

### No serial port appears

- Try a known USB data cable.
- Try another USB port without a hub.
- Install the board's CP210x or CH340 USB-to-serial driver if the OS does not
  provide it.
- Check `dmesg --follow` on Linux while reconnecting the board.

### Permission denied on the serial port

- Check `ls -l "$PORT"`.
- Add the user to the port's group, commonly `dialout`, then log out/in.
- Close serial monitors and IDEs already using the port.

### Flashing remains at `Connecting...`

- Hold **BOOT**, tap **EN/RESET**, then retry.
- Reduce baud from `460800` to `115200`.
- Disconnect peripherals attached to boot-strapping GPIO pins.

### Build uses the wrong chip or stale configuration

- Verify `CONFIG_IDF_TARGET="esp32"` in generated `sdkconfig`.
- Verify the versioned stock images, then run
  `idf.py -B build-m0dul0 set-target esp32`.
- If CMake state is irreparably stale, back up build artifacts and run
  `idf.py -B build-m0dul0 fullclean`, followed by
  `idf.py -B build-m0dul0 build`.

### ESP32 flashes but does not advertise

- Inspect the serial log for controller, Bluedroid, or attribute-table errors.
- Confirm the target is `esp32` and Bluetooth is enabled in `sdkconfig`.
- Recheck the raw advertising field lengths and 31-byte total limit.
- Power-cycle the board after flashing.

### gratttool cannot see or connect to the board

```bash
sudo systemctl start bluetooth
sudo rfkill unblock bluetooth
bluetoothctl power on
gratttool --scan
```

Use a USB BLE dongle passed directly into the Linux VM if the host's built-in
adapter is not visible to the guest.

### Handles do not match the command sheet

Run:

```bash
gratttool -b <ESP32_BLE_ADDRESS> --enumerate
```

Match characteristics by UUID, update the organizer sheet, and then update
participant hints. Numeric handles can change after target, ESP-IDF, or table
changes.

### Hidden notifications do not appear

Some challenges intentionally send notifications without declaring the Notify
property. BlueZ may discard them for an unprivileged process:

```bash
sudo gratttool -b <ESP32_BLE_ADDRESS> \
  --char-write-req -a <HANDLE> -n 69 --listen
```

### Flag 15 cannot change the client address

The adapter must support address changes. Test before the event:

```bash
sudo gratttool --bdaddr show
sudo gratttool --bdaddr 11:22:33:44:55:66
```

Record the original address and restore it afterward. If the chipset rejects
the operation, use a supported USB dongle or provide an organizer exception for
that challenge.

## Final organizer checklist

- [ ] Both `firmware/` image sets pass their `SHA256SUMS` checks.
- [ ] All customized prompts, triggers, outputs, and accepted values agree.
- [ ] Hints and organizer command sheet updated.
- [ ] ESP32 target selected and build completes without errors.
- [ ] Firmware inspector reports valid checksums/hashes.
- [ ] Board flashes and serial startup is clean.
- [ ] BLE scan shows the intended name.
- [ ] Live UUID/handle enumeration recorded.
- [ ] Score starts at 0 and flag 1 increments it.
- [ ] All 20 challenges tested from a fresh boot.
- [ ] Notification, indication, MTU, and address-changing hardware tested.
- [ ] Organizer-only solutions excluded from the participant bundle.
- [ ] Stock restore procedure tested on one board.
