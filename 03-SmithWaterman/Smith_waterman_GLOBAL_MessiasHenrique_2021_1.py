'''
|-------------------------------------------------|
|     Aluno: Messias Henrique da Silva Santos;    |
|     Disciplina: Tópicos em Bioinformática;      |
|     Período: 2021.1;                            |
|-------------------------------------------------|
'''

import csv

match = 3
mismatch = -1
gap = -2

#Sequencia de número 20 na lista de frenquência:
vertical = 'GAGAAGAGAACUGAAGAGAGUGUUCAAUAUUGUUUCUUCGGCACCCAUGAAGCAGGCAGUCACCAUUGUAGAAACCUGGGAAAUCUUCCUGCCGCCCUACUUACAGGGGGCGCACGACUGCAGUCGGCCGUUGCAGUGCUCAACGGCCCGCGGCUACUAUUUUGCAGAUAUCCGUUUCGUUGCUGCCGGGCAGGCCAGCG'
horizontal = 'GAGAGUGUUCAAUAUUGUUUCUUCGGCUCGGCACCCAUGAAGCAGGCAGUCACCAUUGUAGAAACAAAACCUGGGAAAUCUUCCUGCCGCCCUACUUACAGGGGGCGCAAGGCACGACUGCAGUCGGCCGUUG'

def matching(letra1, letra2):
   return match if letra1 == letra2 else mismatch

def inicializacao(vertical, horizontal):
    m = len(vertical) + 1
    n = len(horizontal) + 1

    #Cria a matriz com zeros;
    matriz = [[0 for i in range(0, n+1)] for j in range(0, m+1)]

    matriz[0][0] = 'X'
    matriz[0][1] = 'U'
    matriz[1][0] = 'U'

    #Preenche com as sequencias;
    for i in range(2, n+1): 
        matriz[0][i] = horizontal[i-2]
    for j in range(2, m+1): 
        matriz[j][0] = vertical[j-2]
    
    #Preenche com os gaps;
    for i in range(2, m+1):
        matriz[i][1] = gap * (i-1)
    for j in range(2, n+1):
        matriz[1][j] = gap * (j-1)
    
    return matriz

def preenche(matriz, vertical, horizontal):
    #Função: cria uma matriz com os scores e com as possíveis movimentações;
    m = len(vertical) + 2
    n = len(horizontal) + 2

    #Inicializa a matriz com A's.
    matriz_direcoes = [['A' for i in range(0, n)] for j in range(0, m)]

    #Preenche as duas primeiras linhas.
    for i in range(0, m):
        matriz_direcoes[i][0] = [matriz[i][0], ' ']
    for i in range(1, m):
        matriz_direcoes[i][1] = [matriz[i][1], 'S']

    #Preenche as duas primeiras colunas.
    for j in range(0, n):
        matriz_direcoes[0][j] = [matriz[0][j], ' ']
    for j in range(1, n):
        matriz_direcoes[1][j] = [matriz[1][j], 'S']

    #Prenche com os scores.
    for i in range(2, m):
        for j in range(2, n):

            diagonal = matriz[i - 1][j - 1] + matching(horizontal[j - 2], vertical[i - 2])
            esquerda = matriz[i][j - 1] + gap
            baixo = matriz[i - 1][j] + gap
            direcoes = [diagonal, esquerda, baixo]
        
            matriz[i][j] = max(direcoes)
            indice = direcoes.index(max(direcoes)) #maior entre: [diagonal, esquerda, baixo];

            if indice == 0: #maior: diagonal
                matriz_direcoes[i][j] = [max(direcoes), "/"]
                if matriz[i][j] == esquerda: matriz_direcoes[i][j].append(">") #caso também venha pela esquerda
                if matriz[i][j] == baixo: matriz_direcoes[i][j].append("|") #caso também venha por cima
            elif indice == 1: #maior: esquerda
                matriz_direcoes[i][j] = [max(direcoes), ">"]
                if matriz[i][j] == diagonal: matriz_direcoes[i][j].append("/") #caso também venha pela diagonal
                if matriz[i][j] == baixo: matriz_direcoes[i][j].append("|") #caso também venha por cima 
            else: #maior: baixo   
                matriz_direcoes[i][j] = [max(direcoes), "|"]
                if matriz[i][j] == diagonal: matriz_direcoes[i][j].append("/") #caso também venha pela diagonal
                if matriz[i][j] == esquerda: matriz_direcoes[i][j].append(">") #caso também venha pela esquerda

    return [matriz, matriz_direcoes]

def calculaScore (matriz, num_linhas, num_colunas):
    score = matriz[num_linhas-1][num_colunas-1]
    return score

def backtrace(matriz, vertical, horizontal):
    x = len(vertical)+1
    y = len(horizontal)+1
    sequencia1 = []
    sequencia2 = []

    while (x > 1 or y > 1):
        if len(matriz[x][y]) > 2:
            if "/" in matriz[x][y] and "|" in matriz[x][y]:
                if matriz[x-1][y-1] > matriz[x-1][y]:
                    sequencia1.append(vertical[x-2])
                    sequencia2.append(horizontal[y-2])
                    x-=1
                    y-=1
                elif matriz[x-1][y-1] < matriz[x-1][y]:
                    sequencia1.append(vertical[x-2])
                    sequencia2.append("-")
                    x-=1
            elif "/" in matriz[x][y] and ">" in matriz[x][y]:
                if matriz[x-1][y-1] > matriz[x][y-1]:
                    sequencia1.append(vertical[x-2])
                    sequencia2.append(horizontal[y-2])
                    x-=1
                    y-=1
                elif matriz[x-1][y-1] < matriz[x][y-1]:
                    sequencia1.append("-")
                    sequencia2.append(horizontal[y-2])
                    y-=1
        else:
            if "/" in matriz[x][y][1]:
                sequencia1.append(vertical[x-2])
                sequencia2.append(horizontal[y-2])
                x-=1
                y-=1
            elif "|" in matriz[x][y][1]:
                sequencia1.append(vertical[x-2])
                sequencia2.append("-")
                x-=1
            elif ">" in matriz[x][y][1]:
                sequencia1.append("-")
                sequencia2.append(horizontal[y-2])
                y-=1
            else:
                if y == 1:
                    sequencia1.append(vertical[x-2])
                    sequencia2.append("-")
                    y-=1
                    break
                elif x == 1:
                    sequencia1.append("-")
                    sequencia2.append(horizontal[y-2])
                    x-=1

    return [sequencia1, sequencia2]

def salvaResultados(matriz, sequencia1, sequencia2):
    
    with open('MessiasHenrique_MatrizScores_GLOBAL.csv', 'w') as file:
        csv_w = csv.writer(file, delimiter=';')
        for linha in matriz:
            csv_w.writerow(linha)

    with open('MessiasHenrique_Alinhamento_GLOBAL.txt', 'w') as alinhamento:
        
        alinhamento.write(" ============= [ ALINHAMENTO GLOBAL ]===============\n\n")
        alinhamento.write(" ======= Match: " + str(match) + " | Mismatch: " + str(mismatch) + " | Gap: " + str(gap) + " =======\n\n")
        alinhamento.write(" ===   Vertical: " + str(sequencia1))
        alinhamento.write("\n")
        alinhamento.write(" === Horizontal: " + str(sequencia2))
        alinhamento.write("\n\n")
        alinhamento.write(" === Score: " + str(calculaScore(matrizScores, len(vertical) + 2, len(horizontal) + 2)))

if __name__ == "__main__":

    #Inicialização da matriz.
    matriz = inicializacao(vertical , horizontal)

    #Matrizes de score e a de movimentação.
    matrizScores, matrizDirecoes = preenche(matriz, vertical, horizontal)
    
    #Alinhamento.
    sequencia1, sequencia2 = backtrace(matrizDirecoes, vertical, horizontal)

    #Salva sequencias em arquivo .txt e a matriz de score em arquivo .csv;
    salvaResultados(matrizScores, sequencia1[::-1], sequencia2[::-1])