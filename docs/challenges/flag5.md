# Flag 5 — `0x0032` — `Write anything here`

A maintenance hatch at UUID `0xff05`, value handle `0x0032`, challenges you with the ASCII message `Write anything here`. Send any byte to that same writable characteristic and read it again to uncover the 20-character response; submit the raw response to device handle `0x002c`, then submit its wrapped form to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
