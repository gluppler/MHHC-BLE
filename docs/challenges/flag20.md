# Flag 20 — `0x005a` — `md5 of author's github handle`

The final breadcrumb at UUID `0xff17`, value handle `0x005a`, reads `md5 of author's github handle` and leads outside the badge to <https://github.com/gluppler>. Take the profile handle in its `@username` form, hash that exact ASCII text without a trailing newline, keep the first 20 lowercase hexadecimal characters, submit the raw result to device handle `0x002c`, and then submit the wrapped result to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
