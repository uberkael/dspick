import tomllib
import tomli_w


FILENAME = "config.toml"


def parse_toml():
	with open(FILENAME, "r") as f:
		return tomllib.loads(f.read())


def save_toml(data):
	with open(FILENAME, "wb") as f:
		tomli_w.dump(data, f)


config = parse_toml()

if __name__ == "__main__":
	print(config)
