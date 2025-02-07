# agents/code_auditor.py

from utils.ai_api import get_ai_api

class CodeAuditor:
    def __init__(self, ai_api=None):
        self.ai_api = get_ai_api(ai_api)

    def audit_code(self, code):
        prompt = f"""
        Audit the following Manim animation code:

        {code}

        Ensure that:
        1. The code is complete, correct, and can run without errors.
        2. Ensure that each slide is written as its own class so that each slide is saved as a separate video
        2. All necessary imports are present.
        3. There are no undefined variables or logical errors.
        4. All Manim objects and animations are used correctly.
        5. Allow animations for any graphical representations only
        6. Have each scene begin with the text on the screen. Do not animate text
        6. The `ensure_in_frame` function is defined at the beginning of the script.
        7. The `ensure_in_frame` function is used for all major mobjects (text, images, complex shapes) to keep them within the frame.
        8. All content fits within the frame and remains visible throughout the animation.
           - Check for appropriate use of scale, position, and camera movements.
           - No text or objects extend beyond the edges of the screen.
           - Verify that animations don't move objects out of view unintentionally.
           - All grid-based graphical animations overlay on top of each other correctly, ie plotted points and lines are within the graph grid
           - Text is not written on top of each other
           - All animations align with the topic being described
           - If you cannot fit the whole script within your maximimum word count, print it in separate parts that do not overlap
           - Slide titles are moved to the top of the screen and are not covering animations
           - All graphs and diagrams are labeled for understanding
        9. Do not fade out any text or animation. Just do an instant clear of all mobjects to the next slide

        If any issues are found, provide the corrected code with explanations for each change.
        If the code is satisfactory, state that no changes are needed.

        """
        audit_result = self.ai_api.generate_response(prompt)
        
        if "no changes are needed" in audit_result.lower():
            return code
        else:
            return self.fix_code(code, audit_result)

    def fix_code(self, original_code, audit_result):
        prompt = f"""
    
        Original code:
        {original_code}

        Audit result:
        {audit_result}

        Please provide the corrected and complete Manim animation code that addresses all issues mentioned in the audit result.
        Ensure that:
        1. The `ensure_in_frame` function is defined at the beginning of the script.
        2. The `ensure_in_frame` function is used for all major mobjects to keep them within the frame.
        3. All content fits within the frame and remains visible throughout the animation.
        Add comments explaining the changes made to improve visibility and framing.
        4. Rewrite the code in its entirety with the suggested changes. Do not truncate the code in any way
        """
        return self.ai_api.generate_response(prompt)