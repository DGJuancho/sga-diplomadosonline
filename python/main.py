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
            national_id = input("Ingrese la cédula: ").strip()
            full_name = input("Ingrese el nombre completo: ").strip()
            email = input("Ingrese el correo electrónico: ").strip()

            # 2. Pedir el nombre del programa (ej: "Python Core") 📖
            program_name = input("Ingrese el nombre de la materia/programa: ").strip()

            # 3. Seleccionar tipo de programa 📚
            program = None
            while True:
                print("\nSeleccione el tipo de programa:")
                print("1. Curso")
                print("2. Diplomado")
                print("3. Bootcamp")
                prog_option = input("Opción (1-3): ").strip()

                if prog_option == "1":
                    program = Course(program_name)
                    break
                elif prog_option == "2":
                    program = Diploma(program_name)
                    break
                elif prog_option == "3":
                    program = Bootcamp(program_name)
                    break
                else:
                    print("❌ Opción inválida. Debe seleccionar 1, 2 o 3.")

            # 4. Crear el objeto estudiante
            new_student = Student(
                national_id=national_id,
                full_name=full_name,
                email=email,
                program=program,
            )

            # 5. Registrar el objeto estudiante
            sga.register_student(new_student)
            print("\n¡Estudiante registrado exitosamente! ✅")

        elif option == "7":
            print("¡Gracias por usar el sistema SGA-DO!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
