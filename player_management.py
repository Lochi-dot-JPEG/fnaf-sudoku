import game

def run_game():
    # TODO turn this into a menu where you can choose how many with buttons
    # 1, 2, 3, 4
    player_count = 0
    valid_player_count = False
    while not valid_player_count:
        try:
            player_count = int(input("How many players are there?"))
        except:
            print("Enter a valid integer")
            continue
        valid_player_count = True

    print("Player count is", player_count)

    result = game.play()
    if result.survived:
        print("Puzzle took: " + str(result.time) + " seconds")
    else:
        print("Survived for: " + str(result.time) + " seconds")



