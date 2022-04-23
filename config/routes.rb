Rails.application.routes.draw do
  resources :games, only: %i(new create)
  resources :game_images, only: %i(new create)
end
