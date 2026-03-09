import game

def run_game():
    # TODO turn this into a menu where you can choose how many with buttons
    # 1, 2, 3, 4
    player_count = 0
    player_count = game.ask("How many players are there?", ["1","2","3","4"])
    if player_count == "_quit":
        exit()
    player_count = int(player_count)

    print("Player count is", player_count)

    result = game.play()
    if result.survived:
        print("Puzzle took: " + str(result.time) + " seconds")
    else:
        print("Survived for: " + str(result.time) + " seconds")



