import json
import os
import time
from pathlib import Path

from anthropic import Anthropic

RUTA_DATOS = Path("datos_radar.json")
SISTEMA = """Sos un clasificador de noticias políticas argentinas. Dado un titular de noticia, devolvé ÚNICAMENTE un JSON con este formato exacto (sin texto adicional):
{\"Tema\": string, \"Territorio\": string, \"Tono\": string, \"Referentes\": [string]}
Tema: una de estas categorías: Economía, Educación, Seguridad, Salud, Infraestructura, Transporte, Política, Social, Medio Ambiente, Opinión Pública.
Territorio: una de: Córdoba Capital, Interior, Córdoba, Nacional.
Tono: positivo, neutro o negativo (desde la perspectiva del gobierno provincial).
Referentes: lista de nombres propios de políticos mencionados en el titular (puede ser lista vacía)."""


def clasificar_nota(cliente, titular):
    for intento in range(2):
        try:
            resp = cliente.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system=SISTEMA,
                messages=[{"role": "user", "content": titular}],
            )
            contenido = "".join(b.text for b in resp.content if hasattr(b, "text"))
            return json.loads(contenido)
        except Exception:
            if intento == 0:
                time.sleep(2)
            else:
                raise


def main():
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("Falta ANTHROPIC_API_KEY")
    if not RUTA_DATOS.exists():
        raise FileNotFoundError("No existe datos_radar.json")

    datos = json.loads(RUTA_DATOS.read_text(encoding="utf-8"))
    cliente = Anthropic(api_key=key)
    procesadas = 0

    for nota in datos:
        if nota.get("Tema") != "Sin clasificar":
            continue
        try:
            resultado = clasificar_nota(cliente, nota.get("Titular", ""))
            nota["Tema"] = resultado.get("Tema", nota.get("Tema", "Sin clasificar"))
            nota["Territorio"] = resultado.get("Territorio", nota.get("Territorio", "Sin clasificar"))
            nota["Tono"] = resultado.get("Tono", nota.get("Tono", "neutro"))
            nota["Referentes"] = resultado.get("Referentes", nota.get("Referentes", []))
        except Exception as exc:
            print(f"[ERROR] No se pudo clasificar: {nota.get('Titular','')} -> {exc}")
        procesadas += 1
        if procesadas % 10 == 0:
            print(f"Progreso: {procesadas} notas procesadas")

    RUTA_DATOS.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Clasificación finalizada. Notas procesadas: {procesadas}")


if __name__ == "__main__":
    main()
