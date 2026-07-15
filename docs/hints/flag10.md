## Flag 10 Hint

Read handle `0x003e` and automate what its ASCII prompt requests. Connection
setup dominates runtime when each `gratttool` invocation reconnects, so expect
the simple shell loop to take several minutes on some BlueZ adapters. The
firmware counter is global, but the documented 1,001-read loop guarantees the
threshold even when this is the first challenge attempted after boot.
