# M0DUL0CTF player-facing challenge descriptions

These 20 files are ready to copy into CTFd. Each title contains the live GATT
value-handle location and the ASCII prompt or value shown by the customized
ESP32. The handles were verified with `gratttool --enumerate` against the final
firmware build.

Every challenge uses two submissions:

1. Write the recovered raw 20-character value to UUID `0xff02`, value handle
   `0x002c`, so the ESP32 records the solve.
2. Wrap that raw value as `M0DUL0CTF{<raw-value>}` and submit the complete wrapper
   to CTFd so the event platform records the solve.

Read UUID `0xff01`, value handle `0x002a`, to check the device score. Challenges
are independent and may be solved in any order; no flag requires an earlier
flag to be completed first.

CTFd flag format: `M0DUL0CTF{xxxxxxxxxxxxxxxxxxxx}`, where every `x` is one
lowercase hexadecimal character (`0-9a-f`).

| Flag | CTFd challenge title |
| ---: | --- |
| 1 | [`0x002c` — `12345678901234567890`](flag1.md) |
| 2 | [`0x002e` — `d205303e099ceff44835`](flag2.md) |
| 3 | [`0x0030` — `MD5 of Device Name`](flag3.md) |
| 4 | [`0x0016` — `2b00042f7481c7b056c4b410d28f33cf`](flag4.md) |
| 5 | [`0x0032` — `Write anything here`](flag5.md) |
| 6 | [`0x0034` — `Write the ascii value "yo" here`](flag6.md) |
| 7 | [`0x0036` — `Write the hex value 0x07 here`](flag7.md) |
| 8 | [`0x0038` → `0x003a` — `Write 0xC9 to handle 58`](flag8.md) |
| 9 | [`0x003c` — `Brute force my value 00 to ff`](flag9.md) |
| 10 | [`0x003e` — `Read me 1000 times`](flag10.md) |
| 11 | [`0x0040` — `Listen to me for a single notification`](flag11.md) |
| 12 | [`0x0043` → `0x0045` — `Listen to handle 0x0045 for a single indication`](flag12.md) |
| 13 | [`0x0048` — `Listen to me for multi notifications`](flag13.md) |
| 14 | [`0x004b` → `0x004d` — `Listen to handle 0x004d for multi indications`](flag14.md) |
| 15 | [`0x0050` — `Connect with BT MAC address 11:22:33:44:55:66`](flag15.md) |
| 16 | [`0x0052` — `Set your connection MTU to 444`](flag16.md) |
| 17 | [`0x0054` — `Write+resp 'hello'`](flag17.md) |
| 18 | [`0x0056` — `No notifications here! really?`](flag18.md) |
| 19 | [`0x0058` — `So many properties!`](flag19.md) |
| 20 | [`0x005a` — `md5 of author's github handle`](flag20.md) |

Organizer solutions are kept in the
[live-verified write-up set](../writeups/README.md), with a condensed command
reference in [`../../ble_ctf_commands.txt`](../../ble_ctf_commands.txt).
