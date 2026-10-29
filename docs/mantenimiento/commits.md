# Mensajes de commit

Este repositorio adopta [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
para los nuevos commits. Los anteriores se conservan.

Escribe el mensaje con esta forma:

```text
tipo(alcance): descripción breve
```

El alcance es opcional. Como norma del proyecto, usa tipos en minúsculas y
descripciones en español que indiquen qué cambió.

| Tipo | Cuándo usarlo |
|---|---|
| `feat` | Agregas una función. |
| `fix` | Corriges un fallo. |
| `docs` | Actualizas documentación. |
| `style` | Cambias formato del código sin alterar su comportamiento. |
| `refactor` | Reorganizas código conservando su comportamiento. |
| `test` | Agregas o corriges pruebas. |
| `ci` | Modificas la automatización de GitHub. |
| `build` | Cambias herramientas de construcción o dependencias. |
| `chore` | Realizas otras tareas de mantenimiento. |

Ejemplos del proyecto:

```bash
git commit -m "docs(portal): simplifica el tutorial de Git"
git commit -m "feat(web): añade favicons institucionales"
git commit -m "fix(compilacion): corrige la ruta de los recursos"
```

Si el cambio rompe compatibilidad, añade `!` antes de los dos puntos y explica
la consecuencia. También puedes indicarla en un pie `BREAKING CHANGE:`.
El cuerpo y los pies son opcionales y se separan con una línea en blanco.

Separa cambios independientes en commits distintos. Esta es una norma documentada;
el workflow actual no comprueba automáticamente los mensajes.
