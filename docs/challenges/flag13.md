# Flag 13 — `0x0048` — `Listen to me for multi notifications`

A noisy broadcast channel at UUID `0xff0f`, value handle `0x0048`, announces `Listen to me for multi notifications` before mixing decoys with the real message. Trigger the characteristic while listening, inspect every notification until the 20-character hexadecimal answer appears, submit that raw value to device handle `0x002c`, and then submit its wrapped form to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
