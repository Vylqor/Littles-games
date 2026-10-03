import random
import os

SIZE = 7
START = (0, 0)
EXIT = (SIZE - 1, SIZE - 1)
LIVES = 3

player = START
has_key = False
visited = {START}

# Place la clé, les pièges et les trésors
available_cells = [
    (x, y)
    for y in range(SIZE)
    for x in range(SIZE)
    if (x, y) not in (START, EXIT)
]

random.shuffle(available_cells)
key = available_cells.pop()
traps = set(available_cells[:6])
treasures = set(available_cells[6:10])


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_map():
    print("\n   " + " ".join(str(x) for x in range(SIZE)))

    for y in range(SIZE):
        row = []

        for x in range(SIZE):
            cell = (x, y)

            if cell == player:
                symbol = "P"
            elif cell == EXIT:
                symbol = "E"
            elif cell not in visited:
                symbol = "?"
            elif cell == key and not has_key:
                symbol = "K"
            else:
                symbol = "."

            row.append(symbol)

        print(f"{y}  " + "  ".join(row))


def nearby_message():
    x, y = player  # Récupère la position du joueur

    nearby_traps = sum(
        (x + dx, y + dy) in traps
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
    )

    if nearby_traps:
        print("Tu sens un danger à proximité...")


def get_move():
    controls = {
        "w": (0, -1),
        "s": (0, 1),
        "a": (-1, 0),
        "d": (1, 0),
    }

    while True:
        command = input(
            "\nDéplacement avec W/A/S/D, ou Q pour quitter : "
        ).lower()

        if command == "q":
            return None

        if command in controls:
            return controls[command]

        print("Commande invalide. Utilise W, A, S, D ou Q.")


print("=== LE DONJON PERDU ===")
print("Trouve la clé, récupère les trésors et atteins la sortie.")
print("La carte se dévoile au fur et à mesure de ton exploration.")
print("Commandes : W = haut, A = gauche, S = bas, D = droite")

while LIVES > 0:
    show_map()
    print(f"\nVies : {LIVES} | Clé : {'oui' if has_key else 'non'}")
    nearby_message()

    move = get_move()

    if move is None:
        print("Tu as quitté le donjon.")
        break

    dx, dy = move
    x, y = player
    new_position = (x + dx, y + dy)

    if not (0 <= new_position[0] < SIZE and 0 <= new_position[1] < SIZE):
        print("Un mur bloque le passage !")
        continue

    player = new_position
    visited.add(player)

    if player in traps:
        traps.remove(player)
        LIVES -= 1
        print("Tu as marché sur un piège ! Tu perds une vie.")

    elif player in treasures:
        treasures.remove(player)
        print("Tu as trouvé un trésor ! ✨")

    elif player == key and not has_key:
        has_key = True
        print("Tu as trouvé la clé ! 🔑")

    elif player == EXIT:
        if has_key:
            print("\nTu as ouvert la sortie et échappé au donjon ! Bravo ! 🎉")
            break
        print("La sortie est verrouillée. Trouve d’abord la clé !")

if LIVES == 0:
    print("\nTu n’as plus de vies. Le donjon a gagné !")
