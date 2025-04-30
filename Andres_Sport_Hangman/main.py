# From Andres Sandoval
import pygame
import math
import random
import os

# ✅ Print current working directory (for debugging)
print("Current Working Directory:", os.getcwd())

# ✅ Ensure the script runs from the correct directory
expected_directory = "/Users/andyman/Desktop/Hangman 3"
if os.getcwd() != expected_directory:
    print(f"❗ Warning: Python is running in {os.getcwd()}, not {expected_directory}")
    print("🔄 Changing to the correct directory...")
    try:
        os.chdir(expected_directory)  # Change to the correct folder
        print("✅ Successfully changed to:", os.getcwd())
    except Exception as e:
        print(f"❌ Error: {e}")

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sports Hangman Game!")

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
TOPIC_FONT = pygame.font.SysFont('comicsans', 35)

# ✅ Load images & Move them lower
image_folder = "images"
full_image_folder_path = os.path.join(os.getcwd(), image_folder)
print(f"🔍 Looking for images in: {full_image_folder_path}")

images = []
for i in range(7):
    image_path = os.path.join(image_folder, f"hangman{i}.png")
    print(f"Checking for image: {image_path}")

    if os.path.exists(image_path):
        images.append(pygame.image.load(image_path))
        print(f"✅ Loaded {image_path} successfully!")
    else:
        print(f"❌ Error: Image file '{image_path}' not found!")

# game variables
hangman_status = 0

# Sports-themed word categories
words_dict = {
    "BASKETBALL": ["DRIBBLE", "DUNK", "LAYUP", "REBOUND", "JUMPSHOT", "COURT", "ASSIST"],
    "SOCCER": ["GOAL", "PENALTY", "FREEKICK", "OFFSIDE", "MIDFIELDER", "HEADER", "REFEREE"],
    "BASEBALL": ["HOMERUN", "PITCHER", "INFIELD", "OUTFIELD", "BATTER", "STRIKE", "UMPIRE"],
    "FOOTBALL": ["TOUCHDOWN", "QUARTERBACK", "FIELDGOAL", "TACKLE", "INTERCEPTION", "BLITZ", "FUMBLE"],
    "TENNIS": ["SERVE", "VOLLEY", "FOREHAND", "BACKHAND", "DEUCE", "RACKET", "ADVANTAGE"]
}

# Select a random topic and word
current_topic = random.choice(list(words_dict.keys()))
word = random.choice(words_dict[current_topic])
guessed = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw():
    win.fill(WHITE)

    # draw title
    text = TITLE_FONT.render("SPORTS HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    
    # draw topic (remains at the top)
    topic_text = TOPIC_FONT.render(f"Topic: {current_topic}", 1, BLACK)
    win.blit(topic_text, (WIDTH/2 - topic_text.get_width()/2, 90))

    # ✅ Move hangman images lower to avoid overlap
    win.blit(images[hangman_status], (150, 150))  # Lowered Y-position from 100 to 150

    # ✅ Ensure the word fits within the screen & move it to the right
    display_word = " ".join([letter if letter in guessed else "_" for letter in word])

    # Adjust font size dynamically if word is long
    if len(word) > 8:
        word_font = pygame.font.SysFont('comicsans', 50)  # Smaller font for long words
    else:
        word_font = WORD_FONT  # Default font

    text = word_font.render(display_word, 1, BLACK)

    # ✅ Move word display slightly to the right
    text_x = WIDTH/2 - text.get_width()/2 + 100  # Added +100 to shift right
    win.blit(text, (text_x, 300))  # Lowered to prevent cutting off

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    
    # Show the correct word if player lost
    if message == "You LOST!":
        correct_word = TOPIC_FONT.render(f"The word was: {word}", 1, BLACK)
        win.blit(correct_word, (WIDTH/2 - correct_word.get_width()/2, HEIGHT/2 + 50))
    
    pygame.display.update()
    pygame.time.delay(3000)

def reset_game():
    global hangman_status, word, guessed, current_topic
    hangman_status = 0
    guessed = []
    
    # Select a new random topic and word
    current_topic = random.choice(list(words_dict.keys()))
    word = random.choice(words_dict[current_topic])
    
    # Reset all letter buttons to visible
    for letter in letters:
        letter[3] = True

def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        
        if won:
            display_message("You WON!")
            reset_game()
            return
        
        if hangman_status == 6:
            display_message("You LOST!")
            reset_game()
            return
    
# Start game loop
while True:
    main()
