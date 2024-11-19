import numpy as np
from math import log2

def dividir_polinomios(grado:int, divisor:list[int]):
    dividendo = [1]
    for _ in range(grado):
        dividendo.append(0)


    largo_dividendo = len(dividendo)
    largo_divisor = len(divisor)

    restar_lista:list = divisor.copy()
    while largo_dividendo >= largo_divisor:
        largo_restar = largo_dividendo-largo_divisor
        for _ in range(largo_restar):
            restar_lista.append(0)
        restar = np.array(restar_lista)
        

        # Resta
        resultado_resta = []
        for (i, j) in zip(dividendo, restar):
            if i == 0:
                if j == 0:
                    resultado_resta.append(0)
                elif j == 1:
                    resultado_resta.append(1)
            elif i == 1:
                if j == 0:
                    resultado_resta.append(1)
                elif j == 1:
                    resultado_resta.append(0)
        
        dividendo = []
        band = True
        for i in resultado_resta:
            if i == 0 and band:
                pass
            else:
                band = False
                dividendo.append(i)

        largo_dividendo = len(dividendo)
    
    return(dividendo)


def generar_campo(generador:list[int] = [1,0,0,1,1], componentes: int = 16):
    log_componentes = int(log2(componentes))
    campo = [[0 for _ in range(log_componentes)]]
    long_generador = len(generador)
    for i in range(0, componentes-1):
        nuevo = dividir_polinomios(i, generador)
        ceros = [0 for _ in range(log_componentes - len(nuevo))]
        campo.append(ceros + nuevo)
    return campo

if __name__ == "__main__":
    campo = generar_campo([1,0,0,1,1], 16)
    i = -1
    for fila in campo:
        print(i, fila)
        i+=1