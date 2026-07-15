# Flag 19 — `0x0058` — `So many properties!`

An overloaded terminal at UUID `0xff16`, value handle `0x0058`, exclaims `So many properties!` because Read, Write, Notify, Broadcast, and Extended behavior all meet there. Exercise the characteristic to recover a 10-character read half and a 10-character notification half, join them in read-then-notification order, submit the raw 20-character result to `0x002c`, and then wrap it for CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
