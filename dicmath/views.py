import azure.cognitiveservices.speech as speechsdk
from flask import redirect, render_template, session

from dicmath import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/listen', methods=['POST'])
def listen():
    text = speech_to_text()
    text_to_speech(text)

    math = text_to_math(text)
    session['text'] = math

    return redirect('/')


def speech_to_text():
    speech_config = speechsdk.SpeechConfig(subscription=app.config['AZURE_SPEECH_KEY'], region=app.config['AZURE_SPEECH_REGION'])
    speech_config.speech_recognition_language = app.config['LANGUAGE']

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print('Speak into your microphone.')
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

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
    mapping = {
        'égale': '=',
        'plus': '+',
        'moins': '-',
        'fois': '*',
        'sur': '/',
        'au': '',
        'carré': '^ 2',
        'cube': '^ 3',
        'un': '1',
    }

    text = text.translate(str.maketrans('', '', '.')) # Remove the '.' characters
    L = text.split()

    for i, elem in enumerate(L):
        elem = elem.lower()
        if elem in mapping:
            L[i] = mapping[elem]

    return ' '.join(filter(lambda x: x, L))
