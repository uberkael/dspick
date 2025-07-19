#!/usr/bin/env python
import subprocess
import sys
from prediction.prediction import predict


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


line = sys.stdin.read().strip().split('|')
line = [li.strip() for li in line]
context = ' | '.join(line[:-1])
last_command = line[-1]
last = last_command


if last_command == "":
	last = last_command
else:
	last = predict(context=context, description=last_command).command

result: str = f"{context} | {last}"
print(result)
