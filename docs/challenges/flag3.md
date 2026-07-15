# Flag 3 — `0x0030` — `MD5 of Device Name`

An identity officer hid the next credential behind the instruction `MD5 of Device Name` at UUID `0xff04`, value handle `0x0030`. Determine the badge's advertised device name, hash that exact ASCII name without a trailing newline, keep the first 20 lowercase hexadecimal characters, submit that raw result to device handle `0x002c`, and then send the wrapped version to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
