# Flag 14 intended solution — `0xff10` / `0x004b` and `0xff11` / `0x004d`

The helper text says `Listen to handle 0x004d for multi indications`. Listen
while writing trigger byte `69` to `0x004d`, allow `gratttool` to confirm each
indication, discard the decoy messages, and decode the final indication.

- Device ASCII prompt: `Listen to handle 0x004d for multi indications`
- Prompt location: UUID `0xff10`, value handle `0x004b`
- Indication location: UUID `0xff11`, value handle `0x004d`, CCC `0x004e`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x004b \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x004d -n 69 --listen
```

The live run received two `U no want this msg` indications followed by the
bytes for `b6f3a47f207d38e16ffa`. Press Ctrl-C, then submit the final value:

```bash
gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'b6f3a47f207d38e16ffa' | xxd -ps)
```

Live verification advanced the score to `14/20` and confirmed the corrected
server confirmation-state handling.

- Raw ESP32 submission: `b6f3a47f207d38e16ffa`
- CTFd flag: `M0DUL0CTF{b6f3a47f207d38e16ffa}`
