from utils.ai_api import get_ai_api

class detailer:
    def __init__(self, ai_api=None):
        self.ai_api = get_ai_api(ai_api)

    def request_changes(self, plan):
        changeNeeded = input("Would you like to make any additions to the current plan? (Yes/No)")

        if changeNeeded[0].lower() == "y":
            requests = input("Please type the section number you would like to change and describe the changes you would like")
            return self.detail_plan(plan, requests)
        else:
              return plan

    def detail_plan(self, plan, changes):
                prompt = f"""
                Current Plan:
                {plan}

                Change Requests:
                {changes}

                Please make the specific edits necessary to the Current Plan to incorporate the Change Requests.
                Ensure that the changes are made to the specific section number included in the request.
                Ensure that the plan is still structured as a professor would structure a lesson plan
                Provide a complete, updated plan incorporating all of the changes requested
                """
                return self.ai_api.generate_response(prompt)

    
