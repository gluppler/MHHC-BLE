# Flag 16 — `0x0052` — `Set your connection MTU to 444`

The badge's wide-channel gate at UUID `0xff13`, value handle `0x0052`, displays `Set your connection MTU to 444` and watches the negotiated ATT connection rather than a text claim. Establish a real MTU of 444 and read the characteristic for its 20-character response, restore your client setting afterward, submit the raw response to `0x002c`, and then submit the wrapped form to CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
