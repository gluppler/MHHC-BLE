# Flag 6 intended solution — `0xff06` / `0x0034`

The characteristic's ASCII prompt is `Write the ascii value "yo" here`.
Convert `yo` to its raw byte representation, write it to the same value handle,
then read the handle again to recover the flag.

- Device ASCII prompt: `Write the ascii value "yo" here`
- Challenge location: UUID `0xff06`, value handle `0x0034`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0034 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x0034 \
  -n $(echo -n 'yo' | xxd -ps)

gratttool -b "$TARGET" --char-read -a 0x0034 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'c55c6314b3db0a6128af' | xxd -ps)
```

Observed decoded result: `c55c6314b3db0a6128af`. Live verification advanced
the score to `6/20`.

- Raw ESP32 submission: `c55c6314b3db0a6128af`
- CTFd flag: `M0DUL0CTF{c55c6314b3db0a6128af}`
