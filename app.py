from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

def carregar():
    try:
        with open("escala.json", "r") as f:
            return json.load(f)
    except:
        return {}

def salvar(dados):
    with open("escala.json", "w") as f:
        json.dump(dados, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def home():
    escala = carregar()

    if request.method == "POST":
        data = request.form["data"]
        lider = request.form["lider"]
        funcao = request.form["funcao"]

        if data not in escala:
            escala[data] = []

        escala[data].append({
            "lider": lider,
            "funcao": funcao
        })

        salvar(escala)
        return redirect("/")

    return render_template("index.html", escala=escala)


@app.route("/remover", methods=["POST"])
def remover():
    escala = carregar()

    data = request.form["data"]
    index = int(request.form["index"])

    del escala[data][index]

    if len(escala[data]) == 0:
        del escala[data]

    salvar(escala)
    return redirect("/")


@app.route("/editar", methods=["POST"])
def editar():
    escala = carregar()

    data = request.form["data"]
    index = int(request.form["index"])

    escala[data][index]["lider"] = request.form["lider"]
    escala[data][index]["funcao"] = request.form["funcao"]

    salvar(escala)
    return redirect("/")


app.run(debug=True)