# Flag 4 — `0x0016` — `2b00042f7481c7b056c4b410d28f33cf`

The public advertisement is only the badge's cover identity; the Generic Access service keeps a deeper record at Device Name UUID `0x2a00`, value handle `0x0016`, whose ASCII value is `2b00042f7481c7b056c4b410d28f33cf`. Read that standard GATT location, take its first 20 characters as the raw device answer, write them to `0x002c`, and submit the same answer in the event wrapper to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
