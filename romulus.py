"""
:module: romulus.py
:description: Romulus app

:author: Arthur Moore <arthur.moore85@gmail.com>
:date: 31/12/16
"""
import npyscreen as npyscreen
from forms import FilterForm

__author__ = 'arthur'

# Switch to True for debugging. Set settings in PyCharm
# to handle remote debugging on localhost port 5678
DEBUG = False


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
            # Set DEBUG above to True, and you will be able to use remote
            # debugging for PyCharm and Visual Studio Code.
            import ptvsd
            ptvsd.enable_attach("my_secret", address=('localhost', 3000))
        self.addForm('MAIN', FilterForm, name="System filter ")


if __name__ == '__main__':
    app = App()
    app.run()
