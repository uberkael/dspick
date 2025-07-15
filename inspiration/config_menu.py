import questionary
from pprint import pprint
import os
from typing import Dict, Any

# Configuración inicial por defecto
DEFAULT_CONFIG = {
	"llm": {
		"type": "ollama",
		"cache": True,
		"model": "ollama/mistral"
	}
}


def clear_screen():
	"""Limpia la pantalla de la consola"""
	os.system('cls' if os.name == 'nt' else 'clear')


def show_main_menu(config: Dict[str, Any]) -> Dict[str, Any]:
	"""Muestra el menú principal y maneja la navegación"""
	while True:
		clear_screen()
		print("╭────────────────────────╮")
		print("│  DsPick Configuration  │")
		print("╰────────────────────────╯\n")

		# Mostrar configuración actual
		pprint(config["llm"], indent=2, width=40)
		print("\n")

		# Menú de opciones
		choice = questionary.select(
			"Seleccione una opción para configurar:",
			choices=[
				{"name": "1. Tipo de LLM", "value": "type"},
				{"name": "2. Habilitar caché", "value": "cache"},
				{"name": "3. Modelo específico", "value": "model"},
				{"name": "4. Guardar y salir", "value": "save"},
				{"name": "5. Salir sin guardar", "value": "exit"},
			],
			use_shortcuts=True,
			use_arrow_keys=True,
			use_jk_keys=True,
			instruction="(Use ↑/↓ o j/k para navegar, Enter para seleccionar)"
		).ask()

		if choice == "type":
			config["llm"]["type"] = questionary.select(
				"Seleccione el tipo de LLM:",
				choices=[
					{"name": "OpenAI", "value": "openai"},
					{"name": "Anthropic", "value": "anthropic"},
					{"name": "Llama 2", "value": "llama2"},
					{"name": "Google Gemini", "value": "gemini"},
					{"name": "Mistral", "value": "mistral"},
				],
				default=config["llm"]["type"]
			).ask()

		elif choice == "cache":
			config["llm"]["cache"] = questionary.confirm(
				"¿Habilitar caché para respuestas LLM?",
				default=config["llm"]["cache"]
			).ask()

		elif choice == "model":
			# Modelos dependientes del tipo seleccionado
			model_choices = {
				"openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
				"anthropic": ["claude-3-opus", "claude-3-sonnet", "claude-2"],
				"llama2": ["llama2-7b", "llama2-13b", "llama2-70b"],
				"gemini": ["gemini-pro", "gemini-ultra"],
				"mistral": ["mistral-7b", "mixtral-8x7b"],
			}.get(config["llm"]["type"], ["default-model"])

			config["llm"]["model"] = questionary.select(
				f"Seleccione modelo para {config['llm']['type']}:",
				choices=model_choices,
				default=config["llm"]["model"]
			).ask()

		elif choice == "save":
			# Aquí podrías guardar a un archivo TOML/JSON
			print("\nConfiguración guardada (simulado):")
			pprint(config, indent=2)
			input("\nPresione Enter para continuar...")
			return config

		elif choice == "exit":
			if questionary.confirm("¿Salir sin guardar los cambios?").ask():
				return None


if __name__ == "__main__":
	# Iniciar la herramienta
	final_config = show_main_menu(DEFAULT_CONFIG.copy())

	if final_config:
		print("\nConfiguración final:")
		pprint(final_config)
	else:
		print("\nNo se guardaron cambios.")
