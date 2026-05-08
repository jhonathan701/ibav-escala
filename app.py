from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# 🔥 SUPABASE
BASE_URL = "https://jhxmstvwgpdthxzmehqg.supabase.co/rest/v1/ESCALA"

ANEXOS_URL = "https://jhxmstvwgpdthxzmehqg.supabase.co/rest/v1/ANEXOS"

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

    # ➕ ADICIONAR ESCALA
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

    # 🔍 BUSCA ESCALA
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

    # 📎 BUSCAR ANEXOS
    resposta_anexos = requests.get(
        ANEXOS_URL + "?select=*",
        headers=HEADERS
    )

    anexos = resposta_anexos.json()

    return render_template(
        "index.html",
        escala=escala,
        anexos=anexos
    )

# ❌ REMOVER ESCALA
@app.route("/remover/<int:id>")
def remover(id):

    requests.delete(
        f"{BASE_URL}?id=eq.{id}",
        headers=HEADERS
    )

    return redirect("/")

# ✏️ EDITAR ESCALA
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

# 📎 ADICIONAR ANEXO
@app.route("/anexar", methods=["POST"])
def anexar():

    arquivo = request.files.get("arquivo")

    nome_arquivo = ""

    if arquivo and arquivo.filename != "":

        nome_arquivo = arquivo.filename

        # 🔥 ENVIAR PARA STORAGE SUPABASE
        upload_url = "https://jhxmstvwgpdthxzmehqg.supabase.co/storage/v1/object/anexos/" + nome_arquivo

        headers_upload = {
            "apikey": KEY,
            "Authorization": f"Bearer {KEY}",
            "Content-Type": arquivo.content_type
        }

        requests.post(
            upload_url,
            headers=headers_upload,
