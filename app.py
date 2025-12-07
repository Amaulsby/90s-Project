from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os

app = Flask(__name__)

# Demo-only secret key
app.secret_key = "dev-secret-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "forum.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    # We only need username for the header; posts are static in the template
    username = None
    if "user_id" in session:
        db = get_db()
        row = db.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        username = row["username"] if row else None
    return render_template("index.html", username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()  # PLAIN TEXT FOR DEMO ONLY

        if not username or not password:
            return render_template("register.html", error="Username and password required.")

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            db.commit()
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Username already taken.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get user input from the form
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        db = get_db()

        # ⚠️ UNSAFE VERSION — SQL Injection Vulnerable (Proof of Concept)
        query = (
            'SELECT id, username FROM users WHERE username = "' + username +
            '" AND password = "' + password + '"'
        )

        row = db.execute(query).fetchone()

        if row:
            session["user_id"] = row["id"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))


@app.route("/users-dump")
def users_dump():
    """
    Demo-only page that shows all usernames + passwords.
    You can present this as "what an attacker could see after exploiting a vulnerable app."
    """
    db = get_db()
    users = db.execute("SELECT username, password FROM users ORDER BY id").fetchall()
    return render_template("users_dump.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)

