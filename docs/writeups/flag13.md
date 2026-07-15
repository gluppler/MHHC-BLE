# Flag 13 intended solution — `0xff0f` / `0x0048`

The ASCII prompt `Listen to me for multi notifications` signals a sequence.
Listen while writing trigger byte `69`, ignore the decoy text `U no want this
msg`, and decode the final 20-byte notification as the flag.

- Device ASCII prompt: `Listen to me for multi notifications`
- Challenge location: UUID `0xff0f`, value handle `0x0048`
- CCC descriptor: handle `0x0049`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0048 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x0048 -n 69 --listen
```

The live run received two decoy notifications followed by bytes decoding to
`c9457de5fd8cafe349fd`. Press Ctrl-C after that value appears, then submit it:

```bash
gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'c9457de5fd8cafe349fd' | xxd -ps)
```

Live verification advanced the score to `13/20`.

- Raw ESP32 submission: `c9457de5fd8cafe349fd`
- CTFd flag: `M0DUL0CTF{c9457de5fd8cafe349fd}`
