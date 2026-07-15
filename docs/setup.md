# Build and flash M0DUL0-CTF

The repository is ready to clone, build, and flash on an original ESP32. The
fastest complete instructions are in [`QUICKSTART.md`](../QUICKSTART.md).

## Flash the tested release

From the repository root, install esptool, verify the three checked-in images,
and flash them at their required offsets:

```bash
python3 -m venv .venv-esptool
. .venv-esptool/bin/activate
python -m pip install --upgrade esptool
(cd firmware/m0dul0 && sha256sum -c SHA256SUMS)

PORT=/dev/ttyUSB0
python -m esptool --chip esp32 --port "$PORT" --baud 460800 \
  --before default_reset --after hard_reset \
  write_flash --flash_mode dio --flash_size 2MB --flash_freq 40m \
  0x1000 firmware/m0dul0/bootloader.bin \
  0x8000 firmware/m0dul0/partition-table.bin \
  0x10000 firmware/m0dul0/ble_ctf.bin
```

The supplied images target the original ESP32. ESP32-S3 and ESP32-C6 require a
fresh target-specific build and testing.

## Build from source

The tested Docker workflow uses ESP-IDF's `release-v5.5` image and writes all
generated files to the ignored `build-m0dul0/` directory:

```bash
docker run --rm \
  -v "$PWD":/project -w /project \
  -u "$(id -u):$(id -g)" -e HOME=/tmp \
  espressif/idf:release-v5.5 \
  idf.py -B build-m0dul0 set-target esp32 build
```

With a native ESP-IDF 5.5 shell, run the same build action:

```bash
idf.py -B build-m0dul0 set-target esp32 build
idf.py -B build-m0dul0 -p /dev/ttyUSB0 flash
```

For customization dependencies, CTFd deployment, validation, troubleshooting,
and stock recovery, use the
[`complete organizer guide`](../SETUP_GUIDE.md).
