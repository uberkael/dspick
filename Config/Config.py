from dotenv import load_dotenv
import os
import tomllib
import dspy  # type: ignore


def parse_toml(filename):
	with open(filename, "r") as f:
		return tomllib.loads(f.read())


load_dotenv()
google_key = os.getenv("GOOGLE_API_KEY")

parse_toml("config.toml")

# Disable cache for the LM
# dspy.configure_cache(
# 	enable_disk_cache=False,
# 	enable_memory_cache=False,
# )


# lm = dspy.LM(model='ollama/qwen3')
# lm = dspy.LM(model='ollama/deepseek-r1')
# lm = dspy.LM(model='ollama/deepseek-v2')
# lm = dspy.LM(model='ollama/mistral')
# lm = dspy.LM(model='ollama/gemma3')
# lm = dspy.LM('gemini/gemini-2.5-pro', api_key=google_key)
lm = dspy.LM('gemini/gemini-2.5-flash-lite-preview-06-17', api_key=google_key)

dspy.configure(lm=lm)
