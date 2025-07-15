import urwid

# Opciones del menú
menu_opciones = ["Configurar Git",
								"Configurar Docker", "Configurar Vim", "Salir"]


def menu_principal():
	cuerpo = [urwid.Text(
		"Selecciona una herramienta para configurar:\n"), urwid.Divider()]

	for option in menu_opciones:
		boton = urwid.Button(option)
		urwid.connect_signal(boton, 'click', opcion_seleccionada, option)
		cuerpo.append(urwid.AttrMap(boton, None, focus_map='reversed'))

	return urwid.ListBox(urwid.SimpleFocusListWalker(cuerpo))


def opcion_seleccionada(boton, option):
	if option == "Salir":
		raise urwid.ExitMainLoop()
	respuesta = urwid.Text([f"\nHas elegido: {option}\n\nPulsa Q para salir."])
	contenido = urwid.Filler(respuesta, valign='top')
	main.original_widget = urwid.Overlay(contenido, menu, align='center', width=(
		'relative', 80), valign='middle', height=('relative', 60))


def salir_con_q(key):
	if key in ('q', 'Q'):
		raise urwid.ExitMainLoop()


menu = menu_principal()
main = urwid.MainLoop(menu, unhandled_input=salir_con_q)
main.run()
