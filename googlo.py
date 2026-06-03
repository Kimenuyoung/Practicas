import random

OBJETIVO = 10**100
MAX_GENERACIONES = 20

poblacion = [8, 4, 7, 1, 7, 6]
print("Generación 0:", poblacion)

generacion = 1


while generacion <= MAX_GENERACIONES:
    
    # Selección de padres (los 3 primeros)
    padres = poblacion[:3]
    print("\nPadres seleccionados:", padres)

    hijos = []

    # Cruce (combinaciones)
    for i in range(len(padres) - 1):
        for j in range(i + 1, len(padres)):
            p1 = padres[i]
            p2 = padres[j]

            # Operaciones
            suma = p1 + p2
            multiplicacion = p1 * p2

            hijos.append(suma)
            hijos.append(multiplicacion)

            # Potencia (controlada para evitar números gigantes)
            if p2 < 6:
                potencia = p1 ** p2
                hijos.append(potencia)

    print("Hijos generados:", hijos)

    # Mutación (invertir un número aleatorio)
    mutado = random.randint(0, len(hijos) - 1)
    hijos[mutado] = int(str(hijos[mutado])[::-1])

    print(f"Generación {generacion} después de mutación:", hijos)

    # Nueva generación
    poblacion = hijos
    maximo = max(poblacion)

    print("Máximo actual:", maximo)

    # Condición de parada
    if maximo >= OBJETIVO:
        print("\n ¡Se alcanzó el objetivo (10^100)!")
        break

    generacion += 1

print("\nResultado final:")
print("Última generación:", poblacion)
print("Número más grande encontrado:", max(poblacion))