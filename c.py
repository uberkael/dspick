#!/usr/bin/env python
import sys


linea = sys.stdin.read().strip().split('|')
linea = [li.strip() for li in linea]
last_command = linea[-1]
# print(linea)

REEMPLAZOS = {
	"chose second column": "awk '{print $2}'",
	"chose first column": "awk '{print $1}'",
	"show all processes": "ps aux",
}

for clave, reemplazo in REEMPLAZOS.items():
	if clave in last_command:
		last_command = reemplazo

final_prompt = linea[:-1] + [last_command]
final_prompt = ' | '.join(final_prompt)
print(final_prompt)
