# olivanegra.es

Web de Oliva Negra · Chef & Eventos, publicada con GitHub Pages en www.olivanegra.es.

- `index.html`, `ca/`, `en/`, `fr/`: la web en los cuatro idiomas (generada).
- `reservas/`: página del evento actual (olivanegra.es/reservas) con botones a Tebi y WhatsApp.
  Es la página a la que apuntan los anuncios y la bio de Instagram; se escribe a mano, no la genera build.py.
- `fuente/`: plantilla en español, traducciones y el script que genera la web
  (`python3 fuente/build.py <salida> all`, después copiar `img/` y `media/`).
