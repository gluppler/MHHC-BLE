## Flag 16 Hint

Read handle `0x0052` and do what it says. The client must trigger a real ATT MTU
negotiation with `gratttool --mtu`; the server watches the negotiated value and
exposes the flag when it matches. This operation requires elevated privileges.
Restore the host setting with `sudo gratttool -m 517` afterward.
