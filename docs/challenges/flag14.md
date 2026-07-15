# Flag 14 — `0x004b` → `0x004d` — `Listen to handle 0x004d for multi indications`

The acknowledged-message relay at helper UUID `0xff10`, value handle `0x004b`, reports `Listen to handle 0x004d for multi indications`, directing you to UUID `0xff11` at `0x004d`. Listen, trigger the indication sequence, confirm and inspect every response until the real 20-character value arrives, submit it raw to `0x002c`, and then submit the wrapped value to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
