import pygame
import time
from datetime import datetime

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Set resolution (required for Pygame)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 120, 215)
RED = (255, 0, 0)

# Define desktop icons
icons = {
    "Shutdown": pygame.Rect(50, 50, 80, 80),
    "Calculator": pygame.Rect(150, 50, 80, 80),
    "Notepad": pygame.Rect(250, 50, 80, 80)
}

def draw_desktop():
    """Draws the desktop with icons and clock"""
    font = pygame.font.Font(None, 24)
    screen.fill(GRAY)
    
    for name, rect in icons.items():
        pygame.draw.rect(screen, BLUE, rect)
        text_surface = font.render(name, True, WHITE)
        screen.blit(text_surface, (rect.x + 10, rect.y + 30))
    
    # Draw clock
    time_text = datetime.now().strftime("%H:%M:%S")
    clock_surface = font.render(time_text, True, WHITE)
    screen.blit(clock_surface, (700, 10))  # Placed near the right side
    
    pygame.display.flip()

def draw_close_button():
    """Draw a custom close button"""
    font = pygame.font.Font(None, 32)
    close_button_rect = pygame.Rect(750, 10, 40, 30)
    pygame.draw.rect(screen, RED, close_button_rect)
    text_surface = font.render("X", True, WHITE)
    screen.blit(text_surface, (close_button_rect.x + 10, close_button_rect.y + 5))
    return close_button_rect

def calculator():
    """Simple built-in calculator"""
    font = pygame.font.Font(None, 32)
    input_text = ""
    running = True
    while running:
        screen.fill(WHITE)
        text_surface = font.render("Calculator", True, BLACK)
        screen.blit(text_surface, (50, 50))
        text_surface = font.render("-------------------------------------------------------------------", True, BLUE)
        screen.blit(text_surface, (50, 70))
        text_surface = font.render("" + input_text, True, BLACK)
        screen.blit(text_surface, (50, 100))
        
        close_button = draw_close_button()
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if close_button.collidepoint(event.pos):
                    return  # Close the calculator when close button is clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        input_text = str(eval(input_text))  # Compute expression
                    except:
                        input_text = "Error!"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Delete last character
                elif event.key == pygame.K_ESCAPE:
                    return  # Exit calculator
                else:
                    input_text += event.unicode  # Add typed character

def shutdown():
    """Simple built-in calculator"""
    font = pygame.font.Font(None, 32)
    input_text = ""
    running = True
    while running:
        screen.fill(WHITE)
        text_surface = font.render("Shutting down", True, BLACK)
        screen.blit(text_surface, (50, 50))
        text_surface = font.render("-------------------------------------------------------------------", True, BLUE)
        screen.blit(text_surface, (50, 70))
        text_surface = font.render("KenterPy OS is shutting down...", True, BLACK)
        screen.blit(text_surface, (50, 100))

        pygame.display.flip()

        pygame.time.delay(5000)  # Simulate loading delay
        pygame.quit
        exit()

def notepad():
    """Simple built-in notepad"""
    font = pygame.font.Font(None, 24)
    text = []
    running = True
    while running:
        screen.fill(WHITE)
        text_surface = font.render("Notepad", True, BLACK)
        screen.blit(text_surface, (50, 50))
        text_surface = font.render("-------------------------------------------------------------------", True, BLUE)
        screen.blit(text_surface, (50, 70))
        y_offset = 100
        for line in text:
            screen.blit(font.render(line, True, BLACK), (50, y_offset))
            y_offset += 30
        
        close_button = draw_close_button()
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if close_button.collidepoint(event.pos):
                    return  # Close the notepad when close button is clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    text.append("")  # New line
                elif event.key == pygame.K_BACKSPACE and text:
                    if text[-1]:  # Remove character from last line
                        text[-1] = text[-1][:-1]
                    elif len(text) > 1:  # Remove empty line
                        text.pop()
                elif event.key == pygame.K_ESCAPE:
                    return  # Exit notepad
                else:
                    if not text:
                        text.append("")
                    text[-1] += event.unicode  # Append typed character

def boot_main():
    """Boot script execution function"""
    font = pygame.font.Font(None, 24)
    messages = [
        "KenterPy OS Booting...",
        "Initializing system...",
        "Starting shell...",
        "Welcome to KenterPy OS!"
    ]
    
    screen.fill(BLACK)
    y_offset = 100
    for message in messages:
        text_surface = font.render(message, True, (0, 255, 255))  # Cyan text
        screen.blit(text_surface, (50, y_offset))
        pygame.display.flip()
        pygame.time.delay(500)  # Simulate loading delay
        y_offset += 30

    pygame.time.delay(1000)
    main()  # Start desktop

def main():
    running = True
    clock = pygame.time.Clock()
    while running:
        draw_desktop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for name, rect in icons.items():
                    if rect.collidepoint(mouse_pos):
                        if name == "Calculator":
                            calculator()
                        elif name == "Notepad":
                            notepad()
                        elif name == "Shutdown":
                            shutdown()
        
        clock.tick(30)

    pygame.quit()
boot_main()
