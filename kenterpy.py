# SOFTWARE NAME IS KENTERPY
# SOFTWARE TYPE IS EMULATION
import pygame
import os
import importlib.util
import time
import tkinter as tk
from tkinter import filedialog
import shutil  # Import shutil to handle file copying

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KenterPy Emulator")

# Path to the custom font (assuming it's converted to .ttf)
font_path = "system/font/vga850.ttf"
font = pygame.font.Font(font_path, 24)  # Using the custom VGA font

# Load boot screen assets
logo_path = "system/logo.png"
logo = pygame.image.load(logo_path) if os.path.exists(logo_path) else None

def show_boot_screen():
    """Displays the boot screen with the logo and BIOS message."""
    start_time = time.time()
    while time.time() - start_time < 4:
        screen.fill((0, 0, 0))  # Black background
        
        # Display logo in center
        if logo:
            logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(logo, logo_rect)
        
        # Display BIOS message
        text_surface = font.render("Press F1 to open BIOS", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    open_bios()  # Call BIOS function
    
    # Clear the screen after boot screen
    screen.fill((0, 0, 0))
    pygame.display.flip()

def open_bios():
    """Function to display BIOS menu."""
    running = True
    while running:
        screen.fill((0, 0, 255))
        
        # Display BIOS text options
        text_surface = font.render("BIOS Menu", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(text_surface, text_rect)

        text_surface = font.render("-------------------------------------------------------------------------------------------------------------", True, (0, 100, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text_surface, text_rect)
        
        text_surface = font.render("1. Boot into Other OS", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        
        text_surface = font.render("2. Power Off", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(text_surface, text_rect)
        
        text_surface = font.render("3. Add Font", True, (255, 255, 255))  # New option to add font
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(text_surface, text_rect)

        text_surface = font.render("4. View Fonts", True, (255, 255, 255))  # New option to view fonts
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    boot_into_other_os()  # Call function to boot into another OS
                elif event.key == pygame.K_2:
                    pygame.quit()  # Power off the emulator
                    exit()
                elif event.key == pygame.K_3:
                    add_font()  # Call function to add a font
                elif event.key == pygame.K_4:
                    view_fonts()  # Call function to view available fonts

def boot_into_other_os():
    """Function to boot into another OS by selecting a folder or using default folder."""
    # Check if the mainos.txt file exists and read the directory if present
    mainos_file = "system/mainos.txt"
    os_folder = "os"

    if os.path.exists(mainos_file):
        with open(mainos_file, 'r') as file:
            os_dir = file.read().strip()
        
        # If the directory from mainos.txt is valid, boot into it
        if os.path.exists(os_dir) and os.path.isdir(os_dir):
            boot_script_path = os.path.join(os_dir, "boot.py")
            if os.path.exists(boot_script_path):
                # Load and run the boot.py from the directory stored in mainos.txt
                output_lines = load_boot_script(os_dir)  # Pass directory to load_boot_script
                run_script_in_window(output_lines)
            else:
                show_error_and_return_bios(f"KENTERPY: No operating systems found.")
        else:
            show_error_and_return_bios(f"KENTERPY: Invalid instruction in mainos.txt: '{os_dir}'")
    else:
        # If mainos.txt doesn't exist, boot from default 'os' folder
        output_lines = load_boot_script()  # Use the default loader
        run_script_in_window(output_lines)

def add_font():
    """Function to allow the user to select and add a font."""
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter root window
    
    # Open the file dialog to select a font file
    font_file = filedialog.askopenfilename(title="Select a Font File", filetypes=[("TrueType Fonts", "*.ttf")])
    
    if font_file:
        # Ensure the system font directory exists
        font_dir = "system/font"
        if not os.path.exists(font_dir):
            os.makedirs(font_dir)
        
        # Copy the selected font file to the font directory
        try:
            shutil.copy(font_file, font_dir)  # Use shutil.copy() to copy the font
            show_error_and_return_bios("Font added successfully.")
        except Exception as e:
            show_error_and_return_bios(f"Error adding font: {str(e)}")

def view_fonts():
    """Function to display the list of available fonts."""
    font_dir = "system/font"
    try:
        fonts = [f for f in os.listdir(font_dir) if f.endswith(".ttf")]
        if fonts:
            display_fonts(fonts)
        else:
            show_error_and_return_bios("No fonts available.")
    except Exception as e:
        show_error_and_return_bios(f"Error viewing fonts: {str(e)}")

def display_fonts(fonts):
    """Display the list of available fonts on the screen."""
    running = True
    while running:
        screen.fill((0, 0, 100))  # Black background
        
        # Display fonts
        y_offset = 50
        text_surface = font.render("View fonts", True, (255, 255, 255))  # New option to add font
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(text_surface, text_rect)

        text_surface = font.render("ESC to go back to menu.", True, (255, 255, 255))  # New option to add font
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
        screen.blit(text_surface, text_rect)
        for font_file in fonts:
            text_surface = font.render(font_file, True, (255, 255, 255))  # White text
            screen.blit(text_surface, (50, y_offset))
            y_offset += 30
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    open_bios()  # Return to BIOS menu when ESC is pressed

def show_error_and_return_bios(message):
    """Show error message for 5 seconds and then return to BIOS menu."""
    start_time = time.time()
    
    while time.time() - start_time < 5:
        screen.fill((0, 0, 0))  # Black background
        
        # Display error message
        text_surface = font.render(message, True, (255, 0, 0))  # Red text for errors
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
    
    open_bios()  # After 5 seconds, return to the BIOS menu

def load_boot_script(os_dir="os"):
    """Loads and runs boot.py inside the Pygame window."""
    script_path = os.path.join(os_dir, "boot.py")
    if not os.path.exists(script_path):
        return ["KENTERPY: No operating systems found."]
    
    try:
        spec = importlib.util.spec_from_file_location("boot_script", script_path)
        boot_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(boot_module)
        
        # Check if the script has a boot_main() function
        if hasattr(boot_module, "boot_main"):
            return boot_module.boot_main(screen, font)
        else:
            return ["KENTERPY: Kernel Panic!"]
    except Exception as e:
        return [f"Error: {e}"]

def run_script_in_window(output_lines):
    """Run and display the output from boot.py in the window."""
    running = True
    while running:
        screen.fill((0, 0, 0))  # Black background
        
        y_offset = 50
        for line in output_lines:
            text_surface = font.render(line, True, (0, 255, 0))  # Green text
            screen.blit(text_surface, (50, y_offset))
            y_offset += 30
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Execute the default OS loader if the user hasn't interacted with the BIOS
def execute_default_loader():
    """Try loading the OS by checking the mainos.txt or default folder."""
    if os.path.exists("system/mainos.txt"):
        boot_into_other_os()
    else:
        output_lines = load_boot_script()  # Default boot
        run_script_in_window(output_lines)

pygame.display.set_caption("KenterPy Emulator")

# Start the boot process, showing the boot screen
show_boot_screen()

# Start the default OS loading process
execute_default_loader()

pygame.quit()
