# Flag 8 intended solution — `0xff08` / `0x0038` and `0xff09` / `0x003a`

Reading handle `0x0038` returns `Write 0xC9 to handle 58`. The prompt uses
decimal 58, which is hexadecimal handle `0x003a`. Write byte `c9` to `0x003a`,
then reread `0x0038` to obtain the flag.

- Device ASCII prompt: `Write 0xC9 to handle 58`
- Prompt location: UUID `0xff08`, value handle `0x0038`
- Write target: UUID `0xff09`, value handle `0x003a`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0038 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x003a -n c9

gratttool -b "$TARGET" --char-read -a 0x0038 \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'f8b136d937fad6a2be9f' | xxd -ps)
```

Use explicit `0x003a` with `gratttool`. A bare `-a 58` is parsed as hexadecimal
`0x0058` by this tool and targets Flag 19 instead. The corrected command exposed
`f8b136d937fad6a2be9f`; live verification advanced the score to `8/20`.

- Raw ESP32 submission: `f8b136d937fad6a2be9f`
- CTFd flag: `M0DUL0CTF{f8b136d937fad6a2be9f}`
