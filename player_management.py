import game

def run_game():
    result = game.play()
    if result.survived:
        print("Puzzle took: " + str(result.time) + " seconds")
    else:
        print("Survived for: " + str(result.time) + " seconds")

