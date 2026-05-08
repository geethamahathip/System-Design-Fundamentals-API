#!/usr/bin/env sh
set -eu

if [ -x "./.bin/upsk.exe" ]; then
  ./.bin/upsk.exe next "$@"
else
  upsk next "$@"
fi
