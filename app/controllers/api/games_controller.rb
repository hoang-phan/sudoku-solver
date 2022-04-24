module Api
  class GamesController < ActionController::API
    def create
      @matrix = Solver::ImprovedHumanized.new(game_params).call || game_params
      render json: @matrix
    end

    private

    def game_params
      params.require(:matrix)
    end
  end
end