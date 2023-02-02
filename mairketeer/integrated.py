#!/usr/bin/env python3

import os
import openai

from information.company_information import CompanyInformation
from information.customer_information import CustomerInformation
from information.email_sequence_information import EmailSequenceInformation

from email_components.hooks import Hooks

openai.api_key = os.getenv("OPENAI_API_KEY")


def format_background_info_prompt(company_info, customer_info, email_sequence_info, email_prompt):
    prompt = f"""
    Company Information
    Name: {company_info.name}
    Company Name: {company_info.company_name}
    Product Name: {company_info.product_name}
    Product Description: {company_info.product_description}

    Customer Information
    Desires: {customer_info.desires}
    Target Audience: {customer_info.target_audience}
    Pains: {customer_info.pains}
    Target Demographic: {customer_info.target_demographic}

    Email Sequence Information
    Number of Emails: {email_sequence_info.number_of_emails}
    Type of Email Sequence: {email_sequence_info.type_of_email_sequence}
    Sequence Purpose: {email_sequence_info.sequence_purpose}
    {email_prompt}
    """
    return prompt


def generate_response(email_prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=email_prompt,
        max_tokens=1000,
        temperature=0.7,
        top_p=0,
        n=1,
    )
    return response["choices"][0]["text"]

def generate_email(company_info, customer_info, email_sequence_info, email_prompt):
    email_prompt = format_background_info_prompt(company_info, customer_info, email_sequence_info, email_prompt)
    return generate_response(email_prompt) 

def create_prompt_for_openai_to_generate_email_sequence(company_info, customer_info, email_sequence_info):
    prompt = "Using the information above, generate a prompt that will be used downstream for another AI to complete the task of creating an email sequence."
    email_prompt = generate_email(company_info, customer_info, email_sequence_info, prompt)
    return email_prompt.replace("\n", " ")  # strip newlines

def create_an_email_sequence(company_info, customer_info, email_sequence_info, prompt):
    return generate_email(company_info, customer_info, email_sequence_info, prompt)

def intialize_background_info():
    company_info = CompanyInformation()
    customer_info = CustomerInformation()
    email_sequence_info = EmailSequenceInformation()
    return company_info, customer_info, email_sequence_info


def create_hooks(company_info, customer_info, email_sequence_info):
    hooks = Hooks()
    return hooks.create_new_hooks(
        hooks, company_info, customer_info, email_sequence_info
    )


def main():
    company_info, customer_info, email_sequence_info = intialize_background_info()
    print(create_hooks(company_info, customer_info, email_sequence_info))
    # prompt = create_prompt_for_openai_to_generate_email_sequence(company_info, customer_info, email_sequence_info)
    # print(prompt)
    # email_sequence = create_an_email_sequence(company_info, customer_info, email_sequence_info, prompt)
    # print(email_sequence)



if __name__ == "__main__":
    main()
