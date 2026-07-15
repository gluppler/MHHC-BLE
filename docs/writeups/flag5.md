# Flag 5 intended solution — `0xff05` / `0x0032`

The ASCII prompt at UUID `0xff05` says `Write anything here`. Write any byte to
the same value handle, read it again, and the characteristic returns the
20-character flag.

- Device ASCII prompt: `Write anything here`
- Challenge location: UUID `0xff05`, value handle `0x0032`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0032 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x0032 -n 41

gratttool -b "$TARGET" --char-read -a 0x0032 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n '3873c0270763568cf7aa' | xxd -ps)
```

Observed decoded result: `3873c0270763568cf7aa`. Live verification advanced
the score to `5/20`.

- Raw ESP32 submission: `3873c0270763568cf7aa`
- CTFd flag: `M0DUL0CTF{3873c0270763568cf7aa}`
