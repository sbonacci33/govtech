import json
import os
from datetime import timedelta
from pathlib import Path

from flask import Flask, jsonify, render_template


FALLBACK_DATOS = [
    {"Fecha": "2026-04-28", "Medio": "La Voz del Interior", "Titular": "Presupuesto provincial bajo revisión ante caída de recaudación", "Tema": "Economía", "Territorio": "Córdoba", "Tono": "neutro"},
    {"Fecha": "2026-04-28", "Medio": "Cadena 3", "Titular": "Docentes anuncian paro para el miércoles por falta de acuerdo salarial", "Tema": "Educación", "Territorio": "Córdoba", "Tono": "negativo"},
    {"Fecha": "2026-04-27", "Medio": "El Doce", "Titular": "Inseguridad en barrio Güemes: vecinos reclaman mayor presencia policial", "Tema": "Seguridad", "Territorio": "Córdoba Capital", "Tono": "negativo"},
    {"Fecha": "2026-04-27", "Medio": "Infobae", "Titular": "Inflación de abril sorprende al mercado con baja mayor a la esperada", "Tema": "Economía", "Territorio": "Nacional", "Tono": "positivo"},
    {"Fecha": "2026-04-26", "Medio": "La Mañana de Córdoba", "Titular": "Municipalidad inaugura obras de pavimentación en zona sur", "Tema": "Infraestructura", "Territorio": "Córdoba Capital", "Tono": "positivo"},
    {"Fecha": "2026-04-26", "Medio": "Cadena 3", "Titular": "UEPC rechaza propuesta del gobierno y endurece postura", "Tema": "Educación", "Territorio": "Córdoba", "Tono": "negativo"},
    {"Fecha": "2026-04-25", "Medio": "La Voz del Interior", "Titular": "Tarifas de transporte: el debate que vuelve a la agenda legislativa", "Tema": "Transporte", "Territorio": "Córdoba", "Tono": "neutro"},
    {"Fecha": "2026-04-25", "Medio": "Télam", "Titular": "Casa Rosada define estrategia ante presión sindical nacional", "Tema": "Política", "Territorio": "Nacional", "Tono": "neutro"},
]


def cargar_datos_radar() -> list[dict]:
    ruta = Path(__file__).resolve().parent / "datos_radar.json"
    if ruta.exists():
        with ruta.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    else:
        datos = FALLBACK_DATOS
    return sorted(datos, key=lambda x: x.get("Fecha", ""), reverse=True)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=30)

    @app.route("/")
    def home() -> str:
        return render_template("index.html")

    @app.route("/radar")
    def radar() -> str:
        datos = cargar_datos_radar()
        datos_json = json.dumps(datos, ensure_ascii=False)
        return render_template("radar.html", datos_json=datos_json)

    @app.route("/api/datos")
    def api_datos():
        return jsonify(cargar_datos_radar())

    @app.route("/servicios")
    def servicios() -> str:
        return render_template("servicios.html")

    @app.route("/equipo")
    def equipo() -> str:
        return render_template("equipo.html")

    @app.route("/contacto")
    def contacto() -> str:
        return render_template("contacto.html")

    return app


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    create_app().run(debug=debug_mode)
