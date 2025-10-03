# -*- coding: utf-8 -*-
import os
from .local_adapter import LocalAdapter
# (Opcional futuro) from .openai_adapter import OpenAIAdapter

def get_provider():
    provider = os.environ.get("AI_PROVIDER", "local").lower()
    if provider == "local":
        return LocalAdapter()
    # elif provider == "openai":
    #     return OpenAIAdapter(api_key=os.environ.get("AI_API_KEY",""))
    return LocalAdapter()
