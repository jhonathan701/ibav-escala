from flask import Flask, render_template, request, redirect, session
from supabase import create_client

app = Flask(__name__)
app.secret_key = "segredo123"

# 🔥 CONFIG SUPABASE
url = "https://jhxmstvwgpdthxzmehqg.supabase.co"
key = "SUA_KEY_AQUI"  # 👉 cole sua publishable key aqui

supabase = create_client(url, key)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        if not session.get("admin"):
            return redirect("/")

        data = request.form["data"]
        lider = request.form["lider"]
        funcao = request.form["funcao"]

        supabase.table("escala").insert({
            "data": data,
            "lider": lider,
            "funcao": funcao
        }).execute()

        return redirect("/")

    resultado = supabase.table("escala").select("*").execute()
    escala = resultado.data

    return render_template("index.html", escala=escala, admin=session.get("admin"))


@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.form["data"]

    resultado = supabase.table("escala").select("*").eq("data", data).execute()
    escala = resultado.data

    return render_template("index.html", escala=escala, admin=session.get("admin"))


@app.route("/remover", methods=["POST"])
def remover():
    if not session.get("admin"):
        return redirect("/")

    id = request.form["id"]

    supabase.table("escala").delete().eq("id", id).execute()

    return redirect("/")


# 🔐 LOGIN
@app.route("/login", methods=["POST"])
def login():
    senha = request.form["senha"]

    if senha == "1234":
        session["admin"] = True

    return redirect("/")


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


if __name__ == "__main__":
    app.run()
