"""
El módulo main, contiene el menú de opciones que utilizará el Sistema de Gestión Académica de Diplomados Online para cumplir con las funcionalidades requeridas.

Author: DGJuancho
Date: 09/2026
"""

# 1. Librería Python

# 2. Módulos del proyecto
from entities import Student, Professor, Bootcamp, Course, Diploma
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

        elif option == "7":
            print("¡Gracias por usar el sistema SGA-DO!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
