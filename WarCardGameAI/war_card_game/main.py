import customtkinter as ctk
from PIL import Image, ImageTk
from game_logic import Game
from custom_messagebox import show_custom_messagebox

# Global variable to store user theme
userTheme = ""


def on_generate_cards(root, entry):
    global userTheme
    userTheme = entry.get()
    if userTheme:
        root.destroy()  # Close the input window
    else:
        show_custom_messagebox(root, title="Input Required", message="Please enter a theme!")


def main_game(user_theme):
    game = Game(user_theme)

    # Initialize main game window
    game_window = ctk.CTk()
    game_window.title("War Card Game")
    game_window.geometry("1600x960")

    # Center the main game window
    center_window(game_window, 1600, 960)

    # Load assets
    image_path = "assets/ui_elements/card_back.png"
    card_back_img = ctk.CTkImage(Image.open(image_path), size=(150, 250))

    # Main game frame
    game_frame = ctk.CTkFrame(game_window)
    game_frame.pack(fill="both", expand=True)

    # Configure the grid to be equal size and not change width
    for i in range(5):
        game_frame.columnconfigure(i, weight=1, minsize=100)
    for i in range(3):
        game_frame.rowconfigure(i, weight=1, minsize=100)

    round_label = ctk.CTkLabel(game_frame, text=f"Round: {game.round}", font=("Helvetica", 24), text_color="white")
    round_label.grid(row=0, column=1, sticky="n", padx=10, pady=(20, 0))

    alert_label = ctk.CTkLabel(game_frame, text=f"{game.alert}", font=("Helvetica", 24), text_color="white", width=300, wraplength=280, anchor="center")
    alert_label.grid(row=0, column=3, sticky="n", padx=10, pady=(20, 0))

    opponent_deck_label = ctk.CTkLabel(game_frame, image=card_back_img, text='')
    opponent_deck_label.grid(row=0, column=2, sticky="nsew", pady=0)

    player_deck_label = ctk.CTkLabel(game_frame, image=card_back_img, text='')
    player_deck_label.grid(row=2, column=2, sticky="nsew", pady=0)

    opponent_card_label = ctk.CTkLabel(game_frame, image=card_back_img, text='')
    opponent_card_label.grid(row=1, column=1, sticky="nsew", padx=0)

    player_card_label = ctk.CTkLabel(game_frame, image=card_back_img, text='')
    player_card_label.grid(row=1, column=3, sticky="nsew", padx=0)

    def next_round():
        nonlocal game
        game.play_round()

        try:
            player_card_image_path = f"assets/card_images/{game.player.active_card.id}.png"
            player_card_image = ctk.CTkImage(Image.open(player_card_image_path), size=(150, 250))
            player_card_label.configure(image=player_card_image)
            player_card_name_label.configure(text=f"Name: {game.player.active_card.name}",
                                             font=("Helvetica", 14, "bold"))
            player_card_power_label.configure(text=f"Power: {game.player.active_card.power}",
                                              font=("Helvetica", 14, "bold"))
            player_card_description_label.configure(text=f"{game.player.active_card.description}",
                                                    font=("Helvetica", 12), wraplength=150)
        except Exception as e:
            print(f"Error loading player card image: {e}")

        try:
            opponent_card_image_path = f"assets/card_images/{game.opponent.active_card.id}.png"
            opponent_card_image = ctk.CTkImage(Image.open(opponent_card_image_path), size=(150, 250))
            opponent_card_label.configure(image=opponent_card_image)
            opponent_card_name_label.configure(text=f"Name: {game.opponent.active_card.name}",
                                               font=("Helvetica", 14, "bold"))
            opponent_card_power_label.configure(text=f"Power: {game.opponent.active_card.power}",
                                                font=("Helvetica", 14, "bold"))
            opponent_card_description_label.configure(text=f"{game.opponent.active_card.description}",
                                                      font=("Helvetica", 12), wraplength=150)
        except Exception as e:
            print(f"Error loading opponent card image: {e}")

        round_label.configure(text=f"Round: {game.round}")
        alert_label.configure(text=f"{game.alert}")
        if game.winner:
            show_custom_messagebox(game_window, "Game Over",
                                   f"{'Player' if game.winner == 'Player' else 'Opponent'} has no cards left. {game.winner} WINS the game!")

    # Create a frame for player card details
    player_card_frame = ctk.CTkFrame(game_frame, fg_color='transparent', width=200, height=150)
    player_card_frame.grid(row=1, column=4, sticky="nsew")

    player_card_name_label = ctk.CTkLabel(player_card_frame, text="", font=("Helvetica", 14, "bold"), width=180)
    player_card_name_label.pack(anchor="n")
    player_card_power_label = ctk.CTkLabel(player_card_frame, text="", font=("Helvetica", 14, "bold"), width=180)
    player_card_power_label.pack(anchor="n", pady=(10, 0))
    player_card_description_label = ctk.CTkLabel(player_card_frame, text="", font=("Helvetica", 12), wraplength=150,
                                                 width=180)
    player_card_description_label.pack(anchor="n", pady=(10, 0))

    # Create a frame for opponent card details
    opponent_card_frame = ctk.CTkFrame(game_frame, fg_color='transparent', width=200, height=150)
    opponent_card_frame.grid(row=1, column=0, sticky="nsew")

    opponent_card_name_label = ctk.CTkLabel(opponent_card_frame, text="", font=("Helvetica", 14, "bold"), width=180)
    opponent_card_name_label.pack(anchor="n")
    opponent_card_power_label = ctk.CTkLabel(opponent_card_frame, text="", font=("Helvetica", 14, "bold"), width=180)
    opponent_card_power_label.pack(anchor="n", pady=(10, 0))
    opponent_card_description_label = ctk.CTkLabel(opponent_card_frame, text="", font=("Helvetica", 12), wraplength=150,
                                                   width=180)
    opponent_card_description_label.pack(anchor="n", pady=(10, 0))

    next_round_button = ctk.CTkButton(game_frame, text="Next Round", font=("Helvetica", 18), command=next_round,
                                      width=200, height=100)
    next_round_button.grid(row=2, column=4, sticky="n")

    game_window.mainloop()


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y - 20}")


def main():
    global userTheme

    # Initialize main application window
    root = ctk.CTk()
    root.title("War Card Game")
    root.geometry("1000x800")

    # Center the main application window
    center_window(root, 1000, 800)

    # Create and configure widgets
    welcome_label = ctk.CTkLabel(root, text="Select theme of your game!", font=("Helvetica", 32), text_color="white")
    welcome_label.pack(pady=(200, 10))

    example_label = ctk.CTkLabel(root, text="For example: Harry Potter, Dragons, Witcher, Apocalypse and so on!",
                                 font=("Helvetica", 16), text_color="white")
    example_label.pack(pady=(0, 10))

    entry = ctk.CTkEntry(root, font=("Helvetica", 18), width=350, height=40)
    entry.pack(pady=(10, 10))

    generate_button = ctk.CTkButton(root, text="GENERATE CARDS", font=("Helvetica", 18),
                                    command=lambda: on_generate_cards(root, entry), width=350, height=30)
    generate_button.pack(pady=0)

    # Run the main application loop
    root.mainloop()

    # Check if a theme was entered and start the game
    if userTheme:
        main_game(userTheme)


if __name__ == "__main__":
    main()
