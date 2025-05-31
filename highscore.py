import pygame
import json
import os

SCORES_FILE = "scores.json"
MAX_ENTRIES = 10

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def submit_score(name, score):
    scores = load_scores()
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    scores = scores[:MAX_ENTRIES]  # Keep only top N
    save_scores(scores)

def high_score_screen(screen, screen_width, background):
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 32)
    scores = load_scores()

    running = True
    while running:
        screen.blit(background, (0, 0))

        title = font.render("Leaderboard", True, (255, 255, 0))
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))

        for i, entry in enumerate(scores):
            text = small_font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, 120 + i * 40))

        exit_text = small_font.render("Press SPACE to return to Main Menu", True, (0, 255, 0))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, 520))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False
