# Flag 11 — `0x0040` — `Listen to me for a single notification`

A radio courier at UUID `0xff0c`, value handle `0x0040`, will speak only once after displaying `Listen to me for a single notification`. Start a notification listener while triggering the writable characteristic, decode the single 20-byte asynchronous message, submit its raw ASCII value to device handle `0x002c`, and then submit the event-wrapped version to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
