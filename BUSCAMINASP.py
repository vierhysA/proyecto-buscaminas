"""Buscaminas"""
import random
import time

partidas = []

def crear_usuario():
    """creación del user y datas"""
    nombre_usuario = input("Ingrese su nombre de usuario ->    ")
    correo_usuario = input("Ingrese el correo previo del usuario ->   ")
    usuario_id = random.randint(10000, 99999)
    return [nombre_usuario, correo_usuario, usuario_id]


def escoger_nivel():
    """escoger modos de juegos con las condiciones de cada uno"""
    print("NIVELES DISPONIBLES ->  ")
    print("1. easy")
    print("2. medium")
    print("3. expert")

    nivel = input("Escoge el modo del juego (easy, medium, expert):")
    if nivel == "easy":
        return 6, 6, 4, "easy"
    elif nivel == "medium":
        return 8, 8, 9, "medium"
    elif nivel == "expert":
        return 10, 10, 15, "expert"
    else:
        print("Nivel escogido inválido, estará en modo easy")
        return 6, 6, 4, "easy"


def inicio_tablero(filas, columnas):
    """visualización del tablero en forma de -"""
    tablero = []
    for _ in range(filas):
        fila = ["-"] * columnas
        tablero.append(fila)
    return tablero


def colocar_minas(tablero, minas):
    """poner minas aleatorias en el tablero dependiendo del mood"""
    t_fila = len(tablero)
    t_columna = len(tablero[0])
    minas_colocadas = 0
    while minas_colocadas < minas:
        f = random.randint(0, t_fila - 1)
        c = random.randint(0, t_columna - 1)
        if tablero[f][c] != "MINA":
            tablero[f][c] = "MINA"
            minas_colocadas += 1


def contar_minas(tablero, fila, columna):
    """conteo de minas al rededor del sitio donde el usuario hizo el movimiento"""
    total = 0
    filas = len(tablero)
    columnas = len(tablero[0])
    for i in range(fila - 1, fila + 2):
        for j in range(columna - 1, columna + 2):
            if 0 <= i < filas and 0 <= j < columnas:
                if not (i == fila and j == columna):
                    if tablero[i][j] == "MINA":
                        total += 1
    return total


def ver_tablero(tablero):
    """condiciones para imprimir el tablero"""
    for fila in tablero:
        for elemento in fila:
            print(elemento, end=" ")
        print()


def inicio_juego(nombre, usuario_id, filas, columnas, minas, nivel):
    """se recopita los datos para luego imprimirlos y se toman condiciones para las minas"""
    tablero_verdadero = inicio_tablero(filas, columnas)
    tablero_jugador = inicio_tablero(filas, columnas)
    colocar_minas(tablero_verdadero, minas)

    puntos = 0
    minas_descubiertas = 0
    seguras = filas * columnas - minas
    ini_tiempo = time.time()

    while minas_descubiertas < seguras:
        ver_tablero(tablero_jugador)
        print(" -PUNTAJE- ", puntos)

        fila = int(input("FILA: "))
        columna = int(input("COLUMNA: "))

        if fila < 0 or fila >= filas or columna < 0 or columna >= columnas:
            print("-ESTÁS FUERA DEL TABLERO-")

        elif tablero_jugador[fila][columna] != "-":
            print("-CASILLA YA DESCUBIERTA-")

        elif tablero_verdadero[fila][columna] == "MINA":
            tablero_jugador[fila][columna] = "MINA"
            ver_tablero(tablero_jugador)
            print("-ACABAS DE PISAR UNA MINA-")
            print("JUEGO TERMINADO, PERDISTE.")
            print("JUGADOR", nombre)
            print("ID", usuario_id)
            print("PUNTAJE", puntos)
            return True, puntos, time.time() - ini_tiempo

        else:
            minas_cercas = contar_minas(tablero_verdadero, fila, columna)
            tablero_jugador[fila][columna] = str(minas_cercas)
            puntos += 1
            minas_descubiertas += 1

    ver_tablero(tablero_jugador)
    print("FELICIDADES, GANASTE EL JUEGO")
    puntos += 10
    print("JUGADOR", nombre)
    print("ID", usuario_id)
    print("PUNTAJE", puntos)
    print("NIVEL DE DIFICULTAD", nivel)
    return False,puntos, time.time() - ini_tiempo


def ordenar_partidas(partidas):
    """orden de todas las partidas dependiendo del tiempo que se hayan tomado"""
    n = len(partidas)
    for i in range(n):
        for j in range(0, n-i-1):
            if partidas[j]["tiempo"] > partidas[j+1]["tiempo"]:
                partidas[j], partidas[j+1] = partidas[j+1], partidas[j]     


def main():
    """uso de modularidad"""
    jugar_denuevo = True
    while jugar_denuevo:
        usuario = crear_usuario()
        filas, columnas, minas, nivel = escoger_nivel()
        resultado, puntos, tiempo = inicio_juego(usuario[0], usuario[2], filas, columnas, minas, nivel)

        partidas.append({
            "nombre": usuario[0],
            "usuario_ID": usuario[2],
            "nivel": nivel,
            "puntos_en_total": puntos,
            "tiempo": tiempo,
            "resultado": resultado
        })
        
        print("= PARTIDAS JUGADAS =")
        for partida in partidas:
            print(f"JUGADOR: {partida['nombre']}, ID: {partida['usuario_ID']}, NIVEL: {partida['nivel']}, PUNTOS EN TOTAL: {partida['puntos_en_total']}, TIEMPO: {partida['tiempo']:.2f}, RESULTADO: {'PERDIÓ' if partida['resultado'] else 'GANÓ'} ")
        
        partidas_hard = [partida for partida in partidas if partida['nivel'] == "expert" and partida['resultado']]
        ordenar_partidas(partidas_hard)

        for i, partida in enumerate(partidas_hard[:3], 1):
            print(f"{i}. JUGADOR: {partida['nombre']}, ID: {partida['usuario_ID']}, PUNTOS: {partida['puntos']}, TiEMPO: {partida['tiempo']:.2f}")

        jugar_denuevo = input("Desea jugar de nuevo? (s/n):")
        if jugar_denuevo.lower() != "s":
            break

main()
