from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

# 📁 PASTA UPLOADS
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🔥 SUPABASE
BASE_URL = "https://jhxmstvwgpdthxzmehqg.supabase.co/rest/v1/ESCALA"

# 🔑 KEY
KEY = "sb_publishable_PxE3jfK1no41uW0a0DiTLA_ghKc5gBR"

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}

# 🏠 HOME
@app.route("/", methods=["GET", "POST"])
def home():

    # ➕ ADICIONAR
    if request.method == "POST":

        arquivo = request.files.get("anexo")

        nome_arquivo = ""

        if arquivo and arquivo.filename != "":

            nome_arquivo = arquivo.filename

            caminho = os.path.join(
                app.config["UPLOAD_FOLDER"],
                nome_arquivo
            )

            arquivo.save(caminho)

        dados = {
            "data": request.form["data"],
            "lider": request.form["lider"],
            "funcao": request.form["funcao"],
            "anexo": nome_arquivo
        }

        requests.post(
            BASE_URL,
            headers=HEADERS,
            json=dados
        )

        return redirect("/")

    # 🔍 BUSCA
    busca = request.args.get("busca", "").lower()

    resposta = requests.get(
        BASE_URL + "?select=*",
        headers=HEADERS
    )

    escala = resposta.json()

    # 🔎 FILTRO
    if busca:

        escala = [
            item for item in escala
            if busca in item["data"].lower()
            or busca in item["lider"].lower()
        ]

    return render_template(
        "index.html",
        escala=escala
    )

# ❌ REMOVER
@app.route("/remover/<int:id>")
def remover(id):

    requests.delete(
        f"{BASE_URL}?id=eq.{id}",
        headers=HEADERS
    )

    return redirect("/")

# ✏️ EDITAR
@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):

    dados = {
        "lider": request.form["lider"],
        "funcao": request.form["funcao"]
    }

    requests.patch(
        f"{BASE_URL}?id=eq.{id}",
        headers=HEADERS,
        json=dados
    )

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
