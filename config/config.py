from dotenv import load_dotenv
import os
import dspy  # type: ignore
from config.file_config import config


# Early exit if config is empty
try:
	llm_config = config["llm"]
	llm_type = llm_config["type"]
	model = llm_config["model"]
except KeyError as e:
	raise ValueError(f"Config LLM {e} not found in config.toml. Run 'dspick config'")


def initialize_lm(env_key, model):
	load_dotenv()
	key = os.getenv(env_key)
	if not key:
		raise ValueError(f"{env_key} not found in environment variables")
	return dspy.LM(model, api_key=key)


# Initialize LM based on type
match llm_type:
	case "anthropic":
		lm = initialize_lm("ANTHROPIC_API_KEY", model)
	case "google":
		lm = initialize_lm("GOOGLE_API_KEY", model)
	case "groq":
		lm = initialize_lm("GROQ_API_KEY", model)
	case "groq":
		lm = initialize_lm("GROQ_API_KEY", model)
	case "ollama":
		lm = dspy.LM(model=model)
	case _:
		raise ValueError(f"Unsupported LLM type: {llm_type}\nRun 'dspick config'")


if not config["general"]["cache"]:
	# Disable cache for the LM
	dspy.configure_cache(
		enable_disk_cache=False,
		enable_memory_cache=False,
	)

# Set LM for DSPy
dspy.configure(lm=lm)
