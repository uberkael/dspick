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

# Initialize LM based on type
match llm_type:
	case "anthropic":
		load_dotenv()
		key = os.getenv("ANTHROPIC_API_KEY")
		if not key:
			raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
		lm = dspy.LM(model, api_key=key)
	case "google":
		load_dotenv()
		key = os.getenv("GOOGLE_API_KEY")
		if not key:
			raise ValueError("GOOGLE_API_KEY not found in environment variables")
		lm = dspy.LM(model, api_key=key)
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
