# Flag 17 — `0x0054` — `Write+resp 'hello'`

A request-response console at UUID `0xff14`, value handle `0x0054`, waits behind the terse prompt `Write+resp 'hello'`. Send ASCII `hello` with a write request that expects a response, read the handle for the resulting 20-character value, submit that raw value to device handle `0x002c`, and then submit its wrapped version to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
