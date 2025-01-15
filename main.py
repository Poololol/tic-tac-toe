import asyncio
async def main():
    
    #import micropip
    #await micropip.install("pygame-ce")
    import generic_tictactoe_client as client
    import generic_tictactoe_server as server
    import pygame

    # Set Pygame's rendering to webgl
    import os
    os.environ["SDL_RENDER_DRIVER"] = "webgl"
    print(f"Changed mode to webgl: {os.environ["SDL_RENDER_DRIVER"]}")
    os.environ["SDL_VIDEO_X11_WMCLASS"] = "pygame-ce"
    print(f"Gave render control to Pygame: {os.environ["SDL_VIDEO_X11_WMCLASS"]}")
    canvas_id = 'pygame-canvas'
    os.environ["SDL_WINDOWID"] = f"#{canvas_id}"
    print(f"Changed Pygame window to canvas: {os.environ["SDL_WINDOWID"]}")
        
    # Initialize pygame separately
    pygame.init()
    print("Initialized Pygame")
    
    screen = pygame.display.set_mode((500, 500))
    print("Screen Inited w/o opengl")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    
    def TextInput(name: str, text: str, event: pygame.event.Event | None, color: pygame.Color, surface: pygame.Surface, pos):
        font = pygame.font.Font(None, int(surface.get_size()[0]/10))
        texty = font.render(f'{name}: ', True, color)
        surface.blit(texty, pos)
        if event:
            key = event.__dict__['unicode']
            text += key
        texty2 = font.render(text, True, color)
        surface.blit(texty2, (pos[0]+texty.get_width(), pos[1]))
        return text
    
    while True:
        pygame.draw.rect(screen, 0, (0, 0, 500, 500), width=0)
        bC = pygame.draw.rect(screen, 32467, (0, 0, 500, 250), width=0)
        bS = pygame.draw.rect(screen, 35247, (0, 250, 500, 250), width=0)
        text = font.render('Client', True, 16**6-1)
        screen.blit(text, (200, 100))
        text = font.render('Server', True, 16**6-1)
        screen.blit(text, (200, 350))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.dict['pos'][1] >= 250:
                    menu = True
                    ip = ''
                    while menu:
                        screenSize = screen.get_size()
                        pygame.draw.rect(screen, 0, ((0, 0), screenSize))
                        TextInput('IP', ip, None, 16**6-1, screen, (100,100))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.dict['key'] == pygame.K_RETURN:
                                    menu = False
                                elif event.dict['unicode'] in '1234567890.':
                                    ip = TextInput('IP', ip, event, 16**6-1, screen, (100,100))
                                elif event.dict['key'] == pygame.K_BACKSPACE:
                                    ip = ip[0:len(ip)-1]
                        pygame.display.update()
                        clock.tick(60)
                    pygame.display.quit()
                    asyncio.run(server.main2(ip))
                else:
                    asyncio.run(client.main1())
        pygame.display.update()
        clock.tick(60)

asyncio.ensure_future(main())
