# Flag 2 intended solution — `0xff03` / `0x002e`

UUID `0xff03` exposes the flag directly as an ASCII characteristic value. Read
value handle `0x002e`, decode the returned hex bytes, and submit the resulting
20 characters to the common submission handle.

- Device ASCII value: `d205303e099ceff44835`
- Challenge location: UUID `0xff03`, value handle `0x002e`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x002e \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'd205303e099ceff44835' | xxd -ps)
```

Observed decoded output: `d205303e099ceff44835`. Live verification advanced
the score to `2/20`.

- Raw ESP32 submission: `d205303e099ceff44835`
- CTFd flag: `M0DUL0CTF{d205303e099ceff44835}`
