class GamesController < ApplicationController
  def new
    @matrix = [nil] * 81
  end

  def create
    @matrix = Solver::Backtrack.new(game_params).call
    render :new
  end

  private

  def game_params
    params.require(:matrix)
  end
end
