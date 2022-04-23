require 'rails_helper'

RSpec.describe Solver::Backtrack do
  it_behaves_like "a solver", except: [3]
end
