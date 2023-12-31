import random
import time
import os
import sys
from enemy import A, B, C
from maze_generator import MazeGenerator, print_maze, move_player
from dialogues import Dialogues, get_player_name

player_stats = {'health': 100, 'attack': 10, 'defense': 5}

def karate_chop(enemy):
    damage = player_stats['attack'] + random.randint(1, 5)
    enemy.take_damage(damage)
    print(f"You used Karate Chop and dealt {damage} damage!")


def run_away():
    print("You ran away from the enemy.")
    return True  # Indicate that the player successfully ran away


def print_enemy_stats(enemy):
    if enemy.health > 0:
        print(f"Enemy Stats - Health: {enemy.health}, Attack: {enemy.attack}, Defense: {enemy.defense}")



def handle_enemy_encounter():
    enemy_type = random.choice([A(), B(), C()])
    Dialogues.enemy_encounter()

    print(f"You encountered {enemy_type.name}!")
    print_enemy_stats(enemy_type)

    while enemy_type.is_alive() and player_stats['health'] > 0:
        print(f"Your Health: {player_stats['health']}")
        print(f"{enemy_type.name}'s Health: {enemy_type.health}")
        print("Choose your move:")
        print("1. Attack")
        print("2. Karate Chop")
        print("3. Run Away")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            player_attack = max(0, player_stats['attack'] + random.randint(-2, 2))
            enemy_type.take_damage(player_attack)
            print(f"You attacked and dealt {player_attack} damage to {enemy_type.name}!")

        elif choice == "2":
            karate_chop(enemy_type)
        elif choice == "3":
            if run_away():
                break
        else:
            print("Invalid choice. You hesitated and the enemy took advantage!")
            enemy_attack = max(0, enemy_type.attack + random.randint(-2, 2))
            player_stats['health'] -= max(0, enemy_attack - player_stats['defense'])
            print(f"{enemy_type.name} attacked and dealt {enemy_attack} damage!")

        print_enemy_stats(enemy_type)  # Display enemy stats after the player's move

        if enemy_type.is_alive():
            enemy_attack = max(0, enemy_type.attack + random.randint(-2, 2))
            player_stats['health'] -= max(0, enemy_attack - player_stats['defense'])
            print(f"{enemy_type.name} attacked and dealt {enemy_attack} damage!")

    if player_stats['health'] <= 0:
        print("You were defeated. Game over.")
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again == "yes":
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    # Check if the enemy's health reached 0
    if not enemy_type.is_alive():
        print(f"You defeated {enemy_type.name}! The enemy is dead.")

    return True

def print_ending_dialogue():
    Dialogues.dialogue_6()
    time.sleep(5)

    Dialogues.dialogue_7()
    time.sleep(5)
    print("Congratulations! You reached the exit!")
    print("Thank you for playing. Exiting the game...")

def main():
    maze_size = 9

    # Opening dialogue
    Dialogues.start_menu()
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        print("Starting the game...")
        time.sleep(2)
        player_name = get_player_name()
        time.sleep(1)
        print(f"\nHello, {player_name}! Let's start the game.")
        time.sleep(3)
        Dialogues.dialogue_0()
        time.sleep(5)
    elif choice == "2":
        Dialogues.credits()
        return
    elif choice == "3":
        print("Exiting the game...")
        return
    else:
        print("Invalid choice. Exiting the game...")
        return

    while True:
        maze_generator = MazeGenerator(maze_size, maze_size)
        maze_generator.generate_maze()
        current_position = maze_generator.get_start_position()
        checkpoint_positions = maze_generator.get_checkpoint_positions()
        player_stats = {'health': 100, 'attack': 10, 'defense': 5}

        while True:
            print_maze(current_position, maze_generator.get_maze())

            # Check if the current position is a checkpoint with the value 3
            if maze_generator.get_maze()[current_position[0]][current_position[1]] == 3:
                 Dialogues.checkpoint_reached()

            move = input("Enter move (W/A/S/D): ").lower()
            if move in {'w', 'a', 's', 'd'}:
                current_position = move_player(current_position, move, maze_generator.get_maze())

                # Check if the player reached a checkpoint
                if current_position in maze_generator.get_checkpoint_positions():
                    Dialogues.checkpoint_reached()
                    maze_generator.get_maze()[current_position[0]][current_position[1]] = ' '  # Remove the checkpoint

                # Check for a random enemy encounter
                if random.random() < 0.4:
                    if not handle_enemy_encounter():
                        continue  # If the player failed to run away, continue the loop

            else:
                print("Invalid move! Use W/A/S/D.")
                continue

            if maze_generator.get_maze()[current_position[0]][current_position[1]] == 1:
                print("Invalid move! You cannot move through walls.")
                continue

            if current_position == (maze_size - 1, maze_size - 1):
                print_ending_dialogue()
                return  # Exit the game when the player reaches the exit
            
            if current_position == (maze_size - 2, maze_size - 1):
                Dialogues.dialogue_6()
                time.sleep(5)
                Dialogues.checkpoint_reached()
                handle_enemy_encounter()
                return  # Exit the game when the player reaches the exit
            
            if current_position == (maze_size - 6, maze_size - 7):
                Dialogues.dialogue_1()
                time.sleep(5)
                Dialogues.dialogue_2()
                time.sleep(5)
                Dialogues.dialogue_3()
                time.sleep(5)
                Dialogues.dialogue_4()
                time.sleep(5)
                Dialogues.dialogue_5()
                time.sleep(5)
                continue

if __name__ == "__main__":
    main()
