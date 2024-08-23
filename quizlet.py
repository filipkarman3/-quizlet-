import random
import pretty_errors
import math as maths

# pretty colours -------------------------------------------------------------------------------------- #
class C:
    reset = "\033[0m"
    red = "\033[31m"
    green = "\033[32m"
    cyan = "\033[96m"
    bold = "\033[1m"

# quizlet class --------------------------------------------------------------------------------------- #
class Quizlet:
    def __init__(s):
        s.words = s.read_file()
        random.shuffle(s.words)
        s.main_loop()

    # read items from text file ----------------------------------------------------------------------- #
    def read_file(s):
        text = open("quizlet.txt", "r")
        words = []

        line = text.readline().split(",")
        while (len(line) == 5):
            words.append(line[:4])
            words[-1][0] = words[-1][0].split(";")
            words[-1][1] = words[-1][1].split(";")
            line = text.readline().split(",")
        return words

    # main loop --------------------------------------------------------------------------------------s #
    def main_loop(s):
        s.max_wrong = 8 # editable
        s.wrong = 0
        s.looped_once = False
        s.word = s.choose_random_starting_point()

        while (True):
            if (s.word.chosen):
                s.response = s.ask_user_question()
                if (s.response[0] == "find"):
                    s.find()
                elif (s.response[0] == "-a"):
                    s.words.append(s.add_word())
                elif (s.response[0] == "-am"):
                    s.words.append(s.add_word_multiple())
                elif (s.response[0] in ["-h", "-help"]):
                    s.print_help()
                elif (s.response[0] == "-x"):
                    s.exit()
                elif (s.response[0] == "-reshuffle"):
                    random.shuffle(s.words)
                else:
                    s.wrong += s.word.respond(s.response[0])
                    s.words[s.word.index] = s.word.reformat()

                    if (s.wrong > s.max_wrong): s.restart()

            s.word = s.choose_next_word()

    # looping through list ---------------------------------------------------------------------------- #
    def choose_random_starting_point(s):
        s.pos = random.randint(0, len(s.words)-1)
        return Word(s.pos, s.words[s.pos])

    def choose_next_word(s):
        s.pos = s.pos + 1 if (s.pos + 1 < len(s.words)) else 0
        s.looped_once = True if (s.pos == 0) else False
        return Word(s.pos, s.words[s.pos])

    # ask user question ------------------------------------------------------------------------------- #
    def ask_user_question(s):
        return input(f"{C.bold}\n{s.word.question}: {C.reset}").strip().lower().split(";")

    # find -------------------------------------------------------------------------------------------- #
    def find(s):
        # check if the user entered the command correctly. If not, ask the user the next question
        validated = s.validate_input()
        if not validated: return

        s.found = s.search_for_word() # find the word the user typed in, return all found instances as a list of positions in s.words
        if (len(s.found) == 0): print("The word could not be found")
        else:
            s.word_selected = s.print_find_results_and_get_user_selection() # print the found words nicely, ask the user which one he wants, return a value corresponding to the index of the word in s.words
            if (s.word_selected == "x"): return
            while (True):
                response = s.find_word_ask_user_action() # ask the user what they want to do with the word
                if (response == "edit"):
                    s.words[s.word_selected] = s.add_word_multiple()
                elif (response == "add-english"):
                    s.words[s.word_selected][0].append(s.found_word_add_english())
                elif (response == "add-spanish"):
                    s.words[s.word_selected][1].append(s.found_word_add_spanish())
                elif (response == "remove"):
                    if (s.found_word_remove() == 1): return
                elif (response in ["h", "help"]):
                    s.print_help()
                elif (response == "x"):
                    return
                else:
                    print("Enter a valid value. Type \"help\" if stuck")

    # make sure the user has entered dato in the correct format
    def validate_input(s):
        if (len(s.response)) < 2:
            print("Incorrect formatting. find;TERM")
            return False
        return True

    # find the word the user is looking for
    def search_for_word(s):
        to_search = s.response[1]
        found = []

        for i in range(len(s.words)):
            for english_word in s.words[i][0]:
                if (to_search in english_word):
                    if (i not in found): found.append(i)

            for spanish_word in s.words[i][1]:
                if (to_search in spanish_word):
                    if (i not in found): found.append(i)

        return found

    # here's the found words, which one do you want to select?    
    def print_find_results_and_get_user_selection(s):
        while (True):
            try:
                print("\nHere is a list of found words. Select the desired number.")
                for num, index in enumerate(s.found, 1):
                    word = s.words[index]
                    print(f"{num}) {word[0]}, {word[1]}")

                response = input(" > ").strip().lower()
                if (response == "x"): return response
                
                response = int(response)
                if (response > len(s.found)): raise Exception()
                else: return s.found[response-1]
            except:
                print("Enter a valid value")

    # here's the data on the word, now what do you want to do with it?
    def find_word_ask_user_action(s):
        return input("\nWhat do you want to do? ").strip().lower()

    # add english terms to an existing word
    def found_word_add_english(s):
        while True:
            english = input("\nEnter an english term: ").lower().strip()
            if (("," in english) or (";" in english) or (english in ["", "x"])):
                print("Cannot include commas or semicolons")
            else:
                return english

    # add spanish terms to an existing word
    def found_word_add_spanish(s):
        while True:
            spanish = input("\nEnter a spanish term: ").lower().strip()
            if (("," in spanish) or (";" in spanish) or (spanish in ["", "x"])):
                print("Cannot include commas or semicolons, or be the letter x")
            else:
                return spanish

    # remove a found word
    def found_word_remove(s):
        if (len(s.words) <= 2):
            print("Cannot remove a word if there are less than three words in total")
        else:
            s.words.pop(s.word_selected)
            return 1 # if successfully removed a word, go back to asking questions

    # add word ---------------------------------------------------------------------------------------- #
    def add_word(s):
        word = [[], [], 0, 0]

        while True:
            english = input(f"{C.bold}Enter an english term: {C.reset}").lower().strip()
            if (("," in english) or (";" in english) or (english == "")):
                print(f"{C.red}Cannot have commas or semicolons in the term{C.reset}\n")
            else:
                word[0].append(english)
                break

        while True:
            spanish = input(f"{C.bold}Enter a spanish term: {C.reset}").lower().strip()
            if (("," in spanish) or (";" in spanish) or (spanish == "")):
                print(f"{C.red}Cannot have commas or semicolons in the term{C.reset}\n")
            else:
                word[1].append(spanish)
                break

        return word

    def add_word_multiple(s):
        word = [[], [], 0, 0]

        print()
        while True:
            english = input(f"{C.bold}Enter an english term (x to exit): {C.reset}").lower().strip()

            if (english == "x"):
                if (len(word[0]) == 0): print(f"{C.red}You must add enter at least one english term{C.reset}")
                else: break
            elif (("," in english) or (";" in english) or (english == "")):
                print(f"{C.red}Cannot have commas or semicolons in the term\n{C.reset}")
            else:
                word[0].append(english)

        print()
        while True:
            spanish = input(f"{C.bold}Enter a spanish term (x to exit): {C.reset}").lower().strip()

            if (spanish == "x"):
                if (len(word[1]) == 0): print(f"{C.red}You must add enter at least one spanish term\n{C.reset}")
                else: break
            elif (("," in spanish) or (";" in spanish) or (spanish == "")):
                print(f"{C.red}Cannot have commas or semicolons in the term\n{C.reset}")
            else:
                word[1].append(spanish)

        return word

    # print help -------------------------------------------------------------------------------------- #
    def print_help(s):
        print(f"{C.cyan}\nx - go back\nfind;X - search for X\n\tremove - get rid of the word\n\tedit - edit the word\n\tadd-english - add an english term to the word\n\tadd-spanish - add a spanish term to the word\n-a - add a word\n-am - add a word with multiple translations\n-reshuffle - self-explanatory{C.reset}")

    # exit -------------------------------------------------------------------------------------------- #
    def exit(s):
        total_successes = 0
        total_attempts  = 0
        for word in s.words:
            total_attempts  += int(word[2])
            total_successes += int(word[3])
        if total_attempts == 0: print("\nLifetime success rate: 0%")
        else:                   print(f"\nLifetime success rate: {int(100*total_successes/total_attempts)}%")

        to_write = ""
        for word in s.words:
            to_write_small = ""
            for i in range(len(word[0])):
                if (i != len(word[0])-1):
                    to_write_small += f"{word[0][i]};"
                else:
                    to_write_small += f"{word[0][i]},"

            for i in range(len(word[1])):
                if (i != len(word[1])-1):
                    to_write_small += f"{word[1][i]};"
                else:
                    to_write_small += f"{word[1][i]},"

            to_write_small += f"{word[2]},{word[3]},\n"
            to_write += to_write_small

        open("quizlet.txt", "w").write(to_write)
        exit()

    # reshuffle the words until the 10th wrong one ---------------------------------------------------- #
    def restart(s):
        if (not s.looped_once):
            s.wrong = 0
            s.temp = s.words[:s.pos+1]
            random.shuffle(s.temp)
            s.words = s.temp + s.words[s.pos+1:]
            s.pos = 0

# word class ------------------------------------------------------------------------------------------ #
class Word:
    def __init__(s, index, word):
        s.index = index
        s.english = word[0]
        s.spanish = word[1]
        s.attempts_total = int(word[2])
        s.attempts_success = int(word[3])

        # s.chosen = (s.attempts_success == 0) or ((s.attempts_success/s.attempts_total - 0.03)**3<random.randint(0, 100)/100)
        # s.chosen = (s.attempts_success == 0) or ((1/(1+maths.e**(-10*(s.attempts_success/s.attempts_total-0.25))) - 0.03)<random.randint(0, 100)/100)
        s.chosen = False
        if s.attempts_success == 0: s.chosen = True
        elif (s.attempts_success/s.attempts_total < 0.4) and random.randint(0, 1000) > 200: s.chosen = True
        elif (s.attempts_success/s.attempts_total < 0.6) and random.randint(0, 1000) > 900: s.chosen = True
        elif random.randint(0, 1000) > 990: s.chosen = True
        s.generate_question_and_response()
    
    def generate_question_and_response(s):
        if (random.randint(0, 3) != 0):
            s.question = random.choice(s.english)
            s.answer = s.spanish
        else:
            s.question = random.choice(s.spanish)
            s.answer = s.english

    def respond(s, response):
        s.attempts_total += 1
        if (response in s.answer):
            s.attempts_success += 1
            print(f"{C.green}{s.answer}{C.reset}")
            return 0 # add nothing to the wrong count
        else:
            print(f"{C.red}{s.answer}{C.reset}")
            return 1 # wrong += 1

    def reformat(s):
        return [s.english, s.spanish, s.attempts_total, s.attempts_success]

Quizlet()