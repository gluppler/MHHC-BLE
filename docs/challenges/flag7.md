# Flag 7 — `0x0036` — `Write the hex value 0x07 here`

A low-level control panel at UUID `0xff07`, value handle `0x0036`, prints `Write the hex value 0x07 here` and expects a raw byte rather than the characters `0` and `7`. Write byte `07`, read the same handle for the 20-character result, submit that raw value to `0x002c`, and then submit the event-wrapped value to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
