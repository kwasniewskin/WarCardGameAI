import customtkinter as ctk
from PIL import Image, ImageTk
from game_logic import Game
from custom_messagebox import show_custom_messagebox, show_custom_messagebox_with_retry
import sys

# Global variable to store user theme
userTheme = ""


def on_generate_cards(root, entry, loading_label):
    global userTheme
    userTheme = entry.get()
    if userTheme:
        # Display loading animation and text
        loading_label.configure(text="Generating required assets...")
        entry.configure(state="disabled")
        generate_button.configure(state="disabled")

        # Load assets and start the game
        root.after(100, load_assets_and_start_game, root, entry, loading_label)
    else:
        show_custom_messagebox(root, title="Input Required", message="Please enter a theme!")


def load_assets_and_start_game(root, entry, loading_label):
    try:
        game = Game(userTheme)  # Initialize game and load assets
        root.destroy()  # Close the input window
        main_game(game)  # Start the main game
    except Exception as e:
        show_custom_messagebox_with_retry(root, "Error", f"An error occurred while generating the game assets: {e}",
                                          lambda: retry_generate_cards(root, entry, loading_label), quit_program)


def retry_generate_cards(root, entry, loading_label):
    entry.configure(state="normal")
    generate_button.configure(state="normal")
    loading_label.configure(text="")
    entry.delete(0, ctk.END)  # Clear the entry field


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y - 20}")


def animate_card_flip(label, new_image, duration=500):
    def update_image(progress):
        if progress < 0.5:
            scale = 1 - 2 * progress
        else:
            label.configure(image=new_image)
            scale = 2 * progress - 1
        label.scale = scale
        label.update()
        if progress < 1:
            label.after(int(duration / 20), update_image, progress + 0.05)

    update_image(0)


def main_game(game):
    # Initialize main game window
    game_window = ctk.CTk()
    game_window.title("War Card Game")
    game_window.geometry("1600x960")

    # Center the main game window
    center_window(game_window, 1600, 960)

    # Load assets
    image_path = "assets/ui_elements/card_back.png"
    card_back_img = ctk.CTkImage(Image.open(image_path), size=(320, 480))

    # Main game frame
    game_frame = ctk.CTkFrame(game_window)
    game_frame.pack(fill="both", expand=True)

    for i in range(3):
        game_frame.columnconfigure(i, weight=1, minsize=100)
    for i in range(3):
        game_frame.rowconfigure(i, weight=1, minsize=100)

    round_label = ctk.CTkLabel(game_frame, text=f"Round: {game.round}", font=("Helvetica", 32), text_color="white")
    round_label.grid(row=0, column=1, sticky="n", padx=10, pady=(30, 0))

    alert_label = ctk.CTkLabel(game_frame, text=f"{game.alert}", font=("Helvetica", 32), text_color="white", width=300,
                               wraplength=280, anchor="center")
    alert_label.grid(row=1, column=1, sticky="ns", padx=10, pady=(20, 0))

    # Opponent frame
    opponent_frame = ctk.CTkFrame(game_frame, fg_color='transparent')
    opponent_frame.grid(row=0, column=0, sticky="s", pady=(20, 0))

    opponent_label = ctk.CTkLabel(opponent_frame, text="Opponent", font=("Helvetica", 32), text_color="white")
    opponent_label.pack(anchor="n")
    opponent_cards_left_label = ctk.CTkLabel(opponent_frame, text=f"Cards left: {game.opponent.deck.number_of_cards}",
                                             font=("Helvetica", 24),
                                             text_color="white")
    opponent_cards_left_label.pack(anchor="center")

    # Player frame
    player_frame = ctk.CTkFrame(game_frame, fg_color='transparent')
    player_frame.grid(row=0, column=2, sticky="s", pady=(20, 0))

    player_label = ctk.CTkLabel(player_frame, text="Player", font=("Helvetica", 32), text_color="white")
    player_label.pack(anchor="n")
    player_cards_left_label = ctk.CTkLabel(player_frame, text=f"Cards left: {game.player.deck.number_of_cards}",
                                           font=("Helvetica", 24),
                                           text_color="white")
    player_cards_left_label.pack(anchor="center")

    # Opponent card placement
    opponent_card_label = ctk.CTkLabel(game_frame, image=card_back_img, text='')
    opponent_card_label.grid(row=1, column=0, sticky="nsew", pady=0)

    # Frame for opponent card details
    opponent_card_frame = ctk.CTkFrame(game_frame, fg_color='transparent', width=200, height=150)
    opponent_card_frame.grid(row=2, column=0, sticky="nsew")

    opponent_card_name_label = ctk.CTkLabel(opponent_card_frame, text="", font=("Helvetica", 14, "bold"), width=180)
    opponent_card_name_label.pack(anchor="n")
    opponent_card_power_label = ctk.CTkLabel(opponent_card_frame, text="", font=("Helvetica", 14, "bold"), width=180)
    opponent_card_power_label.pack(anchor="n", pady=(10, 0))
    opponent_card_description_label = ctk.CTkLabel(opponent_card_frame, text="", font=("Helvetica", 12), wraplength=150,
                                                   width=180)
    opponent_card_description_label.pack(anchor="n", pady=(10, 0))

    # Player card placement
    player_card_label = ctk.CTkLabel(game_frame, image=card_back_img, text='')
    player_card_label.grid(row=1, column=2, sticky="nsew", pady=0)

    # Frame for player card details
    player_card_frame = ctk.CTkFrame(game_frame, fg_color='transparent', width=200, height=150)
    player_card_frame.grid(row=2, column=2, sticky="nsew")

    player_card_name_label = ctk.CTkLabel(player_card_frame, text="", font=("Helvetica", 14, "bold"), width=180)
    player_card_name_label.pack(anchor="n")
    player_card_power_label = ctk.CTkLabel(player_card_frame, text="", font=("Helvetica", 14, "bold"), width=180)
    player_card_power_label.pack(anchor="n", pady=(10, 0))
    player_card_description_label = ctk.CTkLabel(player_card_frame, text="", font=("Helvetica", 12), wraplength=150,
                                                 width=180)
    player_card_description_label.pack(anchor="n", pady=(10, 0))

    def next_round():
        nonlocal game
        game.play_round()

        try:
            # Player card image
            player_card_image_path = f"assets/card_images/{game.player.active_card.id}.png"
            player_card_image = ctk.CTkImage(Image.open(player_card_image_path), size=(320, 480))
            animate_card_flip(player_card_label, player_card_image)
            player_card_name_label.configure(text=f"Name: {game.player.active_card.name}",
                                             font=("Helvetica", 20, "bold"))
            player_card_power_label.configure(text=f"Power: {game.player.active_card.power}",
                                              font=("Helvetica", 20, "bold"))
            player_card_description_label.configure(text=f"{game.player.active_card.description}",
                                                    font=("Helvetica", 14), wraplength=250)

            # Opponent card image
            opponent_card_image_path = f"assets/card_images/{game.opponent.active_card.id}.png"
            opponent_card_image = ctk.CTkImage(Image.open(opponent_card_image_path), size=(320, 480))
            animate_card_flip(opponent_card_label, opponent_card_image)
            opponent_card_name_label.configure(text=f"Name: {game.opponent.active_card.name}",
                                               font=("Helvetica", 20, "bold"))
            opponent_card_power_label.configure(text=f"Power: {game.opponent.active_card.power}",
                                                font=("Helvetica", 20, "bold"))
            opponent_card_description_label.configure(text=f"{game.opponent.active_card.description}",
                                                      font=("Helvetica", 14), wraplength=250)
        except Exception as e:
            print(f"Error loading one of card images: {e}")

        round_label.configure(text=f"Round: {game.round}")
        alert_label.configure(text=f"{game.alert}")
        opponent_cards_left_label.configure(text=f"Cards left: {game.opponent.deck.number_of_cards}")
        player_cards_left_label.configure(text=f"Cards left: {game.player.deck.number_of_cards}")
        if game.winner:
            show_custom_messagebox(game_window, "Game Over",
                                   f"{'Opponent' if game.winner == 'Player' else 'Player'} has no cards left. {game.winner} WINS the game!")

    next_round_button = ctk.CTkButton(game_frame, text="Next Round", font=("Helvetica", 18), command=next_round,
                                      width=200, height=100)
    next_round_button.grid(row=2, column=1, sticky="n")

    game_window.mainloop()


def quit_program():
    sys.exit()


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

    loading_label = ctk.CTkLabel(root, text="", font=("Helvetica", 16), text_color="white")
    loading_label.pack(pady=(10, 10))

    global generate_button
    generate_button = ctk.CTkButton(root, text="GENERATE CARDS", font=("Helvetica", 18),
                                    command=lambda: on_generate_cards(root, entry, loading_label), width=350, height=30)
    generate_button.pack(pady=0)

    # Run the main application loop
    root.mainloop()


if __name__ == "__main__":
    main()
