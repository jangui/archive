all: main.o game.o textureManager.o GameObject.o
	g++ main.o Game.o TextureManager.o GameObject.o -o bomb_hotel -w -lSDL2 -lSDL2_image

main.o: main.cpp
	g++ -c main.cpp

game.o: Game.cpp Game.h
	g++ -c Game.cpp

textureManager.o: TextureManager.cpp TextureManager.h
	g++ -c TextureManager.cpp

gameobject.o: GameObject.cpp GameObject.h
	g++ -c GameObject.cpp

clean:
	rm -f bomb_hotel main.o Game.o TextureManager.o GameObject.o
