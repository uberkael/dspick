__dspick() {
	local output=$(echo "$READLINE_LINE" | uv run dspick.py)
	READLINE_LINE="$output"
	READLINE_POINT=${#READLINE_LINE}
}

bind -x '"\C-g":__dspick'
