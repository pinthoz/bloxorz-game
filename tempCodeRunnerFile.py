if gameObj.falling:
                        temp_surface = pygame.Surface((400, 275), pygame.SRCALPHA)  # Crie uma superfície temporária com suporte a transparência
                        for f in range(0, 200, 20):
                            draw_block_on_temp_surface(x, y, temp_surface, box_component, f)  # Desenhe o bloco na superfície temporária
                            screen.blit(background, (0, 0))
                            screen.blit(pygame.transform.scale(display, (400 * 1.8, 275 * 1.8)), (60, 120))
                            screen.blit(pygame.transform.scale(temp_surface, (400 * 1.8, 275 * 1.8)), (60, 120))  # Desenhe a superfície temporária na tela
                            pygame.display.update()
                            pygame.time.delay(50)  # Adicione um atraso para tornar a animação mais suave