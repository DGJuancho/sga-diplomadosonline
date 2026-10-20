# 📑 Plan de Acción y Alcance del MVP **Sistema de Gestión Académica (SGA-DO)**

**Autor:** Juan Carlos V. Núñez T.
**Diplomado:** Programación - Diplomados Online
**Versión:** v1.0.0
**Estado:** MVP Backend Core en Python (Completado y Listo para QA de Facilitador)

---

## 🎯 Alcance del Producto Mínimo Viable (MVP)

Para dar solución a la crisis operativa en la gestión de datos de la academia, se diseñó e implementó un motor core en consola bajo los principios de la Programación Orientada a Objetos (POO), integrando herencia, polimorfismo, estructuras de datos avanzadas (Pilas LIFO y Colas FIFO) y persistencia segura en archivos planos (`.txt`).

El plan de trabajo ejecutado comprende:

1. Análisis de requerimientos funcionales y diseño de la arquitectura.
2. Configuración inicial del repositorio público y control de versiones con Git/GitHub.
3. Modelado de clases jerárquicas (Persona, Alumno, Profesor y Programas Académicos con reglas polimórficas).
4. Desarrollo del motor funcional en Python con bucle interactivo de consola.
5. Carga de data semilla oficial y pruebas unitarias (Casos de Prueba CP-01, CP-02 y CP-03).
6. **Prototipo funcional en Python completado y listo para los protocolos de prueba por parte del facilitador.**

---

## 🏛️ Arquitectura y Reglas de Negocio (EVAL-02)

- **Jerarquía de Personas:** Clases base `Persona` y derivadas `Alumno` y `Profesor`.
- **Evaluación Polimórfica (`evaluarAprobacion()`):**
  - **Curso:** Promedio $\ge 10.0$.
  - **Diplomado:** Promedio $\ge 14.0$.
  - **Bootcamp:** Exige estrictamente 3 notas completas y ninguna menor a $14.0$.

---

## 📊 Estructuras de Datos y Persistencia

- **Opción 4 (Pila / LIFO):** Historial dinámico para deshacer el último registro de notas erróneas.
- **Opción 5 (Cola / FIFO):** Procesamiento secuencial para la exportación del reporte a `certificados_pendientes.txt`.
- **Persistencia Crítica (EVAL-01):** Escritura inmediata en disco (`alumnos.txt`, `profesores.txt`) para prevenir pérdida de datos ante cierres inesperados.
