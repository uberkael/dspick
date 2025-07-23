import os
import pickle
import random
from tqdm import tqdm  # type: ignore
from time import sleep
from difflib import SequenceMatcher
import dspy  # type: ignore
from dspy.teleprompt import LabeledFewShot  # type: ignore
from dspy.teleprompt import BootstrapFewShot  # type: ignore
from dspy.teleprompt import BootstrapFewShotWithRandomSearch  # type: ignore
from dspy.teleprompt import MIPROv2  # type: ignore
# from dspy.teleprompt import KNNFewShot  # type: ignore
from rich import print
from rich.rule import Rule
from config.config import lm, config
from signature import DescriptionCommand
from optimizer.dataset import test, train


_ = lm
base_predict = dspy.Predict(DescriptionCommand)
SCORES_FILE = "optimizer/scores.pkl"


############
# Validate # MARK: Validate
############
def validate_command(example: dspy.Example, pred, trace=None) -> float:
	"""Validate the sentiment of a tweet."""
	a = example.command.lower()  # type: ignore
	b = pred.command.lower()
	# Avoid Quotas
	if config["general"]["throttling"]:
		sleep(60 / config["general"]["rpm"])
	return SequenceMatcher(None, a, b).ratio()


###############
# File Scores # MARK: File
###############
def get_scores_data(file=SCORES_FILE) -> dict:
	if os.path.exists(file):
		with open(file, "rb") as f:
			return pickle.load(f)
	return {}


def save_scores_to_file(dic, file=SCORES_FILE):
	with open(file, "wb") as f:
		pickle.dump(dic, f)


stored_scores = get_scores_data()


#########
# Utils # MARK: Utils
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
	scores = stored_scores.get(tipo, [])
	if scores:
		return scores
	scores = calculate(pred, validate_command)
	stored_scores[tipo] = scores
	if scores:
		save_scores_to_file(stored_scores)
	return scores


##################
# Baseline Score # MARK: Baseline
##################
def baseline():
	name = "Base:"
	print(f"[cyan]{name}")
	scores = get_scores("baseline_scores", base_predict)
	accuracy = sum(scores) / len(scores)
	print(f"Accuracy: {accuracy}")
	print(Rule('-'))
	return name, accuracy, base_predict


#######################
# Few Shot Optimizers # MARK: Few Shot
#######################
def labeled_few_shot():
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
		predict = optimizer.compile(base_predict, trainset=train)

	print("[#ff8800]Calculating Scores")
	scores = get_scores("lfs_scores", predict)
	accuracy = sum(scores) / len(scores)

	print(f"Accuracy: {accuracy}")
	print(Rule('-'))
	# Save
	predict.save(path, save_program=False)
	return name, accuracy, predict


def bootstrap_few_shot():
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
		predict = optimizer.compile(base_predict, trainset=train)

	print("[#ff8800]Calculating Scores")
	scores = get_scores("scores", predict)
	accuracy = sum(scores) / len(scores)

	print(f"Accuracy: {accuracy}")
	print(Rule('-'))
	# Save
	predict.save(path, save_program=False)
	return name, accuracy, predict


def bootstrap_few_show_with_random_search():
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
			max_bootstrapped_demos=2,
			max_errors=5,
			max_labeled_demos=4,
			metric=validate_command,
			num_candidate_programs=4,
			num_threads=1,
			max_rounds=1,
		)
		predict = optimizer.compile(base_predict, trainset=random.sample(train, 10))

	print("[#ff8800]Calculating Scores")
	scores = get_scores("scores", predict)
	accuracy = sum(scores) / len(scores)

	print(f"Accuracy: {accuracy}")
	print(Rule())
	# Save
	predict.save(path, save_program=False)
	return name, accuracy, predict


#####################
# Prompt Optimizers # MARK: Prompt
#####################
def miprov2():
	name = "MIPROv2:"
	path = "optimizer/copro.pkl"
	print(f"[cyan]{name}")
	if os.path.exists(path):
		print(f"[green]Loading file {name}")
		predict = dspy.Predict(DescriptionCommand)
		predict.load(path)
	else:
		print(f"[yellow]Training {name}")
		optimizer = MIPROv2(
			metric=validate_command,
			prompt_model= lm,
			num_threads=1
		)
		predict = optimizer.compile(base_predict, trainset=train, valset=test)

	print("[#ff8800]Calculating Scores")
	scores = get_scores("copro_scores", predict)
	accuracy = sum(scores) / len(scores)

	print(f"Accuracy: {accuracy}")
	print(Rule('-'))
	# Save
	predict.save(path, save_program=False)
	return name, accuracy, predict


############
# Combined # MARK: Combined
############
def example_and_prompt(best_example):
	ename, _, epredict = best_example
	name = f"{ename} + MIPROv2:"
	path = "optimizer/EP.pkl"
	print(f"[cyan]{name}")
	if os.path.exists(path):
		print(f"[green]Loading file {name}")
		predict = dspy.Predict(DescriptionCommand)
		predict.load(path)
	else:
		print(f"[yellow]Training {name}")
		optimizer = MIPROv2(
			metric=validate_command,
			prompt_model= lm,
			num_threads=1
		)
		predict = optimizer.compile(epredict, trainset=train, valset=test)

	print("[#ff8800]Calculating Scores")
	scores = get_scores("EP_scores", predict)
	accuracy = sum(scores) / len(scores)

	print(f"Accuracy: {accuracy}")
	print(Rule('-'))
	# Save
	predict.save(path, save_program=False)
	return name, accuracy, predict


def optimize_strategies(strategies):
	final = baseline()
	for strategy in strategies:
		try:
			current = strategy()
			if current[1] > final[1]:
				final = current
		except Exception:
			continue
	return final


########
# Main # MARK: Main
########
def optimize():
	# Few Shots
	s_examples = [
		labeled_few_shot,
		bootstrap_few_shot,
		bootstrap_few_show_with_random_search,
	]
	best_example = optimize_strategies(s_examples)
	# Prompt
	best_prompt = miprov2()
	# Combined
	best_combined = example_and_prompt(best_example)

	bests = [best_example, best_prompt, best_combined]
	final = max(bests, key=lambda x: x[1])

	name, acc, predict = final
	predict.save("optimized.pkl", save_program=False)
	print(name, acc)
	print("Save <optimized.pkl>")


if __name__ == '__main__':
	optimize()
