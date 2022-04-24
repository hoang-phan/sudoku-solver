Rails.application.routes.draw do
  root to: "games#new"
  resources :games, only: %i(new create)
  resources :game_images, only: %i(new create)

  namespace :api do
    resources :games, only: %i(create)
  end
end
