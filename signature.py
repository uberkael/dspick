import dspy  # type: ignore


class DescriptionCommand(dspy.Signature):
	"""Given a description, return a single command and arguments to perform that action."""
	description: str = dspy.InputField(desc="Command description")
	command: str = dspy.OutputField(desc="A single command with arguments to execute in the terminal")
