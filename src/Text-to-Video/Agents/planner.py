from utils.ai_api import get_ai_api

class Planner:
    def __init__(self, ai_api=None):
        self.ai_api = get_ai_api(ai_api)

    def create_plan(self, topic):
        prompt = f"""
        Create a comprehensive plan for explaining the topic: {topic}
        The plan should cover all necessary components and subtopics related to {topic}.
        Include key concepts, algorithms, formulas, and practical applications.
            - Include an introduction
            - Include advantages and disadvantages
            - Include practical applications
            - Include final summary
        Organize the plan in a structured format with main sections and subsections.
        Ensure that the plan is suitable for creating an educational animation.
        Do not include information about the history of the algorithms
        Keep the plan concise to the most important topics necessary to understand the topic.
        """
        return self.ai_api.generate_response(prompt)