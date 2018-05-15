"""
:module: romulus.py
:description: Romulus app

:author: Arthur Moore <arthur.moore85@gmail.com>
:date: 31/12/16
"""
import npyscreen as npyscreen
from forms import SearchForm

__author__ = 'arthur'

# Switch to True for debugging. Set settings in PyCharm
# to handle remote debugging on localhost port 5678
DEBUG = True


class App(npyscreen.NPSAppManaged):
    """
    Main Romulus app
    """
    # Declaring some shared variables.
    CLEAN_RESULTS = []
    RESULTS = None
    SELECTED_RESULT = None
    RESULTS_DICT = {}
    SCRAPER_OBJ = None

    def onStart(self):
        """
        Initialize the forms.
        """
        if DEBUG:
            import pydevd
            pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)
        self.addForm('MAIN', SearchForm, name="Search for ROM")


if __name__ == '__main__':
    app = App()
    app.run()
