from utils.ai_api import get_ai_api

class VideoEditor:
    def __init__(self, ai_api=None):
        self.ai_api = get_ai_api(ai_api)

    def request_changes(self, original_code):
        for slide, scene in self.__dict__.items():
            if isinstance(slide, scene):
                while True:
                    response = input(f"Would you like to make changes to this slide? (yes/no): ").strip().lower()
                    if response in ['yes', 'no', 'y', 'n']:
                        break
                    print("Please enter yes or no")
                    
                if response.startswith('y'):
                    request = input(f"Describe changes for this slide: ").strip()
                    self.change_video(request, original_code)
                else:
                     return self
            

    def change_video(self, original_code, change_request):
                prompt = f"""
                Current Animation Code:
                {original_code}

                Change Requests:
                {change_request}

                Ensure that:
                1. If an additional slide is requested, ensure that you place it before or after the dictionary key the change was requested in
                    - Before or after is the verbage used within the request to tell where to place the additional slide
                2. For any changes made, ensure the following
                    - All content fits within the frame and remains visible throughout the animation.
                    - Check for appropriate use of scale, position, and camera movements.
                    - No text or objects extend beyond the edges of the screen.
                    - Verify that animations don't move objects out of view unintentionally.
                    - All grid-based graphical animations overlay on top of each other correctly, ie plotted points and lines are within the graph grid
                    - Text is not written on top of each other
                    - All animations align with the topic being described
                    - Slide titles are moved to the top of the screen and are not covering animations
                    - All graphs and diagrams are labeled for understanding
                3. Provide a complete, updated Animation code incorporating all of the changes requested

                Important: For spacing and alignment of mobjects, reference the ensure_in_frame function which is being used in the script

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

    


