import pygame, sys
from settings import WIDTH, HEIGHT
from level import Level
from items import Carrot
from explosion import Explosion

# Pygame setup
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font("assets/fonts/prstart.ttf", 20)
pygame.display.set_caption("Bombs & Carrots!")
clock = pygame.time.Clock()

# Game setup
level = Level(WIN)
explosionList = [[],[]]

# Game UI
FONT_SCORE = pygame.font.Font("assets/fonts/prstart.ttf", 20)
carrot_icon = pygame.transform.scale(pygame.image.load("assets/ui/icon_carrot.png"), (48, 48))
player_1_icon = pygame.transform.scale(pygame.image.load("assets/ui/icon_player1.png"), (48, 48))
player_2_icon = pygame.transform.scale(pygame.image.load("assets/ui/icon_player2.png"), (48, 48))

# Events
def events():
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 

            for player in level.player_obj:
                if player.bombing == True:
                    
                    # Verify bug of having more than 1 bomb
                    if len(player.bombs) > 1:
                        player.bombs.pop(0)

                    # Get Bomb Position
                    x = player.bombs[0].rect.x - 30
                    y = player.bombs[0].rect.y - 30
                    id = int(player.id)-1

                    # Create Explosion
                    explosion = Explosion((x, y))
                    explosionList[id].append(explosion)
                    
                    # Destroy bomb
                    level.player_obj[id].bombs.clear()
                    level.player_obj[id].bombing = False

                    # Get the bomb area
                    destruction_area = pygame.Rect(explosion.rect)
                    destruction_area.width -= 20
                    destruction_area.height -= 20
                    destruction_area.x += 20
                    destruction_area.y += 20

                    # Destroy Boxes
                    for box in level.boxes.sprites():
                        if destruction_area.colliderect(box.rect):
                            box.kill()

            pygame.time.set_timer(pygame.USEREVENT, 0)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# Main Menu Fase
def main_menu():

    # Variables
    menu = True
    play_text_y = HEIGHT-200
    text_speed = 0.7

    # Create UI
    play_text = FONT.render("Press left click to Start!", True, 'white')
    logo = pygame.transform.scale(pygame.image.load("assets/ui/logo.png"), (344, 152))

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Text Movement
        if (play_text_y < HEIGHT-215 or play_text_y > HEIGHT-185):
            text_speed *= -1
        play_text_y -= text_speed

        # Display UI
        WIN.blit(logo, (WIDTH/2 - logo.get_width()/2 , 50))
        WIN.blit(play_text, (WIDTH/2-play_text.get_width()/2, play_text_y))

        # Close UI
        if pygame.mouse.get_pressed()[0]:
            menu = False

        pygame.display.update()
        clock.tick(60)
        WIN.fill('black')


# Setup Game Fase
def setup_game_menu():

    # Variables
    game_start = False 
    level.pre_run()
    carrot_count = 0
    player_color = (141, 176, 36)

    # Create UI
    text_0 = FONT.render("Player " + str(carrot_count+1), True, player_color)
    text_1 = FONT.render("         select a box and hide your Carrot!", True, 'white')

    while not game_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        text_0 = FONT.render("Player " + str(carrot_count+1), True, player_color)
        WIN.blit(text_1, (WIDTH/2-text_1.get_width()/2, 30))
        WIN.blit(text_0, (WIDTH/2-text_1.get_width()/2, 30))

        for box in level.boxes.sprites():
            if pygame.mouse.get_pressed()[0] and box.rect.collidepoint(pygame.mouse.get_pos()):
                #box.kill()
                carrot = Carrot((box.rect.x, box.rect.y), carrot_count)
                level.insert_carrot(carrot)
                carrot_count += 1
                player_color = (66, 117, 216)
                level.pre_run()
                pygame.time.delay(300)
                if carrot_count == 2:
                    game_start = True

        pygame.display.update()
        clock.tick(60)


# Main Game
def game_ui():
    
    score = [0,0]
    for player in level.player_obj:
        score[int(player.id)-1] = FONT_SCORE.render("x" + str(player.points), True, 'black')

    WIN.blit(player_1_icon, (10, 10))
    WIN.blit(carrot_icon, (50, 10))
    WIN.blit(score[0], (90, 20 + score[0].get_height()/2))

    WIN.blit(player_2_icon, (WIDTH - 50, 10))
    WIN.blit(carrot_icon, (WIDTH - 90, 10))
    WIN.blit(score[1], (WIDTH - 90 - score[1].get_width(), 20 + score[1].get_height()/2))


def main():

    # First Menus
    main_menu()
    pygame.time.delay(300)
    setup_game_menu()

    # Game Loop
    while True:
        events()
        
        level.run()

        # Draw the explosions
        if len(explosionList[0]) > 0:
            for explosion in explosionList[0]:
                explosion.update(0.25)
                WIN.blit(explosion.image, explosion.rect)

        if len(explosionList[1]) > 0:
            for explosion in explosionList[1]:
                explosion.update(0.25)
                WIN.blit(explosion.image, explosion.rect)

        # Draw the in game UI
        game_ui()

        # Check if its needed to reset the level
        if len(level.carrots) < 2:
            level.reset_level()
            setup_game_menu()

        pygame.display.update()
        clock.tick(60)



if __name__ == "__main__":
    main()