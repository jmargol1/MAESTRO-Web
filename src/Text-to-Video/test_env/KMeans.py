from manim import *
import numpy as np
from sklearn.datasets import make_blobs

def ensure_in_frame(mobject, buffer=0.5):
    """Ensures that a mobject fits within the frame with specified buffer."""
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
        # Create all text elements
        title = Text("Introduction to Clustering", font_size=36)
        title.to_edge(UP, buff=0.5)
        # Center the title horizontally
        title.shift(RIGHT * (config.frame_width/2 - title.get_center()[0]))
        
        # Definition section
        definition_title = Text("What is Clustering?", font_size=28, color=BLUE)
        definition_text = Text(
            "• Clustering is a technique that groups similar data points together\n" +
            "• Points within a cluster are more similar to each other than to points in other clusters\n" +
            "• It is an unsupervised learning method, meaning it doesn't require labeled data",
            font_size=24,
            line_spacing=0.5
        )
        
        # Types section
        types_title = Text("Types of Clustering", font_size=28, color=BLUE)
        types_text = Text(
            "Hierarchical Clustering:\n" +
            "• Creates a tree-like hierarchy of clusters\n" +
            "• Can be agglomerative (bottom-up) or divisive (top-down)\n\n" +
            "Non-Hierarchical Clustering:\n" +
            "• K-means: Partitions data into k predetermined clusters\n" +
            "• DBSCAN: Density-based clustering for finding arbitrary shapes\n" +
            "• Mean-shift: Finds clusters by identifying density peaks",
            font_size=24,
            line_spacing=0.5
        )
        
        # Create layout group and arrange vertically
        content = VGroup(
            definition_title,
            definition_text,
            types_title,
            types_text
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        # Position content below title
        content.next_to(title, DOWN, buff=0.7)
        
        # Center the content horizontally
        content_center = content.get_center()
        content.shift(RIGHT * (config.frame_width/2 - content_center[0]))
        
        # Ensure everything fits in frame
        entire_scene = VGroup(title, content)
        ensure_in_frame(entire_scene, buffer=0.75)
        
        # Add all elements to scene at once (no text animation)
        self.add(title, definition_title, definition_text, types_title, types_text)
        self.wait(3)
        
        # Clear scene instantly
        self.clear()

class Slide2(Scene):
    def construct(self):
        # Title
        title = Text("K-means Clustering", font_size=40)
        title.to_edge(UP, buff=0.5)
        title.shift(RIGHT * (config.frame_width/2 - title.get_center()[0]))
        
        # Definition text with larger font
        definition = Text(
            "K-means Algorithm:\n" +
            "• Partitions data into K user-defined clusters\n" +
            "• Each cluster is represented by its centroid (mean)\n" +
            "• Data points are assigned to nearest centroid",
            font_size=28,
            line_spacing=0.5
        )
        
        # Choosing K text with larger font
        k_importance = Text(
            "Choosing K:\n" +
            "• Critical parameter that affects clustering quality\n" +
            "• Too few clusters: Underfitting\n" +
            "• Too many clusters: Overfitting",
            font_size=28,
            line_spacing=0.5
        )
        
        # Create text layout and center it
        text_group = VGroup(definition, k_importance).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        text_group.next_to(title, DOWN, buff=0.7)
        
        # Center the text_group horizontally
        text_group.shift(RIGHT * (config.frame_width/2 - text_group.get_center()[0]))
        
        # Ensure everything fits in frame
        entire_scene = VGroup(title, text_group)
        ensure_in_frame(entire_scene, buffer=0.75)
        
        # Add all elements
        self.add(title, definition, k_importance)
        self.wait(3)
        self.clear()

class Slide3(Scene):
    def construct(self):
        # Title
        title = Text("K-means Algorithm Steps", font_size=40)
        title.to_edge(UP, buff=0.5)
        title.shift(RIGHT * (config.frame_width/2 - title.get_center()[0]))
        
        # Steps text
        steps = Text(
            "1. Decide on the number of clusters, K\n\n" +
            "2. Initialize K cluster centroids\n\n" +
            "3. Assign each data point to the nearest centroid\n\n" +
            "4. Recalculate centroids based on new memberships\n\n" +
            "5. Repeat until no memberships change",
            font_size=32,
            line_spacing=0.5
        )
        
        # Position steps below title
        steps.next_to(title, DOWN, buff=0.7)
        
        # Center steps horizontally
        steps.shift(RIGHT * (config.frame_width/2 - steps.get_center()[0]))
        
        # Ensure everything fits in frame
        entire_scene = VGroup(title, steps)
        ensure_in_frame(entire_scene, buffer=0.75)
        
        # Add all elements
        self.add(title, steps)
        self.wait(3)
        self.clear()

class Slide4(Scene):
    def construct(self):
        # Title - properly centered
        title = Text("K-means Clustering Demonstration", font_size=40)
        title.move_to(UP * 3)
        self.add(title)

        # Create coordinate system with smaller range and moved down
        axes = Axes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            axis_config={
                "include_tip": True,
                "numbers_to_include": [-1, 1]
            },
            x_length=6,
            y_length=6
        ).shift(DOWN * 0.5)

        # Add axis labels
        x_label = Text("X", font_size=24).next_to(axes.x_axis, DOWN)
        y_label = Text("Y", font_size=24).next_to(axes.y_axis, LEFT)
        labels = VGroup(x_label, y_label)

        # Add iteration counter
        iter_counter = Text("Iteration: 1", font_size=28).to_corner(UR, buff=0.5)
        
        # Colors for clusters
        colors = [RED, BLUE, GREEN]

        # Create predefined cluster centers
        cluster_centers = [
            [-1, -0.5],    # Bottom left
            [0.2, 1],      # Top middle
            [1.2, -0.8]    # Bottom right
        ]

        # Generate points around cluster centers
        points = []
        point_colors = []
        for i, center in enumerate(cluster_centers):
            # Generate 10 points around each center
            for _ in range(10):
                point = [
                    center[0] + np.random.normal(0, 0.2),
                    center[1] + np.random.normal(0, 0.2)
                ]
                points.append(point)
                point_colors.append(colors[i])

        # Create larger dots
        dots = VGroup(*[
            Dot(
                axes.coords_to_point(p[0], p[1]),
                radius=0.08,
                color=c
            ) for p, c in zip(points, point_colors)
        ])

        # Initial centroid positions (deliberately misplaced)
        initial_centroids = [
            [-1.5, 1],     # Top left
            [0.5, -1.5],   # Bottom middle
            [1.5, 0.5]     # Top right
        ]

        # Intermediate centroid positions for controlled convergence
        intermediate_positions = [
            [
                [-1.3, 0.3],   # First iteration
                [-1.1, -0.2],  # Second iteration
                [-1.0, -0.5]   # Final iteration (cluster mean)
            ],
            [
                [0.3, -0.7],   # First iteration
                [0.25, 0.2],   # Second iteration
                [0.2, 1]       # Final iteration (cluster mean)
            ],
            [
                [1.4, -0.1],   # First iteration
                [1.3, -0.5],   # Second iteration
                [1.2, -0.8]    # Final iteration (cluster mean)
            ]
        ]

        # Create centroids
        centroids = VGroup(*[
            Dot(
                axes.coords_to_point(x[0], x[1]),
                color=colors[i],
                radius=0.12
            ) for i, x in enumerate(initial_centroids)
        ])

        # Add elements to scene
        ensure_in_frame(VGroup(axes, labels, dots, centroids))
        self.play(Create(axes))
        self.add(labels)
        self.play(Create(dots))
        self.play(Create(centroids))
        self.add(iter_counter)

        # Perform 3 iterations 
        for iteration in range(3):
            # Update iteration counter
            new_counter = Text(f"Iteration: {iteration + 1}", font_size=28).to_corner(UR, buff=0.5)
            self.remove(iter_counter)
            self.add(new_counter)
            iter_counter = new_counter

            # Assign points to nearest centroid
            cluster_assignments = [[] for _ in range(3)]
            for i, dot in enumerate(dots):
                distances = [np.linalg.norm(
                    np.array([dot.get_center()[0], dot.get_center()[1]]) - 
                    np.array([c.get_center()[0], c.get_center()[1]])
                ) for c in centroids]
                closest = np.argmin(distances)
                cluster_assignments[closest].append(points[i])
                
                # Change dot color to match closest centroid
                self.play(dot.animate.set_color(colors[closest]), run_time=0.2)

            # Move centroids to intermediate positions
            for i in range(3):
                new_pos = intermediate_positions[i][iteration]
                self.play(
                    centroids[i].animate.move_to(
                        axes.coords_to_point(new_pos[0], new_pos[1])
                    ),
                    run_time=0.8
                )

            self.wait(0.5)

        self.wait(1)
        self.clear()

class Slide5(Scene):
    def construct(self):
        # Title
        title = Text("K-means Cost Function", font_size=40)
        title.move_to(UP * 3)
        
        # Cost function formula using proper LaTeX
        formula = MathTex(
            r"J = \sum_{i=1}^{K} \sum_{x \in C_i} \|x - \mu_i\|^2",
            font_size=36
        )
        
        # Formula explanation with proper subscript notation
        formula_explanation = Text(
            "where:\n" +
            "• J is the cost function\n" +
            "• K is the number of clusters\n" +
            "• x is a data point in cluster Ci\n" +
            "• μi is the centroid of cluster i",
            font_size=28,
            line_spacing=0.5
        )
        
        # Group formula and explanation
        formula_group = VGroup(formula, formula_explanation)
        formula_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        # Cost function properties
        properties = Text(
            "\nCost Function Properties:\n\n" +
            "• Measures sum of squared Euclidean distances\n" +
            "• Algorithm minimizes this cost at each step:\n" +
            "   - Assignment step: Points join their closest centroid\n" +
            "   - Update step: Centroids move to cluster means\n\n" +
            "• Convergence is guaranteed because:\n" +
            "   - Cost decreases with each step\n" +
            "   - There are finite possible assignments\n" +
            "   - Algorithm stops when assignments don't change",
            font_size=28,
            line_spacing=0.5
        )
        
        # Arrange all content
        content = VGroup(formula_group, properties)
        content.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        content.next_to(title, DOWN, buff=0.7)
        
        # Center everything horizontally
        for mob in [title, content]:
            mob.shift(RIGHT * (config.frame_width/2 - mob.get_center()[0]))
        
        # Ensure everything fits in frame
        entire_scene = VGroup(title, content)
        ensure_in_frame(entire_scene, buffer=0.75)
        
        # Add all elements
        self.add(title, formula, formula_explanation, properties)
        self.wait(3)
        self.clear()

class Slide6(Scene):
    def construct(self):
        # Title
        title = Text("Strategies for Choosing K", font_size=40)
        title.move_to(UP * 3)
        
        # Content with strategies
        strategies = Text(
            "1. Domain Expert Input\n" +
            "   • Utilize expert knowledge of the field\n" +
            "   • Based on business requirements or known patterns\n\n" +
            "2. Optimization of SSE\n" +
            "   • Sum of Squared Errors\n" +
            "   • Not recommended as SSE always decreases with larger K\n\n" +
            "3. Elbow Method\n" +
            "   • Plot the cost function for different K values\n" +
            "   • Identify the 'elbow point' where decrease becomes less rapid",
            font_size=32,
            line_spacing=0.5
        )
        
        # Position content below title
        strategies.next_to(title, DOWN, buff=0.7)
        
        # Center everything horizontally
        for mob in [title, strategies]:
            mob.shift(RIGHT * (config.frame_width/2 - mob.get_center()[0]))
        
        # Ensure everything fits in frame
        entire_scene = VGroup(title, strategies)
        ensure_in_frame(entire_scene, buffer=0.75)
        
        # Add all elements
        self.add(title, strategies)
        self.wait(3)
        self.clear()

class Slide7(Scene):
    def construct(self):
        # Title
        title = Text("Parameter Selection - Elbow Method", font_size=40)
        title.move_to(UP * 3)
        
        # Create coordinate system - adjusted size and position
        axes = Axes(
            x_range=[0, 10],
            y_range=[0, 100],
            axis_config={"include_tip": True},
            x_length=7,  # Slightly shorter to accommodate labels
            y_length=5   # Slightly shorter to accommodate labels
        ).shift(DOWN * 0.5)

        # Add axis labels with smaller font and better positioning
        x_label = Text("K", font_size=20).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("SSE", font_size=20).next_to(axes.y_axis, LEFT, buff=0.3)
        labels = VGroup(x_label, y_label)

        # Create grid
        vertical_lines = VGroup(*[
            Line(
                start=axes.c2p(x, 0),
                end=axes.c2p(x, 100),
                stroke_width=0.5,
                color=GRAY
            )
            for x in range(1, 11)
        ])

        horizontal_lines = VGroup(*[
            Line(
                start=axes.c2p(0, y),
                end=axes.c2p(10, y),
                stroke_width=0.5,
                color=GRAY
            )
            for y in range(0, 101, 10)
        ])

        grid = VGroup(vertical_lines, horizontal_lines)

        # Create elbow curve points
        points = [
            (1, 90),
            (2, 65),
            (3, 35),  # Elbow point
            (4, 25),
            (5, 20),
            (6, 17),
            (7, 15),
            (8, 13)
        ]

        # Create broken line segments
        lines = VGroup()
        for i in range(len(points)-1):
            start = axes.coords_to_point(points[i][0], points[i][1])
            end = axes.coords_to_point(points[i+1][0], points[i+1][1])
            line = Line(start, end, color=BLUE)
            lines.add(line)

        # Add elbow point
        elbow_point = Dot(
            axes.coords_to_point(3, 35),
            color=RED,
            radius=0.1
        )
        
        elbow_label = Text("Elbow Point (K=3)", font_size=24, color=RED)
        elbow_label.next_to(elbow_point, UR, buff=0.2)

        # Group all elements for ensure_in_frame
        all_elements = VGroup(axes, grid, lines, labels, elbow_point, elbow_label)
        ensure_in_frame(all_elements)

        # Add elements to scene
        self.add(title)
        self.play(Create(axes))
        self.add(labels)
        self.play(Create(grid))
        self.play(Create(lines))
        self.play(Create(elbow_point))
        self.add(elbow_label)
        
        self.wait(2)
        self.clear()

class Slide8(Scene):
    def construct(self):
        # Title
        title = Text("K-means: Choosing Optimal K", font_size=40)
        title.move_to(UP * 3)
        self.add(title)

        # Create three coordinate systems
        axes_group = VGroup()
        labels_group = VGroup()
        titles = ["Underfitting (K=2)", "Good Fit (K=3)", "Overfitting (K=4)"]

        for i, title_text in enumerate(titles):
            axes = Axes(
                x_range=[-2, 2],
                y_range=[-2, 2],
                axis_config={"include_tip": False},
                x_length=4,
                y_length=4
            ).shift((i-1)*4.5*RIGHT + DOWN * 0.5)

            # Add subtle grid
            grid = VGroup()
            for x in range(-2, 3):
                grid.add(Line(
                    axes.c2p(x, -2),
                    axes.c2p(x, 2),
                    stroke_width=0.5,
                    stroke_opacity=0.3
                ))
            for y in range(-2, 3):
                grid.add(Line(
                    axes.c2p(-2, y),
                    axes.c2p(2, y),
                    stroke_width=0.5,
                    stroke_opacity=0.3
                ))

            title_label = Text(title_text, font_size=24).next_to(axes, UP, buff=0.2)
            axes_group.add(VGroup(axes, grid))
            labels_group.add(title_label)

        # Define three clear cluster centers
        true_centers = [
            [-1, -0.5],   # Bottom left
            [0.2, 1],     # Top middle
            [1.2, -0.8]   # Bottom right (will be split in K=4)
        ]

        # Generate points around centers
        points = []
        for center in true_centers:
            for _ in range(10):
                point = [
                    center[0] + np.random.normal(0, 0.15),
                    center[1] + np.random.normal(0, 0.15)
                ]
                points.append(point)

        # Define centroids for each K
        centroids = {
            2: [[-0.5, 0], [0.7, 0]],           # K=2
            3: true_centers,                     # K=3 (true clusters)
            4: [[-1, -0.5], [0.2, 1], [0.8, -0.8], [1.6, -0.8]]  # K=4 (splitting right cluster)
        }

        # Colors for different K values
        colors = {
            2: [RED, BLUE],
            3: [RED, BLUE, GREEN],
            4: [RED, BLUE, GREEN, YELLOW]
        }

        # Add elements to scene
        self.play(Create(axes_group))
        self.add(labels_group)

        # Plot points and centroids for each case
        for i, (axes, k) in enumerate(zip(axes_group, [2, 3, 4])):
            # Plot points
            for point in points:
                # Find nearest centroid
                distances = [np.linalg.norm(np.array(point) - np.array(c)) for c in centroids[k]]
                nearest = np.argmin(distances)
                dot = Dot(
                    axes[0].coords_to_point(point[0], point[1]),
                    color=colors[k][nearest],
                    radius=0.06
                )
                self.play(Create(dot), run_time=0.05)

            # Add centroids
            for j, center in enumerate(centroids[k]):
                centroid = Dot(
                    axes[0].coords_to_point(center[0], center[1]),
                    color=colors[k][j],
                    radius=0.12
                )
                self.play(Create(centroid), run_time=0.2)

        self.wait(2)
        self.clear()

class Slide9(Scene):
    def construct(self):
        # Title
        title = Text("Strengths of K-means Clustering", font_size=40)
        title.move_to(UP * 3)
        
        # Content with strengths
        strengths = Text(
            "• Simple and easy to implement\n\n" +
            "• Fast convergence on large datasets\n\n" +
            "• Relatively efficient: O(tKn)\n" +
            "   where t = iterations, K = clusters, n = points\n\n" +
            "• Easily adaptable to new data points\n\n" +
            "• Memory efficient for large datasets\n\n" +
            "• Works well with numerical features\n\n" +
            "• Results are easy to interpret and explain",
            font_size=32,
            line_spacing=0.5
        )
        
        # Position content below title
        strengths.next_to(title, DOWN, buff=0.7)
        
        # Center everything horizontally
        for mob in [title, strengths]:
            mob.shift(RIGHT * (config.frame_width/2 - mob.get_center()[0]))
        
        # Ensure everything fits in frame
        entire_scene = VGroup(title, strengths)
        ensure_in_frame(entire_scene, buffer=0.75)
        
        # Add all elements
        self.add(title, strengths)
        self.wait(3)
        self.clear()


class Slide10(Scene):
    def construct(self):
        # Title
        title = Text("Limitations of K-means Clustering", font_size=40)
        title.move_to(UP * 3)
        
        # Content with limitations
        limitations = Text(
            "• Sensitive to starting centroids\n\n" +
            "• Not suitable for nonconvex clusters\n\n" +
            "• Requires specifying K in advance\n\n" +
            "• Cannot handle noisy data and outliers",
            font_size=32,
            line_spacing=0.5
        )
        
        # Position content below title
        limitations.next_to(title, DOWN, buff=0.7)
        
        # Center everything horizontally
        for mob in [title, limitations]:
            mob.shift(RIGHT * (config.frame_width/2 - mob.get_center()[0]))
        
        # Ensure everything fits in frame
        entire_scene = VGroup(title, limitations)
        ensure_in_frame(entire_scene, buffer=0.75)
        
        # Add all elements
        self.add(title, limitations)
        self.wait(3)
        self.clear()

class Slide11(Scene):
    def construct(self):
        # Title
        title = Text("K-means: Key Takeaways", font_size=40)
        title.move_to(UP * 3)
        
        # Content with conclusion points
        conclusion = Text(
            "• Simple yet powerful clustering algorithm\n\n" +
            "• Best suited for well-separated, spherical clusters\n\n" +
            "• Success depends on careful selection of K\n\n" +
            "• Use the elbow method unless domain expertise suggests specific K\n\n" +
            "• Consider data characteristics before applying\n\n" +
            "• Balance between underfitting and overfitting",
            font_size=32,
            line_spacing=0.5
        )
        
        # Position content below title
        conclusion.next_to(title, DOWN, buff=0.7)
        
        # Center everything horizontally
        for mob in [title, conclusion]:
            mob.shift(RIGHT * (config.frame_width/2 - mob.get_center()[0]))
        
        # Ensure everything fits in frame
        entire_scene = VGroup(title, conclusion)
        ensure_in_frame(entire_scene, buffer=0.75)
        
        # Add all elements
        self.add(title, conclusion)
        self.wait(3)
        self.clear()