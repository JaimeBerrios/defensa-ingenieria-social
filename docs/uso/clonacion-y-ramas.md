# Clonar el repositorio y trabajar en equipo

Sustituye `nombra-tu-rama` por el nombre que elijas para tu proyecto en todos
los comandos de esta guía. Crear una rama permite conservar `main` como base
de la plantilla mientras desarrollas el proyecto.

Necesitas Git instalado y acceso al repositorio. Para publicar cambios necesitas
permiso de escritura; clonar por sí solo no concede ese permiso.

## Elegir HTTPS o SSH

Ambos métodos descargan el mismo proyecto. Ejecuta solo una de las alternativas
de clonación, en la carpeta donde quieras guardar el repositorio.

- **HTTPS:** al solicitar autenticación, usa un gestor de credenciales o un token
  de acceso de GitHub, según tu configuración; no la contraseña de tu cuenta.
  No escribas tokens dentro de las URL ni los guardes en archivos del proyecto.
- **SSH:** necesitas una clave SSH configurada en tu equipo y su clave pública
  registrada en tu cuenta de GitHub. Puedes comprobar la conexión con
  `ssh -T git@github.com`; una autenticación correcta indica que GitHub no ofrece
  acceso a una shell. En la primera conexión verifica la huella del servidor
  antes de aceptarla.

## 1. Clonar el repositorio completo

**Con HTTPS:**

```bash
git clone https://github.com/JaimeBerrios/Plantilla-Documentos.git
```

**Con SSH:**

```bash
git clone git@github.com:JaimeBerrios/Plantilla-Documentos.git
```

## 2. Entrar al repositorio

```bash
cd Plantilla-Documentos
```

## 3. Verificar la rama inicial

```bash
git branch --show-current
git status
```

Para este ejemplo, la rama inicial debe ser `main` y el árbol de trabajo debe
estar limpio. Si el clon nuevo está en otra rama, cambia a `main` con
`git switch main` antes de continuar. Si ya estabas trabajando en este repositorio,
revisa y guarda tus cambios antes de cambiar de rama; no los descartes.

## 4. Crear y cambiar a la rama del proyecto

Este paso corresponde a quien inicia el proyecto. Si la rama ya está publicada,
usa las opciones de colaboración de abajo.

```bash
git switch -c nombra-tu-rama
```

## 5. Confirmar el cambio

```bash
git branch
```

Salida esperada (el asterisco señala la rama activa):

```text
  main
* nombra-tu-rama
```

## 6. Publicar la rama en GitHub

```bash
git push -u origin nombra-tu-rama
```

`-u` establece el seguimiento de la rama remota para los siguientes `git push`
y `git pull`. Este comando publica la rama incluso si todavía comparte el mismo
commit que `main`.

**¿Este push modifica `main`?** No. El comando envía la rama
`nombra-tu-rama`. Para incorporar después sus cambios en `main`
hace falta una operación adicional, como fusionar la rama o aceptar un Pull
Request dirigido a `main`. La rama conserva los archivos e historial de la
plantilla; lo que queda separado es el desarrollo posterior.

## Colaboración en equipo

Una vez publicada la rama, cada integrante puede elegir una de estas tres
opciones. Antes de editar o enviar cambios, comprueba con `git status` que estás
en `nombra-tu-rama`.

### Opción 1: clonar directamente la rama del proyecto (recomendada)

**Con HTTPS:**

```bash
git clone -b nombra-tu-rama --single-branch https://github.com/JaimeBerrios/Plantilla-Documentos.git
cd Plantilla-Documentos
```

**Con SSH:**

```bash
git clone -b nombra-tu-rama --single-branch git@github.com:JaimeBerrios/Plantilla-Documentos.git
cd Plantilla-Documentos
```

`--single-branch` limita la descarga y el seguimiento a esa rama; conserva su
historial, incluidos los commits que comparte con `main`. No equivale a descargar
solo el último commit.

### Opción 2: clonar todo y cambiar a la rama

**Con HTTPS:**

```bash
git clone https://github.com/JaimeBerrios/Plantilla-Documentos.git
cd Plantilla-Documentos
git switch nombra-tu-rama
```

**Con SSH:**

```bash
git clone git@github.com:JaimeBerrios/Plantilla-Documentos.git
cd Plantilla-Documentos
git switch nombra-tu-rama
```

En un clon nuevo, Git crea la rama local con seguimiento cuando encuentra una
única rama remota con ese nombre.

### Opción 3: usar un repositorio que ya tienes

Desde la carpeta del repositorio, si todavía no existe la rama local:

```bash
git fetch origin
git switch -c nombra-tu-rama --track origin/nombra-tu-rama
```

Estos comandos sirven tanto si `origin` usa HTTPS como si usa SSH. Si ya existe
la rama local, basta con `git switch nombra-tu-rama`.

Si el clon se creó con `--single-branch` para otra rama, descarga explícitamente
la rama del proyecto antes de crear su vínculo local:

```bash
git remote set-branches --add origin nombra-tu-rama
git fetch origin
git switch -c nombra-tu-rama --track origin/nombra-tu-rama
```

## Comandos frecuentes de desarrollo

| Comando | Función |
|---|---|
| `git status` | Muestra la rama activa y los archivos modificados. |
| `git diff` | Permite revisar los cambios antes de prepararlos. |
| `git add .` | Prepara los cambios de la carpeta actual y sus subcarpetas; desde la raíz, los de todo el proyecto, excepto archivos ignorados. Revisa antes qué vas a incluir. |
| `git diff --cached` | Muestra los cambios preparados para el commit. |
| `git commit -m "Mensaje"` | Guarda los cambios preparados en un commit local. |
| `git push` | Envía los commits a la rama remota configurada para seguimiento. |
| `git pull --ff-only` | Integra cambios remotos solo si puede avanzar sin crear una fusión. |

Al empezar una sesión, con el árbol de trabajo limpio:

```bash
git status
git pull --ff-only
```

Después de editar y revisar el trabajo:

```bash
git diff
git add .
git diff --cached
git commit -m "docs(reporte): actualiza el contenido del proyecto"
git push
```

`git pull` descarga e integra cambios según la configuración de Git. Aquí se
usa `--ff-only` para detenerse si las historias han divergido. Si falla el pull
o Git rechaza el push porque otro integrante publicó primero, coordinen la
integración y resuelvan los conflictos antes de volver a enviar; no usen
`git push --force` para sobrescribir el trabajo compartido.

Trabajar en una rama no impide técnicamente modificar `main`. El equipo debe
comprobar siempre la rama activa; quien administre GitHub puede configurar
protección de `main` para exigir revisiones antes de integrar cambios.

## Continuar con el reporte

Sigue la [guía de uso](guia-de-uso.md): completa `datos/datos.md`, registra las
fuentes y prepara el contenido. Desde la raíz, valida y compila:

```bash
python3 compilar.py --verificar
python3 compilar.py
```

En Windows puedes usar `python` en lugar de `python3`. Por defecto se genera
únicamente `pdf/reporte.pdf`; incluye `--con-presentacion` solo cuando también
necesites la presentación PDF y web.
