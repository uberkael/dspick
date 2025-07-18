import os
import dspy  # type: ignore
import platform
from config.config import lm
from signature import DescriptionCommand


_ = lm


def predict(
	q: str = "list all files and hidden files in the current directory",
	path = "optimized.pkl") -> DescriptionCommand:
	"""Predict the command to execute based on the description."""
	d = f"in a operating system: {platform.system()}, what is the command and arguments to do: {q}"
	if os.path.exists(path):
		p = dspy.Predict(DescriptionCommand)
		p.load(path)
		return p(description=d)
	else:
		p = dspy.Predict(DescriptionCommand)
		return p(description=d)
