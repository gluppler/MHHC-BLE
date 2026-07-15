## Flag 8 Hint

Follow the instruction at handle `0x0038` and pay close attention to its number
base. The prompt's handle 58 is decimal, which is `0x003a`. With `gratttool`,
use the explicit hexadecimal form `-a 0x003a`; bare `-a 58` is treated as
hexadecimal `0x0058`.
