#!/usr/bin/env bash

__dspick_dir=$(dirname "$(readlink -f "$0")")

__dspick() {
	local output=$(cd "$__dspick_dir" && echo "$READLINE_LINE" | uv run dspick.py)
	READLINE_LINE="$output"
	READLINE_POINT=${#READLINE_LINE}
}

bind -x '"\C-g":__dspick'
