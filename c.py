#!/usr/bin/env python
import subprocess
import sys


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


def selector(opciones):
	try:
		# Ejecuta fzf con la lista de opciones
		result = subprocess.run(
			["fzf"],
			input="\n".join(opciones),
			text=True,
			capture_output=True,
			check=True
		)
		return result.stdout.strip()
	except subprocess.CalledProcessError:
		return None  # si se cancela con Esc


# print(linea)
# print(len(linea))
if last_command == "":
	# print("No command provided.")
	opciones = ["saludar", "salir", "ayuda", "listar", "borrar"]
	last = selector(opciones)
else:
	# print("For")
	for clave, reemplazo in REEMPLAZOS.items():
		if clave in last_command:
			last = reemplazo


final_prompt: list[str] = linea[:-1] + [last]
final: str = ' | '.join(final_prompt)
print(final)
