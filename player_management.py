import game
import ui
import globals
import pygame


def run_game():
    # Ask how many players there are, then convert the string result into an integer
    player_count = int(ui.ask("How many players are there?", ["1", "2", "3", "4"]))
    globals.player_count = player_count

    # Ask the player what difficulty to play on
    globals.difficulty = ui.ask(
        "How difficult are the puzzles?", ["Normal", "Hard", "Nightmare"]
    )

    if player_count == 1:
        # Play one round if it is singleplayer
        game.play()
    else:
        # Play multiple rounds for mulitplayer and announce a winner
        results: list[game.Result] = []
        for i in range(player_count):
            # Add one to the index because it starts counting from zero
            ui.announce(["Player " + str(i + 1), "Start!"])
            results.append(game.play())

            # Exit this loop if the player has selected to return to title within the last round
            if globals.returning_to_title:
                return
        announce_best_result(results)


def announce_best_result(results: list[game.Result]):
    survivors = [i for i, r in enumerate(results) if r.survived]
    if survivors:
        # Find the survivor with the shortest time
        best_idx = 0
        lowest_time = globals.max_time + 1
        for survivor in survivors:
            time = results[survivor].time
            if time < lowest_time:
                highest_time = time
                best_idx = survivor

        ui.announce(["Player " + str(best_idx + 1), "solved the game fastest!"])
    else:
        # Find the player with the longest survival time
        best_idx = 0
        highest_time = -1
        for survivor in survivors:
            time = results[survivor].time
            if time > highest_time:
                highest_time = time
                best_idx = survivor

        ui.announce(["Player " + str(best_idx + 1), "survived the longest!"])
