import os
import openai
import pyttsx3
import speech_recognition as sr
import time

# Set up the ChatGPT API
openai.api_key = ""

#Initialiser le module text to speech 
engine = pyttsx3.init()

# Define functions to convert speech to text and text to speech
def trascribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping Unknown error")


# Define a function to generate a response using ChatGPT
def generate_response(prompt):
    try:
        # print(prompt)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{prompt} , be clear and précise ask questions if needed",
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=2
        )
        return response['choices'][0]['text']
    except Exception as e:
        raise e


# Define a function to speak the responces
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def take_audio_input(word):
    # Setting up the trigger word 
    print(f'Say "{word}" to start recording your question.')

    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == word:
                # recording more audio 
                filename = 'C:\\Users\\rapha\\Desktop\\input.wav'
                print(' __ listening...')
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, 'wb') as f:
                        f.write(audio.get_wav_data())
                return trascribe_audio_to_text(filename)
        except Exception as e:
            print("An error occurred: {}".format(e))


def main():
    # setting up the script
    print(" give this assistant a name :")
    ainame = input(' >> ')

    ok = True
    while ok:
        # transcribing audio to text 
        text = take_audio_input(ainame) 
        print(f" >> {text}")

        if text:
            # generate response using ChatGPT 

            response = generate_response(text)
            print(f" __ {response}")

            # playing the text out loud 
            speak_text(response)
            keep = input("would you like to ask something else [Y/N] : ")
            ok = (keep.lower() == "y")

if __name__ == "__main__":
    main()
