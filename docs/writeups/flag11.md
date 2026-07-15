# Flag 11 intended solution — `0xff0c` / `0x0040`

The ASCII prompt at handle `0x0040` says `Listen to me for a single
notification`. Start `gratttool` in listen mode while writing the trigger byte
`69`; the device sends the flag in one notification on the same handle.

- Device ASCII prompt: `Listen to me for a single notification`
- Challenge location: UUID `0xff0c`, value handle `0x0040`
- CCC descriptor: handle `0x0041`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0040 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x0040 -n 69 --listen
```

The live listener printed:

```text
Notification handle = 0x0040 value: 35 65 63 33 37 37 32 62 63 64 30 30 63 66 30 36 64 38 65 62
```

Those bytes decode to `5ec3772bcd00cf06d8eb`. Press Ctrl-C after capture,
then submit it:

```bash
gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n '5ec3772bcd00cf06d8eb' | xxd -ps)
```

Live verification advanced the score to `11/20`.

- Raw ESP32 submission: `5ec3772bcd00cf06d8eb`
- CTFd flag: `M0DUL0CTF{5ec3772bcd00cf06d8eb}`
