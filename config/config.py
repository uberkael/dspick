from dotenv import load_dotenv
import os
import dspy  # type: ignore
from config.file_config import config


lm = None

match config["llm"]["type"]:
	case "ollama":
		if "ollama" in config:
			lm = dspy.LM(model=config["ollama"]["model"])
		else:
			raise ValueError("Ollama model not specified in config.toml")
	case "google":
		if model := config["google"]["model"]:
			load_dotenv()
			google_key = os.getenv("GOOGLE_API_KEY")
			lm = dspy.LM(model, api_key=google_key)
		else:
			raise ValueError("Google model not specified in config.toml")
	case _:
		raise ValueError(f"Unsupported LLM type: {config['llm']['type']}")

if not config["llm"]["cache"]:
	# Disable cache for the LM
	dspy.configure_cache(
		enable_disk_cache=False,
		enable_memory_cache=False,
	)

if not lm:
	raise ValueError("No language model configured. Please check your config.toml file.")

dspy.configure(lm=lm)
