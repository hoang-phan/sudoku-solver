class GamesController < ApplicationController
  def new
    @matrix = [nil] * 81
  end

  def create
    @matrix = Solver::ImprovedHumanized.new(game_params).call
    render :new
  end

  private

  def game_params
    params.require(:matrix)
  end
end
