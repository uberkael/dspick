import json
import dspy  # type: ignore


data: dict

with open("optimizer/data.json", "r") as f:
	data = json.load(f)["data"]


train_size = 70
test_size = len(data) - train_size

# data_train = data[:train_size]
# data_test = data[train_size:]
train = []
test = []
for i, line in enumerate(data):
	example = dspy.Example(
		command=line.get("command"),
		description=line.get("description")
	).with_inputs("description")

	if i < train_size:
		train.append(example)
	else:
		test.append(example)


if __name__ == "__main__":
	print(data)
