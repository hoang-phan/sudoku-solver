# Sudoku Solver

Ruby on Rails webapp, API and plugin to solve basic Sudoku

## Description

This projects are shipped with 3 functionalities:

- Ability to solve a sudoku in a webapp using 3 different algorithms
	- Backtrack
	- Humanized
	- Humanized with fail fast

## Getting Started

### Dependencies

Ruby 3, Rails 7, Python 3, pip3, Ubuntu (preferred) or MacOS

### Installing

Clone this repository

```sh
https://github.com/hoang-phan/sudoku-solver.git
```

Install Ruby on Rails gems

```sh
cd sudoku-solver && bundle
```

Install apt packages:

```sh
xargs -a Aptfile sudo apt-get install
```

Install pip packages:

```sh
pip3 install -r requirements.txt
```

### Executing program

Create database
```sh
bundle exec rails db:create
```

Run server
```sh
bundle exec rails server
```

To install sudoku.net plugin, install [Tampermonkey](https://www.tampermonkey.net/) and copy script-sudoku-net.js to a new script

## Authors

Hoang Phan
[@hoang-phan](https://github.com/hoang-phan)

## Acknowledgments

* [OpenCV-Sudoku-Solver](https://github.com/murtazahassan/OpenCV-Sudoku-Solver)