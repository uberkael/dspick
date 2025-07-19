local __dspick_dir="${0:a:h}"

function dspick() {
	local input="$BUFFER"
	local output
	output=$(cd "$__dspick_dir" && print -r -- "$input" | uv run dspick.py)
	BUFFER="$output"
	CURSOR=${#BUFFER}
}

# Create the zle widget
zle -N dspick

# Bind Ctrl+G to the function
bindkey '^G' dspick
