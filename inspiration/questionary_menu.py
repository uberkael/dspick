import questionary


respuesta = questionary.select(
	"¿Qué herramienta quieres configurar?",
	choices=["Git", "Docker", "Vim"]
).ask()

print("Elegiste:", respuesta)
