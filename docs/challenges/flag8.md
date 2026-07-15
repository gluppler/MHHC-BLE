# Flag 8 — `0x0038` → `0x003a` — `Write 0xC9 to handle 58`

A misrouted work order appears at UUID `0xff08`, value handle `0x0038`, with the ASCII instruction `Write 0xC9 to handle 58`; handle 58 is decimal and therefore points to UUID `0xff09` at hexadecimal handle `0x003a`. Write byte `c9` to `0x003a`, reread `0x0038` for the 20-character answer, submit it raw to `0x002c`, and then wrap it for CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
