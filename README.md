# 📺 Mi Lista IPTV Personal

Lista M3U de canales de TV en vivo, gestionada con GitHub para actualización automática.

---

## 🚀 Cómo usar en tu reproductor

Copia el enlace **raw** de `lista.m3u` y pégalo en tu app:

```
https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/lista.m3u
```

> Cada vez que el reproductor cargue la lista, descargará la versión más reciente.

### Apps compatibles
| App | Plataforma | Cómo agregar |
|-----|-----------|--------------|
| VLC | Windows/Mac/Linux/Android/iOS | Media → Abrir URL de red |
| TiviMate | Android/FireTV | Agregar lista → URL |
| IPTV Smarters | Android/iOS | M3U URL |
| Kodi (PVR IPTV) | Multiplataforma | M3U Plus URL |
| OTT Navigator | Android | Agregar fuente M3U |

---

## ✏️ Cómo agregar o editar canales

### Opción A — Directo en GitHub (más fácil)
1. Abre `canales.json` en GitHub
2. Haz clic en el ícono de lápiz ✏️
3. Agrega tu canal siguiendo la estructura:
```json
{
  "nombre": "Nombre del Canal",
  "id": "id-unico",
  "logo": "https://url-del-logo.png",
  "url": "https://enlace-del-stream"
}
```
4. Haz commit → la lista se regenera automáticamente (si usas GitHub Actions)

### Opción B — Script local
```bash
# Edita canales.json con cualquier editor
# Luego ejecuta:
python generar_lista.py

# Sube los cambios:
git add .
git commit -m "Actualizar canales"
git push
```

---

## 📁 Estructura del repositorio

```
├── lista.m3u          ← Lista final (importa esta en tu app)
├── canales.json       ← Base de datos de canales (edita aquí)
├── generar_lista.py   ← Script generador
└── README.md
```

---

## ⚠️ Notas importantes

- Este repositorio es de **uso personal y privado**
- Los enlaces de streaming deben ser fuentes legales o de tu propia red
- Si el repositorio es público, cualquiera con el link puede ver tus canales
- Se recomienda mantener el repo **privado** y usar el raw link con token si es necesario

---

## 🔄 Automatización con GitHub Actions (opcional)

Puedes crear `.github/workflows/generar.yml` para que la lista se regenere automáticamente cada vez que edites `canales.json`:

```yaml
name: Generar lista M3U
on:
  push:
    paths:
      - 'canales.json'
jobs:
  generar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - run: python generar_lista.py
      - uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "Auto: actualizar lista.m3u"
```
