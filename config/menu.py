import npyscreen  # type: ignore
import signal
from file_config import config, save_toml


signal.signal(signal.SIGINT, lambda sig, frame: exit(0))


def get_models(llm_type):
	return config.get(llm_type, {}).get("models", ["<Select a Type>"])


class ConfigForm(npyscreen.Form):
	def create(self):
		self.add_handlers({
			ord('q'): exit,
			ord('Q'): exit,
			155: exit,
			27: exit,
			17: exit,
		})
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

		self.type = self.add(
			npyscreen.TitleCombo,
			name="Type:",
			values=config.get("llm", {}).get("types"),
			value=config.get("llm", {}).get("types").index(config.get("llm", {}).get("type")))

		self.type.when_value_edited = self.update_type  # type: ignore

		self.model_combo = self.add(
			npyscreen.TitleCombo,
			name="Model:",
			values=get_models(config.get("llm", {}).get("type")),
			value=get_models(config.get("llm", {}).get("type")).index(config.get("llm", {}).get("model")) if (config.get("llm", {}).get("model")) in get_models(config.get("llm", {}).get("type")) else 0)

		self.cache = self.add(
			npyscreen.Checkbox,
			name="Cache:",
			value=config.get("general", {}).get("cache", False))

		self.throttling = self.add(
			npyscreen.Checkbox,
			name="Enable Throttling",
			value=config.get("general", {}).get("throttling", True))

		self.throttling.when_value_edited = self.update_throttling  # type: ignore

		self.rpm = self.add(
			npyscreen.TitleSlider,
			lowest=1,
			name="Requests per Minute (Quotas):",
			out_of=300,
			step=5,
			value=int(config.get("general", {}).get("rpm", 12)),
			width=60,
			hidden=not self.throttling.value)

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

	def update_type(self):
		if (idx := self.type.value) < 0:
			return
		selected_type = self.type.values[idx]
		models = get_models(selected_type)
		self.model_combo.values = models  # type: ignore
		self.model_combo.value = 0 if self.model_combo.value >= len(models) else self.model_combo.value  # type: ignore
		self.model_combo.display()

	def update_throttling(self):
		self.rpm.hidden = not self.throttling.value  # type: ignore
		if not self.throttling.value:
			self.rpm.value = 12  # type: ignore
		self.rpm.display()

	def afterEditing(self):
		self.parentApp.setNextForm(None)
		config["llm"]["type"] = self.type.values[self.type.value]
		config["llm"]["model"] = self.model_combo.values[self.model_combo.value]
		config["general"]["cache"] = self.cache.value
		config["general"]["throttling"] = self.throttling.value
		try:
			config["general"]["rpm"] = max(1, int(self.rpm.value))
		except ValueError:
			config["general"]["rpm"] = 12


class ConfigApp(npyscreen.NPSAppManaged):
	def onStart(self):
		self.addForm('MAIN', ConfigForm)


if __name__ == '__main__':
	ConfigApp().run()
	save_toml(config)
	print("Configuration Saved")
