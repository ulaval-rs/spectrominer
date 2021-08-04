import sys

from spectrominer.ui.app import GUIApp
from spectrominer.web.app import make_web_app


def gui():
    app = GUIApp()
    app.mainloop()


def web(debug: bool = False):
    app = make_web_app()
    app.run_server(debug=debug)


if __name__ == '__main__':
    if 'web' in sys.argv[1:]:
        web('debug' in sys.argv[1:])
    else:
        gui()
