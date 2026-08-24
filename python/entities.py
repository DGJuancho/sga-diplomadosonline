"""
El módulo entities, contiene las entidades que se utilizarán dentro del Sistema de Gestión Académica de Diplomados Online.

Author: DGJuancho
Date: 08/2026
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Person(ABC):
    """Clase base para representar a una persona en el sistema"""

    def __init__(self, national_id: str, full_name: str, email: str) -> None:
        self._national_id = national_id
        self._full_name = full_name
        self._email = email

    @property
    def national_id(self) -> str:
        """Retorna la cédula o ID único de la persona"""
        return self._national_id

    @property
    def full_name(self) -> str:
        """Retorna el nombre de la persona"""
        return self._full_name

    @property
    def email(self) -> str:
        """REtorna el correo electrónico de la persona"""
        return self._email

    @abstractmethod
    def get_role(self) -> str:
        """Método abstracto que obliga a las subclases a identificarse"""


class Professor(Person):
    """Clase para definir a los profesores del diplomado"""

    def __init__(
        self,
        national_id: str,
        full_name: str,
        email: str,
        specialty: str,
        assigned_subject: str,
    ) -> None:
        super().__init__(national_id, full_name, email)
        self._specialty: str = specialty
        self._assigned_subject: str = assigned_subject

    @property
    def specialty(self):
        """Retorna la especialidad del profesor"""
        return self._specialty

    @property
    def assigned_subject(self):
        """Retorna la asignatura que enseña el profesor"""
        return self._assigned_subject


class Student(Person):
    """Clase para definir a los estudiantes del diplomado"""

    def __init__(
        self,
        national_id: str,
        full_name: str,
        email: str,
        program: AcademicProgram | None = None,
        grades_list: list[float] | None = None,
    ) -> None:
        super().__init__(national_id, full_name, email)
        self._program: AcademicProgram | None = program
        self._grades_list: list[float] = grades_list if grades_list is not None else []

    @property
    def program(self) -> AcademicProgram | None:
        """Retorna el programa que está cursando el estudiante"""
        return self._program

    @property
    def grades_list(self) -> list[float]:
        """Retorna la lista de notas del estudiante"""
        return self._grades_list

    def is_approved(self) -> bool:
        """La función delega al programa académico el cálculo correspondiente"""
        if not self._program:
            return False
        return self._program.is_approved(self._grades_list)

    def add_grade(self, grade: float) -> bool:
        """
        Agrega una nota si no se ha alcanzado el límite de 3 y está en el rango [0, 20].
        Retorna True si la nota fue añadida con éxito; False en caso contrario.
        """

        if len(self._grades_list) >= 3 or not (0 <= grade <= 20):
            return False

        self._grades_list.append(grade)
        return True

    def remove_last_grade(self) -> bool:
        """
        Remueve la última nota de la lista si existe.
        Retorna True si se removió una nota; False si la lista estaba vacía.
        """

        if not self._grades_list:
            return False

        self._grades_list.pop()
        return True


class AcademicProgram(ABC):
    def __init__(self, program_name: str) -> None:
        self._program_name: str = program_name

    @property
    def program_name(self) -> str:
        return self._program_name

    @abstractmethod
    def is_approved(self, grades: list[float]) -> bool:
        """Método polimórfico para evaluar si el estudiante está aprobado, de acuerdo a la modalidad"""


class Course(AcademicProgram):
    """Modalidad Curso: Requiere un promedio mayor o igual a 10.0"""

    def __init__(self, program_name: str) -> None:
        super().__init__(program_name)

    def is_approved(self, grades: list[float]) -> bool:
        if not grades:
            return False
        average: float = sum(grades) / len(grades)
        return average >= 10.0


class Diploma(AcademicProgram):
    """Modalidad Diplomado: Requiere un promedio mayor o igual a 14.0"""

    def __init__(self, program_name: str) -> None:
        super().__init__(program_name)

    def is_approved(self, grades: list[float]) -> bool:
        if not grades:
            return False
        average: float = sum(grades) / len(grades)
        return average >= 14


class Bootcamp(AcademicProgram):
    """Modalidad Bootcamp: Ninguna nota individual debe ser menor a 14.0"""

    def __init__(self, program_name: str) -> None:
        super().__init__(program_name)

    def is_approved(self, grades: list[float]) -> bool:
        if not grades:
            return False
        # Si alguna nota es estrictamente menor a 14, queda reprobado
        return all(grade >= 14.0 for grade in grades)
