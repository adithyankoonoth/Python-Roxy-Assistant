import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import operator

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def perform_math(expression):
    try:
        operators = {
            'plus': '+',
            'minus': '-',
            'multiply': '*',
            'multiplied': '*',
            'times': '*',
            'divide': '/',
            'divided': '/'
        }
        
        for word, symbol in operators.items():
            expression = expression.replace(word, symbol)
        
        parts = expression.split()
        numbers = []
        op = None
        
        for part in parts:
            if part.replace('.', '').isdigit():
                numbers.append(float(part))
            elif part in ['+', '-', '*', '/']:
                op = part
        
        if len(numbers) != 2 or op is None:
            return None
            
        operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        
        result = operations[op](numbers[0], numbers[1])
        return result
    except:
        return None

def get_wikipedia_info(query):
    try:
        query = query.strip()
        info = wikipedia.summary(query, sentences=10)
        return info
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple matches. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "Sorry, I could not find any information about that topic"
    except Exception as e:
        return f"Sorry, an error occurred: {str(e)}"

def take_command():
    command = ''  
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'roxy' in command:
                command = command.replace('roxy', '')
            print(f"Recognized command: {command}")  
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    return command.strip()

def run_roxy():
    command = take_command()
    if not command:  
        return
        
    print(f"Processing command: {command}") 
    
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('playing ' + song)
        pywhatkit.playonyt(song)

    elif 'who are you' in command:
        talk('my name is roxy')

    elif 'my name is' in command:
        talk('Hey there! , nice to meet you. how can i assist you ? do you wanna hear a song ?')
    
    elif ' created you' in command:
        talk('i was created by Adithyan ,also known as ak,when he bunked his university lectures on 4th january 2025 at 12:45 PM.')

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    
    elif 'calculate' in command:
        expression = command.replace('calculate', '')
        result = perform_math(expression)
        if result is not None:
            talk(f'The result is {result}')
        else:
            talk('Sorry, I could not perform that calculation')
    
    elif 'tell me about' in command:
        query = command.replace('tell me about', '').strip()
        print(f"Searching Wikipedia for: {query}") 
        info = get_wikipedia_info(query)
        print(info)
        talk(info)
    
    elif 'who is' in command or 'who the heck is' in command:
        query = command.replace('who is', '').replace('who the heck is', '').strip()
        print(f"Searching Wikipedia for: {query}")  
        info = get_wikipedia_info(query)
        print(info)
        talk(info)
    
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    
    else:
        talk('Please say the command again.')

while True:
    try:
        run_roxy()
    except KeyboardInterrupt:
        print("\nExiting program...")
        break