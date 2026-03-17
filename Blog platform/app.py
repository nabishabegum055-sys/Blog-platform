from flask import Flask, render_template, request, redirect, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- USERS ----------

def load_users():
    try:
        with open("users.json","r") as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open("users.json","w") as f:
        json.dump(users,f)

# ---------- POSTS ----------

def load_posts():
    try:
        with open("posts.json","r") as f:
            return json.load(f)
    except:
        return []

def save_posts(posts):
    with open("posts.json","w") as f:
        json.dump(posts,f)

# ---------- HOME ----------

@app.route("/")
def home():
    posts = load_posts()
    return render_template("index.html",posts=posts)

# ---------- REGISTER ----------

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        users = load_users()
        users.append({
            "username":request.form["username"],
            "password":request.form["password"]
        })
        save_users(users)
        return redirect("/login")
    return render_template("register.html")

# ---------- LOGIN ----------

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        users = load_users()
        for u in users:
            if u["username"] == request.form["username"] and u["password"] == request.form["password"]:
                session["user"] = u["username"]
                return redirect("/")
    return render_template("login.html")

# ---------- LOGOUT ----------

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")

# ---------- CREATE ----------

@app.route("/create",methods=["GET","POST"])
def create():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        posts = load_posts()
        posts.append({
            "id":len(posts)+1,
            "title":request.form["title"],
            "content":request.form["content"],
            "image":request.form["image"],
            "likes":0,
            "comments":[]
        })
        save_posts(posts)
        return redirect("/")
    return render_template("create.html")

# ---------- POST VIEW ----------

@app.route("/post/<int:id>",methods=["GET","POST"])
def post(id):
    posts = load_posts()
    for p in posts:
        if p["id"] == id:

            if request.method == "POST":
                p["comments"].append({
                    "user":session.get("user","Anonymous"),
                    "text":request.form["comment"],
                    "time":datetime.now().strftime("%d %b %Y %H:%M")
                })
                save_posts(posts)

            return render_template("post.html",post=p)
    return "Not Found"

# ---------- LIKE ----------

@app.route("/like/<int:id>")
def like(id):
    posts = load_posts()
    for p in posts:
        if p["id"] == id:
            p["likes"] += 1
    save_posts(posts)
    return redirect("/")

# ---------- DELETE ----------

@app.route("/delete/<int:id>")
def delete(id):
    posts = load_posts()
    posts = [p for p in posts if p["id"] != id]
    save_posts(posts)
    return redirect("/")

# ---------- EDIT ----------

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    posts = load_posts()
    for p in posts:
        if p["id"] == id:
            if request.method == "POST":
                p["title"] = request.form["title"]
                p["content"] = request.form["content"]
                p["image"] = request.form["image"]
                save_posts(posts)
                return redirect("/")
            return render_template("edit.html",post=p)

    return "Not Found"

if __name__ == "__main__":
    app.run(debug=True)