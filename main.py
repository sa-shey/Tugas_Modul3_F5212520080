
from views.buku_view import BukuView
from controllers.buku_controller import BukuController

if __name__ == "__main__":
    view = BukuView()
    app = BukuController(view)
    view.controller = app
    app.load_data()
    view.mainloop()
