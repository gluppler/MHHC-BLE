# Flag 9 — `0x003c` — `Brute force my value 00 to ff`

The one-byte lock at UUID `0xff0a`, value handle `0x003c`, taunts operators with `Brute force my value 00 to ff`. Enumerate the possible byte values from `00` through `ff`, reading after each write until the prompt changes into a 20-character answer; submit that raw answer to device handle `0x002c`, then submit the wrapped form to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
