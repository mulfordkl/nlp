import re

def match_phrase(input: str):
    input = input.lower()
    if re.match("goodbye", input):
        response = 1
        return response

    response = re.sub(r"^yes", "I see", input)
    response = re.sub(r"^no", "Why not?", response)
    response = re.sub(r".*you.*", "Let's not talk about me", response)
    response = re.sub(r"i am", "Do you enjoy being", response)
    response = re.sub(r"what is", "Why do you ask about", response)
    response = re.sub(r"why is", "Why do you think", response)
    response = re.sub(r"my", "Your", response)
    if input is response:
        response = "Please go on."

    return response.capitalize()

def main():
    print("Hello. Please tell me about your problems.")
    while True:
        user_input = input("> ")
        response = match_phrase(user_input)
        if response == 1:
            print("Goodbye!")
            break
        else:
            print(response)
        



if __name__ == '__main__':
    main()