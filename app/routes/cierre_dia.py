# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from app.extensions import get_db
from app.models.cierre_dia import CierreDia

cierre_bp = Blueprint("cierre_dia", __name__)

@cierre_bp.route("/cierre-dia", methods=["GET", "POST"])
def cierre():
    try:
        db = get_db()
        hoy = date.today()
        entry = db.query(CierreDia).filter_by(user_id=1, fecha=hoy).first()

        if request.method == "POST":
            emocion = request.form.get("emocion", "").strip()
            reflexion = request.form.get("reflexion", "").strip()

            if not emocion and not reflexion:
                flash("Por favor escribe algo para cerrar el día.", "warning")
            else:
                if not entry:
                    entry = CierreDia(user_id=1, fecha=hoy)
                    db.add(entry)

                entry.emocion = emocion
                entry.reflexion = reflexion
                db.commit()
                flash("Cierre del día guardado con éxito 🙏", "success")
                return redirect(url_for("cierre_dia.cierre"))

        return render_template("cierre_dia.html", entry=entry, hoy=hoy)

    except Exception as e:
        return f"<h3>Error interno:</h3><pre>{e}</pre>", 500