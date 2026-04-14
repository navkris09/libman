from flask import Flask, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy


def main(debug=False):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "narainthegoatandkrishnathegoat"

    babel = Babel(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)

    with app.app_context():
        db.metadata.reflect(bind=db.engine)

    class_dict = {}

    for table_name, table in db.metadata.tables.items():
        cls = type(table_name.capitalize(), (db.Model,), {"__table__": table})
        class_dict[table_name] = cls

    admin = Admin(app, name="Admin Panel", theme=Bootstrap4Theme(swatch="darkly"))

    book_type = class_dict["book_type"]
    books = class_dict["books"]

    if book_type:

        class BookTypeView(ModelView):
            column_list = (
                "isbn",
                "title",
                "author",
                "genre",
                "date_published",
                "latest_revision",
            )
            form_columns = (
                "isbn",
                "title",
                "author",
                "genre",
                "date_published",
                "latest_revision",
            )
            column_labels = {
                "isbn": "ISBN",
                "title": "TITLE",
                "author": "AUTHOR",
                "genre": "GENRE",
                "date_published": "DATE PUBLISHED",
                "latest_revision": "LATEST REVISION",
            }
            column_searchable_list = ["title", "author", "isbn"]
            column_filters = ["genre"]

    if books:

        class BooksView(ModelView):
            column_list = ("book_id", "isbn", "condition")
            form_columns = ("book_id", "isbn", "condition")
            column_labels = ("book_id", "isbn", "condition")

    if book_type:
        admin.add_view(BookTypeView(book_type, db.session, name="Books"))

    @app.route("/")
    def index():
        return redirect(url_for("admin.index"))

    app.run(debug=debug)


if __name__ == "__main__":
    main(debug=True)
