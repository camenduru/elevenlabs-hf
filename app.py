import random 
import gradio as gr 
import numpy as np 
from elevenlabs import voices, generate, set_api_key, UnauthenticatedRateLimitError

def generate_voice(text, voice_name, model_name, api_key):
    try:
        audio = generate(text, voice=voice_name, model=model_name, api_key=api_key)
    except UnauthenticatedRateLimitError as e:
        raise gr.Error("Thanks for trying out ElevenLabs TTS! You've reached the free tier limit. Please provide an API key to continue.") 
    except Exception as e:
        raise gr.Error(e)
    return (44100, np.frombuffer(audio, dtype=np.int16))

badges = """
<div style="display: flex">
<span style="margin-right: 5px"> 

[ ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ](https://github.com/elevenlabs-python)
 
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
A demo of the world's most advanced TTS systems, made by [ElevenLabs](https://elevenlabs.io). Eleven Monolingual is designed to generate highly realistic voices in English, where Eleven Multilingual is a single model supporting multiple languages including English, German, Polish, Spanish, Italian, French, Portuguese, and Hindi. 
"""

with gr.Blocks() as block:
    gr.Markdown("# ElevenLabs TTS")
    gr.Markdown(badges)
    gr.Markdown(description)
    
    input_text = gr.Textbox(
        label="Input Text", 
        lines=2, 
        value="Hi! I'm Eleven, the worlds most advanced TTS system.",
        elem_id="input_text"
    )

    all_voices = voices() 
    input_voice = gr.Dropdown(
        [ voice.name for voice in all_voices ], 
        value=random.choice(all_voices).name,
        label="Voice", 
        elem_id="input_voice"
    )

    input_model = gr.Radio(
        ["eleven_monolingual_v1", "eleven_multilingual_v1"],
        label="Model",
        value="eleven_multilingual_v1",
        elem_id="input_model",
    )

    input_api_key = gr.Textbox(
        label="API Key (Optional)",
        lines=1,
        elem_id="input_api_key"
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
        
    inputs = [input_text, input_voice, input_model, input_api_key]
    outputs = [out_audio]
    
    run_button.click(
        fn=generate_voice, 
        inputs=inputs, 
        outputs=outputs, 
        queue=True
    )

block.queue() 
block.launch() 