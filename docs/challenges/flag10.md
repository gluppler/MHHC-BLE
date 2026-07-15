# Flag 10 — `0x003e` — `Read me 1000 times`

A stubborn counter at UUID `0xff0b`, value handle `0x003e`, repeats `Read me 1000 times` until the firmware's read threshold is exceeded. Automate repeated reads of that characteristic until its ASCII value changes into the 20-character answer, submit the raw answer to `0x002c`, and then submit its event-wrapped form to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
