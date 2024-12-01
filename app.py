from flask import Flask, render_template, session, redirect, url_for
from form import LoginForm, SignupForm
app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecretkey"

users = [
    {"id": 1, "full_name": "saneeep", "email": "team@email.com", "password": "adminpass"},
]

AI_model_data = [{
    "type": "LLM",
    "description": "LLM is a type of AI model that uses large language models to generate text."
},{
    "type": "RAG",
    "description": "RAG is a type of AI model that uses retrieval augmented generation to generate text."
},{
    "type": "Embedding",
    "description": "Embedding is a type of AI model that uses embeddings to generate text."
},{
    "type": "Vector Database",
    "description": "Vector Database is a type of AI model that uses vector databases to generate text."
}]

@app.route("/")
def home():
    data = {
        "title": "Home: AI-powered chatbot",
        "content": "This is a chatbot powered by AI.",
        "type_of_AI_model": [model["type"] for model in AI_model_data]
    }
    return render_template("home.html", **data)

@app.route("/about/<type>")
def about(type):
    data = {
        "title": "About: AI-powered chatbot",
        "model": [model for model in AI_model_data if model["type"] == type][0]
    }
    return render_template("about.html", **data)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data), None)
        if user is None:
            return render_template("login.html", form=form, message="Invalid credentials")
        else:
            session["user"] = user
            return render_template("login.html", message="Login successful")
    elif form.errors:
        print(form.errors.items())
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("home", _scheme="http", _external=True))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        print(form.full_name.data, form.email.data, form.password.data)
        new_user = {
            "id": len(users) + 1,
            "full_name": form.full_name.data,
            "email": form.email.data,
            "password": form.password.data
        }
        users.append(new_user)
        print(users)
        return render_template("signup.html", message="Signup successful")
    elif form.errors:
        print(form.errors.items())
    return render_template("signup.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

