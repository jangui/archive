#include "Game.h"

class GameObject {
public:
  GameObject(const char* texturesheet, int x, int y);
  ~GameObject();

  void Update();
  void Render();

private:
  int xpos;
  int ypos;
  SDL_Texture* objTexture;
  SDL_Rect srcRect, dstRect;
  SDL_Renderer* renderer;

};
