import generar_campo_galois

# tabla = [
#     [0,0,0],
#     [0,0,1],
#     [0,1,0],
#     [1,0,0],
#     [0,1,1],
#     [1,1,0],
#     [1,1,1],
#     [1,0,1]
# ]


def obtener_alfa_desde_entero(alfa:int, tabla: list[list[int]]):
    if alfa == -1:
        return tabla[0]
    return tabla[(alfa)%(len(tabla)-1)+1]




def sumar_bits(alfa_1:list[int], alfa_2:list[int]):
    resultado = []
    for x,y in zip(alfa_1,alfa_2):
        if x != y:
            resultado.append(1)
        else:
            resultado.append(0)
    return resultado


def obtener_alfa_entero_desde_espacio(alfa: list[int], tabla: list[list[int]]):
    i = 0
    for fila in tabla:
        band = True
        for valor_fila,valor_alfa in zip(fila, alfa):
            if valor_fila != valor_alfa:
                band = False
                break
        if band:
            return i-1
        i += 1



def sumar_polinomios(pol_1:list[tuple[int,int]], pol_2:list[tuple[int,int]], tabla: list[list[int]]):
    resultado = []
    grado_pol_1 = pol_1[0][0]
    grado_pol_2 = pol_2[0][0]
    grado_max = max(grado_pol_1, grado_pol_2)
    pol_1_expandido:list[tuple[int,int]] = []
    pol_2_expandido:list[tuple[int,int]] = []
    i = grado_max
    j = 0
    while i >= 0:
        if j < len(pol_1) and i == pol_1[j][0]:
            pol_1_expandido.append(pol_1[j])
            j += 1
        else:
            pol_1_expandido.append((i,-1))
        i -= 1
    i = grado_max
    j = 0
    while i >= 0:
        if j < len(pol_2) and i == pol_2[j][0]:
            pol_2_expandido.append(pol_2[j])
            j += 1
        else:
            pol_2_expandido.append((i,-1))
        i -= 1

    for (x_1,alfa_1), (x_2,alfa_2) in zip(pol_1_expandido, pol_2_expandido):
        alfa_nuevo_bits = sumar_bits(obtener_alfa_desde_entero(alfa_1, tabla), obtener_alfa_desde_entero(alfa_2, tabla))
        alfa_nuevo = obtener_alfa_entero_desde_espacio(alfa_nuevo_bits, tabla)
        if alfa_nuevo != -1:
            resultado.append((x_1,alfa_nuevo))
    return resultado








def dividir_polinomios(tabla: list[list[int]], dividendo:list[tuple[int,int]], divisor:list[tuple[int,int]]):
    primero_dividendo = dividendo[0]
    primero_divisor = divisor[0]
    cociente:list[tuple[int, int]] = []
    
    while primero_dividendo[0] >= primero_divisor[0]:
        restar = []
        x_cociente = primero_dividendo[0] - primero_divisor[0]
        alfa_cociente = primero_dividendo[1] - primero_divisor[1]
        alfa_cociente = alfa_cociente % (len(tabla)-1)
        cociente.append((x_cociente, alfa_cociente))

        for (x_divisor,alfa_divisor) in divisor:
            restar.append((x_divisor+x_cociente, (alfa_divisor+alfa_cociente)%(len(tabla)-1)))

        nuevo_dividendo = sumar_polinomios(dividendo, restar, tabla)
        
        dividendo = []
        for x,alfa in nuevo_dividendo:
            if alfa != -1:
                dividendo.append((x,alfa))
        # print(dividendo)
        if len(dividendo) == 0:
            break

        primero_dividendo = dividendo[0]
    return dividendo, cociente


if __name__ == "__main__":
    print(dividir_polinomios(generar_campo_galois.generar_campo([1,0,1,1], 8), [(6,1), (4,1), (3,2), (2,0)], [(2,0),(1,4),(0,3)]))