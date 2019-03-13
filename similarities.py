# Creamos la función de similitud
# ¡OJO! Para evitar similitudes muy altas (debido a la cantidad de ceros)
# solo contamos, para la similitud, las propiedades que tengan valor 1 en
# alguno de los items.
def equal_sim(item1, item2):
    dif = 0
    atr = 0
    for i in range(len(item1)):
        if item1[i] != item2[i]:
            dif = dif + 1
        if item1[i] == 1 or item2[i] == 1:
            atr = atr + 1
    return float(atr - dif)/float(atr)