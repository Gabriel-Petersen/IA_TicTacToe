import os, random, copy, math
import TrainingNeural

ans = ""
board = [[0, 0, 0], 
         [0, 0, 0], 
         [0, 0, 0]]

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
    
def ShowBoard():
    global board
    print()
    
    for x in [0, 1, 2]:
        print('|', end=' ')
        for y in [0, 1, 2]:
            if board[y][x] == 0:
                print (" ", end=' ')
            elif board[y][x] == 1:
                print ("X", end=' ')
            else:
                print ("O", end=' ')

        print ('|')
    print ()
    
def PlayerTurn ():
    global board
    print("É a sua vez, observe o tabuleiro e decida em qual linha e em qual coluna irá posicionar a sua marca")
    movedone = False
    while movedone == False:
        ShowBoard()
        options = [1, 2, 3]
        x = int(input("Em que linha deseja efetuar a sua jogada? "))
        while x not in options:
            print("Dígito não reconhecido. Digite apenas o número 1, 2 ou 3")
            x = int(input("Em que linha deseja efetuar a sua jogada? "))
        
        y = int(input("Em que coluna deseja efetuar a sua jogada? "))
        while y not in options:
            print("Dígito não reconhecido. Digite apenas o número 1, 2 ou 3")
            y = int(input("Em que coluna deseja efetuar a sua jogada? "))

        print (f"Você escolheu a posição {x, y}")
        y -= 1
        x -= 1
        if board [y][x] == 0:
            board [y][x] = 1
            print ("Jogada efetuada com sucesso!!")
            movedone = True
        else:
            print ("Essa casa já está ocupada. Tente novamente por favor.")

def RandomGame ():
    global board
    print ("Sorteando aleatoriamente quem começa...")
    turn = random.randrange(2, 4)
    if turn == 2:
        print ("Você começa!")
        turn = 1
    else:
        print ("A máquina começará")
        turn = -1
    
    while WinnerChecker(board) == 0:
        if turn == 1:
            PlayerTurn()
            turn *= -1
        else:
            movedone = False
            while movedone == False:
                x = random.randrange(0, 3)
                y = random.randrange(0, 3)
                if board[y][x] == 0:
                    board[y][x] = turn
                    movedone = True
                    print (f"O computador jogou na posição ({x+1}, {y+1})")
            ShowBoard()
            turn *= -1

    if WinnerChecker(board) == 1:
        return True
    elif WinnerChecker(board) == -1:
        return False
    else:
        return "empate"

def MachineTurn(clones):
    global board
    collection = list()
    options = list()
    scores = list()

    for i in range(clones):
        collection.append(copy.deepcopy(board))
    
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
        
    board [move[0]][move[1]] = -1

def MonteCarlo():
    global board
    clones = 100 * int(input("Digite a quantidade de clones: "))

    print ("Sorteando aleatoriamente quem começa...")
    turn = random.randrange(2, 4)
    if turn == 2:
        print ("Você começa!")
        turn = 1
    else:
        print ("A máquina começará")
        turn = -1
    
    while WinnerChecker(board) == 0:
        if turn == 1:
            PlayerTurn()
            ShowBoard()
        else:
            MachineTurn(clones)
        turn *= -1

    ShowBoard()

    if WinnerChecker(board) == 1:
        return True
    elif WinnerChecker(board) == -1:
        return False
    else:
        return "empate"

def NeuralNetwork():
    global board
    dataBase = TrainingNeural.best

    print ("Sorteando aleatoriamente quem começa...")
    verify = input("Deseja realizar verificações? (responda com apenas 's' ou 'n')")
    while verify not in ('s', 'n'):
        verify = input("Input não compreendido, tente novamente (responda apenas com 's' ou 'n')")

    if verify == 's':
        data1 = TrainingNeural.NeuralSystem(TrainingNeural.lastBest[0], TrainingNeural.lastBest[1], TrainingNeural.lastBest[2], TrainingNeural.lastBest[3])
        data2 = TrainingNeural.NeuralSystem(TrainingNeural.best[0], TrainingNeural.best[1], TrainingNeural.best[2], TrainingNeural.best[3])
        print ("Realizando verificação em 100 etapas...")
        score1 = data1.PlayGame(2000, 100)
        score2 = data2.PlayGame(2000, 100)
        if score1 > score2:
            dataBase = TrainingNeural.lastBest
    else:
        print("Verificação não realizada, utilizando dados do último treinamento")

    machine = TrainingNeural.NeuralSystem(dataBase[0], dataBase[1], dataBase[2], dataBase[3])
    turn = random.randrange(2, 4)
    if turn == 2:
        print ("Você começa!")
        turn = 1
    else:
        print ("A máquina começará.")
        turn = -1

    while (WinnerChecker(board)) == 0:
        if turn == 1:
            PlayerTurn()
            ShowBoard()
            turn *= -1
        else:
            manipulatedBoard = copy.deepcopy(board)
            for i in range(3):
                for j in range(3):
                    manipulatedBoard[i][j] = -1 * board[i][j]

            aiPosition = machine.MakeMove(manipulatedBoard, False)[0]
            board[math.floor(aiPosition/3)][aiPosition%3] = -1
            turn *= -1

    ShowBoard()

    if WinnerChecker(board) == 1:
        return True
    elif WinnerChecker(board) == -1:
        return False
    else:
        return "empate"
    
while ans != "n":
    os.system("cls")

    #montagem do tabuleiro

    for y in [0, 1, 2]:
        for x in [0, 1, 2]:
            board[y][x] = 0

    #interação inicial com o jogador

    print ("Bem vindo ao jogo da velha inteligente (ou não rsrsrs)!")

    challenge = input("Deseja jogar contra o oponente inteligente? (digite s ou n) ")
    while challenge not in ("s", "n"):
        challenge = input ("Resposta não compreendida, tente novamente. (Responda apenas com s ou n) ")
    
    if challenge == "s":
        AItype = input("Prefere jogar contra o Monte Carlo ou contra a Rede Neural? (digite Monte Carlo ou Rede Neural, simplesmente) ")
        while AItype.casefold().strip().replace(" ", "") not in ("redeneural", "montecarlo"):
            print (f"Você digitou {AItype}")
            AItype = input ("Resposta não compreendida, tente novamente. (digite Monte Carlo ou Rede Neural, simplesmente) ")
        
        AItype = AItype.casefold().strip().replace(" ", "")

        if AItype == "montecarlo":
            game = MonteCarlo()
            if game == True:
                print ("\nVocê venceu!!!\n")
            elif game == False:
                print ("\nDerrotado :(\n")
            else:
                print ("\nEmpate :/\n")
        else:
            game = NeuralNetwork()
            if game == True:
                print ("\nVocê venceu!!!\n")
            elif game == False:
                print ("\nDerrotado :(\n")
            else:
                print ("\nEmpate :/\n")
    else:
        game = RandomGame()
        if game == True:
            print ("Parabéns! Você venceu!! Não é muito mérito, mas ok")
        
        elif game == False:
            print ("Como raios você perdeu para um bot aleatório???")
        else:
            print ("Empate :(")

    ans = input("Ainda deseja jogar? ")
