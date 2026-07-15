# Flag 15 — `0x0050` — `Connect with BT MAC address 11:22:33:44:55:66`

An identity checkpoint at UUID `0xff12`, value handle `0x0050`, grants access only after stating `Connect with BT MAC address 11:22:33:44:55:66`. Record your own client adapter's original address, temporarily use the requested address, reconnect and read the 20-character response, restore your original address, submit the raw response to device handle `0x002c`, and then wrap it for CTFd.

**Flag format:** `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where each `x` is one lowercase hexadecimal character (`0-9a-f`).
