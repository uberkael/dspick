from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


def seleccionar_opcion(opciones):
	completer = WordCompleter(opciones, ignore_case=True, sentence=True)
	seleccion = prompt("Selecciona una opción: ", completer=completer)
	return seleccion


# Ejemplo de uso
if __name__ == "__main__":
	opciones = ["saludar", "salir", "ayuda", "listar", "borrar"]
	resultado = seleccionar_opcion(opciones)
	print(f"Elegiste: {resultado}")
