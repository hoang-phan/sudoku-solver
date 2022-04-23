module Solver
  class ImprovedHumanized
    attr_accessor :matrix, :pool

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
      prepare_pool
      recursive_solve(matrix, pool)
    end

    def recursive_solve(matrix, pool)
      while true
        result = next_deterministic_fillable(pool)
        break if result.blank?

        value, index = result
        matrix, pool = fill_matrix(matrix, index, value, pool)
      end

      return matrix if all_filled?(matrix)

      while true
        index = next_fillable(matrix)
        return nil if index.blank?

        els = pool[index]
        return nil if els.blank?

        new_matrix = matrix.dup
        new_pool = pool.dup
        new_matrix, new_pool = fill_matrix(new_matrix, index, els[0], new_pool)
        
        result = recursive_solve(new_matrix, new_pool)
        return result if result

        pool[index] -= [els[0]]
      end
    end

    def prepare_pool
      @pool = matrix.map { (1..9).to_a }
      matrix.each_with_index do |value, index|
        @matrix, @pool = fill_matrix(matrix, index, value, pool)
      end
    end

    def next_deterministic_fillable(pool)
      result = next_unique_value(pool)
      return result if result

      9.times do |i|
        row_indexes = 9.times.map { |y| i * 9 + y }
        result = next_unique_index(pool, row_indexes)
        return result if result

        col_indexes = 9.times.map { |x| x * 9 + i }
        result = next_unique_index(pool, col_indexes)
        return result if result
      end

      3.times do |x_block|
        3.times do |y_block|
          square_indexes = 3.times.flat_map do |xi|
            x = x_block * 3 + xi

            3.times.map do |yi|
              y = y_block * 3 + yi
              x * 9 + y
            end
          end
          result = next_unique_index(pool, square_indexes)
          return result if result
        end
      end

      nil
    end

    def next_unique_value(pool)
      pool.each_with_index do |els, index|
        return [els[0], index] if els.count == 1
      end

      nil
    end

    def next_unique_index(pool, indexes)
      pool_h = {}

      indexes.each do |index|
        pool[index].each do |el|
          pool_h[el] ||= []
          pool_h[el] << index
        end
      end

      pool_h.each do |el, ins|
        return [el, ins[0]] if ins.count == 1
      end

      nil
    end

    def next_fillable(matrix)
      matrix.each_with_index do |value, index|
        return index if value == 0
      end
    end

    def fill_matrix(matrix, index, value, pool)
      return [matrix, pool] if value == 0

      matrix[index] = value
      pool[index] = []

      x = index / MATRIX_SIZE
      y = index % MATRIX_SIZE

      9.times do |i|
        pool[i * MATRIX_SIZE + y] -= [value]
        pool[x * MATRIX_SIZE + i] -= [value]
      end

      xblock_start = x / 3 * 3
      yblock_start = y / 3 * 3

      (xblock_start..(xblock_start + 2)).each do |xi|
        (yblock_start..(yblock_start + 2)).each do |yi|
          pool[xi * MATRIX_SIZE + yi] -= [value]
        end
      end

      [matrix, pool]
    end

    def all_filled?(matrix)
      matrix.all?(&:positive?)
    end

    def p_matrix(matrix)
      p "Matrix"
      matrix.each_slice(MATRIX_SIZE) do |slice|
        p slice.join(" ")
      end
    end

    def p_pool(pool)
      p "Pool"
      pool.each_slice(MATRIX_SIZE) do |slice|
        row = slice.map do |els|
          els.join.rjust(9)
        end
        p row.join(" ")
      end
    end
  end
end
