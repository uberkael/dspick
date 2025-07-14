#!/usr/bin/env python
import subprocess
import sys


line = sys.stdin.read().strip().split('|')
line = [li.strip() for li in line]
last_command = line[-1]
last = last_command

REPLACEMENTS = {
	"chose second column": "awk '{print $2}'",
	"chose first column": "awk '{print $1}'",
	"first": "head -n 1",
	"show all": "ps aux",
}


def selector(options):
	opts = [f'"{k}") echo {v}' for k, v in options.items()]
	preview = f"case {{}} in\n{';;'.join(opts)}\nesac"
	try:
		result = subprocess.run(
			["fzf", "--preview", preview],
			input="\n".join(options.keys()),
			text=True,
			capture_output=True,
			check=True
		)
		return result.stdout.strip()
	except subprocess.CalledProcessError:
		return ""  # if cancel Esc


if last_command == "":
	sel = selector(REPLACEMENTS)
	last = REPLACEMENTS.get(sel, "")
else:
	for clave, reemplazo in REPLACEMENTS.items():
		if clave in last_command:
			last = reemplazo


final_prompt: list[str] = line[:-1] + [last]
final: str = ' | '.join(final_prompt)
print(final)
