# Flag 6 — `0x0034` — `Write the ascii value "yo" here`

The badge's informal operator waits at UUID `0xff06`, value handle `0x0034`, and greets you with `Write the ascii value "yo" here`. Translate `yo` into its raw ASCII bytes, write them to the same characteristic, read back the revealed 20-character value, submit it raw to device handle `0x002c`, and then wrap it for CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
