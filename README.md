# DsPick

AI Shell Completions:

Like Navi, but with DSPy under the hood.\
Ask, Get a CLI command, Done.

## Installation

Load `dspick` in your shell.

bash:
```bash
source dspick.bash
```

zsh:
```shell
source dspick.zsh
```

Add `.env` with API keys for your LLM provider.
(ollama does not need it)

```
ANTHROPIC_API_KEY=xxxxxx
GOOGLE_API_KEY=xxxxxx
GROQ_API_KEY=xxxxxx
MISTRAL_API_KEY=xxxxxx
OPENAI_API_KEY=xxxxxx
...
```



## Configuration

`config.toml` to edit the config manually in .

Or execute the config tool:
```bash
dspick config
```
![config](screens/config.png)

Models:
![models](screens/models.png)

Options:

- **Cache**: LLM responses will be cached.
- **Throttling**: Enable limit `request per minute` to avoid LLM Quotas.

## Optimize

The optimizer tool improves result accuracy by generating an optimized.pkl file.\
This file will be **automatically used if present**.

DSPy can refine prompts and examples to improve LLM responses. The optimization method may vary depending on the LLM being used.

- **Resumable Process**:  Can be restarted if interrupted and some steps completed successfully.

- **Throttling**: Handles rate limits efficiently (see Throttling).


To run the optimizer:
```bash
dspick optimize
```


##### Accuracy improvements:
![models](screens/optimizer.png)
