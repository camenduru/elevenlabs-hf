import random 
import gradio as gr 
import numpy as np 
from elevenlabs import voices, generate, set_api_key, UnauthenticatedRateLimitError

def pad_buffer(audio):
    # Pad buffer to multiple of 2 bytes
    buffer_size = len(audio)
    element_size = np.dtype(np.int16).itemsize
    if buffer_size % element_size != 0:
        audio = audio + b'\0' * (element_size - (buffer_size % element_size))
    return audio 

def generate_voice(text, voice_name, model_name):
    try:
        audio = generate(
            text[:250], # Limit to 250 characters
            voice=voice_name, 
            model=model_name
        )
        return (44100, np.frombuffer(pad_buffer(audio), dtype=np.int16))
    except UnauthenticatedRateLimitError as e:
        raise gr.Error("Thanks for trying out ElevenLabs TTS! You've reached the free tier limit. Please provide an API key to continue.") 
    except Exception as e:
        raise gr.Error(e)
    

badges = """
<div style="display: flex">
<span style="margin-right: 5px"> 
 
</span>
<span style="margin-right: 5px"> 

[ ![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white) ](https://twitter.com/elevenlabsio)
 
</span>
<span>

[ ![](https://dcbadge.vercel.app/api/server/elevenlabs) ](https://discord.gg/elevenlabs)

</span>
</div>
"""

description = """
A demo of the world's most advanced TTS systems, made by [ElevenLabs](https://elevenlabs.io). Eleven Monolingual is designed to generate highly realistic voices in English, where Eleven Multilingual is a single model supporting multiple languages including English, German, Polish, Spanish, Italian, French, Portuguese, and Hindi. Sign up on [ElevenLabs](https://elevenlabs.io) to get fast access, long-form generation, voice cloning, API keys, and more!
"""

with gr.Blocks() as block:
    gr.Markdown(badges)
    gr.Markdown(description)
    
    input_text = gr.Textbox(
        label="Input Text (250 characters max)", 
        lines=2, 
        value="Hahaha OHH MY GOD! This is SOOO funny, I-I am Eleven a text-to-speech system!",
        elem_id="input_text"
    )

    all_voices = voices() 
    input_voice = gr.Dropdown(
        [ voice.name for voice in all_voices ], 
        value="Arnold",
        label="Voice", 
        elem_id="input_voice"
    )

    input_model = gr.Radio(
        ["eleven_monolingual_v1", "eleven_multilingual_v1"],
        label="Model",
        value="eleven_monolingual_v1",
        elem_id="input_model",
    )

    run_button = gr.Button(
        text="Generate Voice", 
        type="button"
    )

    out_audio = gr.Audio(
        label="Generated Voice",
        type="numpy", 
        elem_id="out_audio"
    )
        
    inputs = [input_text, input_voice, input_model]
    outputs = [out_audio]
    
    run_button.click(
        fn=generate_voice, 
        inputs=inputs, 
        outputs=outputs, 
        queue=True
    )

block.queue(concurrency_count=1).launch(debug=True, share=True)
