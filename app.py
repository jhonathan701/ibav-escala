from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "123"

# 🔥 SUPABASE
BASE_URL = "https://jhxmstvwgpdthxzmehqg.supabase.co/rest/v1/escala"

# 👇 SUA KEY
KEY = "sb_publishable_PxE3jfK1no41uW0a0DiTLA_ghKc5gBR"

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}


# 🏠 HOME
@app.route("/", methods=["GET", "POST"])
def home():

    # ADICIONAR
    if request.method == "POST":

        if not session.get("admin"):
            return redirect("/")

        data = request.form["data"]
        lider = request.form["lider"]
        funcao = request.form["funcao"]

        requests.post(
            BASE_URL,
            headers=HEADERS,
            json={
                "data": data,
                "lider": lider,
                "funcao": funcao
            }
        )

        return redirect("/")

    # 🔍 BUSCAR
    buscar = request.args.get("buscar")

    response = requests.get(BASE_URL, headers=HEADERS)

    if response.status_code == 200:

        escala = response.json()

        if buscar:
            escala = [
                item for item in escala
                if buscar.lower() in item["data"].lower()
            ]

    else:
        escala = []

    return render_template(
        "index.html",
        escala=escala,
        admin=session.get("admin")
    )


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


# ▶️ START
if __name__ == "__main__":
    app.run(debug=True)
