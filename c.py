#!/usr/bin/env python
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter


linea = sys.stdin.read().strip().split('|')
linea = [li.strip() for li in linea]
last_command = linea[-1]
# print(linea)
last = last_command

REEMPLAZOS = {
	"chose second column": "awk '{print $2}'",
	"chose first column": "awk '{print $1}'",
	"first": "head -n 1",
	"show all": "ps aux",
}

# print(linea)
# print(len(linea))
if last_command == "":
	print("No command provided.")
else:
	# print("For")
	for clave, reemplazo in REEMPLAZOS.items():
		if clave in last_command:
			last = reemplazo


final_prompt: list[str] = linea[:-1] + [last]
final: str = ' | '.join(final_prompt)
print(final)
