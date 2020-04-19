import players as p
import time

def main():
    player = p.Player(None, 5)
    while True:
        player.getHand()
        player.getDealerCard()
        player.evalHand()
        player.display()
        player.evalBet()
        player.reset()
main()
