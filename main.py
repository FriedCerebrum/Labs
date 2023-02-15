import math
a = int(input("Введите значения числа a: "))
b = int(input("Введите значения числа b: "))
c = int(input("Введите значение числа c: "))
D = b**2-4*a*c
print("Дискриминант равен: ", D)
if D < 0:
    print("Корней нет")
if D == 0:
    x1 = -b/(2*a)
    print("Корень только один")
if D > 0:
    x1 = (-b - math.sqrt(D)) / (2 * a)
    x2 = (-b + math.sqrt(D)) / (2 * a)
    print("Корня целых два", x1, x2)