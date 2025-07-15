import npyscreen  # type: ignore
import signal
from file_config import config, save_toml

signal.signal(signal.SIGINT, lambda sig, frame: exit(0))


def get_models(llm_type):
	return config.get(llm_type, {}).get("models", ["<Select a Type>"])


class ConfigForm(npyscreen.Form):
	def create(self):
		self.add(
			npyscreen.FixedText,
			value="╭────────────────────────╮",
			editable=False)

		self.add(
			npyscreen.FixedText,
			value="│  DsPick Configuration  │",
			editable=False)

		self.add(
			npyscreen.FixedText,
			value="╰────────────────────────╯",
			editable=False)

		self.llm_type = self.add(
			npyscreen.TitleCombo,
			name="Type:",
			values=config["llm"]["types"],
			value=0)

		self.llm_type.when_value_edited = self.update_type

		self.model_combo = self.add(
			npyscreen.TitleCombo,
			name="Model:",
			values=get_models(config["llm"]["type"]),
			value=0)

		self.llm_cache = self.add(
			npyscreen.Checkbox,
			name="cache",
			value=config["llm"].get("cache", False))

		self.add(
			npyscreen.FixedText,
			value="Press 'Q' or 'ESC' to exit",
			editable=False,
			rely=-4)

		self.add(
			npyscreen.FixedText,
			value="OK to Save",
			editable=False,
			rely=-3)

	def handle_input(self, input):
		if input in (ord('q'), ord('Q'), 27):
			self.parentApp.setNextForm(None)
			self.editing = False
			exit(0)
		else:
			super().handle_input(input)

	def update_type(self):
		if (idx := self.llm_type.value) < 0:
			return
		selected_type = self.llm_type.values[idx]
		models = get_models(selected_type)
		self.model_combo.values = models
		self.model_combo.value = 0
		self.model_combo.display()

	def afterEditing(self):
		self.parentApp.setNextForm(None)
		config["llm"]["type"] = self.llm_type.values[self.llm_type.value]
		config["llm"]["model"] = self.model_combo.values[self.model_combo.value]
		config["llm"]["cache"] = self.llm_cache.value


class ConfigApp(npyscreen.NPSAppManaged):
	def onStart(self):
		self.addForm('MAIN', ConfigForm)

	def unhandled_input(self, key):
		if key in ('q', 'Q', 27):
			self.setNextForm(None)
			self.switchFormNow()


if __name__ == '__main__':
	ConfigApp().run()
	save_toml(config)
	print("Configuration Saved")
