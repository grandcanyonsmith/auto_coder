import os
import json
import logging
from typing import List
from openai_secret_manager import OpenAiSecretManager as openai_secret_manager
from formatter import StringFormatter

import openai  # Module for interacting with OpenAI's APIs


class EmailSequence:
    def __init__(self):
        self.background_information = [
            "I'm a software engineer",
            "I'm looking for a job",
            "I'm looking for a job in the Bay Area",
        ]
        self.desired_outcome = [
            "I want to get a job",
            "I want to get a job in the Bay Area",
        ]
        self.number_of_emails = 2

        self.steps = []
        self.subject_lines = []
        self.value_propositions = []
        self.ctas = []
        self.email_sequence = []

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s"
        )

    def openai_generator(
        self,
        model,
        prompt,
        temperature,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty,
    ):
        secrets = openai_secret_manager.get_secret("openai")
        openai.api_key = secrets

        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        # Return the generated text
        return response["choices"][0]["text"]

    def create_steps(self):
        prompt = f'''Background information:\n"""\n{self.background_information}\n"""\n\nDesired Outcome:\n"""\n{self.desired_outcome}\n"""\n\nNumber of emails in the email sequence:\n"""\n{self.number_of_emails}\n"""\n\nSteps in email sequence\n"""\n'''  # noqa
        steps_text = self.openai_generator(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
        )
        self.steps = [step for step in steps_text.split("\n") if step]
        return formatter.format_everything(self.steps)

    def create_subject_lines(self):
        prompt = f'''Steps in email sequence:\n"""\n{' '.join(self.steps)}\n"""\n\nSubject lines for email sequence:\n"""\n'''
        subject_lines_text = self.openai_generator(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
        )
        self.subject_lines = [
            subject_line
            for subject_line in subject_lines_text.split("\n")
            if subject_line != ""
        ]
        return formatter.format_everything(
            self.subject_lines
        )

    def create_value_propositions(self):
        prompt = f'''Background information:\n"""\n{' '.join(self.background_information)}\n"""\n\nDesired Outcome:\n"""\n{' '.join(self.desired_outcome)}\n"""\n\nNumber of emails in the email sequence:\n"""\n{self.number_of_emails}\n"""\n\nValue propositions for email sequence:\n"""\n'''  # noqa
        value_propositions_text = self.openai_generator(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
        )
        self.value_propositions = [
            value_proposition
            for value_proposition in value_propositions_text.split("\n")
            if value_proposition
        ]
        return formatter.format_everything(self.value_propositions)

    def create_prompt(self):
        return f'''Background information:\n"""\n{self.background_information}\n"""\n\nDesired Outcome:\n"""\n{self.desired_outcome}\n"""\n\nNumber of emails in the email sequence:\n"""\n{self.number_of_emails}\n"""\n\nSteps in email sequence:\n"""\n{' '.join(self.steps)}\n"""\n\nSubject lines for email sequence:\n"""\n{' '.join(self.subject_lines)}\n"""\n\nValue propositions for email sequence:\n"""\n{' '.join(self.value_propositions)}\n"""\n\nCTAs for email sequence:\n"""\n'''

    def generate_ctas(self, prompt, model="text-davinci-003"):
        ctas_text = self.openai_generator(
            model=model,
            prompt=prompt,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
        )
        self.ctas = [cta for cta in ctas_text.split("\n") if cta != ""]
        return formatter.format_everything(self.ctas)

    def create_ctas(self):
        prompt = self.create_prompt()
        return self.generate_ctas(prompt)

    def format_prompt(self):
        return f'''Background information:\n"""\n{self.background_information}\n"""\n\nDesired Outcome:\n"""\n{self.desired_outcome}\n"""\n\nNumber of emails in the email sequence:\n"""\n{self.number_of_emails}\n"""\n\nSteps in email sequence:\n"""\n{' '.join(self.steps)}\n"""\n\nSubject lines for email sequence:\n"""\n{' '.join(self.subject_lines)}\n"""\n\nValue propositions for email sequence:\n"""\n{' '.join(self.value_propositions)}\n"""\n\nCTAs for email sequence:\n"""\n{' '.join(self.ctas)}\n"""\n\nEmail sequence:\n"""\n'''

    def generate_email_sequence(self):
        prompt = self.format_prompt()
        email_sequence_text = self.openai_generator(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
        )
        self.email_sequence = email_sequence_text.split("\n")

    def create_email_sequence(self):
        self.generate_email_sequence()
        self.email_sequence = [email for email in self.email_sequence if email != ""]
        return formatter.format_everything(self.email_sequence)

    def __getitem__(self, index):
        return (
            self.steps[index],
            self.subject_lines[index],
            self.value_propositions[index],
            self.ctas[index],
            self.email_sequence[index],
        )

    def __len__(self):
        return len(self.steps)

    def __repr__(self):
        return f"EmailSequence(steps={self.steps}, subject_lines={self.subject_lines}, value_propositions={self.value_propositions}, ctas={self.ctas}, email_sequence={self.email_sequence})"

    def __str__(self):
        return f"EmailSequence(steps={self.steps}, subject_lines={self.subject_lines}, value_propositions={self.value_propositions}, ctas={self.ctas}, email_sequence={self.email_sequence})"

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self):
            raise StopIteration
        self.index += 1
        return self[self.index - 1]

    def __call__(self):
        return self

    def __add__(self, other):
        return EmailSequence(
            steps=self.steps + other.steps,
            subject_lines=self.subject_lines + other.subject_lines,
            value_propositions=self.value_propositions + other.value_propositions,
            ctas=self.ctas + other.ctas,
            email_sequence=self.email_sequence + other.email_sequence,
        )


if __name__ == "__main__":
    formatter = StringFormatter()
    # Create an email sequence
    email_sequence = EmailSequence(
    )

    # Create the steps
    email_sequence.create_steps()

    # Create the subject lines
    email_sequence.create_subject_lines()

    # Create the value propositions
    email_sequence.create_value_propositions()

    # Create the CTAs
    email_sequence.create_ctas()

    # Create the email sequence
    email_sequence.create_email_sequence()

    # Print the email sequence
    print(email_sequence)
            