import subprocess


def fzf_select(options):
	result = subprocess.run(['fzf'], input="\n".join(
		options), text=True, capture_output=True)
	return result.stdout.strip()


selection = fzf_select(["Opción A", "Opción B", "Opción C"])
print("Elegiste:", selection)
