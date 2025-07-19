#!/usr/bin/env python
import sys
from prediction.prediction import predict


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
