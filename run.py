# -*- coding: utf-8 -*-
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Útil para pruebas locales; en producción corre con gunicorn
    app.run(host="0.0.0.0", port=5006, debug=True)
