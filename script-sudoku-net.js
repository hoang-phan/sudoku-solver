// ==UserScript==
// @name         Sudoku.net
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://www.sudoku.net/*
// @grant        none
// ==/UserScript==

var cellSelector = ".sudoku-cell > span";
var buttonContainer = ".game-options";

(function() {
  'use strict';

  var solve = function() {
    var xmlhttp = new XMLHttpRequest();
    var container = document.querySelector('.table-striped tbody');
    var cells = document.querySelectorAll(cellSelector);
    var cellData = Array.from(cells).map(function(el) {
      return el.innerHTML;
    });
    xmlhttp.open("POST", "https://hoang-sudoku-solver.herokuapp.com/api/games");
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.onload = function() {
      var grid = angular.element(document.querySelector("body")).scope().sudokuGrid[0];

      JSON.parse(xmlhttp.response).forEach(function(value, i) {
        var x = Math.floor(i / 9);
        var y = i % 9;
        if (!grid[x][y]) {
          grid[x][y] = value + "!";
          cells[i].innerHTML = value;
        }
      });
    };
    xmlhttp.send(JSON.stringify({ matrix: cellData }));
  }

  var appendButton = function() {
    if (document.querySelector(buttonContainer)) {
      var solveButton = document.createElement("BUTTON");
      var text = document.createTextNode('Solve');
      solveButton.appendChild(text);
      solveButton.style.color = 'red';
      solveButton.onclick = solve;
      document.querySelector(buttonContainer).appendChild(solveButton);
    } else {
      setTimeout(appendButton, 1000);
    }
  }

  setTimeout(appendButton, 4000);
})();
