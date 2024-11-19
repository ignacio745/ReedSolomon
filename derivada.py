def derivar(pol:list[tuple[int,int]]):
    resultado:list[tuple[int,int]] = []
    for comp in pol:
        if comp[0]%2 == 1:
            resultado.append((comp[0]-1, comp[1]))
    return resultado

if __name__ == "__main__":
    print(derivar([(3,4), (2,3), (1,5), (0,2)]))