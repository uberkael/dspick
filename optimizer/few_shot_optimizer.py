import os
import pickle
from tqdm import tqdm  # type: ignore
from time import sleep
import dspy  # type: ignore
from dspy.teleprompt import LabeledFewShot  # type: ignore
from dspy.teleprompt import BootstrapFewShot  # type: ignore
from dspy.teleprompt import BootstrapFewShotWithRandomSearch  # type: ignore
# from dspy.teleprompt import KNNFewShot  # type: ignore
from config.config import lm
from optimizer.dataset import test, train
from difflib import SequenceMatcher
from signature import DescriptionCommand


_ = lm

SCORES_FILE = "optimizer/scores.pkl"


def validate_command(example: dspy.Example, pred, trace=None) -> float:
	"""Validate the sentiment of a tweet."""
	a = example.command.lower()  # type: ignore
	b = pred.command.lower()
	return SequenceMatcher(None, a, b).ratio()


base_predict = dspy.Predict(DescriptionCommand)


###############
# File Scores #
###############
def get_scores_data(file=SCORES_FILE) -> dict:
	if os.path.exists(file):
		with open(file, "rb") as f:
			return pickle.load(f)
	return {}


def save_scores_to_file(dic, file = SCORES_FILE):
	with open(file, "wb") as f:
		pickle.dump(dic, f)


file_scores = get_scores_data()


#########
# Utils #
#########
def calculate(predictor, validate):
	scores = []
	pb = tqdm(test, desc="Processing", unit="item")
	for x in pb:
		pred = predictor(**x.inputs())
		score = validate(x, pred)
		scores.append(score)
	return scores


def get_scores(tipo, pred):
	scores = file_scores.get(tipo, [])
	if scores:
		return scores
	scores = asyncio.run(calculate_async(pred, validate_command, max_concurrency=1))
	# scores = calculate(pred, validate_command)
	file_scores[tipo] = scores
	save_scores_to_file(file_scores)
	return scores


##################
# Baseline Score #
##################
print("Base:")
baseline_scores = get_scores("baseline_scores", base_predict)
base_accuracy = sum(baseline_scores) / len(baseline_scores)
print(f"Accuracy: {base_accuracy}")
print("-" * 60)


##################
# LabeledFewShot #
##################
print("Labeled Few Shot:")
lfs_optimizer = LabeledFewShot()
lfs_predict = lfs_optimizer.compile(
	base_predict, trainset=train)
lfs_scores = get_scores("lfs_scores", lfs_predict)
lfs_accuracy = sum(lfs_scores) / len(lfs_scores)

print(f"Accuracy: {lfs_accuracy}")
print("-" * 60)
# Save
lfs_predict.save(
	"optimizer/lfs.pkl", save_program=False)

####################
# BootstrapFewShot #
####################
# Genera un programa teacher con pocos ejemplos conocidos, este genera más ejemplos y los altos son usados para optimizar el modelo
print("Bootstrap Few Shot:")
bsfs_optimizer = BootstrapFewShot(
	metric=validate_command,
	max_bootstrapped_demos=4,  # Generated examples
	metric_threshold=1  # Minimum quality threshold
)
bsfs_predict = bsfs_optimizer.compile(
	base_predict, trainset=train)
bsfs_scores = get_scores("bsfs_scores", bsfs_predict)
bsfs_accuracy = sum(bsfs_scores) / len(bsfs_scores)

print(f"Accuracy: {bsfs_accuracy}")
print("-" * 60)
# Save
bsfs_predict.save(
	"optimizer/bsfs.pkl", save_program=False)
