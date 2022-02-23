import re

def match_phrase(input: str):
    input = input.lower()
    if re.match("goodbye", input):
        response = 1
        return response
    response = re.sub(r'[^\w\s]', '', input)

    response = re.sub(r".*you.*", "let's not talk about me.", response)

    response = re.sub(r"i am | im", "do you enjoy being", response)
    response = re.sub(r"my", "your", response)
    response = re.sub(r"i ([^ ]*) your ([^ ]*)", r"Why do you \1 your \2", response)
    response = re.sub(r"if i (.*) i (.*)", r"why would you like to \1, if you \2", response)
    response = re.sub(r"i feel ([^ ]*)\b", r"When do you feel \1", response)
    response = re.sub(r"i want", r"Why do you want", response)

    response = re.sub(r"what is", "why do you ask about", response) 
    response = re.sub(r"why is", "why do you think", response) 
    response = re.sub(r".* at your (.*)", r"what do you like about \1?", response)
    response = re.sub(r"what should i do to (.*)", r"if you want to \1 you should talk to a professional", response)


    
    response = re.sub(r"^yes", "i see,", response) 
    response = re.sub(r"^no", "why not?", response) 

    response = re.sub(input, "please go on.", response)

    if not response.endswith("."):
        response = response + "?"

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