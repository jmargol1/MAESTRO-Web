from manim import *
import numpy as np

def ensure_in_frame(mobject, buffer=0.5):
    frame_width = config.frame_width
    frame_height = config.frame_height
    width_scale = (frame_width - 2 * buffer) / mobject.width
    height_scale = (frame_height - 2 * buffer) / mobject.height
    scale_factor = min(width_scale, height_scale, 1)
    mobject.scale(scale_factor)
    mobject.move_to(ORIGIN)
    return mobject

class Slide1(Scene):
    def construct(self):
        title = Text("KNN Introduction", font_size=36)
        title.to_edge(UP, buff=0.5)

        points = [
            "Supervised learning algorithm for classification and regression",
            "Predicts based on similarity to known examples",
            "Common applications:",
            "• Credit scoring",
            "• Medical diagnosis",
            "• Image recognition",
            "• Recommendation systems"
        ]

        bullets = VGroup(*[
            Text(point, font_size=24)
            for point in points
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        ensure_in_frame(bullets)
        bullets.next_to(title, DOWN, buff=0.7)
        
        self.add(title, bullets)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide2(Scene):
    def construct(self):
        title = Text("Key Characteristics of KNN", font_size=36)
        title.to_edge(UP, buff=0.5)

        characteristics = [
            "Instance-based Learning:",
            "• No pre-built model",
            "• Stores all training examples",
            "Lazy Learning:",
            "• Defers decisions until query time",
            "• No training phase required",
            "Decision Mechanism:",
            "• Uses K nearest neighbors",
            "• Majority vote for classification"
        ]

        bullets = VGroup(*[
            Text(char, font_size=24)
            for char in characteristics
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        ensure_in_frame(bullets)
        bullets.next_to(title, DOWN, buff=0.7)
        
        self.add(title, bullets)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide3(Scene):
   def construct(self):
       title = Text("KNN Classification Example: Fish Species", font_size=36)
       title.to_edge(UP, buff=0.5)
       self.add(title)

       axes = Axes(
           x_range=[0, 10, 1],
           y_range=[0, 10, 1],
           axis_config={"include_tip": True}
       ).scale(0.7)
       x_label = axes.get_x_axis_label("Length (cm)")
       y_label = axes.get_y_axis_label("Lightness")
       axes_labels = VGroup(x_label, y_label)
       
       ensure_in_frame(axes)
       axes.next_to(title, DOWN, buff=0.5)
       
       self.play(Create(axes), Write(axes_labels))

       # Fixed points for guaranteed classification outcome
       trout_points = VGroup(
           Dot(axes.c2p(5.3, 5.3), color=GREEN),
           Dot(axes.c2p(5.4, 5.6), color=GREEN),
           Dot(axes.c2p(5.7, 5.4), color=GREEN),
           *[Dot(axes.c2p(np.random.uniform(4, 7), np.random.uniform(4, 7)), color=GREEN)
             for _ in range(7)]
       )
       
       salmon_points = VGroup(
           Dot(axes.c2p(5.6, 5.7), color=RED),  # One of the nearest neighbors
           *[Dot(axes.c2p(np.random.uniform(5, 8), np.random.uniform(5, 8)), color=RED)
             for _ in range(9)]
       )
       
       seabass_points = VGroup(
           Dot(axes.c2p(5.2, 5.8), color=BLUE),  # One of the nearest neighbors
           *[Dot(axes.c2p(np.random.uniform(3, 6), np.random.uniform(3, 6)), color=BLUE)
             for _ in range(9)]
       )

       salmon_label = Text("Salmon", color=RED, font_size=20).next_to(salmon_points, RIGHT)
       seabass_label = Text("Sea Bass", color=BLUE, font_size=20).next_to(seabass_points, LEFT)
       trout_label = Text("Trout", color=GREEN, font_size=20).next_to(trout_points, UP)

       self.play(
           Create(salmon_points), Write(salmon_label),
           Create(seabass_points), Write(seabass_label),
           Create(trout_points), Write(trout_label)
       )

       query_point = Dot(axes.c2p(5.5, 5.5), color=YELLOW)
       query_label = Text("New Fish", font_size=20, color=YELLOW).next_to(query_point, UP)
       self.play(Create(query_point), Write(query_label))

       # Draw lines to pre-selected nearest neighbors
       nearest_points = [
           trout_points[0], trout_points[1], trout_points[2],
           salmon_points[0], seabass_points[0]
       ]
       
       lines = VGroup(*[
           Line(query_point.get_center(), p.get_center(), color=WHITE)
           for p in nearest_points
       ])
       
       self.play(Create(lines))

       result_text = Text(
           "Classification: Trout (3 Trout, 1 Salmon, 1 Sea Bass)",
           font_size=24,
           color=YELLOW
       ).next_to(axes, DOWN, buff=0.5)
       
       self.play(Write(result_text))
       
       self.wait(3)
       self.remove(*self.mobjects)

class Slide4(Scene):
    def construct(self):
        title = Text("Choosing K Value", font_size=36)
        title.to_edge(UP, buff=0.5)

        points = [
            "Small K (1-5):",
            "• More sensitive to local patterns",
            "• Risk of overfitting",
            "Large K (10+):",
            "• Smoother decision boundary",
            "• Risk of underfitting",
            "Optimal K Selection:",
            "• Usually sqrt(n) where n is sample size",
            "• Use cross-validation to tune"
        ]

        bullets = VGroup(*[
            Text(point, font_size=24)
            for point in points
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        ensure_in_frame(bullets)
        bullets.next_to(title, DOWN, buff=0.7)
        
        self.add(title, bullets)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide5(Scene):
   def construct(self):
       title = Text("Distance Metrics", font_size=36)
       title.to_edge(UP, buff=0.5)
       self.add(title)

       formulas = VGroup(
           MathTex(r"Euclidean: d = \sqrt{\sum_{i=1}^n (x_i - y_i)^2}", font_size=24),
           MathTex(r"Manhattan: d = \sum_{i=1}^n |x_i - y_i|", font_size=24),
           MathTex(r"Minkowski: d = (\sum_{i=1}^n |x_i - y_i|^p)^{\frac{1}{p}}", font_size=24)
       ).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.5).shift(UP)
       
       axes = Axes(
           x_range=[-5, 5, 1],
           y_range=[-5, 5, 1],
           axis_config={"include_tip": True}
       ).scale(0.8)
       x_label = axes.get_x_axis_label("X")
       y_label = axes.get_y_axis_label("Y")
       axes_labels = VGroup(x_label, y_label)
       
       ensure_in_frame(axes)
       axes.next_to(formulas, RIGHT, buff=0.8)

       point1 = Dot(axes.c2p(-2, -2), color=RED)
       point2 = Dot(axes.c2p(2, 2), color=BLUE)
       point_labels = VGroup(
           Text("A", font_size=16).next_to(point1, LEFT),
           Text("B", font_size=16).next_to(point2, RIGHT)
       )
       
       euclidean = Line(point1.get_center(), point2.get_center(), color=YELLOW)
       euclidean_midpoint = euclidean.get_center() + UP * 0.3
       euclidean_label = Text("Euclidean", font_size=16, color=YELLOW).move_to(euclidean_midpoint)
       
       manhattan = VGroup(
           Line(point1.get_center(), [point1.get_center()[0], point2.get_center()[1], 0]),
           Line([point1.get_center()[0], point2.get_center()[1], 0], point2.get_center())
       ).set_color(GREEN)
       
       manhattan_label = Text("Manhattan", font_size=16, color=GREEN)
       manhattan_label.next_to(manhattan[0], LEFT, buff=0.4)

       self.add(formulas)
       self.play(
           Create(axes), Write(axes_labels),
           Create(point1), Create(point2), Write(point_labels),
           Create(euclidean), Write(euclidean_label),
           Create(manhattan), Write(manhattan_label)
       )
       
       self.wait(3)  # Added 3 second pause
       self.remove(*self.mobjects)

class Slide6(Scene):
    def construct(self):
        title = Text("Hamming Distance for Categorical Data", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        formula = MathTex(r"Hamming\ Distance = \sum_{i=1}^n [x_i \neq y_i]")
        formula.next_to(title, DOWN, buff=0.5)
        
        example = VGroup(
            Text("Example:", font_size=24),
            Text("String 1: [red, small, round]", color=BLUE, font_size=24),
            Text("String 2: [red, large, square]", color=RED, font_size=24),
            Text("Hamming Distance = 2", color=GREEN, font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        
        example.next_to(formula, DOWN, buff=1.5)
        ensure_in_frame(example)

        self.add(formula, example)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide7(Scene):
    def construct(self):
        title = Text("Importance of Normalization", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # Create two examples: age and income points
        example1 = VGroup(
            Text("Before Normalization:", font_size=24),
            Text("Point A: Age=30, Income=$90,000", font_size=20),
            Text("Point B: Age=40, Income=$100,000", font_size=20),
            MathTex(r"Distance = \sqrt{(30-40)^2 + (90000-100000)^2} = 10000.005", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        example2 = VGroup(
            Text("After Normalization (0-1 scale):", font_size=24),
            Text("Point A: Age=0.3, Income=0.9", font_size=20),
            Text("Point B: Age=0.4, Income=1.0", font_size=20),
            MathTex(r"Distance = \sqrt{(0.3-0.4)^2 + (0.9-1.0)^2} = 0.14", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        examples = VGroup(example1, example2).arrange(DOWN, buff=1)
        ensure_in_frame(examples)
        examples.next_to(title, DOWN, buff=0.7)

        self.add(examples)
        
        conclusion = Text(
            "Without normalization, income dominates the distance calculation",
            font_size=20, color=YELLOW
        ).next_to(examples, DOWN, buff=0.5)
        
        self.add(conclusion)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide8(Scene):
    def construct(self):
        title = Text("Normalization Methods", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # Min-Max Normalization
        minmax = VGroup(
            Text("Min-Max Normalization", font_size=24),
            MathTex(r"x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}", font_size=24),
            Text("Range: [0,1]", font_size=20, color=YELLOW)
        ).arrange(DOWN, buff=0.3)

        # Z-score Standardization
        zscore = VGroup(
            Text("Z-score Standardization", font_size=24),
            MathTex(r"x_{norm} = \frac{x - \mu}{\sigma}", font_size=24),
            Text("Mean=0, Std=1", font_size=20, color=YELLOW)
        ).arrange(DOWN, buff=0.3)

        # Scaling
        scaling = VGroup(
            Text("Feature Scaling", font_size=24),
            MathTex(r"x_{norm} = \frac{x}{max(|x|)}", font_size=24),
            Text("Range: [-1,1]", font_size=20, color=YELLOW)
        ).arrange(DOWN, buff=0.3)

        methods = VGroup(minmax, zscore, scaling).arrange(DOWN, buff=0.8)
        ensure_in_frame(methods)
        methods.next_to(title, DOWN, buff=0.7)

        self.add(methods)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide9(Scene):
    def construct(self):
        title = Text("KNN Advantages", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        advantages = [
            "Easy to understand and implement",
            "Robust to noisy data with large K",
            "Handles multiple classes effectively",
            "Minimal assumptions about data distribution"
        ]

        bullets = VGroup(*[
            Text("• " + adv, font_size=28)
            for adv in advantages
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        
        ensure_in_frame(bullets)
        bullets.next_to(title, DOWN, buff=0.7)
        
        self.add(bullets)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide10(Scene):
    def construct(self):
        title = Text("KNN Disadvantages", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        disadvantages = [
            "Curse of dimensionality and data sparsity",
            "Impact of irrelevant features",
            "High space requirements for training data",
            "High computational cost (instance-based)",
            "Sensitive to noise with small training sets",
            "Requires normalization",
            "Difficulty in choosing K value"
        ]

        bullets = VGroup(*[
            Text("• " + disadv, font_size=24)
            for disadv in disadvantages
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        ensure_in_frame(bullets)
        bullets.next_to(title, DOWN, buff=0.7)
        
        self.add(bullets)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide11(Scene):
    def construct(self):
        title = Text("Practical Challenges & Considerations", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # Feature importance section
        feature_importance = VGroup(
            Text("Feature Importance", font_size=28),
            Text("• Weight features based on relevance", font_size=24),
            Text("• Adaptive feature scaling", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Instance importance section
        instance_importance = VGroup(
            Text("Instance Importance", font_size=28),
            Text("• Distance-weighted voting", font_size=24),
            Text("• Time-based instance weighting", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Missing values section
        missing_values = VGroup(
            Text("Handling Missing Values", font_size=28),
            Text("• Mean/median imputation", font_size=24),
            Text("• KNN-based imputation", font_size=24),
            Text("• Interpolation methods", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Arrange all sections
        all_sections = VGroup(
            feature_importance,
            instance_importance,
            missing_values
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        ensure_in_frame(all_sections)
        all_sections.next_to(title, DOWN, buff=0.7)

        self.add(all_sections)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide12(Scene):
    def construct(self):
        title = Text("Real-World KNN Applications", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # Medical Diagnosis Example
        medical = VGroup(
            Text("Medical Diagnosis", font_size=28, color=BLUE),
            Text("• Features: blood pressure, age, BMI, glucose", font_size=24),
            Text("• Instance weighting: recent cases more important", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Credit Scoring Example
        credit = VGroup(
            Text("Credit Risk Assessment", font_size=28, color=GREEN),
            Text("• Features: income, debt ratio, payment history", font_size=24),
            Text("• Feature importance: payment history > age", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Image Recognition Example
        image = VGroup(
            Text("Facial Recognition", font_size=28, color=RED),
            Text("• Features: facial landmarks, pixel intensities", font_size=24),
            Text("• Feature selection: key points over background", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        # Arrange all sections
        examples = VGroup(medical, credit, image).arrange(DOWN, buff=0.5)
        ensure_in_frame(examples)
        examples.next_to(title, DOWN, buff=0.7)

        self.add(examples)
        self.wait(3)
        self.remove(*self.mobjects)

class Slide13(Scene):
    def construct(self):
        title = Text("Summary: Key Components of KNN", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        key_points = [
            "Core Algorithm:",
            "• Distance-based classification/regression",
            "• K nearest neighbors determine outcome",
            "Essential Steps:",
            "• Feature normalization",
            "• Distance metric selection",
            "• Optimal K value selection",
            "Implementation Considerations:",
            "• Data preprocessing",
            "• Feature importance",
            "• Computational efficiency"
        ]

        bullets = VGroup(*[
            Text(point, font_size=28)
            for point in key_points
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        ensure_in_frame(bullets)
        bullets.next_to(title, DOWN, buff=0.7)
        
        self.add(bullets)
        self.wait(3)
        self.remove(*self.mobjects)