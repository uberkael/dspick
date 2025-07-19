#!/usr/bin/env -S uv run --script
import sys
from prediction.prediction import predict


line = [li.strip() for li in sys.stdin.read().split('|')]
*prev_commands, last_command = line

if last_command == "":
	if prev_commands:
		context = ' | '.join(prev_commands)
		print(f"{context} | ")
	else:
		print()
else:
	if prev_commands:
		context = ' | '.join(prev_commands)
		result = predict(context=context, description=last_command).command
		print(f"{context} | {result}")
	else:
		result = predict(context="", description=last_command).command
		print(result)
