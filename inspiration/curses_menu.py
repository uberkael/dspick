import curses


def main(stdscr):
	stdscr.clear()
	stdscr.addstr(0, 0, "Hola! Pulsa una tecla para continuar...")
	stdscr.refresh()
	stdscr.getkey()


curses.wrapper(main)
