import game
import ui
import globals

def run_game():
    player_count = 0
    player_count = ui.ask("How many players are there?", ["1","2","3","4"])
    globals.difficulty = ui.ask("How difficult are the puzzles?", ["Normal","Hard"])
    if player_count == "_quit":
        exit()
    player_count = int(player_count)

    print("Player count is", player_count)

    if player_count > 1:
        results : list[game.Result] = []
        for i in range(player_count):
            ui.announce(["Player " + str(i + 1), "Start!"])
            results.append(game.play())
            if globals.returning_to_title:
                return
        announce_best_result(results)
    else:
        game.play()



def announce_best_result(results: list[game.Result]):
    survivors = [i for i, r in enumerate(results) if r.survived]
    if survivors:
        # Find the survivor with the shortest time
        best_idx = min(survivors, key=lambda i: results[i].time)
        ui.announce(["Player " + str(best_idx + 1), "solved the game fastest!"])
    else:
        # Find the player with the longest survival time
        best_idx = max(range(len(results)), key=lambda i: results[i].time)
        ui.announce(["Player " + str(best_idx + 1), "survived the longest!"])
