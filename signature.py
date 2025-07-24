import dspy  # type: ignore


class DescriptionCommand(dspy.Signature):
	"""Given a Description, Context and Operating System, return a single
	command and arguments to perform that action, without any file, IP etc as
	example"""
	command: str = dspy.OutputField(desc="A single Command with arguments to execute in the terminal")
	context: str = dspy.InputField(desc="Previous commands pipe as Context")
	description: str = dspy.InputField(desc="Command Description")
	os: str = dspy.OutputField(desc="Operating System")
