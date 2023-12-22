import threading
import time
import speech_recognition as sr
from multiprocessing import Value


class VoiceRecongnizer:
    """
    A class that provides functionality for voice recognition.

    Attributes:
    - recognizer_energy_threshold (int): The energy threshold for voice recognition.
    - recognizer_activation_pause_threshold (float): The pause threshold for detecting activation phrases.
    - recognizer_listen_pause_threshold (int): The pause threshold for listening to commands.
    - recognizer_dynamic_energy_ratio (int): The dynamic energy ratio for voice recognition.
    - activation_phrases (list): A list of activation phrases for voice recognition.
    - recognizer (Recognizer): A speech recognition object.
    - recognizing_processes (list): A list of threads for recognizing audio.
    - __got_activation_phrase (Value): A multiprocessing value for detecting activation phrases.
    """

    recognizer_energy_threshold = 4000
    recognizer_activation_pause_threshold = 0.5
    recognizer_listen_pause_threshold = 1
    recognizer_dynamic_energy_ratio = 3

    activation_phrases = ["robot", "hej bot", "jolly"]
    
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = recognizer_energy_threshold
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_ratio = recognizer_dynamic_energy_ratio
    recognizing_processes = []

    __got_activation_phrase: Value = Value('b', False)

    def __process_audio(self, audio) -> dict:
        """
        Processes audio and returns a dictionary of recognized prompts.

        Args:
        - audio (AudioData): The audio data to be processed.

        Returns:
        - dict: A dictionary of recognized prompts.
        """
        try:
            prompts = self.recognizer.recognize_google(audio, language="sv-SE", show_all=True)
        except sr.UnknownValueError:
            print("Kunde inte förstå ljudet")
        except sr.RequestError:
            print("Kunde inte begära resultat; kontrollera din internetanslutning.")
        except Exception as e:
            print(e)
        
        return prompts

    def __recognize_start_phrase_test(self, audio):
        """
        Recognizes activation phrases from audio.

        Args:
        - audio (AudioData): The audio data to be processed.
        """
        prompts = self.__process_audio(audio)

        if not prompts:
            return

        for prompt in prompts["alternative"]:
            if any(phrase in prompt["transcript"].lower() for phrase in self.activation_phrases):
                self.__got_activation_phrase.value = True

    def __sound_recived_callback(self, recognizer, audio):
        """
        Callback function for recognizing audio.

        Args:
        - recognizer (Recognizer): The speech recognition object.
        - audio (AudioData): The audio data to be processed.
        """
        print("Heard something")
        
        p = threading.Thread(target=self.__recognize_start_phrase_test, args=(audio,))
        self.recognizing_processes.append(p)
        p.start()
        

    def wait_for_activation_phrase(self):
        """
        Waits for an activation phrase to be detected.
        """
        print("Waiting for activation phrase...")
        mic = sr.Microphone()

        self.recognizer.pause_threshold = self.recognizer_activation_pause_threshold
        self.__got_activation_phrase.value = False
        stop_listening = self.recognizer.listen_in_background(mic, self.__sound_recived_callback)

        while self.__got_activation_phrase.value == False:
            time.sleep(0.1)
        
        print("Heard activation phrase")
        stop_listening()

        for p in self.recognizing_processes:
            p.join()

        self.recognizing_processes = []

    def listen_for_command(self):
        """
        Listens for a command and returns the recognized transcript.
        """
        print("Listening for command...")

        self.recognizer.pause_threshold = self.recognizer_listen_pause_threshold
       
        mic = sr.Microphone()
        with mic as source:
            audio = self.recognizer.listen(source)
            prompts = self.__process_audio(audio)
            if prompts:
                return prompts["alternative"][0]["transcript"]
            

if __name__ == "__main__":
    recognizer = VoiceRecongnizer()
    recognizer.wait_for_activation_phrase()
    print("Got activation phrase")
    print(recognizer.listen_for_command())