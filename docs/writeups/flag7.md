# Flag 7 intended solution — `0xff07` / `0x0036`

The ASCII prompt says `Write the hex value 0x07 here`. Send the single raw byte
`07` to value handle `0x0036`, then read the same handle to reveal the flag.

- Device ASCII prompt: `Write the hex value 0x07 here`
- Challenge location: UUID `0xff07`, value handle `0x0036`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0036 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x0036 -n 07

gratttool -b "$TARGET" --char-read -a 0x0036 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n '1179080b29f8da16ad66' | xxd -ps)
```

Observed decoded result: `1179080b29f8da16ad66`. The one-byte write was also
used to verify the firmware's bounded short-write handling. The score advanced
to `7/20`.

- Raw ESP32 submission: `1179080b29f8da16ad66`
- CTFd flag: `M0DUL0CTF{1179080b29f8da16ad66}`
