#!/usr/bin/env python
import subprocess

opciones = [
	"git commit -m \"Mensaje\"",
	"docker-compose up",
	"rsync -avz source/ dest/"
]

try:
	fzf = subprocess.Popen(['fzf', '--prompt=Elige:'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	salida, _ = fzf.communicate(input='\n'.join(opciones).encode())
	print(salida.decode().strip())
except Exception as e:
	print(e)
