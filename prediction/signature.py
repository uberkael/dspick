import dspy  # type: ignore


class CommandQuestion(dspy.Signature):
	"""Given a question, return a single command and arguments to perform the action."""
	question: str = dspy.InputField(desc="User's question")
	command: str = dspy.OutputField(desc="A single command with arguments to execute in the terminal")
