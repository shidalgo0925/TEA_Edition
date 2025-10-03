# app/routes/metas.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import SessionLocal
from app.models.metas import MetaPersonal
from sqlalchemy.orm import joinedload

bp = Blueprint("metas", __name__)

@bp.route("/metas", methods=["GET", "POST"])
def metas_view():
    db_session = SessionLocal()
    try:
        if request.method == "POST":
            categoria = request.form.get("categoria")
            titulo = request.form.get("titulo")
            unidad = request.form.get("unidad")
            valor_objetivo = request.form.get("valor_objetivo")
            tipo = request.form.get("tipo")

            if not titulo or not unidad or not valor_objetivo:
                flash("Todos los campos obligatorios deben estar llenos.", "warning")
                return redirect(url_for("metas.metas_view"))

            nueva_meta = MetaPersonal(
                titulo=titulo,
                categoria=categoria,
                unidad=unidad,
                valor_objetivo=float(valor_objetivo),
                tipo=tipo
            )
            db_session.add(nueva_meta)
            db_session.commit()
            flash("Meta registrada correctamente.", "success")
            return redirect(url_for("metas.metas_view"))

        metas = db_session.query(MetaPersonal).options(joinedload(MetaPersonal.avances)).all()
        return render_template("metas/metas.html", metas=metas)
    except Exception as e:
        db_session.rollback()
        flash("Error inesperado al procesar metas.", "danger")
        return redirect(url_for("metas.metas_view"))
    finally:
        db_session.close()

@bp.route("/metas/<int:meta_id>/editar", methods=["GET", "POST"])
def editar_meta(meta_id):
    db_session = SessionLocal()
    try:
        meta = db_session.query(MetaPersonal).get(meta_id)
        if not meta:
            flash("Meta no encontrada.", "warning")
            return redirect(url_for("metas.metas_view"))

        if request.method == "POST":
            meta.titulo = request.form.get("titulo")
            meta.categoria = request.form.get("categoria")
            meta.unidad = request.form.get("unidad")
            meta.valor_objetivo = float(request.form.get("valor_objetivo"))
            meta.tipo = request.form.get("tipo")
            db_session.commit()
            flash("Meta actualizada correctamente.", "success")
            return redirect(url_for("metas.metas_view"))

        return render_template("metas/editar.html", meta=meta)
    except Exception as e:
        db_session.rollback()
        flash("Error al editar la meta.", "danger")
        return redirect(url_for("metas.metas_view"))
    finally:
        db_session.close()
