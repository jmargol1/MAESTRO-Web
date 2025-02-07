from utils.ai_api import get_ai_api

class Reviewer:
    def __init__(self, ai_api=None):
        self.ai_api = get_ai_api(ai_api)

    def review_plan(self, plan):
        prompt = f"""
        Review the following educational plan:

        {plan}

        Ensure that it covers all necessary components to explain the topic comprehensively.
            - Include an introduction
            - Include advantages and disadvantages
            - Include practical applications
            - Final summary
        Identify any missing crucial information or concepts.
        Suggest improvements or additions to make the plan more complete and effective.
        If the plan is satisfactory, state that no changes are needed.
        """
        review = self.ai_api.generate_response(prompt)
        
        if "no changes are needed" in review.lower():
            return plan
        else:
            return self.refine_plan(plan, review)

    def refine_plan(self, original_plan, review):
        prompt = f"""
        Original plan:
        {original_plan}

        Review comments:
        {review}

        Please refine and improve the original plan based on the review comments.
        Provide a complete, updated plan that incorporates all necessary changes and additions.
        """
        return self.ai_api.generate_response(prompt)