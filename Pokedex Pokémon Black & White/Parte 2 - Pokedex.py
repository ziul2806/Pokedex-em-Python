import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import requests
import pygame

class PokedexApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Pokedex Pokémon: Black & White")
        self.root.geometry("1366x768")

        self.frame_pokedex = tk.Frame(root, width=1366, height=768)
        self.frame_pokedex.pack()

        pygame.init()
        pygame.mixer.music.load("música/Driftveil City [Pokémon_ Black & White].mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.load_pokedex_image("imagens/Pokedex1.png")
        self.create_search_widgets()

    def load_pokedex_image(self, image_path):
        for widget in self.frame_pokedex.winfo_children():
            widget.destroy()
        image_pokedex = tk.PhotoImage(file=image_path)
        label_pokedex = tk.Label(self.frame_pokedex, image=image_pokedex)
        label_pokedex.image = image_pokedex
        label_pokedex.pack()

    def create_search_widgets(self):

        self.button_search = tk.Button(self.frame_pokedex, text="Search", command=self.search_pokemon, font=("Arial Black", 12), bg="gray28", fg = "white", 
        activebackground="gray28", activeforeground ="white", borderwidth=0, width=8, height=0)
        self.button_search.place(x=613, y=565)

        self.label_instruction = tk.Label(self.frame_pokedex, text="Name or Number (1-649):", relief="flat", font=("Arial", 8))
        self.label_instruction.place(x=537, y=496)

        self.entry_pokedex = tk.Entry(self.frame_pokedex, font=("Arial", 8), borderwidth=0, bg="gray94", width=42)
        self.entry_pokedex.place(x=538, y=516)

    def search_pokemon(self):
        input_value = self.entry_pokedex.get().lower()
        if not input_value:
            self.display_not_found_message()
        elif input_value.isdigit() and 1 <= int(input_value) <= 649:
            pokemon_data = self.get_pokemon_info(int(input_value))
        else:
            pokemon_data = self.get_pokemon_info_by_name(input_value)
        
        if pokemon_data:
            self.load_pokedex_image("imagens/Pokedex2.png")
            self.show_pokemon_info(pokemon_data)
            self.label_instruction.destroy()
            self.entry_pokedex.destroy()
            self.button_search.destroy()
        else:
            self.display_not_found_message()

    def get_pokemon_info(self, pokemon_id):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
        if response.status_code == 200:
            return response.json()
        return None

    def get_pokemon_info_by_name(self, pokemon_name):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        if response.status_code == 200:
            return response.json()
        return None

    def display_not_found_message(self):
        self.label_info = tk.Label(self.frame_pokedex, text="Pokémon not found!", font=("Arial", 8))
        self.label_info.place(x=663, y=496)

    def show_pokemon_info(self, pokemon_data):

        # ID
        label_id = tk.Label(self.frame_pokedex, text=f"#{pokemon_data['id']}", font=("Cooper Black", 14), justify=tk.LEFT, bg="grey90", fg="gray60")
        label_id.place(x=370, y=247)

        # Name
        label_name = tk.Label(self.frame_pokedex, text=f"Name: {pokemon_data['name'].capitalize()}", font=("Cooper Black", 16), justify=tk.LEFT, bg="grey90", fg="gray60")
        label_name.place(x=408, y=449)

        # Status Base
        label_status = tk.Label(self.frame_pokedex, text=f"Base stats:", font=("Fixedsys", 10, "bold"), justify=tk.LEFT, bg="#003333", fg="white")
        label_status.place(x=850, y=283)

        label_hp = tk.Label(self.frame_pokedex, text=f"HP: {pokemon_data['stats'][0]['base_stat']}", font=("Fixedsys", 10), justify=tk.LEFT, bg="#003333", fg="khaki1")
        label_hp.place(x=790, y=305)

        label_attack = tk.Label(self.frame_pokedex, text=f"Attack: {pokemon_data['stats'][1]['base_stat']}", font=("Fixedsys", 10), justify=tk.LEFT, bg="#003333", fg="brown2")
        label_attack.place(x=790, y=325)

        label_defense = tk.Label(self.frame_pokedex, text=f"Defense: {pokemon_data['stats'][2]['base_stat']}", font=("Fixedsys", 10), justify=tk.LEFT, bg="#003333", 
        fg="medium turquoise")
        label_defense.place(x=790, y=345)

        label_special_attack = tk.Label(self.frame_pokedex, text=f"Special Attack: {pokemon_data['stats'][3]['base_stat']}", font=("Fixedsys", 10), justify=tk.LEFT, 
        bg="#003333", fg="hot pink")
        label_special_attack.place(x=790, y=365)

        label_special_defense = tk.Label(self.frame_pokedex, text=f"Special Defense: {pokemon_data['stats'][4]['base_stat']}", font=("Fixedsys", 10), justify=tk.LEFT, 
        bg="#003333", fg="spring green")
        label_special_defense.place(x=790, y=385)

        label_speed = tk.Label(self.frame_pokedex, text=f"Speed: {pokemon_data['stats'][5]['base_stat']}", font=("Fixedsys", 10), justify=tk.LEFT, bg="#003333", fg="purple1")
        label_speed.place(x=790, y=405)

        # Basic informations
        self.label_info = tk.Label(self.frame_pokedex, text=f"Basic informations:", font=("Fixedsys", 10, "bold"), justify=tk.LEFT, bg="#003333", fg="white")
        self.label_info.place(x=820, y=437)

        types = '/'.join([t['type']['name'].capitalize() for t in pokemon_data['types']])
        label_type = tk.Label(self.frame_pokedex, text=f"Type: {types}", font=("Fixedsys", 10), justify=tk.LEFT, bg="#003333", fg="ivory2")
        label_type.place(x=790, y=470)

        ability = pokemon_data['abilities'][0]['ability']['name'].capitalize()
        label_ability = tk.Label(self.frame_pokedex, text=f"Main ability: {ability}", font=("Fixedsys", 10), justify=tk.LEFT, bg="#003333", fg="ivory2")
        label_ability.place(x=790, y=490)

        self.load_pokemon_image(pokemon_data)

        # Botões para resetar e sair do programa
        self.button_return = tk.Button(self.frame_pokedex, text="Return", command=self.restart_program, font=("Arial Black", 17), bg="gold", fg="gray35",
        activebackground="gold", activeforeground="gray35", borderwidth=0, width=6, height=0)
        self.button_return.place(x=420, y=567)

        self.button_exit = tk.Button(self.frame_pokedex, text="Exit", command=self.root.destroy, font=("Arial Black", 12), bg="gold", fg="gray35",
        activebackground="gold", activeforeground="gray35", borderwidth=0, width=6, height=0)
        self.button_exit.place(x=782, y=225)

    def load_pokemon_image(self, pokemon_data):
        gif_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{pokemon_data['id']}.gif"
        response = requests.get(gif_url)
        if response.status_code == 200:
            gif_content = response.content
            with open("pokemon.gif", "wb") as f:
                f.write(gif_content)

            gif_frames = []
            for frame in ImageSequence.Iterator(Image.open("pokemon.gif")):
                frame = frame.resize((100, 100))
                gif_frames.append(ImageTk.PhotoImage(frame))

            self.label_pokemon_image = tk.Label(self.frame_pokedex, relief="flat", bg="#FADA77")
            self.label_pokemon_image.place(x=455, y=331)
            self.animate_gif(gif_frames, 0)

    def animate_gif(self, frames, index):
        self.label_pokemon_image.config(image=frames[index])
        self.label_pokemon_image.image = frames[index]
        self.root.after(100, self.animate_gif, frames, (index + 1) % len(frames))

    def restart_program(self):
        if hasattr(self, 'label_info'):
            self.label_info.destroy()
        self.label_pokemon_image.destroy()
        self.load_pokedex_image("imagens/Pokedex1.png")
        self.create_search_widgets()


root = tk.Tk()
app = PokedexApp(root)
root.mainloop()
