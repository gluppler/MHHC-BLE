# Flag 16 intended solution — `0xff13` / `0x0052`

The ASCII instruction is `Set your connection MTU to 444`. Run the read with a
real ATT MTU negotiation at 444; the firmware watches the negotiated value and
replaces the prompt with the flag. `gratttool` requires elevated privileges for
this setting and restarts `bluetoothd`.

- Device ASCII prompt: `Set your connection MTU to 444`
- Challenge location: UUID `0xff13`, value handle `0x0052`
- Required ATT MTU: `444`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0052 \
  | cut -d':' -f2 | xxd -r -p
echo

sudo gratttool -b "$TARGET" --mtu 444 --char-read -a 0x0052
```

The live root-required read reported `ExchangeMTU set to 444` and returned:

```text
Characteristic value/descriptor: 62 31 65 34 30 39 65 35 61 34 65 61 66 39 66 65 35 31 35 38
```

The bytes decode to `b1e409e5a4eaf9fe5158`.

```bash
gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'b1e409e5a4eaf9fe5158' | xxd -ps)

# Restore the host setting after the challenge.
sudo gratttool -m 517
```

Live verification advanced the score to `16/20` and confirmed that the host MTU
setting was restored to `517`.

- Raw ESP32 submission: `b1e409e5a4eaf9fe5158`
- CTFd flag: `M0DUL0CTF{b1e409e5a4eaf9fe5158}`
