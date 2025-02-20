from .constants import MODEL_MESSAGE_FORMAT_MAPPING


def format_local_response(messages: list[dict], model_name: str) -> str:
    message_format = MODEL_MESSAGE_FORMAT_MAPPING.get(model_name, None)

    if message_format is None:
        raise ValueError(
            f"Model {model_name} not supported. Consider adding it to the `MODEL_MESSAGE_FORMAT_MAPPING`."
        )

    formatted_response = ""
    for message in messages:
        if message["role"] == "user":
            formatted_response += message_format["user"].format(
                user_prompt=message["content"]
            )
        elif message["role"] == "assistant":
            formatted_response += message_format["assistant"].format(
                assistant_prompt=message["content"]
            )
        elif message["role"] == "system":
            formatted_response += message_format["system"].format(
                system_prompt=message["content"]
            )
    formatted_response += message_format["end"]
    return formatted_response.lstrip()
