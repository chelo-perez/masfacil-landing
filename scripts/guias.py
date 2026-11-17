# Genera las guías de uso de Trabajo Más Fácil a partir de los .md del repo de la app.
# Uso: python3 scripts/guias.py <carpeta docs/guias de la app>
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import legal

PAGES = [('estudios.md', 'guia-estudios', 'Guía para estudios'),
         ('instructores.md', 'guia-instructores', 'Guía para instructores'),
         ('entidades.md', 'guia-entidades', 'Guía para entidades')]
legal.build(PAGES, sys.argv[1])
