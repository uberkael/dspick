#!/usr/bin/env zsh
local __dspick_dir="${0:a:h}"

function __dspick() {
	local input="$BUFFER"
	local output
	output=$(cd "$__dspick_dir" && print -r -- "$input" | uv run dspick.py)
	BUFFER="$output"
	CURSOR=${#BUFFER}
}

# Create the zle widget
zle -N __dspick

# Bind Ctrl+E to the function
bindkey '^E' __dspick
