import time


class Nodo:
    """Nodo de una lista enlazada simple."""
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    """Cola (FIFO) con nodos enlazados. encolar y desencolar son O(1)."""

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

    def tamano(self):
        return self._tamano

    def __iter__(self):
        """Recorre la cola sin modificarla."""
        actual = self._frente
        while actual:
            yield actual.dato
            actual = actual.siguiente

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"


# Servicios de la compañía de seguros: número -> (nombre, prefijo del ticket)
SERVICIOS = {
    1: ("Siniestros", "S"),
    2: ("Pólizas nuevas", "P"),
    3: ("Pagos", "G"),
    4: ("Reclamos", "R"),
}


class SistemaAtencion:
    """Maneja una Cola por cada servicio."""

    def __init__(self, servicios):
        self.servicios = servicios
        self.colas = {n: Cola() for n in servicios}
        self.contador = {n: 0 for n in servicios}  # último número entregado

    def llega_cliente(self, servicio):
        """C: entrega el número de atención que corresponde y lo encola."""
        self.contador[servicio] += 1
        prefijo = self.servicios[servicio][1]
        ticket = f"{prefijo}-{self.contador[servicio]:03d}"
        self.colas[servicio].encolar(ticket)
        return ticket

    def atender(self, servicio):
        """A: llama al siguiente cliente de la cola. None si no hay nadie."""
        cola = self.colas[servicio]
        return None if cola.esta_vacia() else cola.desencolar()


def mostrar_ayuda():
    print("\n===== SISTEMA DE ATENCIÓN - COMPAÑÍA DE SEGUROS =====")
    print("Servicios:")
    for n, (nombre, _) in SERVICIOS.items():
        print(f"  {n} - {nombre}")
    print("\nComandos:")
    print("  C <servicio>  Llega un cliente (ej: C 1)")
    print("  A <servicio>  Atender al siguiente cliente (ej: A 1)")
    print("  E             Ver estado de las colas")
    print("  S             Salir")


def interpretar(texto):
    """Convierte 'C 1' o 'C1' en ('C', 1). Devuelve None si es inválido."""
    texto = texto.replace(" ", "").upper()
    if len(texto) < 2 or texto[0] not in ("C", "A") or not texto[1:].isdigit():
        return None
    servicio = int(texto[1:])
    return (texto[0], servicio) if servicio in SERVICIOS else None


def main():
    sistema = SistemaAtencion(SERVICIOS)
    inicio_programa = time.perf_counter()
    tiempo_procesando = 0.0  # suma del tiempo que tarda el sistema en responder
    operaciones = 0

    mostrar_ayuda()
    while True:
        entrada = input("\n> ").strip()
        if not entrada:
            continue
        if entrada.upper() == "S":
            break
        if entrada.upper() == "E":
            print("Estado de las colas:")
            for n, (nombre, _) in SERVICIOS.items():
                print(f"  {nombre}: {sistema.colas[n]}")
            continue

        orden = interpretar(entrada)
        if orden is None:
            print("Entrada inválida. Use C o A seguida del número de servicio.")
            mostrar_ayuda()
            continue

        comando, servicio = orden
        nombre = SERVICIOS[servicio][0]

        inicio_op = time.perf_counter()
        if comando == "C":
            resultado = sistema.llega_cliente(servicio)
        else:
            resultado = sistema.atender(servicio)
        duracion = time.perf_counter() - inicio_op

        tiempo_procesando += duracion
        operaciones += 1

        if comando == "C":
            print(f"Su número de atención para {nombre} es: {resultado}")
        elif resultado:
            print(f"Llamando al número {resultado} ({nombre})")
        else:
            print(f"No hay clientes en espera en {nombre}.")
        print(f"Tiempo de la operación: {duracion * 1000:.6f} ms")

    total = time.perf_counter() - inicio_programa
    print("\n===== RESUMEN DE EJECUCIÓN =====")
    print(f"Operaciones realizadas:                {operaciones}")
    print(f"Tiempo de procesamiento del sistema:   {tiempo_procesando * 1000:.6f} ms")
    print(f"Tiempo total de ejecución del programa: {total:.2f} s")
    print("Fin de la simulación.")


if __name__ == "__main__":
    main()
