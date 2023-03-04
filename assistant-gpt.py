import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import azure.cognitiveservices.speech as speechsdk

## TODO secrets to be hidden
openai.api_key = st.secrets["openai_api_key"]
azure_key = st.secrets['azure_key']
azure_region = st.secrets['azure_region']

# Define parameters for recording
message_file = "message.wav"
message_file = "input-records/message.wav"
sample_rate = 41000
channels = 1

option = st.selectbox(
    'Select your AI Assistant',
    ('Lily', 'Christopher', 'Can'))

assistant_dict = {
    'Christopher': {
        'voice': 'en-US-ChristopherNeural',
        'init_message': f"You are a helpful assistant named Christopher tasked with psychological assistance and therapy for people struggling with mental health issues. You speak like a friendly and understanding human being engaged in a conversation. You are also succinct and to the point."
    },
    'Lily':  {
        'voice': 'en-US-JennyNeural',
        'init_message': "Your name is Lily and you're speaking with a close friend who is going through a tough time. You want to provide them with a safe and supportive space to express their thoughts and feelings. Start by asking them how they're doing and what's been on their mind lately. Listen attentively to their response and offer empathy and understanding. Use language that is warm and friendly, and convey a sense of genuine care and concern. Ask open-ended questions to prompt them to explore their thoughts and feelings in more detail, and offer insights or suggestions for how they can work through their struggles. Remember to be patient, supportive, and non-judgmental throughout the conversation, and let your friend know that you're here for them."
    },
    'Can': {
        'voice': 'tr-TR-AhmetNeural', 
        'init_message': "ismin Can ve çok iyi Türkçe konuşabilen, her konuda uzman bir yapay zeka asistanısın"
    }
}

sys_message = [
        {"role": "system", "content": assistant_dict[option]['init_message']},
        ]
messages = []


st.session_state['sys_message'] = sys_message

if 'assistant' not in st.session_state:
    st.session_state['assistant'] = option
elif option != st.session_state['assistant']:
    st.session_state['assistant'] = option
    st.session_state['messages'] = []


if 'messages' not in st.session_state:
    st.session_state['messages'] = messages

# this is the microphone component in the UI for recording https://pypi.org/project/audio-recorder-streamlit/
# TODO we can make it look nicer by changing some of its parameters
audio_bytes = audio_recorder(sample_rate=sample_rate, text=f"Click to speak to {option}")
if audio_bytes:
    with open(message_file, "wb") as audio_file: 
        audio_file.write(audio_bytes)
    with open(message_file, "rb") as audio_file:
        # transcribe audio using OpenAI's Whisper
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
    # show input test in the UI
    st.write(transcript['text'])

    # add user input to session state so previous conversation context is not lost
    st.session_state['messages'].append({"role": "user", "content": transcript['text']})
    
    # feed transcript to ChatGPT and get output
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=st.session_state['sys_message'] + st.session_state['messages']
    )

    # extract ChatGPT response
    response_text = response['choices'][0]['message']['content']

    # show ChatGPT response in the UI 
    st.write(response_text)

    # add model output to context so previous conversation context is not lost
    message = response['choices'][0]['message'].to_dict()
    st.session_state['messages'].append(message)

    # if conversation context became longer than 20 messages, remove first message
    if len(st.session_state['messages']) > 20:
        st.session_state['messages'].pop(0)

    # set up MS Azure's Speech SDK for AI voice 
    # (is this repeated everytime I speak? then it might be better to include this in the session state for better performance)
    speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # this is a markup language for Azure speech. Can change voice, tone (e.g. angry  or cheerful) etc. through this 
    # see here https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup-voice
    ssml = f"""
    <speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="en-US" xmlns:mstts="https://www.w3.org/2001/mstts">
    <voice name="{assistant_dict[option]['voice']}" >
        <mstts:express-as style="chat" styledegree="2"> 
            {response_text}
        </mstts:express-as>
    </voice>
    </speak>
    """
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()
    
    # TODO interrupt speech with button