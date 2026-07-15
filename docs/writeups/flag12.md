# Flag 12 intended solution — `0xff0d` / `0x0043` and `0xff0e` / `0x0045`

The helper characteristic says `Listen to handle 0x0045 for a single
indication`. Listen while writing trigger byte `69` to the indicated value
handle; unlike a notification, `gratttool` confirms the indication for the
server.

- Device ASCII prompt: `Listen to handle 0x0045 for a single indication`
- Prompt location: UUID `0xff0d`, value handle `0x0043`
- Indication location: UUID `0xff0e`, value handle `0x0045`, CCC `0x0046`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0043 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x0045 -n 69 --listen
```

The live listener printed an indication whose bytes decoded to
`c7b86dd121848c77c113`. Press Ctrl-C, then submit it:

```bash
gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'c7b86dd121848c77c113' | xxd -ps)
```

Live verification advanced the score to `12/20`.

- Raw ESP32 submission: `c7b86dd121848c77c113`
- CTFd flag: `M0DUL0CTF{c7b86dd121848c77c113}`
