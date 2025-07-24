from os import path as file_path
import dspy  # type: ignore
from config.config import lm
from signature import DescriptionCommand


_ = lm


def predict(
	context: str,
	description: str = "list all files and hidden files in the current directory",
	os: str = "Linux",
	path = "optimized.pkl") -> DescriptionCommand:
	"""Predict the command to execute based on the description."""
	if file_path.exists(path):
		p = dspy.Predict(DescriptionCommand)
		p.load(path)
		return p(context=context, description=description, os=os)
	else:
		p = dspy.Predict(DescriptionCommand)
		return p(context=context, description=description, os=os)
