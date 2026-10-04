#!/bin/sh
# Static WP1 checks; never installs or loads a host.
set -eu
if [ "$#" -gt 1 ]; then
  echo 'usage: check-plugin.sh [repository-root]' >&2
  exit 2
fi
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$script_dir/check_plugin.py" "$@"
