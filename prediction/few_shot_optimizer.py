import os
import pickle
from time import sleep
import dspy  # type: ignore
from dspy.teleprompt import LabeledFewShot  # type: ignore
# from dspy.teleprompt import BootstrapFewShot  # type: ignore
# from dspy.teleprompt import BootstrapFewShotWithRandomSearch  # type: ignore
# from dspy.teleprompt import KNNFewShot  # type: ignore
from config.config import lm
from dataset import data
from difflib import SequenceMatcher
from signature import DescriptionCommand


_ = lm

SCORES_FILE = "scores.pkl"

train_size = 70
test_size = len(data) - train_size

train = data[:train_size]
test = data[train_size:]


def validate_command(example: dspy.Example, pred, trace=None) -> float:
	"""Validate the sentiment of a tweet."""
	a = example.get("command", "").lower()  # type: ignore
	b = pred.lower()
	return SequenceMatcher(None, a, b).ratio()


base_predict = dspy.Predict(DescriptionCommand)


#############
# File Data #
#############
def get_data(file=SCORES_FILE) -> dict:
	if os.path.exists(file):
		with open(file, "rb") as f:
			return pickle.load(f)
	return {}


def save_to_file(dic, file = SCORES_FILE):
	with open(file, "wb") as f:
		pickle.dump(dic, f)


file_data = get_data()


##################
# Baseline Score #
##################
def calculate(predictor, validate):
	scores = []
	i = 0
	for x in test:
		pred = predictor(**x)
		score = validate(x, pred.command)
		scores.append(score)
		print(i)
		i += 1
		sleep(5)
	return scores


def get_scores(tipo, pred):
	scores = file_data.get(tipo, [])
	if scores:
		return scores
	scores = calculate(pred, validate_command)
	file_data[tipo] = scores
	save_to_file(file_data)
	return scores


baseline_scores = get_scores("baseline_scores", base_predict)
base_accuracy = sum(baseline_scores) / len(baseline_scores)

print(f"Base: {base_accuracy}")


##################
# LabeledFewShot #
##################
lfs_optimizer = LabeledFewShot()
lfs_predict = lfs_optimizer.compile(
	base_predict, trainset=train)

lfs_scores = get_scores("lfs_scores", lfs_predict)
lfs_accuracy = sum(lfs_scores) / len(lfs_scores)

print(f"Labeled Few Shot: {lfs_accuracy}")

# # Save podemos guardar el modelo optimizado
# lfs_predict.save("./optimized_lfs.pkl", save_program=False)
# # Load

# lfs_accuracy = lfs_scores.count(True) / len(lfs_scores)
# lfs_sentiment = lfs_predict(tweet=example_tweet).sentiment
