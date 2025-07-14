# Define the function
function dspick() {
	local input="$BUFFER"
	local output
	output=$(print -r -- "$input" | uv run dspick.py)
	BUFFER="$output"
	CURSOR=${#BUFFER}
}

# Create the zle widget
zle -N dspick

# Bind Ctrl+G to the function
bindkey '^G' dspick
