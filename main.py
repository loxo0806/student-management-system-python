def crear_estudiante(id, nombre, apellido):
    """
    Retorna un diccionario con la información para crear a un nuevo estudiante
    """
    dicc = {
        "id": id,
        "nombre": nombre,
        "apellido": apellido
    }
    return dicc


def comprobar_id(id, archivo):
    """
    Verifica el id del archivo para evitar duplicados y retorna un id único
    """
    ids_vistos = set()
    
    try:
        with open(archivo, "r") as ar:
            for linea in ar:
                partes = linea.strip().split(",")
                if partes[0]:
                    ids_vistos.add(int(partes[0]))
    except FileNotFoundError:
        pass

    
    nuevo_id = int(id)
    while nuevo_id in ids_vistos:
        nuevo_id += 1
    
    return nuevo_id


def agregar_nuevo_estudiante(nuevo_estudiante, archivo):
    """
    Agrega el estudiante al archivo
    """
    with open(archivo, "a") as arc:
        arc.write(f"{nuevo_estudiante["id"]}, {nuevo_estudiante["nombre"]}, {nuevo_estudiante["apellido"]}\n")


def leer_archivo(archivo):
    """
    Lee el contenido del txt, verifica cada estudiante y sus notas, agregando la info a una lista de
    aprobados y reprobados, además, comprueba al mejor estudiante con mejor promedio y retorna la
    información correspondiente
    """
    aprobados = []
    reprobados = []
    mejor_promedio = 0
    mejor_estudiante = None

    try:
        with open(archivo, "r") as ar:
            contenido = ar.readlines()
    except FileNotFoundError:
        return None

    for linea in contenido:
        filtro = linea.strip().split(", ")
        notas = []
        info = f"{filtro[1]}, {filtro[2]}"
        for i in range(1, len(filtro)):
            if filtro[i].isdigit():
                notas.append(float(filtro[i]))
                print(notas)
        
        if notas:
            promedio = round(sum(notas) / len(notas), 2)
            info_estudiante = {"nombre": info, "promedio": promedio}

            if promedio <= 4.0:
                reprobados.append(info_estudiante)
            else:
                aprobados.append(info_estudiante)

            if promedio > mejor_promedio:
                mejor_promedio = promedio
                mejor_estudiante = info_estudiante
    
    print("\nAprobados.\n")
    for e in aprobados:
        print(f"{e["nombre"]}, {e["promedio"]}")
    
    print("\nReprobados\n")
    for r in reprobados:
        print(f"{r["nombre"]}, {r["promedio"]}")

    if mejor_estudiante:
        print("\nMEJOR ESTUDIANTE:\n", mejor_estudiante)

def agregar_notas(id_solicitado, materia, nota, archivo):
    """
    Permite agregar materias a un estudiante específico, permite agregar la materia junto a
    sus respectivas notas, si existe la materia, puedes agregar las notas que se necesite.
    También permite crear multiples materias para cada estudiante
    """
    datos_actualizados = []
    encontrado = False

    try:
        with open(archivo, "r") as arc:
            lineas = arc.readlines()
    except FileNotFoundError:
        return None

    for linea in lineas:
        datos = linea.strip().split(", ")
        if str(id_solicitado) == datos[0]:
            encontrado = True
            if materia in datos:
                #Busca la posición de la materia y agrega la nota justo después
                #de esa posición
                indice_materia = datos.index(materia)
                datos.insert(indice_materia + 1, str(nota))
            else:
                #Si no, se agrega la materia y nota al final de la lista
                datos.append(materia)
                datos.append(nota)
            #Reescribe los datos de lista a str para agregarlos al txt
            #se utiliza map para iterar y convertir todo a str y evitar
            #errores de join
            nueva_linea = ", ".join(map(str, datos)) + "\n"
            #Guarda la nueva linea para sobreescribir en el siguiente bloque
            datos_actualizados.append(nueva_linea)
        else:
            datos_actualizados.append(linea)

    if encontrado:
        with open(archivo, "w") as ar:
            ar.writelines(datos_actualizados)
            return "Datos guardados correctamente"

    else:
        return "Usuario no encontrado"


def promedio_materia(id_estudiante, materia, archivo):
    """
    Retorna el promedio por materia del estudiante
    """
    notas = []

    try:
        with open(archivo, "r") as arc:
            lineas = arc.readlines()
    except FileNotFoundError:
        return None
    
    for linea in lineas:
        datos = linea.strip().split(", ")
        if str(id_estudiante) == datos[0]:
            if materia in datos:
                #El index nos marca el inicio de la posición en que
                #se encuentra la materia
                inicio = datos.index(materia) + 1
                for i in range(inicio, len(datos)):
                    #Verifica si es un número
                    if datos[i].isdigit():
                        notas.append(float(datos[i]))
                    else:
                        #Se rompe el ciclo al encontrar otra materia
                        break

                return sum(notas) / len(notas)


def promedio_general(id_estudiante, archivo):
    """
    Retorna el promedio general de un estudiante
    """
    notas = []

    try:
        with open(archivo, "r") as arc:
            lineas = arc.readlines()
    except FileNotFoundError:
        return None
    
    for linea in lineas:
        datos = linea.strip().split(", ")
        if str(id_estudiante) == datos[0]:
            for i in range(1, len(datos)):
                if datos[i].isdigit():
                    notas.append(float(datos[i]))
            try:
                return sum(notas) / len(notas)
            except ZeroDivisionError:
                return "El estudiante no tiene notas"
    

if __name__ == "__main__":

    archivo = "archivo.txt"
    id = 0

    print("Sistema de gestión de estudiantes\n")
    while True:
        print("1. Ingresar a un nuevo estudiante")
        print("2. Agregar notas")
        print("3. Calcular promedio")
        print("4. Resumen de estudiantes")
        print("5. Salir")

        try:
            opcion = int(input("\nIngresa una opción: "))
        except ValueError:
            print("Opción no válida")
            continue

        if opcion == 1:
            nombre = input("Nombre del estudiante: ").lower()
            apellido = input("Apellido del estudiante: ").lower()

            nuevo_id = comprobar_id(id, archivo)
            nuevo_estudiante = crear_estudiante(nuevo_id, nombre, apellido)
            agregar_nuevo_estudiante(nuevo_estudiante, archivo)
            print("Datos guardados correctamente\n")

        if opcion == 2:
            try:
                id_estudiante = int(input("Ingrese el id del estudiante: "))
            except ValueError:
                print("Dato ingresado no válido, intenta nuevamente\n")
                continue
            materia = input("Ingresa la materia: ").lower()
            nota = int(input("Ingrese la nota: "))
            
            agregar_notas(id_estudiante, materia, nota, archivo)

        if opcion == 3:
            print("\n1. Promedio general")
            print("2. Promedio por materia")

            try:
                entrada = int(input("\nIngrese una opción: "))
            except ValueError:
                print("Opción inválida\n")
                continue
            try:
                id_estudiantes = int(input("\nIngrese el id del estudiante: "))
            except ValueError:
                print("Datos ingresados no válidos, intente nuevamente\n")
                continue

            if entrada == 1:
                promedio = promedio_general(id_estudiantes, archivo)
                print("\nPromedio general del estudiante:\n", promedio)
            
            if entrada == 2:
                materia_solicitada = input("\nIngrese la materia: ")
                promedio_materias = promedio_materia(id_estudiantes, materia_solicitada, archivo)
                print(f"Promedio de {materia_solicitada}:\n", promedio_materias)

        if opcion == 4:
            resumen = leer_archivo(archivo)
            print(resumen)

        if opcion == 5:
            print("Cerrando programa...")
            break
