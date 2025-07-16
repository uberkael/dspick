import json

data: dict

with open("optimizer/data.json", "r") as f:
	data = json.load(f)["data"]


if __name__ == "__main__":
	print(data)
