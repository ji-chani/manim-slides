from manim import *
from manim_slides import Slide
import numpy as np

config.background_color = WHITE
config.media_embed = True

# %%manim_slides -v WARNING --progress_bar None TeachingDemo --manim-slides controls=true
class TeachingDemo(Slide):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Font sizes
        self.TITLE_FONT_SIZE = 48
        self.CONTENT_FONT_SIZE = 0.7 * self.TITLE_FONT_SIZE
        self.SUBTITLE_FONT_SIZE = 0.5 * self.TITLE_FONT_SIZE

        Dot.set_default(color=BLACK)
        Text.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        Axes.set_default(axis_config={"color": BLACK,
                                        "include_numbers": True})

    def construct(self):
         self.construct_title()
         self.construct_objectives()
         self.construct_intro_to_limits()
         self.construct_conceptualizing_limits()
         self.construct_limit_difference()
         self.construct_limit_difference2()
         self.construct_summary()

    def construct_title(self):

        # Empty first Frame
        d = Dot(color=config.background_color).center()
        self.play(Create(d))
        self.next_slide()

        # Main Title Frame
        main_title1 = Text("Intuitive Notion", font_size=self.TITLE_FONT_SIZE)
        main_title2 = Text("of Limits")
        name = Text("by: Cristian B. Jetomo", font_size=self.SUBTITLE_FONT_SIZE)
        self.main_title = VGroup(main_title1, main_title2, name).arrange(DOWN, buff=0.5).center()

        self.play(Write(self.main_title), run_time=2)
        self.next_slide()

    def construct_objectives(self):
        # Learning Objectives
        # (1) header
        header_obj = Text("Learning Objectives", font_size=self.TITLE_FONT_SIZE).to_corner(UL)
        self.wipe(self.main_title, header_obj)
        self.next_slide()

        # (2) objectives
        obj1 = Text("At the end of this module, the students should be able to: ",
                    font_size=self.CONTENT_FONT_SIZE).align_to(header_obj, LEFT).shift(1.5*UP)
        obj2 = paragraph("1. understand limits in relation to Calculus; and",
                        "2. explain the concept of limits graphically and analytically.",
                        font_size=self.CONTENT_FONT_SIZE)
        obj2.next_to(obj1, DOWN).shift(1 * RIGHT)
        objs = VGroup(obj1, obj2)
        self.objectives = VGroup(header_obj, objs)
        self.play(Write(objs), run_time=0.5)
        self.next_slide()

    def construct_intro_to_limits(self):
        # Introduction to Calculus and Limits
        # (1) Title
        title1 = Text("Introduction to Calculus", font_size=self.TITLE_FONT_SIZE)
        title2 = Text("and Limits", font_size=self.TITLE_FONT_SIZE)
        self.subtitle1 = VGroup(title1, title2).arrange(DOWN, buff=0.5).center()
        
        self.wipe(self.objectives, self.subtitle1)
        self.next_slide()

        # --- Visualization
        # (2.1) Calculus
        calc_text = Text("Calculus").scale(0.75).to_edge(LEFT, buff=1)
        calc_box = SurroundingRectangle(calc_text, color=ManimColor("#89b6af"), fill_opacity=0.75, corner_radius=0.1, buff=0.3) 
        self.calculus = VGroup(calc_box, calc_text)

        self.wipe(self.subtitle1, self.calculus)
        self.next_slide()
        
        # (2.2) Differential and Integral
        diff_text = Text("Differential").scale(0.75).center().shift(2.5*UP)
        diff_box = SurroundingRectangle(diff_text, color=ManimColor("#56bbca"), fill_opacity=0.75, corner_radius=0.1, buff=0.3)
        diff_arrow = Arrow(start=calc_box.get_right(), end=diff_box.get_left(), color=ManimColor("#000000"))
        self.differential = VGroup(diff_box, diff_text)

        integ_text = Text("Integral").scale(0.75).center().shift(2.5*DOWN)
        integ_box = SurroundingRectangle(integ_text, color=ManimColor("#56bbca"), fill_opacity=0.75, corner_radius=0.1, buff=0.3)
        integ_arrow = Arrow(start=calc_box.get_right(), end=integ_box.get_left(), color=ManimColor("#000000"))
        self.integral = VGroup(integ_box, integ_text)

        self.arrows = VGroup(diff_arrow, integ_arrow)
        self.play(Create(self.arrows))
        self.play(GrowFromEdge(self.differential, LEFT), GrowFromEdge(self.integral, LEFT))
        self.next_slide()

        # (3) Visualizing Derivatives
        self.visualizing_derivatives()
        
        # (4) Visualizing Integrals
        self.visualizing_integrals()

        # grouping Mobjects for wipe
        self.intro_limits_group = VGroup(self.calculus, self.differential, self.integral, self.arrows, self.deriv_group, self.integ_group)

        self.play(self.intro_limits_group.animate.scale(0.65))
        self.play(self.intro_limits_group.animate.shift(UP))

        rect = SurroundingRectangle(self.intro_limits_group,
                                    color=BLACK, buff=0.5)
        self.play(Create(rect))

        # image of foundation
        foundation = ImageMobject("foundation.png").scale(2.5).next_to(rect, DOWN, buff=0.1)
        foundation_title = Text("Limits", font_size=self.CONTENT_FONT_SIZE).move_to(foundation.get_center())

        self.play(FadeIn(foundation))
        self.play(Write(foundation_title))
        self.next_slide()

        self.intro_limits_group = Group(self.calculus, self.differential, self.integral, self.arrows, self.deriv_group, self.integ_group, rect, foundation, foundation_title)

    def visualizing_derivatives(self):
        box = RoundedRectangle(corner_radius=0, color=BLACK, fill_opacity=0, height=3).move_to(self.differential.get_center() + 4.5 * RIGHT + 0.5*DOWN)
        ax = Axes(color=BLACK, x_length=box.get_right()[0]-box.get_left()[0], y_length=box.get_top()[1]-box.get_bottom()[1], tips=False,
                            axis_config={"color": BLACK}).move_to(box.get_center())

        k = ValueTracker(-3/2*np.pi)
        function = ax.plot(lambda x: np.sin(x), x_range=[-6,6,1], color=BLUE)
        moving_slope = always_redraw(
            lambda: ax.get_secant_slope_group(
                x = k.get_value(),
                graph = function,
                dx = 0.05,
                secant_line_length=1.5,
                secant_line_color=RED
            )
        )
        moving_dot = always_redraw(
            lambda: Dot(color=BLACK).move_to(
                ax.c2p(k.get_value(), function.underlying_function(k.get_value()))
            )
        )
        self.play(Create(box), Create(ax), Create(function))
        self.play(Create(moving_slope), Create(moving_dot))
        self.play(k.animate.set_value(3/2*np.pi), run_time=5, rate_func=linear)
        self.next_slide()

        self.deriv_group = VGroup(box, ax, function, moving_slope, moving_dot)

    def visualizing_integrals(self):
        box = RoundedRectangle(corner_radius=0, color=BLACK, fill_opacity=0, height=3).move_to(self.integral.get_center() + 4.5 * RIGHT + 0.5*UP)
        ax = Axes(color=BLACK, x_range=(-1, 12, 1), y_range=(-1, 3, 1),
                    x_length=box.get_right()[0]-box.get_left()[0], y_length=box.get_top()[1]-box.get_bottom()[1], tips=False,
                    axis_config={"color": BLACK}).move_to(box.get_center())

        function = ax.plot(lambda x: 0.7*np.sqrt(x), x_range=[0,12,0.05], color=BLACK)
        rectangles = VGroup(*[
                    ax.get_riemann_rectangles(
                        function,
                        x_range=[1,11],
                        dx=dx,
                        input_sample_type='left',
                        stroke_width=dx if dx > 0.1 else 0.8
                    ).set_color_by_gradient(BLUE, GREEN).set_stroke(color=BLACK if dx > 0.1 else None)
                    for dx in [1/(i) for i in range(1,10)]
        ])
        r = rectangles[0]

        self.play(Create(box), Create(ax), Create(function), Create(r))
        for rect in rectangles[1:]:
            self.play(Transform(r, rect))
            self.wait(0.3)
        self.next_slide()

        self.integ_group = VGroup(box, ax, function, rectangles)

    def construct_conceptualizing_limits(self):
        # Conceptualizing Limits
        # (1) Title
        self.subtitle2 = Text("Conceptualizing Limits", font_size=self.TITLE_FONT_SIZE).center()
        
        self.wipe(self.intro_limits_group, self.subtitle2)
        self.next_slide()

        # (2.1) Graphical Approach Title
        self.header_graphical = Text("Graphical Approach", font_size=self.CONTENT_FONT_SIZE).to_corner(UL)
        ul = Underline(self.header_graphical, color=BLACK)
        self.header_graphical = VGroup(self.header_graphical, ul)
        self.wipe(self.subtitle2, self.header_graphical)
        self.next_slide()

        t = Text("Consider the function", font_size=self.SUBTITLE_FONT_SIZE)
        eqn1 = MathTex(r"f(x) = \frac{x^3-1}{x-1}, \quad -2 \leq x \leq 2", font_size=1.5*self.SUBTITLE_FONT_SIZE)
        texts = VGroup(t, eqn1).align_to(self.header_graphical, LEFT).arrange(DOWN, buff=0.5).next_to(self.header_graphical, DOWN).shift(DOWN)

        self.play(Write(texts), run_time=0.5)
        self.next_slide()

        # (2.2) Plot
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 6, 1],
                    tips=False).to_edge(RIGHT)
        ax.get_x_axis().numbers.set_color(BLACK)
        ax.get_y_axis().numbers.set_color(BLACK)
        function = ax.plot(lambda x: x**2+x+1, x_range=[-2,2,1], color=WHITE)
        graph1 = ax.plot(lambda x: (x**3-1)/(x-1), x_range=[-2, 0.97, 1], color=BLUE)
        graph2 = ax.plot(lambda x: (x**3-1)/(x-1), x_range=[1.03, 2, 0.05], color=BLUE)
        break_point = Circle(radius=0.10, color=BLUE).move_to(ax.c2p(1,3))
        func_graph = VGroup(graph1, break_point, graph2)
        self.play(Create(ax), Create(func_graph))
        self.next_slide()

        # (2.3) What happens?
        t2 = Tex(r"What happens to $f(x)$ as \\$x$ approaches 1?",
                    font_size=self.CONTENT_FONT_SIZE).next_to(texts, DOWN).shift(DOWN)
        x_limit = ax.get_x_axis().numbers[3]
        self.play(Write(t2), run_time=0.5)
        self.play(Circumscribe(x_limit, color=RED))
        self.next_slide()

        # (2.4) Moving line, points, and value
        t = ValueTracker(0.1)
        moving_dot = always_redraw(
            lambda: Dot(color=BLACK).move_to(
                ax.c2p(t.get_value(), 0)
            )
        )
        dotted_lines = always_redraw(
            lambda: ax.get_lines_to_point(
                ax.c2p(t.get_value(), function.underlying_function(t.get_value())),
                color=BLACK
            )
        )
        moving_xmark = always_redraw(
            lambda: Cross(color=RED, scale_factor=0.1).move_to(
                ax.c2p(0, function.underlying_function(t.get_value()))
            )
        )
        updating_value = always_redraw(
            lambda: DecimalNumber(num_decimal_places=2, font_size=1.5*self.SUBTITLE_FONT_SIZE, color=BLACK)
            .set_value(t.get_value())
            .move_to(ax.c2p(t.get_value()-0.25, 0.25))
        )
        updating_lines_and_points = VGroup(moving_dot, dotted_lines, moving_xmark, updating_value)

        self.play(Create(updating_lines_and_points))
        self.next_slide()
        
        ## from the left
        self.play(t.animate.set_value(0.95), run_time=5)
        self.next_slide()

        ## from the right
        self.play(t.animate.set_value((np.sqrt(21)-1)/2))
        self.next_slide()
        self.play(t.animate.set_value(1.05), run_time=5)
        self.next_slide()

        y_limit = ax.get_y_axis().numbers[2]
        self.play(Circumscribe(y_limit, color=RED))
        self.next_slide()

        # (2.5) Graphical limit
        therefore = Text("Therefore", font_size=self.SUBTITLE_FONT_SIZE)
        graphical_limit = MathTex(r"\lim_{x\to1}f(x) = 3", 
                                font_size=1.5*self.SUBTITLE_FONT_SIZE)
        graphical_limit = VGroup(therefore, graphical_limit).arrange(DOWN, buff=0.5).move_to(ax.c2p(2.5,4))
        self.play(Write(graphical_limit))
        self.next_slide()

        self.graphical_objects = VGroup(self.header_graphical,
                                        texts, t2,
                                        ax, func_graph,
                                        updating_lines_and_points,
                                        graphical_limit)

        # (3.1) Analytical Approach 
        self.header_analytical = Text("Analytical Approach", font_size=self.CONTENT_FONT_SIZE).to_corner(UL)
        ul = Underline(self.header_analytical, color=BLACK)
        self.header_analytical = VGroup(self.header_analytical, ul)
        self.wipe(self.graphical_objects, self.header_analytical)
        self.next_slide()

        self.texts = texts.copy()
        self.play(Write(self.texts), run_time=0.5)
        self.next_slide()

        # appearing values in table of values
        self.table_of_values()

        analytical_limit = graphical_limit.copy().next_to(texts, RIGHT).shift(RIGHT)
        self.play(Write(analytical_limit))
        self.next_slide()

        self.analytical_objects = VGroup(self.header_analytical, 
                                        self.texts, 
                                        self.table, 
                                        analytical_limit)


    def table_of_values(self):
        table = DecimalTable(
            [[0.90, 0.99, 0.999, 0.9999, 1.0001, 1.001, 1.01, 1.1],
            [2.7100, 2.9701, 2.9970, 2.9997, 3.0003, 3.0030, 3.3031, 3.31]],
            row_labels=[MathTex(r"x"), MathTex(r"f(x)")],
            element_to_mobject_config={"num_decimal_places": 4, "color": BLACK,
                                        "font_size": 0.75*48},
            line_config={"color": BLACK},
            include_outer_lines=True,
            h_buff=1
        ).scale(0.7).to_edge(DOWN).shift(0.75*UP)

        left_x = table.get_rows()[0][1:5]
        right_x = table.get_rows()[0][5:]
        left_y = table.get_rows()[1][1:5]
        right_y = table.get_rows()[1][5:]
        for values in [left_x, right_x, left_y, right_y]:
            values.set_color(WHITE)

        self.play(Create(table))
        self.next_slide()
        self.play(left_x.animate.set_color(BLACK))
        self.next_slide()
        
        self.play(left_y[0].animate.set_color(BLACK))
        self.next_slide()
        self.play(left_y[1].animate.set_color(BLACK))
        self.next_slide()
        self.play(left_y[2].animate.set_color(BLACK))
        self.next_slide()
        self.play(left_y[3].animate.set_color(BLACK))
        self.next_slide()
        
        for mobj in right_x[::-1]:
            self.play(mobj.animate.set_color(BLACK), run_time=2/len(right_x))
        self.next_slide()

        for i in reversed(range(4)):
            self.play(right_y[i].animate.set_color(BLACK), run_time=1)
        self.next_slide()

        self.table = table

    def construct_limit_difference(self):
        # How Limits is Different
        # (1) Title
        self.subtitle3 = Text("How Limits is Different", font_size=self.TITLE_FONT_SIZE).center()
        self.wipe(self.analytical_objects, self.subtitle3)
        self.next_slide()

        t1 = Text("Examine the function", font_size=self.SUBTITLE_FONT_SIZE)
        eqn = MathTex(r"f(x) = \frac{x^3-1}{x-1}, \quad -2 \leq x \leq 2", 
                        font_size=1.5*self.SUBTITLE_FONT_SIZE).next_to(t1, DOWN)
        texts = VGroup(t1, eqn).arrange(DOWN, buff=0.5).to_corner(UL)
        t2 = Tex(r"The function is rational and is \\ undefined at $x=1$",
                    font_size=self.CONTENT_FONT_SIZE).next_to(texts, DOWN, buff=0.5)

        self.wipe(self.subtitle3, texts)
        self.next_slide()
        self.play(Write(t2), run_time=0.5)
        self.next_slide()

        # Showing Graph
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 6, 1],
                    tips=False).to_edge(RIGHT)
        ax.get_x_axis().numbers.set_color(BLACK)
        ax.get_y_axis().numbers.set_color(BLACK)
        graph1 = ax.plot(lambda x: (x**3-1)/(x-1), x_range=[-2, 0.97, 1], color=BLUE)
        graph2 = ax.plot(lambda x: (x**3-1)/(x-1), x_range=[1.03, 2, 0.05], color=BLUE)
        break_point = Circle(radius=0.10, color=BLUE).move_to(ax.c2p(1,3))
        func_graph = VGroup(graph1, break_point, graph2)

        self.play(Create(ax), Create(func_graph))
        self.next_slide()

        # Indicating Hole and Limit
        self.play(Indicate(break_point, color=RED, scale_factor=2))
        self.next_slide()

        still = Text("Still", font_size=self.SUBTITLE_FONT_SIZE)
        limit = MathTex(r"\lim_{x\to1}f(x) = 3", 
                                font_size=1.5*self.SUBTITLE_FONT_SIZE)
        limit = VGroup(still, limit).arrange(DOWN, buff=0.5).move_to(ax.c2p(2.5,4))
        self.play(Write(limit))
        self.next_slide()

        self.limit_difference_objects = VGroup(texts, t2,
                                                ax, func_graph,
                                                limit)

        # Conclusion
        conc1 = Text(f"Limits do not care whether a function is defined \n or not at a particular point.",
                            font_size=0.7 * 48, slant=ITALIC)
        conc2 = Text(f"What matters to Limits is what value the function \n (or output) is approaching to as we approach the \n input value to the point we are concerned with.",
                            font_size=0.7 * 48,
                            t2c={"what value the function": RED_E,
                                "(or output) is approaching to as we approach the": RED_E,
                                "input value to the point": RED_E},
                            t2s={"what value the function": ITALIC,
                                "(or output) is approaching to as we approach the": ITALIC,
                                "input value to the point": ITALIC})
        self.conclusion = VGroup(conc1, conc2).arrange(DOWN, buff=1, aligned_edge=LEFT)

        self.wipe(self.limit_difference_objects, conc1)
        self.next_slide()
        
        self.play(Write(conc2), run_time=0.5)
        self.next_slide()

    def construct_limit_difference2(self):

        t1 = Tex(r"Examine the function $f$ whose graph is given by", font_size=self.CONTENT_FONT_SIZE).to_corner(UL)
        ax = Axes(x_range=(-1, 3, 1), y_range=(0,2.5,1), tips=False).scale(0.75).shift(1.5*RIGHT)
        ax.get_x_axis().numbers.set_color(BLACK)
        ax.get_y_axis().numbers.set_color(BLACK)
        
        graph1 = ax.plot(lambda x: x, x_range=[-0.5, 0.98, 1], color=BLUE)
        graph2_point = Circle(radius=0.05, fill_opacity=1, color=BLUE).move_to(ax.c2p(1,2))
        break_point = Circle(radius=0.05, color=BLUE).move_to(ax.c2p(1,1))
        graph3 = ax.plot(lambda x: (x-2)**2,x_range=[1.01, 3, 1], color=BLUE)
        func_graph = VGroup(graph1, break_point, graph2_point, graph3)
        
        self.wipe(self.conclusion, t1)
        self.next_slide()
        
        self.play(Create(ax))
        self.play(Create(func_graph))
        self.next_slide()

        bullets = Paragraph("• At x = 1, the function value is 2",
                            "• Approaching x to 1 from both sides \n   makes the function value approach \n   to 1.",
                            font_size=self.SUBTITLE_FONT_SIZE, line_spacing=1)
        bullets.align_to(t1, LEFT)

        self.play(FadeIn(bullets.chars[0]), Indicate(graph2_point, color=RED))
        self.next_slide()
        self.play(FadeIn(bullets.chars[1:]))
        self.next_slide()

        limit = MathTex(r"\lim_{x\to1}f(x) = 1", 
                        font_size=1.5*self.SUBTITLE_FONT_SIZE).move_to(ax.c2p(2.5, 2))
        self.play(Write(limit))
        self.next_slide()

        self.limit_difference_objects2 = VGroup(t1, ax, func_graph, bullets, limit)


    def construct_summary(self):
        summary_title = Text("Summary", font_size=self.TITLE_FONT_SIZE).center()

        self.wipe(self.limit_difference_objects2, summary_title)
        self.next_slide()

        header_recap = Text("To recap ...", font_size=self.TITLE_FONT_SIZE).to_corner(UL)
        self.wipe(summary_title, header_recap)
        self.next_slide()

        bullets = Paragraph("• Limits is the foundation of Calculus.",
                            "• Limits can be conceptualized intuitively using graphical and \n   analytical approach.",
                            "• In both methods, the approached limit is the same.",
                            "• Limits are only concerned with approaching values, not at \n   the exact defined point.",
                            font_size=self.CONTENT_FONT_SIZE,
                            line_spacing=1)
        bullets.align_to(header_recap, LEFT)
        self.play(FadeIn(bullets.chars[0]))
        self.next_slide()
        self.play(FadeIn(bullets.chars[1:3]))
        self.next_slide()
        self.play(FadeIn(bullets.chars[3]))
        self.next_slide()
        self.play(FadeIn(bullets.chars[4:6]))
        self.next_slide()

        self.summary_objects = VGroup(header_recap, bullets)

        thank_you = Text("Thank you!", font_size=self.TITLE_FONT_SIZE)
        creds = Text("made with:", font_size=self.SUBTITLE_FONT_SIZE).to_corner(DL)
        manim = ManimBanner(dark_theme=False).scale(0.15).next_to(creds, RIGHT)
        
        self.wipe(self.summary_objects, thank_you)
        self.play(FadeIn(creds))
        self.play(Create(manim))
        self.next_slide()


def paragraph(*strs, alignment=LEFT, direction=DOWN, **kwargs):
        texts = VGroup(*[Text(s, **kwargs) for s in strs]).arrange(direction)

        if len(strs) > 1:
            for text in texts[1:]:
                text.align_to(texts[0], direction=alignment)

        return texts
