import os
from datetime import timedelta

from flask import Flask, render_template


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=30)

    @app.route("/")
    def home() -> str:
        return render_template("index.html")

    @app.route("/radar")
    def radar() -> str:
        # Datos de muestra — reemplazar por gspread cuando esté en producción
        import json
        datos = [
          {"Fecha":"2026-04-28","Medio":"La Voz del Interior","Titular":"Presupuesto provincial bajo revisión ante caída de recaudación","Tema":"Economía","Territorio":"Córdoba"},
          {"Fecha":"2026-04-28","Medio":"Cadena 3","Titular":"Docentes anuncian paro para el miércoles por falta de acuerdo salarial","Tema":"Educación","Territorio":"Córdoba"},
          {"Fecha":"2026-04-27","Medio":"El Doce","Titular":"Inseguridad en barrio Güemes: vecinos reclaman mayor presencia policial","Tema":"Seguridad","Territorio":"Córdoba Capital"},
          {"Fecha":"2026-04-27","Medio":"Infobae","Titular":"Inflación de abril sorprende al mercado con baja mayor a la esperada","Tema":"Economía","Territorio":"Nacional"},
          {"Fecha":"2026-04-26","Medio":"La Mañana de Córdoba","Titular":"Municipalidad inaugura obras de pavimentación en zona sur","Tema":"Infraestructura","Territorio":"Córdoba Capital"},
          {"Fecha":"2026-04-26","Medio":"Cadena 3","Titular":"UEPC rechaza propuesta del gobierno y endurece postura","Tema":"Educación","Territorio":"Córdoba"},
          {"Fecha":"2026-04-25","Medio":"La Voz del Interior","Titular":"Tarifas de transporte: el debate que vuelve a la agenda legislativa","Tema":"Transporte","Territorio":"Córdoba"},
          {"Fecha":"2026-04-25","Medio":"Télam","Titular":"Casa Rosada define estrategia ante presión sindical nacional","Tema":"Política","Territorio":"Nacional"},
          {"Fecha":"2026-04-24","Medio":"El Doce","Titular":"Nuevo hospital regional: licitación desierta por segunda vez","Tema":"Salud","Territorio":"Interior"},
          {"Fecha":"2026-04-24","Medio":"La Voz del Interior","Titular":"Siciliano encabeza reunión con intendentes del interior provincial","Tema":"Política","Territorio":"Córdoba"},
          {"Fecha":"2026-04-23","Medio":"Cadena 3","Titular":"Economía Córdoba: exportaciones agropecuarias cayeron 8% en el trimestre","Tema":"Economía","Territorio":"Córdoba"},
          {"Fecha":"2026-04-23","Medio":"Infobae","Titular":"Encuesta: confianza en instituciones provinciales supera promedio nacional","Tema":"Opinión Pública","Territorio":"Nacional"},
          {"Fecha":"2026-04-22","Medio":"La Mañana de Córdoba","Titular":"Obras de cloacas paralizadas en Villa El Libertador","Tema":"Infraestructura","Territorio":"Córdoba Capital"},
          {"Fecha":"2026-04-22","Medio":"El Doce","Titular":"Detienen banda que operaba en zona norte de la capital","Tema":"Seguridad","Territorio":"Córdoba Capital"},
          {"Fecha":"2026-04-21","Medio":"Cadena 3","Titular":"Salud pública: déficit de médicos en hospitales del interior","Tema":"Salud","Territorio":"Interior"},
          {"Fecha":"2026-04-21","Medio":"La Voz del Interior","Titular":"Legislatura aprueba modificación al código de habilitaciones comerciales","Tema":"Política","Territorio":"Córdoba"},
          {"Fecha":"2026-04-20","Medio":"Infobae","Titular":"Dólar estable: el campo retiene liquidación a la espera de definiciones","Tema":"Economía","Territorio":"Nacional"},
          {"Fecha":"2026-04-20","Medio":"El Doce","Titular":"Vecinos de Alta Córdoba bloquean acceso a planta de residuos","Tema":"Medio Ambiente","Territorio":"Córdoba Capital"},
          {"Fecha":"2026-04-19","Medio":"La Voz del Interior","Titular":"Transporte: empresas piden aumento de subsidio o amenazan reducir frecuencias","Tema":"Transporte","Territorio":"Córdoba"},
          {"Fecha":"2026-04-19","Medio":"Cadena 3","Titular":"Gremios de salud anuncian estado de alerta por falta de insumos","Tema":"Salud","Territorio":"Córdoba"},
          {"Fecha":"2026-04-18","Medio":"La Mañana de Córdoba","Titular":"Elecciones 2027: intendentes del PJ definen estrategia territorial","Tema":"Política","Territorio":"Interior"},
          {"Fecha":"2026-04-18","Medio":"Infobae","Titular":"Pobreza en Córdoba baja levemente pero sigue sobre el 35%","Tema":"Economía","Territorio":"Córdoba"},
          {"Fecha":"2026-04-17","Medio":"El Doce","Titular":"Seguridad vial: más de 200 alcoholemias positivas en operativo del fin de semana","Tema":"Seguridad","Territorio":"Córdoba Capital"},
          {"Fecha":"2026-04-17","Medio":"La Voz del Interior","Titular":"Agua potable: EPAS detecta pérdidas estructurales en red del norte","Tema":"Infraestructura","Territorio":"Interior"},
          {"Fecha":"2026-04-16","Medio":"Cadena 3","Titular":"UEPC convoca a asamblea provincial para el lunes","Tema":"Educación","Territorio":"Córdoba"},
          {"Fecha":"2026-04-16","Medio":"La Mañana de Córdoba","Titular":"Municipio lanza programa de empleo para jóvenes en barrios vulnerables","Tema":"Social","Territorio":"Córdoba Capital"},
          {"Fecha":"2026-04-15","Medio":"Infobae","Titular":"Córdoba entre las provincias con mejor gestión fiscal según ranking nacional","Tema":"Economía","Territorio":"Córdoba"},
          {"Fecha":"2026-04-15","Medio":"El Doce","Titular":"Incendio en depósito industrial en zona sur deja pérdidas millonarias","Tema":"Seguridad","Territorio":"Córdoba Capital"},
        ]
        datos_json = json.dumps(datos, ensure_ascii=False)
        return render_template("radar.html", datos_json=datos_json)

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
