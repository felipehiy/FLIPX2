# Flipx2

Flipx2 es un orquestador OSINT para Kali Linux: unifica herramientas ya instaladas,
normaliza sus resultados y conserva evidencia por caso. Está diseñado para dominios,
usuarios y correos que te pertenecen o para los que tienes autorización expresa.

No es un escáner de vulnerabilidades ni ejecuta ataques. Los conectores incluidos usan
recolección pasiva o consultas públicas; las herramientas externas sólo se invocan si
están instaladas localmente.

## Instalación en Kali

```bash
sudo apt install python3-pip dnsutils whois
pipx install .
# o, para desarrollo:
python3 -m pip install -e .
```

## Uso

```bash
# Ver conectores y si las herramientas requeridas existen
flipx2 tools

# Crear y ejecutar un caso (se exige una afirmación explícita de autorización)
flipx2 run --case cliente-acme --domain acme.example --authorized
flipx2 run --case marca --username acme --authorized

# Leer resultados producidos
flipx2 report --case cliente-acme
```

Los artefactos quedan en `~/.local/share/flipx2/cases/<caso>/`: `manifest.json`,
salidas de cada conector y un `report.json` normalizado. Use `FLIPX2_HOME` para
definir otro directorio.

## Extensiones

Los conectores son manifiestos en `src/flipx2/catalog.py`. Añade uno especificando
el binario, argumentos y un nivel (`passive` o `manual`). Flipx2 no reemplaza las
herramientas de Kali; proporciona una capa reproducible para combinarlas. Revisa sus
términos, límites de tasa y requisitos de API antes de activarlas.
