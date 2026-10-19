"""
El módulo main, contiene el menú de opciones que utilizará el Sistema de Gestión Académica de Diplomados Online para cumplir con las funcionalidades requeridas.

Author: DGJuancho
Date: 09/2026
"""

# 1. Librería Python
from typing import Literal

# 2. Módulos del proyecto
from entities import Bootcamp, Course, Diploma, Person, Professor, Student
from file_manager import FileManager
from sga_controller import AcademicManagementSystem


def main() -> None:
    # 1. Instanciar el controlador (carga datos de archivos a memoria)
    file_manager = FileManager()
    sga = AcademicManagementSystem(file_manager)

    # 2. Bucle del menú de opciones (1-7)
    while True:
        print("\n=== SGA-DO: SISTEMA DIPLOMADOSONLINE ===")
        print("1. Registrar Alumno")
        print("2. Registrar Profesor")
        print("3. Registrar Notas a un Alumno")
        print("4. Deshacer Último Registro de Nota")
        print("5. Generar Cola de Certificados")
        print("6. Mostrar Reporte General")
        print("7. Salir")
        print("========================================")

        option = input("Seleccione una opción (1-7): ").strip()

        if option == "1":
            """Lógica para Registrar Alumno"""
            # 1. Pedir datos básicos 👤
            national_id: str = input("Ingrese la cédula (Ej: V-101): ").strip().upper()

            # Validación de duplicados 🛡️
            if sga.find_person_by_id(national_id) is not None:
                print(
                    f"\n❌ Error: La cédula '{national_id}' ya se encuentra registrada en el sistema."
                )
                continue
                # No te permite continuar el registro

            full_name: str = input("Ingrese el nombre completo: ").strip()
            email: str = input("Ingrese el correo electrónico: ").strip()

            # 2. Seleccionar tipo de programa 📚
            program = None
            while True:
                print("\nSeleccione el tipo de programa:")
                print("1. Curso")
                print("2. Diplomado")
                print("3. Bootcamp")
                prog_option = input("Opción (1-3): ").strip()

                if prog_option == "1":
                    program = Course()
                    break
                elif prog_option == "2":
                    program = Diploma()
                    break
                elif prog_option == "3":
                    program = Bootcamp()
                    break
                else:
                    print("❌ Opción inválida. Debe seleccionar 1, 2 o 3.")

            # 3. Crear el objeto estudiante
            new_student = Student(
                national_id=national_id,
                full_name=full_name,
                email=email,
                program=program,
            )

            # 4. Registrar el objeto estudiante
            sga.register_student(new_student)
            print("\n¡Estudiante registrado exitosamente! ✅")

        elif option == "2":
            # 1. Pedir datos básicos 👤
            national_id: str = input("Ingrese la cédula (Ej. V-101): ").strip().upper()

            # Validación de duplicados 🛡️
            if sga.find_person_by_id(national_id) is not None:
                print(
                    f"\n❌ Error: La cédula '{national_id}' ya se encuentra registrada en el sistema."
                )
                # No te permite continuar el registro
                continue

            full_name: str = input("Ingrese el nombre completo: ").strip()
            email: str = input("Ingrese el correo electrónico: ").strip()
            specialty: str = input("Ingrese el nombre de su especialidad: ").strip()
            assigned_subject: str = input("Ingrese el nombre de la materia: ").strip()

            # 2. Crear el objeto profesor
            new_professor = Professor(
                national_id=national_id,
                full_name=full_name,
                email=email,
                specialty=specialty,
                assigned_subject=assigned_subject,
            )

            # . Registrar el objeto profesor
            sga.register_professor(new_professor)
            print("\n¡Profesor agregado exitosamente! ✅")

        elif option == "3":
            """Lógica para agregar nota al alumno"""
            # 1. Pedir la cédula de la persona 👤
            national_id: str = input("Ingrese la cédula (Ej: V-101): ").strip().upper()

            # 2. Obtenemos los datos almacenados para esa persona
            person: Person | None = sga.find_person_by_id(national_id)

            # 3. Se verifica que la persona existe 🛡️
            if person is None:
                print(
                    f"\n❌ Error: La cédula: '{national_id}' no se encuentra registrada en el sistema."
                )
                # No te permite continuar el registro
                continue

            # 4. Se verifica que la persona es un estudiante 🛡️
            if isinstance(person, Professor):
                print(
                    f"\n❌ Error: La cédula: '{national_id}' pertenece al profesor: '{person.full_name}'."
                )
                # No te permite continuar el registro
                continue

            elif isinstance(person, Student):
                print(f"\n✔️ Se agregará la nota al alumno: '{person.full_name}'")

                try:
                    grade_input = input(
                        "Ingrese la nota del estudiante (0.0 - 20.0): "
                    ).strip()
                    grade = float(grade_input)
                    # 2. Validar rango permitido en la escala del SGA
                    if not (0.0 <= grade <= 20.0):
                        print(
                            "\n❌ Error: La nota debe estar comprendida entre 0.0 y 20.0."
                        )
                        continue

                    # 3. Llamar al controlador pasando el tipo correcto (float)
                    if sga.add_grade_to_student(national_id, grade):
                        print(
                            f"\n✅ Nota {grade} registrada exitosamente para {person.full_name}."
                        )
                    else:
                        print(
                            "\n❌ Error: No se pudo agregar la nota. Verifique si el alumno ya alcanzó el límite máximo de notas."
                        )

                except ValueError:
                    print(
                        "\n❌ Error: Debe ingresar un valor numérico válido (ej. 14.5)."
                    )
                    continue

        elif option == "6":
            print("\n==================================================")
            print("        SGA-DO: REPORTE GENERAL DE LA ACADEMIA     ")
            print("==================================================")

            # 1. Obtener las colecciones (desempaquetando la tupla)
            students, professors = sga.get_general_report()

            # 2. Imprimir Sección de Alumnos
            print("\n--- ALUMNOS REGISTRADOS ---")
            if not students:
                print("No hay alumnos registrados.")
            else:
                for student in students:
                    # Invocación polimórfica de aprobación según el tipo de programa
                    status: Literal["APROBADO", "REPROBADO"] = (
                        "APROBADO" if student.is_approved() else "REPROBADO"
                    )

                    # Formateo de notas y promedio
                    grades_str = (
                        ", ".join(f"{g:.1f}" for g in student.grades_list)
                        if student.grades_list
                        else "Sin notas"
                    )
                    avg = student.calculate_average()

                    print(f"• [{student.national_id}] {student.full_name}")
                    print(
                        f"  Programa: {student.program_name} | Notas: [{grades_str}] | Promedio: {avg:.1f} | Estatus: {status}"
                    )

            # 3. Imprimir Sección de Profesores
            print("\n--- PROFESORES ACTIVOS ---")
            if not professors:
                print("No hay profesores registrados.")
            else:
                for prof in professors:
                    # Se acceden a los atributos de la instancia directamente
                    print(
                        f"• [{prof.national_id}] {prof.full_name} | Especialidad: {prof.specialty} | Materia: {prof.assigned_subject}"
                    )

        elif option == "7":
            print("¡Gracias por usar el sistema SGA-DO!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
