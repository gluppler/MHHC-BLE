# Flag 12 — `0x0043` → `0x0045` — `Listen to handle 0x0045 for a single indication`

The reliable dispatch desk at helper UUID `0xff0d`, value handle `0x0043`, orders `Listen to handle 0x0045 for a single indication`, pointing you to indication UUID `0xff0e` at value handle `0x0045`. Listen and trigger that destination, acknowledge the indication through your BLE client, decode its 20-byte answer, submit the raw value to `0x002c`, and then wrap it for CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
