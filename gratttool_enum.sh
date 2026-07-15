#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  printf 'Usage: %s <BLE-address>\n' "${0##*/}" >&2
  exit 2
fi

exec gratttool -b "$1" --enumerate
