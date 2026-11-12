# app.trabajo.masfacil.com.ar

Proyecto de Vercel aparte, sobre este mismo repositorio, con **Root Directory = `app-proxy`**.
Reenvía todo a la app web de Trabajo Más Fácil (Expo Hosting). No tiene archivos propios.

Alta (una vez, en vercel.com): Add New Project → importar `masfacil-landing` → Root Directory `app-proxy`
→ Deploy → Settings → Domains → agregar `app.trabajo.masfacil.com.ar`.

## Link propio de cada red
`app.trabajo.masfacil.com.ar/<slug>` redirige a `/?red=<slug>`: la app muestra la marca de esa red desde el login y la preselecciona al registrarse. Para una red nueva, agregar su redirect en `vercel.json` (con el `slug` de la red en la base). Los logos de cada red se publican en la landing, en `redes/<slug>/`.
