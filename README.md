# Colas-en-py-

## ¿Cómo funcionan los programas?

Ambos usan una clase Cola (estructura FIFO: el primero en entrar es el primero en salir) hecha con nodos enlazados. Cada nodo guarda un dato y apunta al siguiente, y la cola guarda el frente, el final y el tamaño. Por eso encolar y desencolar son O(1).

# Ejercicio 1: Suma de colas

La función sumar_colas(cola_a, cola_b) recorre las dos colas al mismo tiempo, sin vaciarlas, suma cada par de elementos y los encola en una cola nueva. Si una cola es más larga, los elementos sobrantes se copian tal cual. Recorre cada cola una sola vez, así que su complejidad es O(n + m).

El programa tiene un menú para ver el ejemplo del enunciado o crear tus propias colas, y muestra el tiempo de ejecución en milisegundos.

# Ejercicio 2: Colas de servicios para una aseguradora

El sistema guarda una Cola por cada servicio (Siniestros, Pólizas nuevas, Pagos y Reclamos). Se maneja con dos comandos:

- C <servicio>: llega un cliente. Se genera su número de atención (por ejemplo S-001) y se encola.
- A <servicio>: se atiende al siguiente cliente. Se desencola al primero de esa cola y se muestra el número que se está llamando.

Cada servicio lleva su propia numeración y los clientes se atienden en el orden en que llegaron. Además, E muestra el estado de las colas, D agrega clientes de ejemplo, H muestra la ayuda y S sale mostrando un resumen con los tiempos de ejecución.
