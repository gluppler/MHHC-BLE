# Flag 18 — `0x0056` — `No notifications here! really?`

A supposedly silent alarm at UUID `0xff15`, value handle `0x0056`, insists `No notifications here! really?` even though the characteristic can emit an unsolicited message without advertising Notify. Listen with the access your BLE client requires while triggering the write, recover the hidden 20-character notification, submit it raw to `0x002c`, and then submit the event-wrapped form to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
