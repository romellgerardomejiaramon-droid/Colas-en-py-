import time


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

    def frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._frente.dato

    def esta_vacia(self):
        return self._tamano == 0

    def tamano(self):
        return self._tamano

    def __len__(self):
        return self._tamano

    def __iter__(self):
        actual = self._frente
        while actual:
            yield actual.dato
            actual = actual.siguiente

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"


SERVICIOS = {
    1: ("Siniestros", "S"),
    2: ("Pólizas nuevas", "P"),
    3: ("Pagos", "G"),
    4: ("Reclamos", "R"),
}


class SistemaAtencion:

    def __init__(self, servicios):
        self.servicios = servicios
        self.colas = {n: Cola() for n in servicios}
        self.emitidos = {n: 0 for n in servicios}
        self.atendidos = {n: 0 for n in servicios}

    def llega_cliente(self, servicio):
        delante = len(self.colas[servicio])
        self.emitidos[servicio] += 1
        prefijo = self.servicios[servicio][1]
        ticket = f"{prefijo}-{self.emitidos[servicio]:03d}"
        self.colas[servicio].encolar(ticket)
        return ticket, delante

    def atender(self, servicio):
        cola = self.colas[servicio]
        if cola.esta_vacia():
            return None
        ticket = cola.desencolar()
        self.atendidos[servicio] += 1
        return ticket, len(cola)


def mostrar_ayuda():
    print("\n" + "=" * 52)
    print("  SISTEMA DE ATENCIÓN - COMPAÑÍA DE SEGUROS")
    print("=" * 52)
    print("Servicios:")
    for n, (nombre, _) in SERVICIOS.items():
        print(f"  {n} - {nombre}")
    print("\nComandos:")
    print("  C <servicio>  Llega un cliente        (ej: C 1)")
    print("  A <servicio>  Atender siguiente       (ej: A 1)")
    print("  E             Ver estado de las colas")
    print("  D             Agregar clientes de ejemplo")
    print("  H             Ver esta ayuda")
    print("  S             Salir")


def mostrar_estado(sistema):
    print(f"\n{'Servicio':<20}{'En espera':<11}{'Atendidos':<11}Cola")
    print("-" * 56)
    for n, (nombre, _) in SERVICIOS.items():
        cola = sistema.colas[n]
        print(f"{n} - {nombre:<16}{len(cola):<11}{sistema.atendidos[n]:<11}{cola}")


def cargar_datos_ejemplo(sistema):
    llegadas = {1: 4, 2: 2, 3: 5, 4: 3}
    for servicio, cantidad in llegadas.items():
        for _ in range(cantidad):
            sistema.llega_cliente(servicio)
    for servicio in (1, 3, 3):
        sistema.atender(servicio)


def elegir_inicio(sistema):
    print("\n¿Cómo desea iniciar?")
    print("  1. Con clientes de ejemplo (colas ya cargadas)")
    print("  2. Con las colas vacías (yo ingreso los clientes)")
    while True:
        try:
            opcion = input("Elija una opción: ").strip()
        except (KeyboardInterrupt, EOFError):
            opcion = "2"
        if opcion == "1":
            cargar_datos_ejemplo(sistema)
            print("\nSe cargaron clientes de ejemplo:")
            mostrar_estado(sistema)
            return
        if opcion == "2":
            return
        print("Opción inválida. Escriba 1 o 2.")


def interpretar(texto):
    limpio = texto.replace(" ", "").upper()
    if not limpio or limpio[0] not in ("C", "A"):
        return None, "Comando no reconocido. Escriba H para ver la ayuda."
    if len(limpio) == 1:
        return None, f"Falta el número de servicio. Ejemplo: {limpio} 1"
    if not limpio[1:].isdigit() or int(limpio[1:]) not in SERVICIOS:
        return None, f"Servicio inválido. Elija entre 1 y {len(SERVICIOS)}."
    return (limpio[0], int(limpio[1:])), None


def main():
    sistema = SistemaAtencion(SERVICIOS)
    inicio_programa = time.perf_counter()
    tiempo_procesando = 0.0
    operaciones = 0

    mostrar_ayuda()
    elegir_inicio(sistema)
    while True:
        try:
            entrada = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not entrada:
            continue
        comando = entrada.upper()
        if comando == "S":
            break
        if comando == "H":
            mostrar_ayuda()
            continue
        if comando == "E":
            mostrar_estado(sistema)
            continue
        if comando == "D":
            cargar_datos_ejemplo(sistema)
            print("Se agregaron clientes de ejemplo.")
            mostrar_estado(sistema)
            continue

        orden, error = interpretar(entrada)
        if error:
            print(error)
            continue

        accion, servicio = orden
        nombre = SERVICIOS[servicio][0]

        inicio_op = time.perf_counter()
        if accion == "C":
            resultado = sistema.llega_cliente(servicio)
        else:
            resultado = sistema.atender(servicio)
        duracion = time.perf_counter() - inicio_op
        tiempo_procesando += duracion
        operaciones += 1

        if accion == "C":
            ticket, delante = resultado
            print(f"Su número de atención para {nombre} es: {ticket}")
            print(f"Clientes delante de usted: {delante}")
        elif resultado:
            ticket, quedan = resultado
            print(f"Llamando al número {ticket} ({nombre})")
            print(f"Clientes en espera en {nombre}: {quedan}")
        else:
            print(f"No hay clientes en espera en {nombre}.")

        print(f"Tiempo de la operación: {duracion * 1000:.6f} ms | "
              f"Transcurrido: {time.perf_counter() - inicio_programa:.2f} s")

    total = time.perf_counter() - inicio_programa
    print("\n" + "=" * 52)
    print("  RESUMEN FINAL")
    print("=" * 52)
    mostrar_estado(sistema)
    print(f"\nOperaciones realizadas:                 {operaciones}")
    print(f"Tiempo de procesamiento del sistema:    {tiempo_procesando * 1000:.6f} ms")
    print(f"Tiempo total de ejecución del programa: {total:.2f} s "
          f"({total * 1000:.2f} ms)")
    print("Fin de la simulación.")


if __name__ == "__main__":
    main()
