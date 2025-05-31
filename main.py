import pygame
from player import Player
from badguy import Badguy
from bullet import Bullet
import time  
import random
from highscore import high_score_screen, submit_score

from get_player_name import get_player_name

weapon_switch_cooldown = 0.3  # Cooldown time in seconds
last_switch_time = 0


pygame.init()
pygame.mixer.init()



# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load images
background = pygame.image.load("./images/background.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Load and scale images
player_img = pygame.image.load("./images/battleship.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (64, 64))  # Set your desired size

badguy1_img = pygame.image.load("./images/badguy1.png").convert_alpha()
badguy1_img = pygame.transform.scale(badguy1_img, (64, 64))  # Set your desired size

badguy2_img = pygame.image.load("./images/badguy2.png").convert_alpha()
badguy2_img = pygame.transform.scale(badguy2_img, (64, 64))  # Set your desired size

boss_img = pygame.image.load("./images/boss.png").convert_alpha()
boss_img = pygame.transform.scale(boss_img, (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 10))  # Set your desired size

basic_bullet_img = pygame.image.load("./images/blackbullet.png").convert_alpha()
basic_bullet_img = pygame.transform.scale(basic_bullet_img, (16, 16))  # Customize as needed

heavy_bullet_img = pygame.image.load("./images/fatBullet.png").convert_alpha()
heavy_bullet_img = pygame.transform.scale(heavy_bullet_img, (16, 16))  # Customize as needed

sharp_bullet_img = pygame.image.load("./images/sharpBullet.png").convert_alpha()
sharp_bullet_img = pygame.transform.scale(sharp_bullet_img, (16, 16))  # Customize as needed


basic_sound = pygame.mixer.Sound("music/basic.wav")
heavy_sound = pygame.mixer.Sound("music/fire-sound.wav")
sharp_sound = pygame.mixer.Sound("music/sniper.wav")
impact_sound = pygame.mixer.Sound("music/impact.mp3")
die_sound = pygame.mixer.Sound("music/enemy-die.wav")
basic_sound.set_volume(0.5)
heavy_sound.set_volume(0.5)
sharp_sound.set_volume(0.5)
impact_sound.set_volume(0.5)
die_sound.set_volume(0.5)



bullets = {
    "basic": {"image": basic_bullet_img, "speed": 50, "damage": 1, "sound": basic_sound},
    "heavy": {"image": heavy_bullet_img, "speed": 15, "damage": 3, "sound": heavy_sound},
    "sharp": {"image": sharp_bullet_img, "speed": 100, "damage": 2, "sound": sharp_sound}
}

badguys_library = {
    "tie": {"image": badguy1_img, "speed": 1.5, "hp": 2},
    "tie2": {"image": badguy2_img, "speed": 4, "hp": 4},
    "boss": {"image": boss_img, "speed": 0, "hp": 100},
}
selected_bullet = bullets["basic"]

# Sprite groups
bullet_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
badguys = pygame.sprite.Group()

# Player setup
player = Player(player_img, SCREEN_WIDTH/2, SCREEN_HEIGHT - 50, bullet_group, selected_bullet["image"])
all_sprites.add(player)
badguy1 = Badguy(badguy1_img, SCREEN_WIDTH/2, 50, badguys_library['tie']['speed'], badguys_library['tie']['hp'], "tie")
badguy2 = Badguy(badguy2_img, SCREEN_WIDTH/2, 50, badguys_library['tie2']['speed'], badguys_library['tie2']['hp'], "tie2")
boss = Badguy(boss_img, SCREEN_WIDTH/2, 50, badguys_library['boss']['speed'], badguys_library['boss']['hp'], "boss")

all_sprites.add(badguy1)
badguys.add(badguy1)
all_sprites.add(badguy2)
badguys.add(badguy2)
all_sprites.add(boss)
badguys.add(boss)

running = True
main_menu = True
gaming = False
leaderboard = False

while running:
    if main_menu:
        # MAIN MENU LOOP
        pygame.mixer.music.load("music/menu.mp3")
        pygame.mixer.music.play(-1)
        while main_menu:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            title_font = pygame.font.Font(None, 80)
            menu_font = pygame.font.Font(None, 48)
            control_font = pygame.font.Font(None, 32)

            # Title
            title = title_font.render("RETRO BLASTER", True, (255, 100, 100))
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            # Start prompt
            start_text = menu_font.render("Press SPACE to Start", True, (0, 255, 0))
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 200))

            # Controls
            controls = [
                "Left / Right Arrow or A / D to Move",
                "Space Bar to Fire",
                "Shift to Switch Weapon"
            ]
            for i, text in enumerate(controls):
                control_text = control_font.render(text, True, (200, 200, 200))
                screen.blit(control_text, (SCREEN_WIDTH // 2 - control_text.get_width() // 2, 300 + i * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    main_menu = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    main_menu = False
                    gaming = True
                    #pygame.mixer.music.stop()


    elif gaming:
        # RESET EVERYTHING
        bullet_group.empty()
        badguys.empty()
        all_sprites.empty()

        player = Player(player_img, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, bullet_group, selected_bullet["image"])
        all_sprites.add(player)

        score = 0
        kills = 0
        boss_spawned = False
        last_switch_time = time.time()

        # Spawn initial enemies
        all_sprites.add(badguy1)
        badguys.add(badguy1)
        all_sprites.add(badguy2)
        badguys.add(badguy2)

        pygame.mixer.music.load("music/gameplay.mp3")
        pygame.mixer.music.play(-1)
        while gaming:
            screen.blit(background, (0, 0))

            # Input Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gaming = False

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                player.rect.x -= 3
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                player.rect.x += 3
            if key[pygame.K_SPACE]:
                selected_bullet["sound"].play()
                player.fire(selected_bullet["speed"], selected_bullet["damage"])
            player.rect.x = max(0, min(player.rect.x, SCREEN_WIDTH - player.rect.width))

            current_time = time.time()
            if key[pygame.K_LSHIFT] and current_time - last_switch_time > weapon_switch_cooldown:
                # Rotate weapon
                if selected_bullet == bullets["sharp"]:
                    selected_bullet = bullets["basic"]
                elif selected_bullet == bullets["basic"]:
                    selected_bullet = bullets["heavy"]
                elif selected_bullet == bullets["heavy"]:
                    selected_bullet = bullets["sharp"]
                player.bullet_img = selected_bullet["image"]
                last_switch_time = current_time

            # Update and Draw
            all_sprites.update()
            bullet_group.update()

            # Track badguys that were killed
            to_remove = []
            to_spawn = []

            for bullet in bullet_group:
                hit_list = pygame.sprite.spritecollide(bullet, badguys, False)
                for enemy in hit_list:
                    impact_sound.play()
                    enemy.take_damage(bullet.damage)
                    bullet.kill()
                    # Inside bullet collision logic:
                    if enemy.hp <= 0 and not getattr(enemy, "dead", False):
                        die_sound.play()
                        enemy.dead = True
                        score += 10
                        kills += 1
                        to_remove.append(enemy)
                        
                        # Spawn 2 clones of the same type
                        if enemy.type_key and enemy.type_key in badguys_library:
                            if enemy.type_key is "boss":
                                score += 2000

                            else:  
                                bg_data = badguys_library[enemy.type_key]
                                for _ in range(2):
                                    clone = Badguy(
                                        bg_data["image"],
                                        random.randint(50, SCREEN_WIDTH - 40),
                                        0,
                                        bg_data["speed"],
                                        bg_data["hp"],
                                        type_key=enemy.type_key
                                    )
                                    to_spawn.append(clone)
                                


            # Now remove dead enemies
            for enemy in to_remove:
                badguys.remove(enemy)
                all_sprites.remove(enemy)

            # Now add new clones
            for clone in to_spawn:
                badguys.add(clone)
                all_sprites.add(clone)



            # Spawn boss after 100 kills (only once)
            if kills >= 100 and not boss_spawned:
                boss_data = badguys_library['boss']
                boss = Badguy(
                    boss_data["image"],
                    SCREEN_WIDTH - boss_data["image"].get_width() // 2,  # Center horizontally
                    -boss_data["image"].get_height(),  # Start fully off-screen above
                    boss_data["speed"],
                    boss_data["hp"],
                    "boss"
                )
                all_sprites.add(boss)
                badguys.add(boss)

                boss_spawned = True

            # Collision: Enemy touches player OR bottom of screen
            for badguy in badguys:
                badguy.movePattern(SCREEN_WIDTH)
                if badguy.rect.bottom >= SCREEN_HEIGHT or badguy.rect.colliderect(player.rect):
                    die_sound.play()
                    gaming = False
                    leaderboard = True

            # Draw Order
            screen.blit(background, (0, 0))
            bullet_group.draw(screen)
            all_sprites.draw(screen)

            # Score Display
            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))

            pygame.display.flip()
            clock.tick(60)


    elif leaderboard:
        # LEADERBOARD LOOP
        
        leaderboard_running = True
        
        while leaderboard_running:
            player_name = get_player_name(screen, SCREEN_WIDTH, background)
            submit_score(player_name, score)
            high_score_screen(screen, SCREEN_WIDTH, background)
            leaderboard_running = False

        pygame.display.flip()
        clock.tick(60)
        leaderboard = False
        
        main_menu = True

    



                    
