from kivy.app import App
from Presentation.Widgets.TurtleGameWidget import TurtleGameWidget
from Domain.Grid import Grid
from kivy.core.window import Window

class TurtleApp(App):
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

        turtleGame = TurtleGameWidget(grid, grid.gridWidth, grid.gridHeight, (5, 0), (2, 2))
        return turtleGame

if __name__ == '__main__':
    Window.fullscreen = 'auto' 
    TurtleApp().run()