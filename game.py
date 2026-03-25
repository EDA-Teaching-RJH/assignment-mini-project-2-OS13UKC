import random
import re
import csv
import os

class Fighter:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

class Player(Fighter):                          # player inherits from fighter class for the healing and moves
    def __init__(self, name):
        super().__init__(name, 100)
        self.heals = 3

    def heal(self):
        if self.heals > 0:
            self.hp += 40
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.heals -= 1
            return True
        return False

    def attack(self, enemy, move):              # move name, damage and miss chance
        moves = {
            "1": ("Punch", 15, 0.1),
            "2": ("Kick", 30, 0.4),
            "3": ("Gun", 60, 0.7)
        }
        if move not in moves:                   # ensures correct move is inputted
            return "invalid"
        
        name, dmg, miss_chance = moves[move]            # logic for missing a move
        if random.random() > miss_chance:
            enemy.take_damage(dmg)
            return f"You landed a {name} for {dmg} damage!"
        return f"{name} missed!"

class Enemy(Fighter):
    def __init__(self, name, hp):
        super().__init__(name, hp)

    def enemy_turn(self, player):           
        moves = [
            ("Slap", 15, 0.1),
            ("Sweeping kick", 30, 0.4),
            ("Laser", 60, 0.7)
        ]
        move = random.choice(moves)
        name, dmg, miss_chance = move
        if random.random() > miss_chance:
            player.take_damage(dmg)
            return f"{self.name} hit you with a {name} for {dmg} damage!"
        return f"{self.name}'s {name} missed!"

def validate_login(name):
    pattern = r"^[a-zA-Z0-9]{3}$"                   # only allows 3 characters
    return bool(re.fullmatch(pattern, name))

def login_system():
    name = input("enter a 3 character tag")
    while not validate_login(name):
        name = input("tag needs to be exactly 3 letters or numbers. Try again")
    print(f"Alright {name}, lets go")
    return name

def save_score(name, waves_cleared):                    # checks if file exists and updates with new score if better
    filename = "leaderboard.csv"
    scores = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            reader = csv.reader(file)
            scores = list(reader)
    
    updated = False
    for row in scores:
        if row[0] == name:
            if waves_cleared > int(row[1]):
                row[1] = str(waves_cleared)
            updated = True
            break
    
    if not updated:
        scores.append([name, str(waves_cleared)])
        
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(scores)

def show_leaderboard():                             # displays leaderboard even if there is a no one on it yet
    filename = "leaderboard.csv"
    if not os.path.exists(filename):
        print("\nNo one's on the board yet.")
        return
        
    print("\n--- The Big Leagues ---")
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"{row[0]}: {row[1]} waves cleared")

def play_game(player_name):
    player = Player(player_name)
    wave = 1
    enemy_names = ["Thug", "Bouncer", "Rogue", "Ninja"]
    
    while player.is_alive():                                # allows for infinite waves
        print(f"\n--- Wave {wave} ---")
        enemy_name = random.choice(enemy_names)
        enemy_hp = 30 + (wave * 15)                         # health scales with wave number
        enemy = Enemy(enemy_name, enemy_hp)
        
        print(f"{enemy.name} approaches!")
        
        while player.is_alive() and enemy.is_alive():                       # allows for combat to continue until either person dies
            print(f"\nYou: {player.hp}HP | {enemy.name}: {enemy.hp}HP")
            print("1: Punch (Low Risk / Low Dmg)")
            print("2: Kick (Med Risk / Med Dmg)")
            print("3: Gun (High Risk / High Dmg)")
            print(f"4: heal up ({player.heals} left)")
            
            choice = input("choose your move. ")
            
            if choice in ["1", "2", "3"]:
                result = player.attack(enemy, choice)
                print(result)
            elif choice == "4":
                if player.heal():
                    print("You healed yourself")
                else:
                    print("You're completely out of heals!")
                    continue
            else:
                print("That's not a move. Try again.")
                continue
                
            if enemy.is_alive():
                print(enemy.enemy_turn(player))
                
        if player.is_alive():
            print(f"\nYou knocked out the {enemy.name}!")
            wave += 1
            
    print(f"\n Game over. You survived {wave - 1} waves.")
    save_score(player_name, wave - 1)
    show_leaderboard()

if __name__ == "__main__":
    name = login_system()
    play_game(name)