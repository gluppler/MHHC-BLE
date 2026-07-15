# Flag 4 intended solution — `0x2a00` / `0x0016`

The Generic Access service contains Device Name UUID `0x2a00` at value handle
`0x0016`. On this challenge firmware it returns a 32-character ASCII value;
the accepted flag is its first 20 characters.

- Device ASCII value: `2b00042f7481c7b056c4b410d28f33cf`
- Challenge location: GAP UUID `0x2a00`, value handle `0x0016`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0016 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n '2b00042f7481c7b056c4b410d28f33cf' \
  | head -c 20 | xxd -ps)
```

Observed decoded output: `2b00042f7481c7b056c4b410d28f33cf`. Live
verification accepted the truncated value and advanced the score to `4/20`.

- Raw ESP32 submission: `2b00042f7481c7b056c4`
- CTFd flag: `M0DUL0CTF{2b00042f7481c7b056c4}`
