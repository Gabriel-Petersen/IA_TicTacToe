import os, copy, math, random, threading

noise = int(4)

best = [[[-93.76209999999983, 34.74769999999993, -145.86890000000014, 116.9588999999999], [-12.223799999999915, 13.896600000000152, 75.90589999999997, -291.8081000000001], [3.8378000000000023, -50.07120000000013, -261.24270000000075, -182.58679999999964], [133.11109999999985, -67.42309999999982, -24.487000000000027, 22.889700000000122], [-99.3650999999999, -147.2596999999999, -58.349999999999774, -89.08929999999985], [25.873800000000244, 64.48900000000005, 51.14890000000008, -56.37889999999985], [45.02750000000019, 48.26239999999991, 242.76940000000005, -48.666999999999994], [-120.46099999999977, -109.1676, 101.31330000000005, -129.69040000000035], [34.15379999999998, -71.2125000000001, -137.95850000000027, 41.77099999999994], [201.41189999999966, -56.9461999999999, -112.42469999999985, 88.06549999999994]], [-12.276400000000015, -196.20409999999953, 33.990700000000025, 67.95050000000005], [-21.925000000000047, -68.46379999999967, -237.9730000000003, -176.01520000000008], 37.25239999999979]

lastBest = [[[-98.37999999999991, 46.609999999999914, -152.29999999999984, 120.95999999999994], [-10.409999999999922, 6.870000000000119, 72.7399999999999, -301.48000000000025], [5.919999999999998, -55.75999999999999, -258.50000000000006, -187.14999999999975], [124.6100000000001, -66.7299999999999, -10.810000000000038, 31.890000000000043], [-97.3999999999998, -145.56999999999977, -48.10999999999992, -95.8199999999999], [35.24000000000017, 61.81000000000001, 56.76000000000008, -59.06999999999999], [47.53000000000017, 41.27999999999996, 240.85000000000022, -45.33], [-122.85999999999994, -104.8, 103.62000000000013, -122.66000000000011], [34.990000000000016, -79.14000000000003, -146.84000000000003, 
37.80000000000002], [201.51000000000002, -54.20999999999991, -114.75999999999989, 89.88]], [-1.830000000000008, -189.06000000000006, 32.410000000000075, 55.690000000000154], [-19.870000000000022, -65.45999999999994, -227.10000000000008, -173.51000000000025], 44.32999999999997]

class NeuralSystem:

    def __init__(self, wA, wB, bA, bB):
        self.weightsA = wA
        self.weightsB = wB
        self.biasA = bA
        self.biasB = bB
        self.config = [wA, wB, bA, bB]
        self.effect = 0

    def MakeMove (self, board, limit=True):
        _output = 0
        _input = list()
        trytimes = 0
        for x in [0, 1, 2]:
            for y in [0, 1, 2]:
                _input.append(copy.copy(board[x][y]))

        _input.append(trytimes)

        while trytimes < 20:
            aux = [0, 0, 0, 0]
            _input[len(_input) - 1] = trytimes
            for j in range (4):
                for i in range (10):
                    aux[j] += float(_input[i]) * self.weightsA[i][j]
                aux[j] += self.biasA[j]
                
                aux[j] = math.trunc(100*math.tanh(aux[j]))/100
                
            for i in range (4):
                _output += aux[i]*self.weightsB[i]

            _output += self.biasB
            place = int(_output % 9)

            if _input[place] == 0:
                return (place, trytimes)
            else:
                trytimes += 1
                
            if limit == False:
                trytimes = 0

        print ("Bip", end=" / ")
        return ("error", 0)

    def AutoPlay (self, otherPlayer):
        turn = random.randrange(-1, 2, 2)

        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        totalTry = 0

        while (WinnerChecker(board) == 0):
            if turn == 1:
                ans = self.MakeMove(board)
                if ans[0] == 'error':
                    board = [[-1, -1, -1], [0, 0, 0], [0, 0, 0]]
                    self.effect -= 999
                else:
                    board[math.floor(ans[0]/3)][ans[0]%3] = 1
                    totalTry += ans[1]
                turn *= -1
            else:
                manipulatedBoard = copy.deepcopy(board)
                for x in range(3):
                    for y in range(3):
                        manipulatedBoard[x][y] = (-1) * board[x][y]

                ans = otherPlayer.MakeMove(manipulatedBoard)
                if ans[0] == 'error':
                    board = [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
                    self.effect = 0
                    return
                else:
                    board[math.floor(ans[0]/3)][ans[0]%3] = -1
                turn *= -1

        if WinnerChecker(board) == 1:
            self.effect += 10
        elif WinnerChecker(board) == -1:
            self.effect -= 20
        else:
            self.effect += 2

        self.effect -= round(totalTry/13)
    
    def PlayInstance (self, diff):
        turn = random.randrange(-1, 2, 2)

        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        totalTry = 0

        while (WinnerChecker(board) == 0):
            if turn == 1:
                ans = self.MakeMove(board)
                if ans[0] == "error":
                    board = [[-1, -1, -1], [0, 0, 0], [0, 0, 0]]
                    self.effect -= 999
                else:
                    board[math.floor(ans[0]/3)][ans[0]%3] = 1
                    totalTry += ans[1]
                turn *= -1
            else:
                MachineTurn(diff, board)
                turn *= -1

        if WinnerChecker(board) == 1:
            self.effect += 10
        elif WinnerChecker(board) == -1:
            self.effect -= 20
        else:
            self.effect += 2

    def DoAutoTrain(self, otherPlayer, num):
        for _ in range(num):
            self.AutoPlay(otherPlayer)

        return self.effect

    def PlayGame(self, diff, num):
        
        for _ in range (num):
            threading.Thread(target=self.PlayInstance, args=(diff,)).start()

        return self.effect

def WinnerChecker (usingBoard):
    #verificando se linhas trazem vitória

    for line in usingBoard:
        s = 0
        for value in line:
            s += value
        
        if s == 3:
            return 1
        elif s == -3:
            return -1
        
    #verificando se colunas trazem vitória

    for position in range(0, 3):
        s = 0
        for column in range(0, 3):
            s += usingBoard [column][position]

        if s == 3:
            return 1
        elif s == -3: 
            return -1
                
    #verificando se diagonais trazem vitória

    s1 = usingBoard[0][0] + usingBoard[1][1] + usingBoard[2][2]
    s2 = usingBoard[2][0] + usingBoard[1][1] + usingBoard[0][2]
    
    if s1 == 3 or s2 == 3:
        return 1
    elif s1 == -3 or s2 == -3:
        return -1
    
    for line in usingBoard:
        for value in line:
            if value == 0:
                return 0
    return 2

def MachineTurn(clones, field):
    collection = list()
    options = list()
    scores = list()

    for i in range(clones):
        collection.append(copy.deepcopy(field))
    
    for i in range(clones):
        firstMove = ()
        movedone = False
        while movedone == False:
            x = random.randrange(0, 3)
            y = random.randrange(0, 3)
            if collection[i][y][x] == 0:
                collection[i][y][x] = -1
                movedone = True
                firstMove = (y, x)
                if firstMove not in options:
                    options.append(firstMove)
                    scores.append(0)
                
        turn = 1

        while WinnerChecker(collection[i]) == 0:
            if turn == 1:
                movedone = False
                while movedone == False:
                    x = random.randrange(0, 3)
                    y = random.randrange(0, 3)
                    if collection[i][y][x] == 0:
                        collection[i][y][x] = turn
                        movedone = True
                turn *= -1
            else:
                movedone = False
                while movedone == False:
                    x = random.randrange(0, 3)
                    y = random.randrange(0, 3)
                    if collection[i][y][x] == 0:
                        collection[i][y][x] = turn
                        movedone = True
                turn *= -1
        
        result = WinnerChecker(collection[i])
        if result == 2:
            scores[options.index(firstMove)] += 0
        else:
            scores[options.index(firstMove)] += (-1) * result
    
    move = options[scores.index(max(scores))]
        
    field [move[0]][move[1]] = -1

def GeneratePopulation (currentBest, size, genNumber, noise):
    population = list()
    for i in range(size):
        wA = [[0, 0, 0, 0], 
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]
        wB = list()
        biasA = list()
        for a in range(10):
            for i in range (4):
                wA[a][i] = currentBest[0][a][i] + round(float(random.randrange(-1000*noise, 1000*noise))/(500*genNumber), 4)

        for b in range (4):
            wB.append(currentBest[1][b] + round(float(random.randrange(-1000*noise, 1000*noise))/(500*genNumber), 4))
            biasA.append(currentBest[2][b] + round(float(random.randrange(-1000*noise, 1000*noise))/(500*genNumber), 4))

        population.append(NeuralSystem(wA, wB, biasA, currentBest[3] + round(float(random.randrange(-1000*noise, 1000*noise))/(500*genNumber), 4)))

    return population

def RunCode(best, lastBest, noise):
    os.system("cls")

    if input("Deseja realizar o auto-treinamento? (responda com s ou n) ") == 'n':
        evolution = True

        if input("Deseja realizar comparações? (responda com s ou n) ") == "s":
            newOne = NeuralSystem(best[0], best[1], best[2], best[3])
            oldOne = NeuralSystem(lastBest[0], lastBest[1], lastBest[2], lastBest[3])
            iterations = int(input("Digite o número de iterações para a comparação: "))
            oldScore = oldOne.PlayGame(3000, iterations)
            newScore = newOne.PlayGame(3000, iterations) 
            print (f"\nApós jogar {iterations} partidas, a pontuação do indivíduo anterior é de {oldScore}, enquanto a do novo é {newScore}")
            if oldScore > newScore:
                print("Involução do modelo, utilizar-se-á dados da execução anterior")
                evolution = False
                best = lastBest
            else:
                print("Modelo continua evoluindo, o padrão será mantido")

        maxgen = int(input("Quantas gerações você deseja rodar? "))
        pop_size = int(input("Qual o número das populações? "))
        checkpointDistance = int(input("Qual a distância entre as verificações? "))
        population = list()
        bests = list()

        for currentGent in range(maxgen):
            print(f"\nIniciando geração {currentGent + 1}...")
            population = GeneratePopulation(best, pop_size, currentGent + 1, noise)

            individualScore = list()
            a25 = a50 = a75 = False

            for neural in population:
                if maxgen <= 25:
                    individualScore.append(neural.PlayGame(300 + 50*currentGent, 6))
                else:
                    clones = 100 + 30*currentGent
                    if clones >= 1600:
                        individualScore.append(neural.PlayGame(1600, 4))
                    else:
                        individualScore.append(neural.PlayGame(clones, 6))
                progress = 100 * population.index(neural)/pop_size
                if progress >= 25 and a25 == False:
                    print ("\nGeração em 25%")
                    a25 = True
                if progress >= 50 and a50 == False:
                    print ("\nGeração em 50%")
                    a50 = True
                if progress >= 75 and a75 == False:
                    print ("\nGeração em 75%")
                    a75 = True

            print (f"\n\nProgresso total em {round(100*(currentGent + 1)/maxgen, 1)}%")
                
            index = individualScore.index(max(individualScore))
            best = population[index].config

            if currentGent%checkpointDistance == 0 and currentGent > 2 and currentGent < (maxgen - 2):
                bests.append(best)
                print ("\nO melhor indivíduo da geração possui os seguintes dados:")
                print(best)
                score = NeuralSystem(best[0], best[1], best[2], best[3]).PlayGame(1200, 10)
                print (f"\nApós jogar 10 partidas facilitadas, a pontuação dele é de {score}")
                scoreList = list()
                for item in bests:
                    scoreList.append(NeuralSystem(item[0], item[1], item[2], item[3]).PlayGame(1200, 10))
                if score < max(scoreList):
                    print(f"Involução geracional. O melhor da geração atual pontuou {score} enquanto o melhor registrado dentro dos checkpoints pontuou {max(scoreList)}")
                    best = bests[scoreList.index(max(scoreList))]
                    print(f"\nOs novos dados do melhor fitness são:\n{best}")

        print(best)

        bestOne = NeuralSystem(best[0], best[1], best[2], best[3])
        print (f"Após jogar 50 partidas, a pontuação do melhor indivíduo é de {bestOne.PlayGame(3000, 50)}")
        if evolution:
            print ("Uma vez que o modelo continua evoluindo, substitua o 'last best' pelo novo melhor fitness")
        else:
            print ("Uma vez que o ultimo treinamento regrediu o modelo, substitua o 'best' pelo novo melhor fitness")
    else:
        firstBest = copy.deepcopy(best)
        maxgen = int(input("Quantas gerações você deseja rodar? "))
        pop_size = int(input("Qual o número das populações? "))
        
        for currentGen in range(maxgen):
            print (f'Iniciando geração {currentGen + 1}')
            
            population = GeneratePopulation(best, pop_size, currentGen + 1, noise)

            individualScore = list()
            a25 = a50 = a75 = False

            for neural in population:
                individualScore.append(neural.DoAutoTrain(NeuralSystem(lastBest[0], lastBest[1], lastBest[2], lastBest[3]), 6))

                progress = 100 * population.index(neural)/pop_size
                if progress >= 25 and a25 == False:
                    print ("\nGeração em 25%")
                    a25 = True
                if progress >= 50 and a50 == False:
                    print ("\nGeração em 50%")
                    a50 = True
                if progress >= 75 and a75 == False:
                    print ("\nGeração em 75%")
                    a75 = True
            
            print (f"\n\nProgresso total em {round(100*(currentGen + 1)/maxgen, 1)}%")
                
            index = individualScore.index(max(individualScore))
            lastBest = copy.deepcopy(best)
            best = population[index].config

        print(best)

        bestOne = NeuralSystem(best[0], best[1], best[2], best[3])
        firstOne = NeuralSystem(firstBest[0], firstBest[1], firstBest[2], firstBest[3])
        newScore = bestOne.PlayGame(3000, 50)
        oldScore = firstOne.PlayGame(3000, 50)
        print (f"Após jogar 50 partidas, a pontuação do melhor indivíduo é de {newScore}, enquanto que a do indivíduo inicial é {oldScore}")
        if newScore > oldScore:
            print ("Uma vez que o modelo continua evoluindo, substitua o 'last best' pelo novo melhor fitness")
            print (f"Ao jogar o primeiro modelo contra o último um total de 10 vezes a pontuação final do novo modelo foi de {bestOne.DoAutoTrain(firstOne, 10)} pontos, enquanto o primeiro modelo fez {firstOne.DoAutoTrain(bestOne, 10)}")
        else:
            print ("Uma vez que o ultimo treinamento regrediu o modelo, substitua o 'best' pelo novo melhor fitness")
            print (f"Ao jogar o primeiro modelo contra o último um total de 10 vezes a pontuação final do modelo antigo foi de {firstOne.DoAutoTrain(bestOne, 10)} pontos, enquanto o novo modelo fez {bestOne.DoAutoTrain(firstOne, 10)}")

            

if input("Vai rodar o treinamento? ") == 's':
    RunCode(best, lastBest, noise)
