import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def strip_numbers(text):
    if isinstance(text, list):
        text = '\n'.join(text)
    lines = text.split('\n')
    return [f'{line.lstrip("1234567890.")}' for line in lines if not line.startswith(' ') and line]


def add_numbers_infront_of_list(text):
    if isinstance(text, list):
        text = '\n'.join(text)
    lines = text.split('\n')
    return [f'{i+1}. {line}' for i, line in enumerate(lines) if not line.startswith(' '
                                                                                    ) and line]


def create_value_proposition_for_email_sequence(ctas):
    value_propositions = []
    for cta in ctas:
        prompt = f"Call to action:\n\"\"\"\n{cta}\n\"\"\"\n\nValue proposition for the email:\n\"\"\"\n",
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0
        )
        value_propositions.append(response["choices"][0]["text"])
    return value_propositions


def convert_to_jsonl_format(text):
    jsonl_list = []
    print(text)
    for item in text:
        jsonl_dict = {'step_sequence': item}
        jsonl_list.append(jsonl_dict)
    return jsonl_list


def create_steps_for_email_sequence(background_information, desired_outcome, number_of_emails):
    prompt = f"Background information:\n\"\"\"\n{background_information}\n\"\"\"\n\nDesired Outcome:\n\"\"\"\n{desired_outcome}\n\"\"\"\n\nNumber of emails in the email sequence:\n\"\"\"\n{number_of_emails}\n\"\"\"\n\nSteps in email sequence\n\"\"\"\n",
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0
    )
    return response["choices"][0]["text"]


def create_cta_for_email_sequence(subject_lines):
    ctas = []
    for subject_line in subject_lines:
        prompt = f"Subject line:\n\"\"\"\n{subject_line}\n\"\"\"\n\nCall to action for the email:\n\"\"\"\n",
        response = openai.Completion.create(

            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0
        )
        ctas.append(response["choices"][0]["text"])
    return ctas


def ask_user_for_number_of_emails():
    return 4


def ask_user_for_background_information():
    with open('files/background_information.txt', 'r') as file:
        return file.read().replace('\n', '')


def ask_user_for_desired_outcome():
    return "sign up for webinar after watching youtube ad"


def write_email_sequence_to_file(email_sequence):
    with open('email_sequence.jsonl', 'w') as outfile:
        jsonl_list = convert_to_jsonl_format(email_sequence)
        for item in jsonl_list:
            json.dump(item, outfile)
            outfile.write('\n')


def create_subject_lines_for_email_sequence(steps_in_sequence):
    subject_lines = []
    restart_sequence = "{\"step\": ",
    for step in steps_in_sequence:
        print(step)
        prompt = f"Step in the sequence:\n\"\"\"\n{step}\n\"\"\"\n\nSubject line for the email:\n\"\"\"\n",
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=50,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0
        )
        subject_lines.append(response["choices"][0]["text"])
    return subject_line
def create_email_sequence(background_information, desired_outcome, number_of_emails):
    steps_in_sequence = create_steps_for_email_sequence(
        background_information, desired_outcome, number_of_emails)
    steps_in_sequence = strip_numbers(steps_in_sequence)
    steps_in_sequence = add_numbers_infront_of_list(steps_in_sequence)
    subject_lines = create_subject_lines_for_email_sequence(steps_in_sequence)    ctas = create_cta_for_email_sequence(subject_lines)

    value_propositions = create_value_proposition_for_email_sequence(ctas)
    email_sequence = [
        f"{steps_in_sequence[i]}\nSubject Line: {subject_lines[i]}\nCall to Action: {ctas[i]}\nValue Proposition: {value_propositions[i]}"
        for i in range(len(steps_in_sequence))
    ]
    email_r = []
    for e in email_sequence:
        # now use openai to create the whole email
        prompt = f"{e}\n\nEmail:\n\"\"\"\n",
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=500,
            top_p=.9,
            frequency_penalty=0.2,
            presence_penalty=0.2
        )
        email_r.append(response
                       ["choices"][0]["text"])
    return [
        f"{steps_in_sequence[i]}\nSubject Line: {subject_lines[i]}\nCall to Action: {ctas[i]}\nValue Proposition: {value_propositions[i]}\n\nEmail:\n{email_r[i]}"
        for i in range(len(steps_in_sequence))
    ]


def write_formatted_email_sequence_to_file(formatted_email_sequence):
    with open('formatted_email_sequence.txt', 'w') as outfile:
        for email in formatted_email_sequence:
            outfile.write(email+'\n')
def get_email_sequence():
    with open('email_sequence.txt', 'r') as f:
        sequence = f.read()
        sequence_dict = [{'emails': line.strip()}
                         for line in sequence.split('\n')]

    return sequence_dict
def main():
    background_information = ask_user_for_background_information()
    desired_outcome = ask_user_for_desired_outcome()
    number_of_emails = ask_user_for_number_of_emails()
    email_sequence = create_email_sequence(
        background_information, desired_outcome, number_of_emails)
    write_email_sequence_to_file(email_sequence)
    formatted_email_sequence = get_email_sequence()
    print(formatted_email_sequence)
    write_formatted_email_sequence_to_file(formatted_email_sequence)


if __name__ == "__main__":
    main()
