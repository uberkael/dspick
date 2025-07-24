#!/usr/bin/env -S uv run --script
import platform
import sys
from prediction.prediction import predict

line = [li.strip() for li in sys.stdin.read().split('|')]
*prev, last = line
context = ' | '.join(prev) if prev else ""

if last == "":
	print(f"{context} | " if context else "")
else:
	result = predict(context=context, description=last, os=platform.system()).command
	print(f"{context} | {result}" if context else result)
