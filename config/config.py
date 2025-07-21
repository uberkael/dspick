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

api_keys = {
	"anthropic": "ANTHROPIC_API_KEY",
	"google": "GOOGLE_API_KEY",
	"groq": "GROQ_API_KEY",
	"mistral": "MISTRAL_API_KEY",
	"openai": "OPENAI_API_KEY",
}

match llm_type:
	case "anthropic" | "google" | "groq" | "mistral" | "openai":
		load_dotenv()
		key = os.getenv(api_keys[llm_type])
		if not key:
			raise ValueError(f"{api_keys[llm_type]} not found in environment variables")
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
