import subprocess


def selector(options):
	opts = [f'"{k}") echo {v}' for k, v in options.items()]
	preview = f"case {{}} in\n{';;'.join(opts)}\nesac"
	try:
		result = subprocess.run(
			["fzf", "--preview", preview],
			input="\n".join(options.keys()),
			text=True,
			capture_output=True,
			check=True
		)
		return result.stdout.strip()
	except subprocess.CalledProcessError:
		return ""  # if cancel Esc
