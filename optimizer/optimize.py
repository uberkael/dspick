import os
import pickle
from tqdm import tqdm  # type: ignore
from time import sleep
from difflib import SequenceMatcher
import dspy  # type: ignore
from dspy.teleprompt import LabeledFewShot  # type: ignore
from dspy.teleprompt import BootstrapFewShot  # type: ignore
from dspy.teleprompt import BootstrapFewShotWithRandomSearch  # type: ignore
from rich import print
from rich.rule import Rule
# from dspy.teleprompt import KNNFewShot  # type: ignore
from config.config import lm, config
from signature import DescriptionCommand
from optimizer.dataset import test, train


_ = lm

SCORES_FILE = "optimizer/scores.pkl"


def validate_command(example: dspy.Example, pred, trace=None) -> float:
	"""Validate the sentiment of a tweet."""
	a = example.command.lower()  # type: ignore
	b = pred.command.lower()
	# Avoid Quotas
	if config["general"]["throttling"]:
		sleep(60 / config["general"]["rpm"])
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


def save_scores_to_file(dic, file=SCORES_FILE):
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
	scores = calculate(pred, validate_command)
	file_scores[tipo] = scores
	save_scores_to_file(file_scores)
	return scores


def baseline():
	##################
	# Baseline Score #
	##################
	name = "Base:"
	print(f"[cyan]{name}")
	scores = get_scores("baseline_scores", base_predict)
	accuracy = sum(scores) / len(scores)
	print(f"Accuracy: {accuracy}")
	print(Rule('-'))
	return name, scores, accuracy


def labeled_few_shot():
	##################
	# LabeledFewShot #
	##################
	name = "Labeled Few Shot:"
	path = "optimizer/lfs.pkl"
	print(f"[cyan]{name}")
	if os.path.exists(path):
		print(f"[green]Loading file {name}")
		predict = dspy.Predict(DescriptionCommand)
		predict.load(path)
	else:
		print(f"[yellow]Training {name}")
		optimizer = LabeledFewShot()
		while True:
			try:
				predict = optimizer.compile(base_predict, trainset=train)
				break
			except Exception:
				print("[red]❌ Error occurred, retrying in 60 seconds...")
				sleep(62)

	print("[#ff8800]Calculating Scores")
	scores = get_scores("lfs_scores", predict)
	accuracy = sum(scores) / len(scores)

	print(f"Accuracy: {accuracy}")
	print(Rule('-'))
	# Save
	predict.save(path, save_program=False)
	return name, scores, accuracy


def bootstrap_few_shot():
	####################
	# BootstrapFewShot #
	####################
	name = "Bootstrap Few Shot:"
	path = "optimizer/bsfs.pkl"
	print(f"[cyan]{name}")
	if os.path.exists(path):
		print(f"[green]Loading file {name}")
		predict = dspy.Predict(DescriptionCommand)
		predict.load(path)
	else:
		print(f"[yellow]Training {name}")
		optimizer = BootstrapFewShot(
			metric=validate_command,
			max_bootstrapped_demos=4,
			max_labeled_demos=16,
			metric_threshold=1
		)
		while True:
			try:
				predict = optimizer.compile(base_predict, trainset=train)
				break
			except Exception:
				print("[red]❌ Error occurred, retrying in 60 seconds...")
				sleep(62)

	print("[#ff8800]Calculating Scores")
	scores = get_scores("scores", predict)
	accuracy = sum(scores) / len(scores)

	print(f"Accuracy: {accuracy}")
	print(Rule('-'))
	# Save
	predict.save(path, save_program=False)
	return name, scores, accuracy


def bootstrap_few_show_with_random_search():
	####################################
	# BootstrapFewShotWithRandomSearch #
	####################################
	name = "Bootstrap Few Shot With Random Search:"
	path = "optimizer/bsfsrs.pkl"
	print(f"[cyan]{name}")
	if os.path.exists(path):
		print(f"[green]Loading file {name}")
		predict = dspy.Predict(DescriptionCommand)
		predict.load(path)
	else:
		print(f"[yellow]Training {name}")
		optimizer = BootstrapFewShotWithRandomSearch(
			metric=validate_command,
			num_candidate_programs=16,
			max_bootstrapped_demos=8,
			max_labeled_demos=20
		)
		while True:
			try:
				predict = optimizer.compile(base_predict, trainset=train)
				break
			except Exception:
				print("[red]❌ Error occurred, retrying in 60 seconds...")
				sleep(62)


	print("[#ff8800]Calculating Scores")
	scores = get_scores("scores", predict)
	accuracy = sum(scores) / len(scores)

	print(f"Accuracy: {accuracy}")
	print(Rule())
	# Save
	predict.save(path, save_program=False)
	return name, scores, accuracy


def optimize():
	base = baseline()
	lfs = labeled_few_shot()
	bsfs = bootstrap_few_shot()
	bsfsrs = bootstrap_few_show_with_random_search()

	optimizers = [base, lfs, bsfs, bsfsrs]
	accuracy = [o[2] for o in optimizers]
	names = [o[0] for o in optimizers]

	max_acc = max(accuracy)
	max_index = accuracy.index(max_acc)
	name = names[max_index]
	print("Resultado:")
	print(name, max_acc)


if __name__ == '__main__':
	optimize()
