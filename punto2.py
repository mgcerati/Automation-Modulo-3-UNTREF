import math


def raices_cuadratica(a, b, c):
    discriminante = b ** 2 - 4 * a * c

    if discriminante > 0:
        x1 = (-b + math.sqrt(discriminante)) / (2 * a)
        x2 = (-b - math.sqrt(discriminante)) / (2 * a)
        return f"Dos soluciones: x1 = {x1}, x2 = {x2}"
    elif discriminante == 0:
        x = -b / (2 * a)
        return f"Una solución: x = {x}"
    else:
        return "No hay solución real (discriminante negativo)."


a = float(input("Ingrese el valor de a: "))
b = float(input("Ingrese el valor de b: "))
c = float(input("Ingrese el valor de c: "))

print(raices_cuadratica(a, b, c))
