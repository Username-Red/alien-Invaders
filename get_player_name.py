import pygame

def get_player_name(screen, screen_width, background):
    font = pygame.font.Font(None, 48)
    name = ""
    entering = True

    while entering:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        prompt = font.render("Enter Your Name:", True, (255, 255, 255))
        name_text = font.render(name + "|", True, (0, 255, 0))
        screen.blit(prompt, (screen_width // 2 - prompt.get_width() // 2, 200))
        screen.blit(name_text, (screen_width // 2 - name_text.get_width() // 2, 260))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                entering = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode
    return name
