# Flag 10 intended solution — `0xff0b` / `0x003e`

The device says `Read me 1000 times`. Repeated reads increment the firmware's
global read counter; once it is greater than 1000, this characteristic is
replaced by the flag. A 1,001-iteration loop guarantees the threshold from a
fresh boot even when no earlier challenge has been read.

- Device ASCII prompt: `Read me 1000 times`
- Challenge location: UUID `0xff0b`, value handle `0x003e`

## Solve and submit

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x003e \
  | cut -d':' -f2 | xxd -r -p
echo

for i in {1..1001}; do
  gratttool -b "$TARGET" --char-read -a 0x003e >/dev/null
done

gratttool -b "$TARGET" --char-read -a 0x003e \
  | cut -d':' -f2 | xxd -r -p
echo

gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n '6ffcd214ffebdc0d069e' | xxd -ps)
```

Optional timing form used during acceptance:

```bash
/usr/bin/time -f 'elapsed=%E user=%U system=%S' bash -c \
  'for i in {1..1001}; do gratttool -b 24:0A:C4:29:82:CE --char-read -a 0x003e >/dev/null; done'
```

The live run returned `6ffcd214ffebdc0d069e` once the global threshold was
crossed. Reads performed during enumeration and earlier tests also contributed,
so excess loop iterations were stopped after the value appeared. Submission
advanced the score to `10/20`.

- Raw ESP32 submission: `6ffcd214ffebdc0d069e`
- CTFd flag: `M0DUL0CTF{6ffcd214ffebdc0d069e}`
