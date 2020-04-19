#include "Game.h"
#include "TextureManager.h"
#include "GameObject.h"

GameObject *player;
GameObject *player2;

SDL_Renderer *Game::renderer = nullptr;

Game::Game() {
    return;
}

Game::~Game() {
    return;
}

void Game::init(const char *title, int xpos, int ypos, int width, int height, bool fullscreen) {
  int flags = 0;
  if (fullscreen) {
    flags = SDL_WINDOW_FULLSCREEN;
  }

  if (SDL_Init(SDL_INIT_EVERYTHING) == 0) {
    std::cout << "Subsystems initialized!" << std::endl;

    window = SDL_CreateWindow(title, xpos, ypos, width, height, flags);
    if (window) {
      std::cout << "Window Created!" << std::endl;
    }

    renderer = SDL_CreateRenderer(window, -1, 0);
    if (renderer) {
      SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
      std::cout << "Renderer Created!" << std::endl;
    }
    isRunning = true;
  } else {
    isRunning = false;
  }

  player = new GameObject("../assets/player.png", 0, 0);
  player2 = new GameObject("../assets/player2.png", 50, 50);
}

void Game::render() {
  SDL_RenderClear(renderer);

  player->Render();
  player2->Render();

  SDL_RenderPresent(renderer);
}

void Game::update() {
  cnt++;
  player->Update();  
  player2->Update();
}

void Game::handleEvents() {
  SDL_Event event;
  SDL_PollEvent(&event);
  switch (event.type) {
    case SDL_QUIT:
      isRunning = false;
      break;
    default:
      break;
  }
}

void Game::clean() {
  SDL_DestroyWindow(window);
  SDL_DestroyRenderer(renderer);
  SDL_Quit();
  std::cout << "Game Cleaned!" << std::endl;
}
