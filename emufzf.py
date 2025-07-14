from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Crear consola rich
console = Console()

# Lista de comandos/autocompletado
comandos = ["saludar", "salir", "ayuda", "listar", "borrar"]
completer = WordCompleter(comandos, ignore_case=True)

# Crear sesión de prompt
session = PromptSession(completer=completer)


def main():
	while True:
		try:
			user_input = session.prompt("[bold cyan]>>> [/]")
			if user_input == "salir":
				console.print("¡Adiós!", style="bold green")
				break
			elif user_input == "saludar":
				console.print("👋 ¡Hola!", style="bold yellow")
			elif user_input == "ayuda":
				console.print("Comandos disponibles: " +
							  ", ".join(comandos), style="italic blue")
			else:
				console.print(
					f"Comando desconocido: {user_input}", style="red")
		except KeyboardInterrupt:
			continue
		except EOFError:
			break


if __name__ == "__main__":
	main()
