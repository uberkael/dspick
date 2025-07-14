__reemplazar_comando() {
	local output=$(echo "$READLINE_LINE" | uv run c.py)
	READLINE_LINE="$output"
	READLINE_POINT=${#READLINE_LINE}
}

bind -x '"\C-g":__reemplazar_comando'
