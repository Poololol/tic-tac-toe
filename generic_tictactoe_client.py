# https://www.desmos.com/calculator/uqiamamlwm
import asyncio

async def main1():
    import pygame
    import utils
    import network
    import math
    
    screen = pygame.display.set_mode(size=(500, 500), flags=pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    menu = True
    ip = ''
    while menu:
        screenSize = screen.get_size()
        pygame.draw.rect(screen, utils.black, ((0, 0), screenSize))
        utils.TextInput('IP', ip, None, utils.white, screen, (100,100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.dict['key'] == pygame.K_RETURN:
                    menu = False
                elif event.dict['unicode'] in '1234567890.':
                    ip = utils.TextInput('IP', ip, event, utils.white, screen, (100,100))
                elif event.dict['key'] == pygame.K_BACKSPACE:
                    ip = ip[0:len(ip)-1]
        pygame.display.update()
        clock.tick(60)
    net = network.Network(ip)
    
    data = net.connect()
    circle = int(data[1])
    data = data.replace(',', ' ', 1)
    boardSizeY = int(data[4:data.index(',')])
    boardSizeX = int(data[data.index(',')+1:-1])
    print(f'Board Size: {boardSizeX} x {boardSizeY}')
    
    moves:list[tuple] = []
    
    while True:
        screenSize = screen.get_size()
        pygame.draw.rect(screen, utils.black, ((0, 0), screenSize))
    
        playerData = net.sendAndRecieveData((0,0), 2)
        
        if circle:
            center = utils.Coordinate(screenSize[0]/2, screenSize[1]/2)
            radius = min(screenSize)/2
            for ring in range(boardSizeY+1):
                pygame.draw.circle(screen, utils.white, center.xy, radius-ring*radius/(boardSizeY+1), width=1)
            for segment in range(int(boardSizeX)):
                point = utils.Coordinate(radius*math.cos(math.pi*2*segment/boardSizeX), radius*math.sin(math.pi*2*segment/boardSizeX))
                point2 = utils.Coordinate((radius/(boardSizeY+1))*math.cos(math.pi*2*segment/boardSizeX), (radius/(boardSizeY+1))*math.sin(math.pi*2*segment/boardSizeX))
                pygame.draw.line(screen, utils.white, (point+(center)).xy, (point2+center).xy, width=1)
            for move in moves:
                x = (radius*(move[0][1]-.5))/(boardSizeY+1)*math.cos((2*math.pi*(move[0][0]-1.5))/boardSizeX)
                y = (radius*(move[0][1]-.5))/(boardSizeY+1)*math.sin((2*math.pi*(move[0][0]-1.5))/boardSizeX)
                pygame.draw.circle(screen, utils.colors[move[1]], (utils.Coordinate(x,y)+center).xy, radius/(boardSizeY+1)/2.5, width=0)
        else:
            scale = screenSize[0] / boardSizeX
            for i in range(1, boardSizeX):
                pygame.draw.line(screen, utils.white, (i*screenSize[0]/boardSizeX, 0), (i*screenSize[0]/boardSizeX, screenSize[1]), width=1)
            for i in range(1, boardSizeY):
                pygame.draw.line(screen, utils.white, (0, i*screenSize[1]/boardSizeY), (screenSize[0], i*screenSize[1]/boardSizeY), width=1)
            for move in moves:
                mX = move[0][0] - 1
                mY = move[0][1] - 1
                x = scale * (mX + .5)
                y = scale * (mY + .5)
                pygame.draw.circle(screen, utils.colors[move[1]], (x, y), (min(screenSize)/boardSizeX)/2.5, width=0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.dict['pos']
                if circle:
                    x = mousePos[0] - center.x
                    y = (mousePos[1] - center.y)
                    seg = ((int(boardSizeX/(2*math.pi)*math.atan2(y, x))) % boardSizeX) + 1
                    rin = int((boardSizeY+1)*math.sqrt(x**2+y**2)/radius) + 1
                    if y > 0:
                        seg += 1 # I have no idea why
                    if rin != 1:
                        playerData = net.sendAndRecieveData((seg, rin), 2)
                else:
                    x = mousePos[0]
                    y = mousePos[1]
                    pX = int(x / scale) + 1
                    pY = int(y / scale) + 1
                    playerData = net.sendAndRecieveData((pX, pY), 2)
    
            elif event.type == pygame.KEYDOWN:
                key = event.dict['key']
                if key == pygame.K_BACKSPACE:
                    moves = []
        
        for playerNum, playerMove in enumerate(playerData[i] for i in range(playerData['NumPlayers'])):
            if sum(playerMove) != 0:
                moves.append((playerMove, playerNum))
    
        pygame.display.update()
        clock.tick(60)
