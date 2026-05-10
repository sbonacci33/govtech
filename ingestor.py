import json
from pathlib import Path

import feedparser

FUENTES = {
    "La Voz del Interior": "https://www.lavoz.com.ar/arc/outboundfeeds/rss/",
    "Infobae": "https://www.infobae.com/feeds/rss/",
    "Télam": "https://www.telam.com.ar/rss/politica.xml",
    "La Nación": "https://www.lanacion.com.ar/arc/outboundfeeds/rss/",
    "Cadena 3": "https://www.cadena3.com/rss.xml",
}

RUTA_DATOS = Path("datos_radar.json")


def cargar_datos():
    if RUTA_DATOS.exists():
        return json.loads(RUTA_DATOS.read_text(encoding="utf-8"))
    return []


def main():
    datos = cargar_datos()
    urls_existentes = {item.get("URL") for item in datos if item.get("URL")}
    resumen = {medio: 0 for medio in FUENTES}

    for medio, feed_url in FUENTES.items():
        try:
            feed = feedparser.parse(feed_url)
            if feed.bozo:
                raise Exception(str(feed.bozo_exception))
            for entry in feed.entries:
                url = entry.get("link", "").strip()
                if not url or url in urls_existentes:
                    continue
                fecha = ""
                if entry.get("published_parsed"):
                    fecha = f"{entry.published_parsed.tm_year:04d}-{entry.published_parsed.tm_mon:02d}-{entry.published_parsed.tm_mday:02d}"
                datos.append({
                    "Fecha": fecha,
                    "Medio": medio,
                    "Titular": entry.get("title", "").strip(),
                    "URL": url,
                    "Tema": "Sin clasificar",
                    "Territorio": "Sin clasificar",
                    "Tono": "neutro",
                    "Referentes": [],
                })
                urls_existentes.add(url)
                resumen[medio] += 1
        except Exception as exc:
            print(f"[ERROR] Falló {medio}: {exc}")

    RUTA_DATOS.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nResumen de notas nuevas por medio:")
    for medio, cantidad in resumen.items():
        print(f"- {medio}: {cantidad}")


if __name__ == "__main__":
    main()
