from dotenv import load_dotenv
import os
import dspy  # type: ignore
from config.file_config import config
from ratelimit import limits, sleep_and_retry  # type: ignore


lm = None

match config["llm"]["type"]:
	case "ollama":
		if "ollama" in config:
			lm = dspy.LM(model=config["llm"]["model"])
		else:
			raise ValueError("Ollama model not specified in config.toml")
	case "google":
		if model := config["llm"]["model"]:
			load_dotenv()
			google_key = os.getenv("GOOGLE_API_KEY")
			lm = dspy.LM(model, api_key=google_key)
		else:
			raise ValueError("Google model not specified in config.toml")
	case _:
		raise ValueError(f"Unsupported LLM type: {config['llm']['type']}")

if not config["general"]["cache"]:
	# Disable cache for the LM
	dspy.configure_cache(
		enable_disk_cache=False,
		enable_memory_cache=False,
	)

if not lm:
	raise ValueError("No language model configured. Please check your config.toml file.")

# Set LM for DSPy
dspy.configure(lm=lm)


# Rate limit if configured
@sleep_and_retry
@limits(calls=config["general"]["rpm"], period=60)
def rate_limited_call(prompt, **kwargs):
	return dspy.settings.lm(prompt, **kwargs)


class RateLimitedLM:
	def __init__(self, lm):
		self.lm = lm

	@sleep_and_retry
	@limits(calls=60, period=60)
	def __call__(self, prompt, **kwargs):
		return self.lm(prompt, **kwargs)

	def __getattr__(self, attr):
		return getattr(self.lm, attr)


dspy.settings.configure(lm=RateLimitedLM(dspy.settings.lm))
