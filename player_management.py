import game
import ui

def run_game():
    # TODO turn this into a menu where you can choose how many with buttons
    # 1, 2, 3, 4
    player_count = 0
    player_count = ui.ask("How many players are there?", ["1","2","3","4"])
    if player_count == "_quit":
        exit()
    player_count = int(player_count)

    print("Player count is", player_count)

    if player_count > 1:
        results = []
        for i in range(player_count):
            ui.announce(["Player " + str(i + 1), "Start!"])
            results.append(game.play())

    else:
        game.play()
