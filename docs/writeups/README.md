# M0DUL0CTF intended-solution write-ups

These organizer-only write-ups record the solutions verified against the live
`M0DUL0CTF` ESP32 on 2026-07-15. The acceptance unit advertised at
`24:0A:C4:29:82:CE`, exposed all 23 custom characteristics, and reached a final
device score of `20/20`.

For every challenge, the ESP32 accepts the raw 20-character value at UUID
`0xff02`, value handle `0x002c`. CTFd uses the same value wrapped as
`M0DUL0CTF{<20-character-value>}`. Replace the acceptance-unit address in the
examples if a different ESP32 is deployed.

| Flag | Intended-solution write-up | Challenge location | Device ASCII prompt/value |
| ---: | --- | --- | --- |
| 1 | [Welcome submission](flag1.md) | `0xff02` / `0x002c` | `12345678901234567890` |
| 2 | [Direct read](flag2.md) | `0xff03` / `0x002e` | `d205303e099ceff44835` |
| 3 | [Device-name MD5](flag3.md) | `0xff04` / `0x0030` | `MD5 of Device Name` |
| 4 | [Generic Access value](flag4.md) | `0x2a00` / `0x0016` | `2b00042f7481c7b056c4b410d28f33cf` |
| 5 | [Write anything](flag5.md) | `0xff05` / `0x0032` | `Write anything here` |
| 6 | [ASCII write](flag6.md) | `0xff06` / `0x0034` | `Write the ascii value "yo" here` |
| 7 | [Hex write](flag7.md) | `0xff07` / `0x0036` | `Write the hex value 0x07 here` |
| 8 | [Cross-handle write](flag8.md) | `0xff08` / `0x0038`; `0xff09` / `0x003a` | `Write 0xC9 to handle 58` |
| 9 | [Byte enumeration](flag9.md) | `0xff0a` / `0x003c` | `Brute force my value 00 to ff` |
| 10 | [Repeated reads](flag10.md) | `0xff0b` / `0x003e` | `Read me 1000 times` |
| 11 | [Single notification](flag11.md) | `0xff0c` / `0x0040` | `Listen to me for a single notification` |
| 12 | [Single indication](flag12.md) | `0xff0d` / `0x0043`; `0xff0e` / `0x0045` | `Listen to handle 0x0045 for a single indication` |
| 13 | [Multiple notifications](flag13.md) | `0xff0f` / `0x0048` | `Listen to me for multi notifications` |
| 14 | [Multiple indications](flag14.md) | `0xff10` / `0x004b`; `0xff11` / `0x004d` | `Listen to handle 0x004d for multi indications` |
| 15 | [Client address](flag15.md) | `0xff12` / `0x0050` | `Connect with BT MAC address 11:22:33:44:55:66` |
| 16 | [ATT MTU](flag16.md) | `0xff13` / `0x0052` | `Set your connection MTU to 444` |
| 17 | [Write response](flag17.md) | `0xff14` / `0x0054` | `Write+resp 'hello'` |
| 18 | [Hidden notification](flag18.md) | `0xff15` / `0x0056` | `No notifications here! really?` |
| 19 | [Split properties](flag19.md) | `0xff16` / `0x0058` | `So many properties!` |
| 20 | [GitHub handle MD5](flag20.md) | `0xff17` / `0x005a` | `md5 of author's github handle` |

The concise all-in-one command reference remains
[`../../ble_ctf_commands.txt`](../../ble_ctf_commands.txt).
