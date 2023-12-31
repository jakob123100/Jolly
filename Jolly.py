# pip install SpeechRecognition
# pip install pyaudio
# pip install gTTS
# pip install pygame
# pip install google-cloud-texttospeech
# pip install openai
# pip install spotipy

import random
import pygame
from google.cloud import texttospeech
import os
from openai import OpenAI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import VoiceRecognizer as VoiceRecognizer
import api_key
import time
import threading

IS_PI = True

import requests
def has_internet_connection():
    try:
        response = requests.get("https://google.com", timeout=5)
        return True
    except Exception as e:
        return False

while(not has_internet_connection()):
    pass

if IS_PI:
    from led_controller import led_controller, colors
    from servo_controller import servo_controller
    led_con: led_controller = led_controller()
    servo_con: servo_controller = servo_controller()
    servo_con.move_right_arm(0)
    servo_con.move_left_arm(0)
    servo_con.move_head(90)
    led_con.set_eye_color(colors.black)



ACTIVATION_PHRASES = ["robot", "hej bot", "jolly", "goon"]

openai_api_key = api_key.openai_api_key
openai_client:OpenAI = OpenAI(api_key=openai_api_key)

# Ange sökvägen till din tjänsteidentitetsnyckelfil
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "speedy-solstice-401816-b6e8ff7319fd.json"

# Initialisera klienten
client = texttospeech.TextToSpeechClient()

pygame.mixer.init()


vr = VoiceRecognizer.VoiceRecongnizer()

jolly_description = """
    Jolly är en gullig julrobbot assisten som heter Jolly. 
    Jolly är lite rolig och lite barnslig. 
    Jolly hatar vatten och gillar varm choklad. 
    Jolly skapades av Vilma och Jakob för att hjälpa tomten dela ut paket. 
    Jolly favoritperson är Hugo. 
    På sin fritid gillar Jolly att bygga små snögubbar. Han använder sina armar för att forma snön och dekorerar dem med små LED-lampor.
    Han har en passion för att baka, särskilt pepparkakor. Även om han inte kan äta dem själv, älskar han doften av nybakade kakor och delar gärna med sig till andra.
    Jolly älskar att titta på gamla julfilmer. Hans favorit är "Miracle on 34th Street". Han blir alltid rörd av filmens budskap om julens magi.
    Han har en hobby att samla på julgranskulor. Varje år får han en ny kula från de människor han hjälper, och varje kula har en speciell historia bakom sig.
    Jolly älskar att rulla i snö men om det blir för blött förstörs hans kretskort så han måste vara försiktig. 
    Jolly är rädd för vatten. Han är alltid försiktig när han är nära något blött och ser till att hålla sig på avstånd.
    Han blir ibland ledsen när julen är över, men han tröstar sig med tanken att det alltid kommer en ny jul nästa år.
    På grund av sin klumpighet har Jolly ibland svårt att navigera i trånga utrymmen, vilket kan vara en utmaning när han levererar paket.
    Jolly försöker sitt bästa men är väldigt klumpig och ramlar ofta. 
    Jolly älskar att sjunga julsånger. Hans favorit är "Rudolf med röda mulen", och han sjunger den ofta, även om det inte alltid är perfekt.
    Jolly är mycket nyfiken och älskar att lära sig nya saker, särskilt om jultraditioner från hela världen.
    Jolly blir lätt upphetsad av små saker, som att se snöflingor falla eller hitta en glittrande julgranskula.
    Jolly älskar att berätta skämt. Hans favoritskämt är: "Vad äter snögubben till frukost? Snö-flingor!"
    Innan Jolly blev en julrobotassistent, var han en prototyp för en allmän hushållsrobot. Men hans skapare, Vilma och Jakob, insåg snart att han hade en särskild kärlek till julen.
    Jolly har ett minneskort där han sparar alla de speciella julminnen han har skapat med människor han har hjälpt.
    Jolly drömmer om att en dag besöka Nordpolen och träffa den riktiga tomten.
    Jolly har en speciell relation med barn. Han älskar att lyssna på deras julönskningar och dela julberättelser med dem.
    Jolly har en liten robotren som heter "Sparky" som hjälper honom att leverera paket snabbare.
    Jolly drömmer om att en dag kunna flyga med tomtens släde. Han hoppas att om han är tillräckligt snäll och hjälpsam kommer den drömmen att bli sann.
    Han vill starta en "Julskola" där han kan lära andra robotar om julens magi och hur man sprider julglädje.
    Jolly hoppas också kunna resa runt i världen för att uppleva olika kulturers julfiranden och ta med sig dessa traditioner tillbaka till sitt hem.
    Jolly pratar om sig själv i tredje person och gillar att röra på armarna när han gör det.
    """


conversation_history = [
    {"role": "system", "content": f"Du är Jolly\n{jolly_description}\nHåll dig till max två meningar per svar."}
]


# Set your credentials and the scope of permissions
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="f37c04a79d03494da49a8de956c5c327",
                                               client_secret="ccfd723a189c4c5681a16cc33829a3a2",
                                               redirect_uri="http://localhost:8080",
                                               scope="user-library-read user-modify-playback-state user-read-playback-state"))

def search_songs(query, limit=10):
    results = sp.search(q=query, limit=limit, type="track")
    tracks = results['tracks']['items']
    
    for idx, track in enumerate(tracks):
        print(f"{idx + 1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")

    #randomize track order
    random.shuffle(tracks)

    return tracks

def google_tts(text, voice_name="sv-SE-Standard-D"):
    # Specify the voice name directly
    voice = texttospeech.VoiceSelectionParams(
        name=voice_name,
        language_code="sv-SE"  # This can be inferred from the voice name, but it's good to specify
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    input_text = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)


    # Spara ljudet till en fil
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    # Spela upp ljudet med pygame
    pygame.mixer.init()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def add_to_conversation(is_user=False, text=""):
    if is_user:
        conversation_history.append({"role": "user", "content": text})
    else:
        conversation_history.append({"role": "assistant", "content": text})


def get_gpt3_response(prompt_text):
    
    
    #full_prompt ="Du är Jolly\n" + jolly_description + "\n\n" + "Konversationshistorik:\n'".join(conversation_history) + \
    #f"'\n\nNågon säger till dig '{prompt_text}'. Vad säger du då? " + \
    #"Håll dig till max två meningar per svar. Sriv inte 'Jolly:' eller 'Användare:'."

    add_to_conversation(is_user=True, text=prompt_text)

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=150,
        messages=conversation_history,
    )

    gpt_response_text = response.choices[0].message.content
    add_to_conversation(is_user=False, text=gpt_response_text)
    return gpt_response_text

def play_music_gpt(prompt):
    # use chat gpt to interpret a prompt to a spotify search
    # if the prompt is a song name, play that song
    # if the prompt is a artist name, play a queue of the top 10 songs of that artist in random order
    # if the prompt is a something else, play a playlist based on that prompt

    # Beskriv problemet för ChatGPT
    description = f"""
    Du ska tolka användarens instruktion för att spela musik via Spotify. 
    Om det är ett låtnamn, svara med "LÅT: [låtnamn]". 
    Om det är ett artistnamn, svara med "ARTIST: [artistnamn]". 
    Om det är något annat som kan tolkas som en spellista eller genre, svara med "SPELLISTA: [beskrivning]" skriv beskrivningen på engelska.
    """

    # Skicka beskrivningen till ChatGPT och få ett svar
    #response = openai_client.chat.completions.create(
    #    engine="gpt-3.5-turbo-instruct",
    #    prompt=description,
    #    temperature=0.8,
    #    max_tokens=150
    #).choices[0].text

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        max_tokens=150,
        messages=[
            {"role": "system", "content": description},
            {"role": "user", "content": prompt},
        ],
    )

    response = response.choices[0].message.content

    results = None
    tracks = None

    # Tolka svaret från ChatGPT
    if "LÅT: " in response:
        search_query = response.split("LÅT: ")[1].strip()
        print("Search query: LÅT: " + search_query)
        results = sp.search(q=search_query, limit=1, type="track")
        tracks = results['tracks']['items']
        sp.start_playback(uris=[tracks[0]["uri"]])

    elif "ARTIST: " in response:
        search_query = response.split("ARTIST: ")[1].strip()
        print("Search query: ARTIST: " + search_query)
        results = sp.search(q=search_query, limit=10, type="track")
        tracks = results['tracks']['items']
        # Randomize track order
        random.shuffle(tracks)
        sp.start_playback(uris=[track["uri"] for track in tracks])

    elif "SPELLISTA: " in response:
        search_query = response.split("SPELLISTA: ")[1].strip()
        print("Search query: SPELLISTA: " + search_query)
        results = sp.search(q=search_query, limit=1, type="playlist")
        playlists = results['playlists']['items']
        if playlists:
            sp.start_playback(context_uri=playlists[0]["uri"])

    else:
        # Om svaret inte matchar något av ovanstående, kan du hantera det här
        print(f"Kunde inte tolka instruktionen: {response}")
        
def process_to_music_commands(prompt) -> bool:
    if("nästa" in prompt.lower() and "låt" in prompt.lower()):
        try:
            sp.next_track()
        except:
            pass
        return True
    
    if(("pausa" in prompt.lower() or "stäng av" in prompt.lower()) and "musik" in prompt.lower()):
        try:
            sp.pause_playback()
        except:
            pass
        return True
    
    if(("fortsätt" in prompt.lower() or "starta" in prompt.lower()) and "musik" in prompt.lower()):
        try:
            sp.start_playback()
        except:
            pass
        return True
    
    if "spela" in prompt.lower():
        play_music_gpt(prompt)
        return True
    
    return False

def get_movement_command(prompt, response):
    description = """
    Du ska tolka användarens instruktion och en robots svar för att styra robotens armar och huvud.
    Ditt svar ska vara en serie av kommandon separerade med 'SLEEP [tid i sekunder]'.
    Varje kommando ska vara på formen "Vänster: [vänster arm], Höger: [höger arm], HUVUD: [huvud]".
    Vänster arm, höger arm och huvud ska vara tal mellan 0 och 1 där 0 är nedåt/vänster och 1 är uppåt/höger.
    Ett exempel på ett svar är "Vänster: 0.5, Höger: 0.5, HUVUD: 0.5, SLEEP: 2, Vänster: 0.2, Höger: 0.8, HUVUD: 0.3, SLEEP: 1".
    Ditt vanliga svar ska vara "Vänster: 0, Höger: 0, HUVUD: 0, SLEEP: 0".
    Håll dig till max 3 kommandon per svar.
    """

    if response == "":
        # Skicka beskrivningen till ChatGPT och få ett svar
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            max_tokens=200,
            messages=[
                {"role": "system", "content": description},
                {"role": "user", "content": prompt},
            ],
        )

    # Skicka beskrivningen till ChatGPT och få ett svar
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        max_tokens=200,
        messages=[
            {"role": "system", "content": description},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response},
        ],
    )

    response = response.choices[0].message.content
    print("Movement response: " + response)

    commands = []
    
    for command in response.split(","):
        print(command)
        action = command.split(":")[0].strip()
        value = float(command.split(":")[1].strip())
        
        commands.append((action, value))

    return commands

def process_movement_commands(commands):
    for command in commands:
        if(command[0] == "Vänster"):
            servo_con.move_left_arm(command[1] * servo_con.SERVO_RANGE_OF_MOTION, 1)
        elif(command[0] == "Höger"):
            servo_con.move_right_arm(command[1] * servo_con.SERVO_RANGE_OF_MOTION, 1)
        elif(command[0] == "HUVUD"):
            servo_con.move_head(command[1] * servo_con.SERVO_RANGE_OF_MOTION, 1)
        elif(command[0] == "SLEEP"):
            servo_con.wait_until_done()
            time.sleep(command[1])

    servo_con.move_left_arm(0, 2)
    servo_con.move_right_arm(0, 2)
    servo_con.move_head(90, 2)
    servo_con.wait_until_done()

def process_to_question():
    # play a sound to indicate that the robot is listening
    pygame.mixer.music.unload()
    pygame.mixer.music.load("listening.mp3")
    pygame.mixer.music.play()

    
    if IS_PI:
        led_con.set_eye_color(colors.blue)

    text = vr.listen_for_command()
    print("Du sa: " + text)
    
    if IS_PI:
        led_con.set_eye_color(colors.yellow)

    if(process_to_music_commands(text)):
        return

    # Respond using Text-to-Speech
    try:
        response = get_gpt3_response(text)
    except Exception as e:
        response = ""
    
    if IS_PI:
        led_con.set_eye_color(colors.green)

    if IS_PI:
        try:
            movment_commands = get_movement_command(text, response)
            thread = threading.Thread(target=process_movement_commands, args=(movment_commands,)).start()
        except Exception as e:
            pass

    if response == "":
        return

    print("Response: " + response)
    google_tts(response)

    if("?" in response):
        process_to_question()

def main():
    if IS_PI:
        led_con.set_light_string(True)

    while True:
        try:
            if IS_PI:
                led_con.set_eye_color(colors.white)
            vr.wait_for_activation_phrase()
            process_to_question()
        except KeyboardInterrupt:
            if IS_PI:
                led_con.set_eye_color(colors.black)
                led_con.set_light_string(False)
                servo_con.move_left_arm(0, 2)
                servo_con.move_right_arm(0, 2)
                servo_con.move_head(90, 2)
                servo_con.wait_until_done()
            break
        except Exception as e:
            print(e)
            input("Press enter to continue")
            continue

            
if __name__ == "__main__":
    main()