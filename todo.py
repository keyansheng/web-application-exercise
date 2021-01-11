import os, sqlite3
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from timezone_converter import convert_timezone


statuses = ["Pending", "Completed"]


class create_item:
    def __init__(self, todo_row, category_dict):
        self.id = todo_row[0]
        self.category = category_dict[todo_row[1]]
        self.description = todo_row[2]
        self.image = todo_row[3]
        self.status = todo_row[4]
        self.addon = convert_timezone(todo_row[5])


def create_category_dict(db):
    category_rows = db.execute("SELECT * FROM Category")
    category_dict = {}
    for category_row in category_rows:
        category_dict[category_row[0]] = category_row[1]
    return category_dict


def save_file(request):
    image = request.files["image"]
    filename = secure_filename(image.filename)
    path = os.path.join("images", filename)
    image.save(path)
    return filename  # new filename


def remove_file(db, filename):
    if filename:
        file_item_count = db.execute(
            "SELECT COUNT(*) FROM Todo WHERE Image = ?", (filename,)
        ).fetchone()[0]
        path = os.path.join("images", filename)
        if file_item_count == 1 and os.path.exists(path):
            os.remove(path)


app = Flask(__name__)


@app.route("/")
def index():
    db = sqlite3.connect("todo.db")

    category_dict = create_category_dict(db)

    todo_rows = db.execute("SELECT * FROM Todo")
    items = []
    for todo_row in todo_rows:
        items.append(create_item(todo_row, category_dict))

    isempty = not len(items)

    db.close()

    return render_template("index.html", isempty=isempty, items=items)


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    db = sqlite3.connect("todo.db")
    if request.method == "GET":
        category_dict = create_category_dict(db)
        return render_template("add_item.html", category_dict=category_dict)
    try:
        if request.files:
            filename = save_file(request)
            keys = "Category, Description, Image"
            placeholder = "?, ?, ?"
            values = (
                request.form["category"],
                request.form["description"],
                filename,
            )
        else:
            keys = "Category, Description"
            placeholder = "?, ?"
            values = (request.form["category"], request.form["description"])

        db.execute(f"INSERT INTO Todo ({keys}) VALUES({placeholder})", values)
        db.commit()
        db.close()

        return render_template(
            "result.html",
            result="Success",
            result_message="Item added successfully",
        )
    except:
        return render_template(
            "result.html", result="Error", result_message="Failed to add item"
        )


@app.route("/edit_item/<item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    db = sqlite3.connect("todo.db")
    if request.method == "GET":
        category_dict = create_category_dict(db)

        todo_row = db.execute("SELECT * FROM Todo WHERE ID=?", (item_id,))
        item = create_item(todo_row.fetchone(), category_dict)

        return render_template(
            "edit_item.html",
            category_dict=category_dict,
            item=item,
            statuses=statuses,
        )
    try:
        # filename = old filename
        filename = db.execute(
            "SELECT Image FROM Todo WHERE ID = ?", (item_id,)
        ).fetchone()[0]
        if request.files:  # add/change image
            remove_file(db, filename)
            filename = save_file(request)  # filename = new filename
        elif request.form.get("remove-image"):  # remove image
            remove_file(db, filename)
            filename = None  # image removed, filename = None

        keys = "Category = ?, Description = ?, Image = ?, Status = ? "
        values = (
            request.form["category"],
            request.form["description"],
            filename,
            request.form["status"],
            item_id,
        )

        db.execute(f"UPDATE Todo SET {keys} WHERE ID = ?", values)
        db.commit()
        db.close()

        return render_template(
            "result.html",
            result="Success",
            result_message="Item edited successfully",
        )
    except:
        return render_template(
            "result.html", result="Error", result_message="Failed to edit item"
        )


@app.route("/delete_item/<item_id>", methods=["GET", "POST"])
def delete_item(item_id):
    db = sqlite3.connect("todo.db")
    if request.method == "GET":
        category_dict = create_category_dict(db)

        todo_row = db.execute("SELECT * FROM Todo WHERE ID=?", (item_id,))
        item = create_item(todo_row.fetchone(), category_dict)

        return render_template(
            "delete_item.html",
            item=item,
        )
    try:
        # filename = old filename
        filename = db.execute(
            "SELECT Image FROM Todo WHERE ID = ?", (item_id,)
        ).fetchone()[0]
        remove_file(db, filename)

        db.execute("DELETE FROM Todo WHERE ID = ?", (item_id,))
        db.commit()
        db.close()

        return render_template(
            "result.html",
            result="Success",
            result_message="Item deleted successfully",
        )
    except:
        return render_template(
            "result.html",
            result="Error",
            result_message="Failed to delete item",
        )


@app.route("/images/<filename>")
def get_image(filename):
    return send_from_directory("images", filename)


if __name__ == "__main__":
    app.run()
    # app.run(host="0.0.0.0")
