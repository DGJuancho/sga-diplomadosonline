"""
File_Manager es la capa de persistencia del SGA-DO, este módulo se encarga de traducir el texto plano a objetos en la memoria RAM y viceversa. Este módulo es responsables de:
1. Leer los archivos: Validar si los archivos (alumnos.txt y profesores.txt) existen. Si no existen, los crea vacíos para evitar que el programa se rompa con un FileNotFoundError.
2. Escribir los nuevos datos en los archivos: Recibir la lista de objetos y transformarlos en su formato de texto, delimitado por comas.
"""

# 1. Librería Python
from pathlib import Path
from typing import Any

# 2. Módulos del proyecto
from entities import AcademicProgram, Bootcamp, Course, Diploma, Professor, Student


class FileManager:
    def __init__(self, data_dir: str = ".") -> None:
        # Definimos las rutas usando objetos Path
        self._students_file = Path(data_dir) / "alumnos.txt"
        self._professors_file = Path(data_dir) / "profesores.txt"

        # Nos aseguramos de que existan desde el primer instante
        self._ensure_files_exist()

    def _ensure_files_exist(self) -> None:
        """Crea los archivos físicos vacíos si aún no existen en disco."""
        if not self._students_file.exists():
            self._students_file.touch()

        if not self._professors_file.exists():
            self._professors_file.touch()

    def _create_program_instance(self, program_name: str) -> AcademicProgram:
        """Método interno para instanciar el programa académico correspondiente."""
        clean_name = program_name.strip().lower()
        if clean_name == "curso":
            return Course(program_name="Curso")
        elif clean_name == "diplomado":
            return Diploma(program_name="Diplomado")
        elif clean_name == "bootcamp":
            return Bootcamp(program_name="Bootcamp")
        else:
            raise ValueError(
                f"Tipo de programa académico no reconocido: {program_name}"
            )

    def _parse_student_line(self, line: str) -> Student:
        """Convierte una línea CSV limpia en una instancia de la clase Student."""
        parts: list[str] = [item.strip() for item in line.strip().split(sep=",")]

        # Garantizamos que la línea tenga exactamente los 7 campos requeridos
        if len(parts) < 7:
            raise ValueError(f"Linea corrupta o incompleta: '{line}'")

        national_id, full_name, email, program_str = (
            parts[0],
            parts[1],
            parts[2],
            parts[3],
        )

        # Parseo explícito de calificaciones a float
        try:
            grades: list[float] = [float(parts[4]), float(parts[5]), float(parts[6])]
        except ValueError:
            grades: list[float] = [0.0, 0.0, 0.0]

        program_instance: AcademicProgram = self._create_program_instance(
            program_name=program_str
        )

        return Student(
            national_id=national_id,
            full_name=full_name,
            email=email,
            program=program_instance,
            grades_list=grades,
        )

    def _format_student_line(self, student: Student) -> str:
        """Convierte un objeto Estudiante al formato estandarizado CSV."""
        program_name = student.program.program_name if student.program else "Curso"

        # Nos aseguramos que siempre existan 3 notas en el archivo.
        grades = list(student.grades_list)
        while len(grades) < 3:
            grades.append(0.0)

        # Si las notas son enteras (ej. 10.0), se pueden guardar como int o float limpio
        g1: int | Any = int(grades[0]) if grades[0].is_integer() else grades[0]
        g2: int | Any = int(grades[1]) if grades[1].is_integer() else grades[1]
        g3: int | Any = int(grades[2]) if grades[2].is_integer() else grades[2]

        return f"{student.national_id}, {student.full_name}, {student.email}, {program_name}, {g1}, {g2}, {g3}\n"

    def read_students(self) -> list[Student]:
        """Lee el archivo alumnos.txt y retorna la lista de estudiantes."""
        students: list[Student] = []
        with open(self._students_file, mode="r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    try:
                        student: Student = self._parse_student_line(line)
                        students.append(student)
                    except ValueError:
                        continue  # Evita que el sistema se rompa por datos corruptos.
        return students

    def save_all_students(self, students: list[Student]) -> None:
        """Escribe o sobrescribe la información de los alumnos en el archivo."""
        lines: list[str] = [self._format_student_line(student=s) for s in students]
        with open(self._students_file, mode="w", encoding="utf-8") as file:
            file.writelines(lines)

    def _parse_professor_line(self, line: str) -> Professor:
        """Convierte una línea CSV limpia en una instancia de la clase Professor."""
        parts: list[str] = [item.strip() for item in line.strip().split(sep=",")]

        if len(parts) < 5:
            raise ValueError(f"Linea profesor corrupta o incompleta> '{line}'")

        national_id, full_name, email, specialty, subject = (
            parts[0],
            parts[1],
            parts[2],
            parts[3],
            parts[4],
        )

        return Professor(
            national_id=national_id,
            full_name=full_name,
            email=email,
            specialty=specialty,
            assigned_subject=subject,
        )

    def _format_professor_line(self, professor: Professor) -> str:
        """Convierte un objeto Profesor, al formato estandarizado de CSV."""
        return f"{professor.national_id}, {professor.full_name}, {professor.email}, {professor.specialty}, {professor.assigned_subject}\n"

    def read_professors(self) -> list[Professor]:
        """Lee profesores.txt y retorna la lista de Profesores."""
        professors: list[Professor] = []
        with open(self._professors_file, mode="r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    try:
                        prof: Professor = self._parse_professor_line(line)
                        professors.append(prof)
                    except ValueError:
                        continue  # Evita que el sistema se rompa por datos corruptos.
        return professors

    def save_all_professors(self, professors: list[Professor]) -> None:
        """Escribe o sobrescribe la información de los profesores en el archivo."""
        lines: list[str] = [self._format_professor_line(p) for p in professors]
        with open(self._professors_file, mode="w", encoding="utf-8") as file:
            file.writelines(lines)
