from flask import Blueprint, render_template, request, redirect, url_for, session

bp = Blueprint("configuracion", __name__, url_prefix="/configuracion")

@bp.route("/", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        enfoque = request.form.get("enfoque")
        if enfoque in ["reflexivo", "neutro", "militar"]:
            session["enfoque_emocional"] = enfoque
        return redirect(url_for("configuracion.config"))
    
    enfoque_actual = session.get("enfoque_emocional", "reflexivo")
    return render_template("configuracion.html", enfoque=enfoque_actual)
