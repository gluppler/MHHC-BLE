# Flag 3 intended solution — `0xff04` / `0x0030`

Reading UUID `0xff04` returns the ASCII instruction `MD5 of Device Name`.
Discover or read the advertised name `M0DUL0CTF`, calculate its MD5 without a
trailing newline, and use the first 20 lowercase hexadecimal characters.

- Device ASCII prompt: `MD5 of Device Name`
- Challenge location: UUID `0xff04`, value handle `0x0030`
- Hash input: `M0DUL0CTF`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0030 \
  | cut -d':' -f2 | xxd -r -p
echo

echo -n 'M0DUL0CTF' | md5sum

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'M0DUL0CTF' | md5sum | awk '{print $1}' \
  | head -c 20 | xxd -ps)
```

Observed full digest: `637260d8e70610e0d300c5bddd94ee37`. Live
verification accepted its first 20 characters and advanced the score to
`3/20`.

- Raw ESP32 submission: `637260d8e70610e0d300`
- CTFd flag: `M0DUL0CTF{637260d8e70610e0d300}`
