# M0DUL0CTF customized organizer flag map

This table describes the current customized source and the live ESP32 GATT
layout verified with `gratttool --enumerate`. It supersedes stock `BLECTF`
values for event operation. Keep this file out of participant distributions.

The visible advertising name is `M0DUL0CTF`. Submit each raw 20-character ASCII
value to UUID `0xff02`, handle `0x002c`.

Configure each CTFd challenge with the corresponding wrapped static flag
`M0DUL0CTF{<raw-device-value>}`. A player submits the raw inner value to the
ESP32, then submits the complete wrapper to CTFd; the device tracks local
progress while CTFd records the official solve. Exact wrappers are listed in
the individual [`writeups/`](writeups/README.md) files.

| Flag | UUID / live value handle | Challenge condition | Raw device value |
| ---: | --- | --- | --- |
| 1 | Submit at `0xff02` / `0x002c` | Gift from the first hint | `12345678901234567890` |
| 2 | `0xff03` / `0x002e` | Read directly | `d205303e099ceff44835` |
| 3 | `0xff04` / `0x0030` | MD5 of advertised name `M0DUL0CTF`, truncated | `637260d8e70610e0d300` |
| 4 | GAP `0x2a00` / `0x0016` | First 20 characters of the Generic Access Device Name | `2b00042f7481c7b056c4` |
| 5 | `0xff05` / `0x0032` | Write anything, then read | `3873c0270763568cf7aa` |
| 6 | `0xff06` / `0x0034` | Write the requested ASCII value, then read | `c55c6314b3db0a6128af` |
| 7 | `0xff07` / `0x0036` | Write the requested raw hex value, then read | `1179080b29f8da16ad66` |
| 8 | `0xff08` / `0x0038`; `0xff09` / `0x003a` | Write the requested value to the second handle, then read the first | `f8b136d937fad6a2be9f` |
| 9 | `0xff0a` / `0x003c` | Find the triggering byte value | `933c1fcfa8ed52d2ec05` |
| 10 | `0xff0b` / `0x003e` | Exceed the read threshold | `6ffcd214ffebdc0d069e` |
| 11 | `0xff0c` / `0x0040`; CCC `0x0041` | Trigger one notification | `5ec3772bcd00cf06d8eb` |
| 12 | `0xff0d` / `0x0043`; `0xff0e` / `0x0045`; CCC `0x0046` | Trigger one indication | `c7b86dd121848c77c113` |
| 13 | `0xff0f` / `0x0048`; CCC `0x0049` | Receive the second notification | `c9457de5fd8cafe349fd` |
| 14 | `0xff10` / `0x004b`; `0xff11` / `0x004d`; CCC `0x004e` | Receive and confirm the indication sequence | `b6f3a47f207d38e16ffa` |
| 15 | `0xff12` / `0x0050` | Connect from client address `11:22:33:44:55:66` | `aca16920583e42bdcf5f` |
| 16 | `0xff13` / `0x0052` | Negotiate ATT MTU 444 | `b1e409e5a4eaf9fe5158` |
| 17 | `0xff14` / `0x0054` | Write ASCII `hello` with a response | `d41d8cd98f00b204e980` |
| 18 | `0xff15` / `0x0056` | Listen and write despite the missing Notify property | `fc920c68b6006169477b` |
| 19 | `0xff16` / `0x0058` | Combine the read and notification halves | `fbb966958f07e4a0cc48` |
| 20 | `0xff17` / `0x005a` | MD5 of `@gluppler`, truncated | `471b228968e09e9a328f` |

Flag 3 derivation:

```bash
printf %s 'M0DUL0CTF' | md5sum
```

Flag 20 derivation:

```bash
printf %s '@gluppler' | md5sum
```

The full command-by-command acceptance test is in
[`../ble_ctf_commands.txt`](../ble_ctf_commands.txt).
