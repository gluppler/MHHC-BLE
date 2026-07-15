# Flag 1 intended solution — `0xff02` / `0x002c`

The first challenge is the onboarding gift. Its ASCII flag value is supplied by
the challenge material so the player can learn the submission workflow before
having to recover a value from another characteristic.

- Device ASCII value: `12345678901234567890`
- Submission location: UUID `0xff02`, value handle `0x002c`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x002a \
  | awk -F: '{print $2}' | tr -d ' ' | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n '12345678901234567890' | xxd -ps)
```

Live verification: the write was accepted and the score advanced to `1/20`.

- Raw ESP32 submission: `12345678901234567890`
- CTFd flag: `M0DUL0CTF{12345678901234567890}`
