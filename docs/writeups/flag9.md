# Flag 9 intended solution — `0xff0a` / `0x003c`

The ASCII prompt `Brute force my value 00 to ff` asks the player to enumerate
all possible one-byte writes. Read after each write and stop when the prompt is
replaced by a 20-character lowercase hexadecimal value.

- Device ASCII prompt: `Brute force my value 00 to ff`
- Challenge location: UUID `0xff0a`, value handle `0x003c`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x003c \
  | cut -d':' -f2 | xxd -r -p
echo

for i in $(seq 0 255); do
  byte=$(printf '%02x' "$i")
  gratttool -b "$TARGET" --char-write-req -a 0x003c -n "$byte" \
    >/dev/null
  result=$(gratttool -b "$TARGET" --char-read -a 0x003c \
    | cut -d':' -f2 | xxd -r -p)
  if [[ "$result" =~ ^[0-9a-f]{20}$ ]]; then
    printf 'winning byte: %s\nflag: %s\n' "$byte" "$result"
    break
  fi
done
```

The live winning byte was `d1`, which exposed `933c1fcfa8ed52d2ec05`.

```bash
gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n '933c1fcfa8ed52d2ec05' | xxd -ps)
```

Live verification advanced the score to `9/20`.

- Raw ESP32 submission: `933c1fcfa8ed52d2ec05`
- CTFd flag: `M0DUL0CTF{933c1fcfa8ed52d2ec05}`
