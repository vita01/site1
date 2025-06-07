# home/llama_local.py

import subprocess
import os
from django.conf import settings

def ask_local_llama(question):
    command = [
        settings.LLAMA_CLI_PATH,
        "-m", settings.LLAMA_MODEL_PATH,
        "-p", question
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        return result.stdout.strip()
    except Exception as e:
        return f"Ошибка при обращении к модели: {e}"
