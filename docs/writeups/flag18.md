# Flag 18 intended solution — `0xff15` / `0x0056`

The prompt `No notifications here! really?` is deliberately misleading because
the characteristic does not advertise the Notify property. Run `gratttool` with
elevated listen access while writing trigger byte `69`; the unsolicited hidden
notification contains the flag.

- Device ASCII prompt: `No notifications here! really?`
- Challenge location: UUID `0xff15`, value handle `0x0056`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0056 \
  | cut -d':' -f2 | xxd -r -p
echo

sudo gratttool -b "$TARGET" --char-write-req -a 0x0056 -n 69 --listen
```

The live listener printed bytes decoding to `fc920c68b6006169477b`. Press Ctrl-C
after capture, then submit the value:

```bash
gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'fc920c68b6006169477b' | xxd -ps)
```

Live verification advanced the score to `18/20`.

- Raw ESP32 submission: `fc920c68b6006169477b`
- CTFd flag: `M0DUL0CTF{fc920c68b6006169477b}`
