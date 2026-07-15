# Versioned ESP32 firmware images

These are complete three-image flash sets for the original ESP32 target. Do
not mix files between the two directories.

| Address | Image | Purpose |
| ---: | --- | --- |
| `0x1000` | `bootloader.bin` | Second-stage bootloader |
| `0x8000` | `partition-table.bin` | ESP-IDF partition table |
| `0x10000` | `ble_ctf.bin` | BLE CTF application |

- `m0dul0/` is the customized `M0DUL0CTF` release, tested through all 20
  challenges on an ESP32.
- `stock/` preserves the original supplied BLE CTF image for recovery and
  comparison.

Verify a set before flashing:

```bash
(cd firmware/m0dul0 && sha256sum -c SHA256SUMS)
```

See [`QUICKSTART.md`](../QUICKSTART.md) for the complete flash command. Fresh
build output belongs in the ignored `build-m0dul0/` directory; checked-in
release images belong here.
