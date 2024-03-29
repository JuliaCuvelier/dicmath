from pathlib import Path
import re

import azure.cognitiveservices.speech as speechsdk
from playsound import playsound
from pylatex import Document, Math, Section
from sortedcontainers import SortedDict

from dicmath import app


def items_to_equations(items):
    """Converts a list of items to a nested SortedDict of equations.

    Args:
        items (list): A list of Item objects.

    Returns:
        SortedDict: A nested SortedDict containing the equations.
    """
    equations = SortedDict()

    for item in items:
        equations[item.equation] = equations.get(item.equation, SortedDict())
        equations[item.equation][item.line] = equations[item.equation].get(item.line, SortedDict())
        equations[item.equation][item.line][item.block] = item

    return equations


def parse_equation(text):
    """Parses an equation from a given text.

    Args:
        text (str): The text containing the equation.

    Returns:
        list: A list of strings representing the parsed equation.
    """
    L = re.split(r'(\=|\+|\-|\(|\))', text)

    count, temp, result = 0, '', []

    for elem in L:
        if elem == '(':
            count += 1
        elif elem == ')':
            count -= 1

        temp = f'{temp}{elem}'

        if count == 0:
            result.append(temp.strip())
            temp = ''

    result = list(filter(lambda x: x, result))
    return result


def speech_to_text():
    """Transcribes speech to text using Azure Cognitive Services.

    Returns:
        str: The transcribed text.
    """
    speech_config = speechsdk.SpeechConfig(subscription=app.config['AZURE_SPEECH_KEY'], region=app.config['AZURE_SPEECH_REGION'])
    speech_config.speech_recognition_language = app.config['LANGUAGE']

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    base_path = Path(__file__).resolve().parent
    beep_path = base_path / 'static' / 'audio' / 'beep.wav'
    reversed_beep_path = base_path / 'static' / 'audio' / 'beep_reversed.wav'

    print('Speak into your microphone!')
    playsound(str(beep_path))
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    playsound(str(reversed_beep_path))

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print('No speech could be recognized: {}'.format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print('Speech Recognition canceled: {}'.format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print('Error details: {}'.format(cancellation_details.error_details))
            print('Did you set the speech resource key and region values?')

    return ''


def text_to_speech(text):
    """Converts text to speech using Azure Cognitive Services.

    Args:
        text (str): The text to convert to speech.
    """
    speech_config = speechsdk.SpeechConfig(subscription=app.config['AZURE_SPEECH_KEY'], region=app.config['AZURE_SPEECH_REGION'])
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_config.speech_synthesis_voice_name = 'fr-FR-HenriNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print('Speech synthesized for text [{}]'.format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print('Speech synthesis canceled: {}'.format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print('Error details: {}'.format(cancellation_details.error_details))
                print('Did you set the speech resource key and region values?')


def text_to_math(text):
    """Converts natural language text to a mathematical expression.

    Args:
        text (str): The text containing the mathematical expression.

    Returns:
        str: The mathematical expression as a string.
    """

    mapping = {
        'au': '',
        'carré': '^ 2',
        'cube': '^ 3',
        'de': '2',
        'égal': '=',
        'égale': '=',
        'fermer': ')',
        'fois': '*',
        'moins': '-',
        'ouvrir': '(',
        'plus': '+',
        'puissance': '^',
        'sur': '/',
        'un': '1',
        'une': '1',
    }

    text = text.translate(str.maketrans('', '', ',.?')) # Remove the punctuation
    L = text.split()

    for i, elem in enumerate(L):
        elem = elem.lower()
        if elem in mapping:
            L[i] = mapping[elem]

    return ' '.join(filter(lambda x: x, L))


def export_pdf(equations):
    """Exports equations as a PDF file using pylatex.

    Args:
        equations (SortedDict): A nested SortedDict containing the equations.
    """
    doc = Document()

    for equation_number, equation in equations.items():
        with doc.create(Section(f'Equation {equation_number}')):
            for line_number, line in equation.items():
                doc.append(Math(data=[block.data for block in line.values()], escape=False))

    path = Path.home() / 'Downloads' / 'dicmath'
    doc.generate_pdf(path, compiler='pdflatex')
