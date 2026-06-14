#!/usr/bin/env python3
"""
Descargador de canales IPTV desde iptv-org
Filtra canales de El Salvador y Latinoamérica
"""

import urllib.request
import re
from datetime import datetime

# Países a incluir — puedes agregar o quitar
PAISES = {
    "sv": "El Salvador",
    "gt": "Guatemala",
    "hn": "Honduras",
    "ni": "Nicaragua",
    "cr": "Costa Rica",
    "pa": "Panamá",
    "mx": "México",
    "co": "Colombia",
    "ve": "Venezuela",
    "pe": "Perú",
    "cl": "Chile",
    "ar": "Argentina",
    "bo": "Bolivia",
    "ec": "Ecuador",
    "py": "Paraguay",
    "uy": "Uruguay",
    "do": "Rep. Dominicana",
    "cu": "Cuba",
    "pr": "Puerto Rico",
}

BASE_URL = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/{codigo}.m3u"

def descargar_lista(codigo_pais):
    url = BASE_URL.format(codigo=codigo_pais)
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            contenido = resp.read().decode("utf-8", errors="ignore")
            return contenido
    except Exception as e:
        print(f"  ⚠️  No se pudo descargar {codigo_pais}: {e}")
        return None

def parsear_canales(contenido, nombre_pais):
    """Extrae canales del formato M3U y les asigna el grupo del país."""
    canales = []
    lineas = contenido.strip().splitlines()
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            # Reemplazar group-title con el nombre del país
            linea = re.sub(r'group-title="[^"]*"', f'group-title="{nombre_pais}"', linea)
            if 'group-title=' not in linea:
                linea = linea.replace(",", f' group-title="{nombre_pais}",', 1)

            # Buscar la URL en la siguiente línea no vacía
            j = i + 1
            while j < len(lineas) and not lineas[j].strip():
                j += 1
            if j < len(lineas) and lineas[j].strip().startswith("http"):
                canales.append((linea, lineas[j].strip()))
                i = j + 1
                continue
        i += 1
    return canales

def generar_m3u_latino(output_file="lista.m3u"):
    print("📡 Descargando canales de iptv-org...\n")
    todos_canales = []

    for codigo, nombre in PAISES.items():
        print(f"  🌎 {nombre} ({codigo.upper()})...", end=" ", flush=True)
        contenido = descargar_lista(codigo)
        if contenido:
            canales = parsear_canales(contenido, nombre)
            todos_canales.extend(canales)
            print(f"{len(canales)} canales")
        else:
            print("sin datos")

    # Escribir el archivo final
    lineas_salida = [
        "#EXTM3U",
        f"# Lista IPTV Latinoamérica — generada el {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"# Fuente: github.com/iptv-org/iptv",
        f"# Total canales: {len(todos_canales)}",
        "",
    ]

    for extinf, url in todos_canales:
        lineas_salida.append(extinf)
        lineas_salida.append(url)
        lineas_salida.append("")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_salida))

    print(f"\n✅ Lista generada: {output_file}")
    print(f"   Total canales: {len(todos_canales)}")
    print(f"\n💡 Sube '{output_file}' a tu repositorio de GitHub")
    print(f"   Luego usa el enlace raw en tu reproductor.")

if __name__ == "__main__":
    generar_m3u_latino()
