class GameImagesController < ApplicationController
  def new
  end

  def create
    digits = `python3 image_processing.py #{game_image_params.tempfile.path}`
    @matrix = Solver::Backtrack.new(digits.strip.split(',', 81)).call
    render 'games/new'
  end

  private

  def game_image_params
    params.require(:game_image)
  end
end
