import npyscreen
import signal
from reader_config import config

signal.signal(signal.SIGINT, lambda sig, frame: exit(0))


def get_models(llm_type):
	return config.get(llm_type, {}).get("models", ["<Select a Type>"])


class ConfigForm(npyscreen.Form):
	def create(self):
		self.add(
			npyscreen.FixedText,
			value="Sección: llm",
			editable=False)

		self.llm_type = self.add(
			npyscreen.TitleSelectOne,
			name="type:",
			values=config["llm"]["types"],
			max_height=4,
			scroll_exit=True)

		# Conecta evento al cambiar valor
		self.llm_type.when_value_edited = self.update

		self.llm_cache = self.add(
			npyscreen.Checkbox,
			name="cache",
			value=config["llm"]["cache"])

		self.add(
			npyscreen.FixedText,
			value="Sección: model",
			editable=False)

		self.model_combo = self.add(
			npyscreen.TitleCombo,
			name="model:",
			values=[])

		self.add(
			npyscreen.FixedText,
			value="Pulsa Q, ESC o Ctrl+C para salir",
			editable=False)

	def update(self):
		if self.model_combo.value:
			config["llm"]["model"] = self.model_combo.values[self.model_combo.value]
		if self.llm_type.value:
			selected_index = self.llm_type.value[0]
			selected_type = self.llm_type.values[selected_index]
			models = get_models(selected_type)
			self.model_combo.values = models or ["<Select a Type>"]
			self.model_combo.value = None  # Reset selección
			self.model_combo.display()
			config["llm"]["type"] = selected_type
			print(selected_type)

	def afterEditing(self):
		self.parentApp.setNextForm(None)


class ConfigApp(npyscreen.NPSAppManaged):
	def onStart(self):
		self.addForm('MAIN', ConfigForm)

	def unhandled_input(self, key):
		if key in ('q', 'Q', 27):
			self.setNextForm(None)
			self.switchFormNow()
			exit(0)


if __name__ == '__main__':
	ConfigApp().run()
	print(config['llm']["type"])
	print(config['llm']["cache"])
	print(config['llm']["model"])
