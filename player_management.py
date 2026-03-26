import game
import ui
import globals


def run_game():
    player_count = 0
    player_count = ui.ask("How many players are there?", ["1", "2", "3", "4"])
    globals.difficulty = ui.ask("How difficult are the puzzles?", ["Normal", "Hard", "Nightmare"])
    if player_count == "_quit":
        exit()
    player_count = int(player_count)

    globals.player_count = player_count

    if player_count == 1:
        game.play()
    else:
        results: list[game.Result] = []
        for i in range(player_count):
            ui.announce(["Player " + str(i + 1), "Start!"])
            results.append(game.play())
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
            time =  results[survivor].time
            if time < lowest_time:
                highest_time = time
                best_idx = survivor
            
        ui.announce(["Player " + str(best_idx + 1), "solved the game fastest!"])
    else:
        # Find the player with the longest survival time
        best_idx = 0 
        highest_time = -1
        for survivor in survivors:
            time =  results[survivor].time
            if time > highest_time:
                highest_time = time
                best_idx = survivor

        ui.announce(["Player " + str(best_idx + 1), "survived the longest!"])
