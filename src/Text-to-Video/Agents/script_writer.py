from utils.ai_api import get_ai_api

class ScriptWriter:
    def __init__(self, ai_api=None):
        self.ai_api = get_ai_api(ai_api)

    def write_script(self, plan, animation_code):
        prompt = f"""
        Write a comprehensive script spoken as a professor for an educational animation based on the following plan and Manim animation code:

        Plan:
        '''
        {plan}
        '''

        Animation Code:
        '''
        {animation_code}
        '''
        
        The script should:
        1. Introduce the topic and its importance
        2. Explain each concept in a clear and engaging manner
        3. Relate the narration to the visual elements created by the Manim code
        4. Provide examples and real-world applications where appropriate
        5. Summarize key points at the end
        6. Ensure that all the graphs and bullets are descibed in detail
        7. Do not include text about the screen information that would not be read by a narrator
        8. Split up the script by slide and timestamp each slide length
        9. Ensure that each slide in the animation has a corresponding script section

        Format the script with clear sections by slide and timestamps corresponding to the animation.
        """
        return self.ai_api.generate_response(prompt)