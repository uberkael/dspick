#!/usr/bin/env python
import subprocess
import sys
from prediction import predict


line = sys.stdin.read().strip().split('|')
line = [li.strip() for li in line]
last_command = line[-1]
last = last_command


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
	last = last_command
else:
	last = predict(last_command).command

final_prompt: list[str] = line[:-1] + [last]
final: str = ' | '.join(final_prompt)
print(final)
