import os
import dspy  # type: ignore
import platform
from config.config import lm
from signature import DescriptionCommand


_ = lm


def predict(
	context: str,
	description: str = "list all files and hidden files in the current directory",
	path = "optimized.pkl") -> DescriptionCommand:
	"""Predict the command to execute based on the description."""
	d = f"{description}, OS: {platform.system()}"
	if os.path.exists(path):
		p = dspy.Predict(DescriptionCommand)
		p.load(path)
		return p(context=context, description=d)
	else:
		p = dspy.Predict(DescriptionCommand)
		return p(context=context, description=d)
