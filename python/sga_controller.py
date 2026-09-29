"""
Módulo controller para la orquestación del Sistema de Gestión Académica (SGA-DO).

Gestiona la lógica de negocio, mantiene colecciones en memoria (Pila LIFO / Cola FIFO)
y coordina las operaciones con la capa de persistencia (file_manager).

Author: DGJuancho
Date: 08/2026
"""

# 1. Librería Python
from collections import deque

# 2. Módulos del proyecto
from entities import Professor, Student
from file_manager import FileManager


class AcademicManagementSystem:
    """Controlador principal que orquesta el flujo de datos y reglas de negocio del SGA-DO."""

    def __init__(self, file_manager: FileManager) -> None:
        """
        Inicializa las estructuras de datos en memoria y la referencia al gestor de archivos.

        Args:
            file_manager (FileManager): Instancia encargada de I/O de archivos .txt.
        """
        self.file_manager: FileManager = file_manager

        # Colecciones de dominio indexadas por Cédula/ID para acceso rápido
        self.students: dict[str, Student] = {}
        self.professors: dict[str, Professor] = {}

        # Pila (Stack - LIFO) para la Opción 4: Deshacer
        # Guarda referencias del cambio: (instancia_alumno, calificación)
        self.grade_history: list[tuple[Student, float]] = []

        # Cola (Queue - FIFO) para la Opción 5: Generar Certificados
        self.pending_certificates: deque[Student] = deque()

    # --- Carga Inicial y Persistencia ---
    def load_initial_data(self) -> None:
        """Carga la información previa desde los archivos txt hacia la memoria RAM (EVAL-01)."""

        # 1. Obtener las listas de estudiantes y profesores desde el FileManager
        loaded_students: list[Student] = self.file_manager.read_students()
        loaded_professors: list[Professor] = self.file_manager.read_professors()

        # 2. Poblar los diccionarios, indexados por Cédula/ID
        for student in loaded_students:
            self.students[student.national_id] = student

        for professor in loaded_professors:
            self.professors[professor.national_id] = professor

    # --- Reglas de Negocio / Flujos del Menú ---
    def register_student(self, student: Student) -> bool:
        """Registra un alumno en memoria y persiste inmediatamente en alumnos.txt (EVAL-01)."""
        self.students[student.national_id] = student
        self.file_manager.save_all_students(students=list(self.students.values()))
        return True

    def register_professor(self, professor: Professor) -> bool:
        """Registra un profesor en memoria y persiste inmediatamente en profesores.txt (EVAL-01)."""
        self.professors[professor.national_id] = professor
        self.file_manager.save_all_professors(professors=list(self.professors.values()))
        return True

    def add_grade_to_student(self, national_id: str, grade: float) -> bool:
        """
        Opción 3: Busca al estudiante, llama su método para agregar nota, apila la acción en LIFO
        y guarda la nota en el archivo correspondiente.
        """
        student: Student | None = self.students.get(national_id)
        if not student:
            return False

        # Intenta agregar la nota al estudiante
        if not student.add_grade(grade):
            return False

        # 1. Se apila la tupla en la pila LIFO (Opción 4)
        self.grade_history.append((student, grade))

        # 3. Se guarda la información en el archivo correspondiente
        self.file_manager.save_all_students(list(self.students.values()))

        return True

    def undo_last_grade(self) -> tuple[Student, float] | None:
        """
        Opción 4: Extrae el último elemento de la Pila (LIFO), remueve la nota del alumno
        y actualiza la persistencia física.
        """
        if not self.grade_history:
            return None

        # 1. Desapilamos el último registro: Comportamiento LIFO
        student, grade_removed = self.grade_history.pop()

        # 2. se elimina la última nota (llamando al método establecido en la clase Student)
        student.remove_last_grade()

        # 3. Se guarda el cambio en el archivo correspondiente.
        self.file_manager.save_all_students(list(self.students.values()))

        return student, grade_removed

    def generate_certificate_queue(self) -> list[Student]:
        """
        Opción 5: Filtra alumnos aprobados usando polimorfismo (EVAL-02), los inserta en
        la Cola pending_certificates (FIFO) y los procesa hacia certificados_pendientes.txt.
        """

        # 1. Se limpia la cola antes de iniciar.
        self.pending_certificates.clear()

        # 2. Se filtras los estudiantes aprobados y se colocan en cola (FIFO)
        for student in self.students.values():
            if student.is_approved():
                self.pending_certificates.append(student)

        # 3.  Se procesa la cola en el orden (FIFO) a una lista para el reporte
        graduates: list[Student] = []
        while self.pending_certificates:
            approved_student: Student = self.pending_certificates.popleft()
            graduates.append(approved_student)

        # 4. Se guarda el reporte en el archivo de texto
        self.file_manager.save_pending_certificates(graduates)
        return graduates

    def get_general_report(self) -> tuple[list[Student], list[Professor]]:
        """Opción 6: Retorna la lista de alumnos y profesores cargados
        en memoria para que la vista despliegue el reporte general."""

        return list(self.students.values()), list(self.professors.values())
