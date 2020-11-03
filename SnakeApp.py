from kivy.app import App
from Presentation.Widgets.SnakeGameWidget import SnakeGameWidget
from Domain.Grid import Grid, GridPosition
from kivy.clock import Clock

class SnakeApp(App):
    def build(self):
        grid = Grid(11, 11, 
            [[0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
             [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
             [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
             [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1]]
        )

        snakeGame = SnakeGameWidget(grid, grid.gridWidth, grid.gridHeight, (5, 0), (2, 2))

        return snakeGame

if __name__ == '__main__':
    SnakeApp().run()