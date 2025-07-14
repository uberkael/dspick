# %%
import dspy  # type: ignore
import platform
from config import lm


_ = lm


class CommandQuestion(dspy.Signature):
	"""Given a question, return a single command and arguments to perform the action."""
	question = dspy.InputField(desc="User's question")
	command = dspy.OutputField(desc="A single command with arguments to execute in the terminal")


q = "list all files and hidden files in the current directory"
predict = dspy.Predict(CommandQuestion)
prediction = predict(question=f"in a operating system: {platform.system()}, what is the command and arguments to do: {q}")

print("-" * 60)
print(prediction.command)
