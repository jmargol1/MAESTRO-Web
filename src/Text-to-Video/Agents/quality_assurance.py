from utils.ai_api import get_ai_api

class QualityAssurance:
    def __init__(self, ai_api=None):
        self.ai_api = get_ai_api(ai_api)

    def perform_qa(self, plan, animation_code, script):
        prompt = f"""
        Perform a comprehensive quality assurance check on the following educational animation materials:

        Plan:
        ```
        {plan}
        ```

        Animation Code:
        ```
        {animation_code}
        ```

        Script:
        ```
        {script}
        ```

        Ensure that:
        1. The plan covers all necessary topics and concepts
        2. The animation code accurately represents the plan
        3. The script aligns with both the plan and the animation
        4. All components are coherent and work together effectively
        5. The content is accurate, engaging, and educational

        If any issues are found, provide specific recommendations for improvements.
        If everything is satisfactory, state that no changes are needed.
        """
        qa_result = self.ai_api.generate_response(prompt)
        
        if "no changes are needed" in qa_result.lower():
            return True, "QA passed. All components are aligned and effective."
        else:
            return False, qa_result