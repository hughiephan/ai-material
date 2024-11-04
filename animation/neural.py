from manim import *

class RNNStructure(Scene):
    def construct(self):
        squares = VGroup(*[Square(side_length=0.4, color=ORANGE) for _ in range(4)]).arrange(RIGHT, buff=0.5)
        self.play(Write(squares), run_time=2)
        
        lines = VGroup(*[Line(squares[i].get_right(), squares[i+1].get_left()) for i in range(len(squares)-1)])
        self.play(Write(lines), run_time=2)