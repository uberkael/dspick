#!/usr/bin/env bash

selected=$(echo -e "git status\ndocker ps\ngrep TODO *" | fzf --prompt="Comando: ")

if [[ -n "$selected" ]]; then
	printf "%s" "$selected"
fi
