from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# SUPABASE
BASE_URL = "https://jhxmstvwgpdthxzmehqg.supabase.co/rest/v1/ESCALA"

KEY = "sb_publishable_PxE3jfK1no41uW0a0DiTLA_ghKc5gBR"

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# HOME
@app.route("/", methods=["GET", "POST"])
def home():

    # ADICIONAR
    if request.method == "POST":

        dados = {
            "data": request.form["data"],
            "lider": request.form["lider"],
            "funcao": request.form["funcao"]
        }

        requests.post(
            BASE_URL,
            headers=HEADERS,
            json=dados
        )

        return redirect("/")

    # BUSCAR
    resposta = requests.get(
        BASE_URL + "?select=*",
        headers=HEADERS
    )

    escala = resposta.json()

    return render_template("index.html", escala=escala)

# REMOVER
@app.route("/remover", methods=["POST"])
def remover():

    id = request.form["id"]

    requests.delete(
        BASE_URL + f"?id=eq.{id}",
        headers=HEADERS
    )

    return redirect("/")

# EDITAR
@app.route("/editar", methods=["POST"])
def editar():

    id = request.form["id"]

    dados = {
        "lider": request.form["lider"],
        "funcao": request.form["funcao"]
    }

    requests.patch(
        BASE_URL + f"?id=eq.{id}",
        headers=HEADERS,
        json=dados
    )

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
