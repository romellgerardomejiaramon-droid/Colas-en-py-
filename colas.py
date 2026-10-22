import time
from itertools import zip_longest


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:

    def __init__(self):
        self._frente = None
        self._final = None
        self._tamano = 0

    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self._final is None:
            self._frente = nuevo
        else:
            self._final.siguiente = nuevo
        self._final = nuevo
        self._tamano += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._tamano -= 1
        return dato

    def esta_vacia(self):
        return self._tamano == 0

    def __iter__(self):
        actual = self._frente
        while actual:
            yield actual.dato
            actual = actual.siguiente


def sumar_colas(cola_a, cola_b):
    resultado = Cola()
    a, b = iter(cola_a), iter(cola_b)
    while True:
        x = next(a, None)
        y = next(b, None)
        if x is None and y is None:
            break
        resultado.encolar((x or 0) + (y or 0))
    return resultado


def cola_desde_lista(lista):
    c = Cola()
    for n in lista:
        c.encolar(n)
    return c


def leer_cola(nombre):
    while True:
        texto = input(f"Ingrese los números de la {nombre} separados por espacios: ")
        try:
            numeros = [int(t) for t in texto.split()]
        except ValueError:
            print("  Error: solo se permiten números enteros.")
            continue
        if not numeros:
            print("  Error: la cola no puede estar vacía.")
            continue
        return cola_desde_lista(numeros)


def mostrar_resultado(cola_a, cola_b):
    inicio_programa = time.perf_counter()

    inicio_suma = time.perf_counter()
    res = sumar_colas(cola_a, cola_b)
    fin_suma = time.perf_counter()

    print(f"\n{'Cola A':<8}{'Cola B':<8}{'Resultado'}")
    for x, y, r in zip_longest(cola_a, cola_b, res, fillvalue="-"):
        print(f"{x:<8}{y:<8}{r}")

    fin_programa = time.perf_counter()
    print(f"\nTiempo de sumar_colas:      {(fin_suma - inicio_suma) * 1000:.6f} ms")
    print(f"Tiempo total de ejecución:  {(fin_programa - inicio_programa) * 1000:.6f} ms")


def menu():
    while True:
        print("\n===== SUMA DE COLAS =====")
        print("1. Ver ejemplo del enunciado")
        print("2. Crear mis propias colas")
        print("3. Salir")
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            cola_a = cola_desde_lista([3, 4, 2, 8, 12])
            cola_b = cola_desde_lista([6, 2, 9, 11, 3])
            mostrar_resultado(cola_a, cola_b)
        elif opcion == "2":
            cola_a = leer_cola("Cola A")
            cola_b = leer_cola("Cola B")
            mostrar_resultado(cola_a, cola_b)
        elif opcion == "3":
            print("Fin del programa.")
            break
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    menu()
