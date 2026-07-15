# Flag 17 intended solution — `0xff14` / `0x0054`

The prompt `Write+resp 'hello'` requires a write request rather than a
write-without-response command. Write ASCII `hello` to value handle `0x0054`,
then read the same handle to recover the response flag.

- Device ASCII prompt: `Write+resp 'hello'`
- Challenge location: UUID `0xff14`, value handle `0x0054`
- Required ASCII write: `hello`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0054 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x0054 \
  -n $(echo -n 'hello' | xxd -ps)

gratttool -b "$TARGET" --char-read -a 0x0054 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'd41d8cd98f00b204e980' | xxd -ps)
```

Observed decoded result: `d41d8cd98f00b204e980`. Live verification advanced
the score to `17/20` and confirmed the fixed, bounded read-response path.

- Raw ESP32 submission: `d41d8cd98f00b204e980`
- CTFd flag: `M0DUL0CTF{d41d8cd98f00b204e980}`
