import tomllib


def parse_toml(filename):
	with open(filename, "r") as f:
		return tomllib.loads(f.read())


config = parse_toml("config.toml")

if __name__ == "__main__":
	print(config)
