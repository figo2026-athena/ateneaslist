#!/usr/bin/env python3
"""
Generador de lista M3U para IPTV personal
Convierte canales.json → lista.m3u
"""

import json
from datetime import datetime

def generar_m3u(input_file="canales.json", output_file="lista.m3u"):
    with open(input_file, "r", encoding="utf-8") as f:
        datos = json.load(f)

    lineas = []
    lineas.append("#EXTM3U")
    lineas.append(f"# Lista generada el {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lineas.append("")

    total = 0
    for grupo in datos["grupos"]:
        nombre_grupo = grupo["nombre"]
        for canal in grupo["canales"]:
            nombre  = canal.get("nombre", "Sin nombre")
            canal_id = canal.get("id", "")
            logo    = canal.get("logo", "")
            url     = canal.get("url", "")

            if not url or "TU_ENLACE_AQUI" in url:
                print(f"  ⚠️  Saltando '{nombre}' — URL no configurada")
                continue

            extinf = (
                f'#EXTINF:-1 tvg-id="{canal_id}" '
                f'tvg-name="{nombre}" '
                f'tvg-logo="{logo}" '
                f'group-title="{nombre_grupo}",{nombre}'
            )
            lineas.append(extinf)
            lineas.append(url)
            lineas.append("")
            total += 1

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"\n✅ Lista generada: {output_file}")
    print(f"   Canales incluidos: {total}")

if __name__ == "__main__":
    generar_m3u()
