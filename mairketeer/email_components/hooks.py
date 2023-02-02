import sys
sys.path.append("..") # Adds higher directory to python modules path.

from get_values import (
    get_hooks_examples_from_file,
)
import openai


class Hooks:
    def __init__(self):
        self.hooks = []
        self.hooks_examples = get_hooks_examples_from_file()

    def create_new_hooks(self, hooks, company_info, customer_info, email_sequence_info):
        print("Creating new hooks...")

        prompt = f"""
        Example Hooks for a course that teaches you how to tune your car:
        {self.hooks_examples}

        Company Information
        Name: {company_info.name}
        Company Name: {company_info.company_name}
        Product Name: {company_info.product_name}
        Product Description: {company_info.product_description}

        Background Information
        Desires: {customer_info.desires}
        Target Audience: {customer_info.target_audience}
        Pains: {customer_info.pains}
        Target Demographic: {customer_info.target_demographic}


        Hook Information
        Number of Hooks: {email_sequence_info.number_of_emails}
        Type of Hook: {email_sequence_info.type_of_email_sequence}
        Desired Outcome: {email_sequence_info.sequence_purpose}


        Write a 12-15 word hook that will be used to get your target audience to do the desired outcome
        """
        print(prompt)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
            top_p=0,
            n=3,
        )
        return response["choices"][0]["text"]
