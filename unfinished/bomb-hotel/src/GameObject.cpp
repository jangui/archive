#include "GameObject.h"
#include "TextureManager.h"

GameObject::GameObject(const char* texturesheet, int x, int y) {
  objTexture = TextureManager::LoadTexture(texturesheet);
  xpos = x;
  ypos = y;
}

GameObject::~GameObject() {}

void GameObject::Update() {

  xpos++;
  ypos++;

 srcRect.h = 46;
 srcRect.w = 32;
 srcRect.x = 0;
 srcRect.y = 0;

 dstRect.x = xpos;
 dstRect.y = ypos;
 dstRect.w = srcRect.w * 2;
 dstRect.h = srcRect.h * 2;
}

void GameObject::Render() {
  SDL_RenderCopy(Game::renderer, objTexture, &srcRect, &dstRect);

}
