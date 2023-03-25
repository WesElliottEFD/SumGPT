import streamlit as st
import GPT
import Modules.file_io as file_io
from streamlit_toggle import st_toggle_switch
import Components
import json


def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


def set_openai_persona(persona_rec: str, persona_sum: str):
    st.session_state["OPENAI_PERSONA_REC"] = persona_rec
    st.session_state["OPENAI_PERSONA_SUM"] = persona_sum


def set_param(params: GPT.param):
    st.session_state["OPENAI_PARAMS"] = params


def set_chunk_size(size: int):
    st.session_state['CHUNK_SIZE'] = size


def set_delay(time: int):
    st.session_state['DELAY'] = time


def set_final_summary_mode(mode: bool):
    st.session_state['FINAL_SUMMARY_MODE'] = mode


def _set_config(config_file, key: str, default_value):
    if config_file:
        return file_io.read_json_upload(config_file, key)
    else:
        return default_value

def _set_language(language: str):
    st.session_state['OUTPUT_LANGUAGE'] = language

def _set_legacy(enable: bool):
    st.session_state['LEGACY'] = enable
def _legacy(enable: bool, legacy, experimental):
    if not enable:
        return experimental
    else:
        return legacy


def sidebar():
    with st.sidebar:
        st.markdown("## How to use\n"
                    "1. 🔑 Enter your [OpenAI API key](https://beta.openai.com/account/api-keys)\n"
                    "2. 📁 upload your file\n"
                    "3. 🏃 Run\n"
                    "---")

        with st.expander('⚙️ Configs Import'):
            config_file = st.file_uploader("📁 Import Configs", type=['json'])

        api_input = st.text_input(label="🔑 OpenAI API Key",
                                  placeholder="Enter your OpenAI API key (sk-...)",
                                  type="password",
                                  help="You can get your API key from https://beta.openai.com/account/api-keys",
                                  value=_set_config(config_file, "OPENAI_API_KEY", ""))

        enable_legacy = st_toggle_switch(label="Legacy", default_value=_set_config(config_file, "LEGACY", False))
        enable_final_summary = st_toggle_switch(label="Enable Final Summary",
                                                default_value=_set_config(config_file, "FINAL_SUMMARY_MODE", False))
        if enable_final_summary:
            set_final_summary_mode(True)
        if st.session_state['FINAL_SUMMARY_MODE'] != enable_final_summary:
            set_final_summary_mode(enable_final_summary)

        with st.expander('🤖 Bot Persona'):
            language = st.selectbox('Language', ['English', 'Chinese', 'Japanese', 'Korean', 'Spanish', 'French', 'German'])
            default_persona_rec_legacy = 'Provide a detailed and comprehensive summary of the following content in flawless ' \
                                  f'{language}, ensuring all key points are covered. Create a markdown heading (###) that ' \
                                  f'encapsulates the core information of the content. Make sure it is answered in {language}.'
            default_persona_rec = f"""Write a detailed and comprehensive explanation of the following in perfect {language} with no grammar issues, 
ensuring all key points are covered. Create a markdown heading (###) that encapsulates the core information:""" +  \
"""
                                  
{text}
                                  
Structured markdown summary with heading (###): """
            persona_rec = st.text_area('Bot Persona Recursive',
                                       value=_set_config(config_file, "OPENAI_PERSONA_REC", _legacy(enable_legacy, default_persona_rec_legacy, default_persona_rec)),
                                       help='System message is a pre-defined message used to instruct the assistant at the '
                                            'beginning of a conversation. iterating and '
                                            'experimenting with potential improvements can help to generate better outputs.'
                                            'Make sure to use casual language.',
                                       height=250)
            if enable_final_summary:
                default_persona_sum_legacy = 'identify headings in the transcript and summarise them into five ' \
                                        'headings. Use #### headings in markdown. Under headings, summarise at least ' \
                                        '3 key points and then provide detail explanation of the concept based on the ' \
                                        'following text in the way that can be read fluently, make sense and avoid ' \
                                        'repetition. Make sure to include all information. Write it in beautiful and ' \
                                        f'structured markdown in perfect {language}. '
                default_persona_sum = """Write a detailed summary of the following: 
                
{text}
                                      
Identify and summarise them into five headings. Use #### headings in markdown. Under headings, summarize a list of key points that best encapsulate the core information.""" + \
f"""Structured markdown summary with headings in perfect {language} (####): """

                persona_sum = st.text_area('Bot Persona Total Sum',
                                           value=_set_config(config_file, "OPENAI_PERSONA_SUM", _legacy(enable_legacy, default_persona_sum_legacy, default_persona_sum)),
                                           help='This is a pre-defined message for total summarization that is used to'
                                                'instruct the assistant at the beginning of a conversation. ',
                                           height=300)
            else:
                persona_sum = ""

        with st.expander('🔥 Advanced Options'):
            model_options = ['gpt-3.5-turbo', 'gpt-4']
            model_index = model_options.index(_set_config(config_file, "MODEL", 'gpt-3.5-turbo'))
            model = st.selectbox("Model", options=model_options, index=model_index)

            if model == 'gpt-4':
                max_chunk = 4000
            else:
                max_chunk = 2500
            chunk_size = st.slider('Chunk Size (word count)', min_value=0, max_value=max_chunk, step=20,
                                   value=_set_config(config_file, "CHUNK_SIZE", 800))
            max_tokens_rec = st.slider('Max Tokens - Recursive Summary', min_value=0, max_value=4090, step=20,
                                       value=_set_config(config_file, "MAX_TOKENS_REC", 250))
            if enable_final_summary:
                max_tokens_final = st.slider('Max Tokens - Final Summary', min_value=0, max_value=4090, step=20,
                                             value=_set_config(config_file, "MAX_TOKENS_FINAL", 650))
            else:
                max_tokens_final = 0
            temperature = st.slider('Temperature', min_value=0.0, max_value=1.0, step=0.05,
                                    value=_set_config(config_file, "TEMPERATURE", 0.7))
            top_p = st.slider('Top P', min_value=0.0, max_value=1.0, step=0.05,
                              value=_set_config(config_file, "TOP_P", 1.0))
            frequency_penalty = st.slider('Frequency Penalty', min_value=0.0, max_value=2.0, step=0.1,
                                          value=_set_config(config_file, "FREQUENCY_PENALTY", 0.0))
            presence_penalty = st.slider('Presence Penalty', min_value=0.0, max_value=2.0, step=0.1,
                                         value=_set_config(config_file, "PRESENCE_PENALTY", 0.0))
            if st_toggle_switch(label="Delay (free openAI API user)",
                                default_value=_set_config(config_file, "ENABLE_DELAY", False)):
                delay = st.slider('Delay (seconds)', min_value=0, max_value=5, step=1,
                                  value=_set_config(config_file, "DELAY_TIME", 1))
            else:
                delay = 0
            param = GPT.param.gpt_param(
                model=model,
                max_tokens_final=max_tokens_final,
                max_tokens_rec=max_tokens_rec,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            )

        st.download_button(label="📥 Export Configs",
                           data=json.dumps({
                               "OPENAI_API_KEY": api_input,
                               "FINAL_SUMMARY_MODE": enable_final_summary,
                               "OPENAI_PERSONA_REC": persona_rec,
                               "OPENAI_PERSONA_SUM": persona_sum,
                               "CHUNK_SIZE": chunk_size,
                               "MAX_TOKENS_REC": max_tokens_rec,
                               "MAX_TOKENS_FINAL": max_tokens_final,
                               "TEMPERATURE": temperature,
                               "TOP_P": top_p,
                               "FREQUENCY_PENALTY": frequency_penalty,
                               "PRESENCE_PENALTY": presence_penalty,
                               "MODEL": model,
                               "ENABLE_DELAY": delay > 0,
                               "DELAY_TIME": delay
                           }, indent=4),
                           file_name="configs.json")
        Components.Info.info()

        if api_input:
            set_openai_api_key(api_input)

        if persona_rec:
            set_openai_persona(persona_rec, persona_sum)
        _set_language(language)
        set_chunk_size(chunk_size)
        set_param(param)
        set_delay(delay)
        _set_legacy(enable_legacy)