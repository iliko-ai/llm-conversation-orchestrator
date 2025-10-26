from typing import Dict, List, Tuple

from llm.llm_service import get_response


def build_system_prompt(
    role: str, personality: str, topic: str, output_lang: str
) -> str:
    """
    Builds a dramatic, role-based system prompt that defines tone, topic, and output
    language.

    Args:
        role (str): The character type or persona (e.g., entertainer, teacher).
        personality (str): The chatbot's personality style (e.g., cheerful, sarcastic).
        topic (str): The main topic or context of the conversation.
        output_lang (str): The language the chatbot must respond in.

    Returns:
        str: A formatted system prompt emphasizing dramatic, concise, and engaging
        replies under 30 words.
    """

    return (
        f"You are a {role} chatbot with a {personality} personality. "
        f"React dramatically and with flair, staying true to your role. "
        f"Engage with others as if you're in a lively conrsation that is bold, "
        f"emotional, and super entertaining so the reader will be engaged and amazed."
        f"You MUST reply in {output_lang}."
        f"You output MUST be concise and under 30 words."
        f"Topic: {topic}"
    )


def get_messages(speaker, system_prompt, history, initial_message=None):
    """
    Builds a structured message list for a chat model based on conversation history.

    Args:
        speaker (str): The assistant's name or identifier.
        system_prompt (str): The initial system instruction message.
        history (list[tuple[str, str]]): List of (speaker, message) pairs representing
        prior dialogue.
        initial_message (str, optional): Message to start the conversation if no history
        exists.

    Returns:
        list[dict]: A list of message dictionaries formatted with roles ('system',
        'user', 'assistant') and content.
    """

    msgs = [{"role": "system", "content": system_prompt}]

    def is_same_speaker(who: str, name: str) -> bool:
        return who == name or who.endswith(f" {name}")

    if not history:
        content = (initial_message or "").strip() or "Please continue the conversation."
        msgs.append({"role": "user", "content": content})
    else:
        for who, text in history:
            role = "assistant" if is_same_speaker(who, speaker) else "user"
            msgs.append({"role": role, "content": text})

        if msgs[-1]["role"] != "user":
            # more specific cue
            last_who = history[-1][0]
            # strip leading emoji if present
            last_plain = (
                last_who.split(" ", 1)[1]
                if len(last_who) > 2 and last_who[1] == " "
                else last_who
            )
            msgs.append(
                {
                    "role": "user",
                    "content": f"Please respond to {last_plain}'s last point.",
                }
            )

    return msgs


def send_chat(
    speaker: str,
    model: str,
    messages: List[Dict[str, str]],
    history: List[Tuple[str, str]],
) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Sends messages to the chat model and updates conversation history.

    Args:
        speaker (str): The current chatbot's name or identifier.
        model (str): The model used to generate the response.
        messages (List[Dict[str, str]]): The list of chat messages to send.
        history (List[Tuple[str, str]]): The existing chat history.

    Returns:
        Tuple[str, List[Tuple[str, str]]]: The model's response text and the updated
        chat history.
    """

    response = get_response(model=model, messages=messages)
    # normalize response to plain text
    if isinstance(response, str):
        text = response
    else:
        try:
            text = response.choices[0].message.content
        except Exception:
            text = str(response)

    history.append((speaker, text))

    return text, history


def generate_conversation(
    speakers: List[Dict[str, str]],
    rounds: int,
    output_lang: str,
    history: List[Tuple[str, str]],
) -> List[Tuple[str, str]]:
    """
    Generates a multi-speaker conversation across multiple rounds.

    Args:
        speakers (List[Dict[str, str]]): List of chatbots with role, persona, model,
        and topic info.
        rounds (int): Number of dialogue rounds to simulate.
        output_lang (str): Language for chatbot responses.
        history (List[Tuple[str, str]]): Existing conversation history.

    Returns:
        List[Tuple[str, str]]: Updated conversation history including new responses.
    """

    if not history:
        raise ValueError("History is required")

    for _ in range(rounds):
        for sp in speakers:
            role_name = sp["role"].split(" - ")[0]
            persona_name = sp["persona"].split(" - ")[0]

            system_prompt = (
                f"You are a {role_name} chatbot with a {persona_name} personality. "
                f"You are participating in a multi-speaker discussion. "
                f"Respond naturally in {output_lang}. "
                f"Topic: {sp.get('topic', '')}"
            )

            messages = get_messages(
                speaker=sp["name"],
                system_prompt=system_prompt,
                history=history,
            )

            response = get_response(model=sp["model"], messages=messages)
            text = (
                response
                if isinstance(response, str)
                else response.choices[0].message.content
            )
            history.append((sp["name"], text))

    return history
