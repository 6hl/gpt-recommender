CAROT_SYSTEM = """<|system|>
{system_prompt}<|end|>"""

CAROT_USER = """
<|user|>
{user_prompt}<|end|>"""

CAROT_ASSISTANT = """
<|assistant|>
{assistant_prompt}<|end|>"""

CAROT_END_TEMPLATE = """
<|assistant|> """

MODEL_MESSAGE_FORMAT_MAPPING = {
    "Phi-3-mini-4k-instruct.Q4_0.gguf": {
        "system": CAROT_SYSTEM,
        "user": CAROT_USER,
        "assistant": CAROT_ASSISTANT,
        "end": CAROT_END_TEMPLATE,
    },
}
