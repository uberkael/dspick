#!/usr/bin/env -S uv run --script
import argparse
from optimizer import optimize, reset
from config import menu


def main():
	parser = argparse.ArgumentParser(description="DSPick Completions")
	subparsers = parser.add_subparsers(dest="command", required=True)

	parser_optimize = subparsers.add_parser("optimize", help="Optimize LLM")
	parser_optimize.set_defaults(func=optimize)

	parser_reset = subparsers.add_parser("reset", help="Reset the Optimizer")
	parser_reset.set_defaults(func=reset)

	parser_config = subparsers.add_parser("config", help="Configuration Menu")
	parser_config.set_defaults(func=menu)

	args = parser.parse_args()
	args.func()


if __name__ == "__main__":
	main()
