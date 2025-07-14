#!/usr/bin/env zsh

_dspyck_call() {
	local result="$(navi "$@" </dev/tty)"
	printf "%s" "$result"
}

_dspyck_widget() {
	local -r input="${LBUFFER}"
	local -r last_command="$(echo "${input}" | navi fn widget::last_command)"
	local replacement="$last_command"

	if [ -z "$last_command" ]; then
		replacement="$(_dspyck_call --print)"
	elif [ "$LASTWIDGET" = "_dspyck_widget" ] && [ "$input" = "$previous_output" ]; then
		replacement="$(_dspyck_call --print --query "$last_command")"
	else
		replacement="$(_dspyck_call --print --best-match --query "$last_command")"
	fi

	if [ -n "$replacement" ]; then
		local -r find="${last_command}_NAVIEND"
		previous_output="${input}_NAVIEND"
		previous_output="${previous_output//$find/$replacement}"
	else
		previous_output="$input"
	fi

	zle kill-whole-line
	LBUFFER="${previous_output}"
	region_highlight=("P0 100 bold")
	zle redisplay
}

zle -N _dspyck_widget
bindkey '^g' _dspyck_widget
