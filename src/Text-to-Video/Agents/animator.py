# agents/animator.py

from utils.ai_api import get_ai_api

class Animator:
    def __init__(self, ai_api=None):
        self.ai_api = get_ai_api(ai_api)

    def create_animation_code(self, plan):
        prompt = f"""
        Create a Python script using the Manim library to animate the following educational plan:

        {plan}

        Ensure that:
        1. The animation effectively explains all concepts in the plan (animations, examples, plots, etc.).
        2. Use appropriate Manim objects and animations to visualize key ideas.
        3. Include comments explaining each section of the code.
        4. The script should be complete and ready to run with Manim.
        5. Each slide is in its own class so that each can be saved individually
        6. Label the classes for each slide Slide1, Slide2, ...
        7. No animation can have text other than titles. However we need as comments everything that is happening so later we can create a script with the corresponding timestamps.
        8. Create separate animations per each of the topics we plan to cover
        9. All graphical animations include labels 
        10. All animations are cleared at the culmination of the slide
        11. All slides include a title which remains atop the screen throughout the slide
        12. All titles are cleared at the culmination of the slide
        13. All plotted points and models are fit within the graph grid properly
        14. Animations do not overlap with the slide titles
        15. Do not fade out any text or animation. Just do an instant clear of all mobjects to the next slide

        Important: Include the following `ensure_in_frame` function at the beginning of your script, right after the Manim imports:

        ```python
        from manim import *

        def ensure_in_frame(mobject, buffer=0.5):
            frame_width = config.frame_width
            frame_height = config.frame_height
            width_scale = (frame_width - 2 * buffer) / mobject.width
            height_scale = (frame_height - 2 * buffer) / mobject.height
            scale_factor = min(width_scale, height_scale, 1)
            mobject.scale(scale_factor)
            mobject.move_to(ORIGIN)
            return mobject
        ```

        Use this `ensure_in_frame` function for all major mobjects in your scene to prevent content from being cut off or lost outside the frame. Here's an example of how to use it:

        ```python
        class YourScene(Scene):
            def construct(self):
                text = Text("Your text here")
                ensure_in_frame(text)
                self.play(Write(text))
        ```

        Apply this function to all text, images, and complex mobjects in your scene.

        """
        return self.ai_api.generate_response(prompt)