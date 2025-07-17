import os


def delete_files(file_names):
	for file_name in file_names:
		f = f"optimizer/{file_name}"
		if os.path.exists(f):
			try:
				os.remove(f)
			except OSError as e:
				print(f"Error deleting {f}: {e}")


def reset():
	files = [
		"bsfs.pkl",
		"bsfsrs.pkl",
		"lfs.pkl",
		"scores.pkl"]
	print(f"Files:\n\n{'\n'.join(files)}")
	print("\nAre you sure you want to delete the files? (y/n): ")
	answer = input()
	if answer.strip().lower() == "y":
		print("Files Deleted")
		delete_files(files)
	else:
		print("Exiting...")


if __name__ == "__main__":
	reset()
