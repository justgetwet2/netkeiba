from unittest import TestCase 
from tkapp import App, tk, pickle
import warnings
# RuntimeWarning: coroutine 'TestApp._start_app' was never awaited

# python -m unittest discover tests
# python -m unittest tests.test_tkapp

class TestApp(TestCase):

    async def _start_app(self):
        self.app.mainloop()

    def setUp(self):
        p = "./data/jra_220717_updated.pickle"
        with open(p, "rb") as f: 
            races = pickle.load(f)
        root = tk.Tk()
        self.app = App(races, master=root)
        
        warnings.simplefilter('ignore', RuntimeWarning)
        self._start_app()
    
    def tearDown(self):
        self.app.destroy()
    
    def test_startup(self):
        title = self.app.winfo_toplevel().title()
        expected = "JRA 22/07/17 第02回福島06"
        self.assertEqual(title, expected)
