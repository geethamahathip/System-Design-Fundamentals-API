#!/usr/bin/env sh
set -eu

if [ "$#" -gt 0 ]; then
  PAYLOAD="$1"
elif [ -f "./upsk-report.json" ]; then
  PAYLOAD="$(cat ./upsk-report.json)"
else
  echo "Usage: ./upsk-report.sh '<json>' or create ./upsk-report.json" >&2
  exit 1
fi

if [ -x "./.bin/upsk.exe" ]; then
  ./.bin/upsk.exe report "$PAYLOAD"
else
  upsk report "$PAYLOAD"
fi
