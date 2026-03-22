#!/bin/env python3
#
# source [PYTHON3_VENV_PATH]/activate
#

import ollama

# Send a simple chat message and print the response
response = ollama.chat(
    model='gemma3',
    messages=[
        {'role': 'user', 'content': 'Why is the sky blue?'}
    ],
)

print( response['message']['content'] )
