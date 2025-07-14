__mi_widget() {
	local selected=$(./a.py)
	if [[ -n "$selected" ]]; then
		READLINE_LINE="$selected"
		READLINE_POINT=${#READLINE_LINE}
	fi
}

bind -x '"\C-g":__mi_widget'
