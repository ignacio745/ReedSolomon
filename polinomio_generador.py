from euclides import multiplicar_polinomios

def crear_polinomio_generador_palabras_validas(n:int, k:int, campo:list[list[int]]):
    polinomio = multiplicar_polinomios([(1,0), (0,1)], [(1,0), (0,2)], campo)
    for i in range(3, n-k+1):
        polinomio = multiplicar_polinomios(polinomio, [(1,0), (0,i)], campo)
    return polinomio