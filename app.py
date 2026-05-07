from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "123"

# 🔥 SUPABASE
BASE_URL = "https://jhxmstvwgpdthxzmehqg.supabase.co/rest/v1/escala"

# 🔑 SUA KEY
KEY = "sb_publishable_PxE3jfK1no41uW0a0DiTLA_ghKc5gBR"

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}

# 🔥 CARREGAR DADOS
def carregar():
    resposta = requests.get(
        BASE_URL,
        headers=HEADERS
    )

    if resposta.status_code == 200:

        dados = resposta.json()

        escala = {}

        for item in dados:

            data = item["data"]

            if data not in escala:
                escala[data] = []

            escala[data].append({
                "lider": item["lider"],
                "funcao": item["funcao"]
            })

        return escala

    return {}

# 🏠 HOME
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        nova_escala = {
            "data": request.form["data"],
            "lider": request.form["lider"],
            "funcao": request.form["funcao"]
        }

        requests.post(
            BASE_URL,
            headers=HEADERS,
            json=nova_escala
        )

        return redirect("/")

    escala = carregar()

    busca = request.args.get("busca")

    if busca:
        escala_filtrada = {}

        for data, lista in escala.items():
            if busca.lower() in data.lower():
                escala_filtrada[data] = lista

        escala = escala_filtrada

    return render_template("index.html", escala=escala)

# ❌ REMOVER
@app.route("/remover", methods=["POST"])
def remover():

    item_id = request.form["id"]

    requests.delete(
        f"{BASE_URL}?id=eq.{item_id}",
        headers=HEADERS
    )

    return redirect("/")

# ✏️ EDITAR
@app.route("/editar", methods=["POST"])
def editar():

    item_id = request.form["id"]

    novos_dados = {
        "lider": request.form["lider"],
        "funcao": request.form["funcao"]
    }

    requests.patch(
        f"{BASE_URL}?id=eq.{item_id}",
        headers=HEADERS,
        json=novos_dados
    )

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
