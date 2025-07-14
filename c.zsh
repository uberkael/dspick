# Define the function
function replace_command() {
  local input="$BUFFER"
  local output
  output=$(print -r -- "$input" | uv run c.py)
  BUFFER="$output"
  CURSOR=${#BUFFER}
}

# Create the zle widget
zle -N replace_command

# Bind Ctrl+G to the function
bindkey '^G' replace_command
