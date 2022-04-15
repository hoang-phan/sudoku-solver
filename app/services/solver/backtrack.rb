module Solver
  class Backtrack
    attr_accessor :matrix

    MATRIX_SIZE = 9

    def initialize(matrix)
      @matrix = matrix.map(&:to_i)
    end

    def call
      time = Time.now.to_f
      result = solve(matrix)
      p "#{((Time.now.to_f - time) * 1000).round}ms"
      result
    end

    private

    def solve(matrix)
      return matrix if all_filled?(matrix)

      next_cell_index = matrix.index(&:zero?)

      (1..9).each do |number|
        next unless number_valid?(matrix, next_cell_index, number)

        new_matrix = matrix.dup
        new_matrix[next_cell_index] = number

        result_matrix = solve(new_matrix)
        return result_matrix if result_matrix.present?
      end

      nil
    end

    def all_filled?(matrix)
      matrix.all?(&:positive?)
    end

    def number_valid?(matrix, index, number)
      x = index / MATRIX_SIZE
      y = index % MATRIX_SIZE

      MATRIX_SIZE.times do |i|
        return false if matrix[i * MATRIX_SIZE + y] == number
        return false if matrix[x * MATRIX_SIZE + i] == number
      end

      xblock_start = x / 3 * 3
      yblock_start = y / 3 * 3

      (xblock_start..(xblock_start + 2)).each do |xi|
        (yblock_start..(yblock_start + 2)).each do |yi|
          return false if matrix[xi * MATRIX_SIZE + yi] == number
        end
      end

      true
    end

    def p_matrix(matrix)
      p "Matrix"
      matrix.each_slice(MATRIX_SIZE) do |slice|
        p slice.join(" ")
      end
    end
  end
end
