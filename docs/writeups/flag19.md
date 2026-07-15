# Flag 19 intended solution — `0xff16` / `0x0058`

The initial ASCII value `So many properties!` points at the characteristic's
unusual combination of Read, Write, Notify, Broadcast, and Extended properties.
Trigger the listener to recover one 10-character half, then read the same handle
for the other half and concatenate them in read-half-then-notification-half
order.

- Device ASCII prompt: `So many properties!`
- Challenge location: UUID `0xff16`, value handle `0x0058`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0058 \
  | cut -d':' -f2 | xxd -r -p
echo

sudo gratttool -b "$TARGET" --char-write-req -a 0x0058 -n 69 --listen
```

The live notification bytes decoded to `07e4a0cc48`. Press Ctrl-C, then read the
characteristic again:

```bash
gratttool -b "$TARGET" --char-read -a 0x0058 \
  | cut -d':' -f2 | xxd -r -p
echo
```

The read returned `fbb966958f`. Concatenate the read half first and notification
half second: `fbb966958f` + `07e4a0cc48`.

```bash
gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'fbb966958f07e4a0cc48' | xxd -ps)
```

Live verification advanced the score to `19/20`.

- Raw ESP32 submission: `fbb966958f07e4a0cc48`
- CTFd flag: `M0DUL0CTF{fbb966958f07e4a0cc48}`
