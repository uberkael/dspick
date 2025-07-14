import subprocess
import sys

opciones = {
	"chose first column": "awk '{print $1}'",
	"chose second column": "awk '{print $2}'",
	"grep error": "grep 'error'",
}

entrada = sys.stdin.read().strip()

# Filtra claves que están en la línea actual
candidatas = [k for k in opciones if k in entrada]

if not candidatas:
	print(entrada)
	sys.exit(0)

# Lanza FZF para elegir cuál reemplazar
fzf = subprocess.Popen(['fzf'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
salida, _ = fzf.communicate(input='\n'.join(candidatas).encode())

if salida:
	clave = salida.decode().strip()
	reemplazo = opciones[clave]
	entrada = entrada.replace(clave, reemplazo)

print(entrada)
