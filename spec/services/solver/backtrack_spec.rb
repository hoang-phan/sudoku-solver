require 'rails_helper'

RSpec.describe Solver::Backtrack do
  describe '#call' do
    YAML.load_file(Rails.root.join('spec/fixtures/tests.yml')).each_with_index do |data, i|
      context "with input ##{i}" do
        let(:input) { data['input'].split(',', 81) }
        let(:output) { described_class.new(input).call.join(',') }

        it "should be solved" do
          expect(output).to eq data['output']
        end
      end
    end
  end
end
