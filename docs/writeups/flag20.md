# Flag 20 intended solution — `0xff17` / `0x005a`

The final prompt is `md5 of author's github handle`. Visit the author's GitHub
profile at <https://github.com/gluppler>, take the handle in its normal social
form with the leading `@`, hash the exact ASCII text `@gluppler` without a
trailing newline, and keep the first 20 lowercase hexadecimal characters.

- Device ASCII prompt: `md5 of author's github handle`
- Challenge location: UUID `0xff17`, value handle `0x005a`
- Author reference: <https://github.com/gluppler>
- Exact hash input: `@gluppler`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x005a \
  | cut -d':' -f2 | xxd -r -p
echo

echo -n '@gluppler' | md5sum

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n '@gluppler' | md5sum | awk '{print $1}' \
  | head -c 20 | xxd -ps)
```

Observed full digest: `471b228968e09e9a328f9fb6195b5067`. The accepted
20-character prefix was `471b228968e09e9a328f`, and the final live score became
`20/20`.

- Raw ESP32 submission: `471b228968e09e9a328f`
- CTFd flag: `M0DUL0CTF{471b228968e09e9a328f}`
