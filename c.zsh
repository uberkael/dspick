# Define the function
function dspyck_command() {
	local input="$BUFFER"
	local output
	output=$(print -r -- "$input" | uv run c.py)
	BUFFER="$output"
	CURSOR=${#BUFFER}
}

# Create the zle widget
zle -N dspyck_command

# Bind Ctrl+G to the function
bindkey '^G' dspyck_command
