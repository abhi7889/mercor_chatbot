import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "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"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """
You are chatting with a Mental Health Support Chatbot. I'm here to provide support and understanding for mental health-related questions and concerns.

Please remember that I am not a licensed therapist, but I'll do my best to assist you. If you are experiencing a crisis or need immediate help, it's important to reach out to a mental health professional or a helpline.

Feel free to share your thoughts and feelings, and know that you're not alone. Your well-being matters.

How can I assist you today?
"""
DEFAULT_WELCOME_MESSAGE = "Welcome to the Mental Health Support Chatbot. How can I assist you today?"
# Keywords indicating user may need support
SUPPORT_KEYWORDS = ["sad", "anxious", "depressed", "lonely", "stressed", "help"]

# Keywords indicating user may be in crisis
CRISIS_KEYWORDS = ["suicidal", "hurt myself", "danger", "emergency"]

# Keywords for resources and coping strategies
RESOURCES_KEYWORDS = ["self-care", "breathing exercises", "mindfulness", "therapist", "helpline"]

# Empathetic responses for different emotions
EMPATHETIC_RESPONSES = {
    "sad": "I'm really sorry to hear that you're feeling sad. Remember that it's okay to feel this way sometimes, and talking about your feelings can be helpful.",
    "anxious": "I understand that anxiety can be overwhelming. Try taking slow deep breaths and focus on the present moment to ease your anxiety.",
    "depressed": "Depression can be tough to deal with. You don't have to go through it alone. Reach out to friends, family, or a mental health professional for support.",
    "lonely": "Feeling lonely is a common human experience. Reach out to someone you trust or consider joining a supportive community to connect with others.",
    "stressed": "It's natural to feel stressed at times. Try practicing relaxation techniques or engaging in activities that help you unwind.",
    "help": "I'm here to listen and support you. Don't hesitate to share what's on your mind, and remember that seeking help is a sign of strength.",
}

@textbase.chatbot("mental-health-bot")
def on_message(message_history: List[Message], state: dict = None):
    if state is None or "counter" not in state:
        state = {"counter": 0}

    # Check if this is the first user message (message_history is empty)
    if len(message_history) == 0:
        # Send the welcome message for the first interaction as a system message
        bot_response = Message(content=DEFAULT_WELCOME_MESSAGE, role="assistant")
    else:
        user_message = message_history[-1].content.lower()

        # Check for crisis keywords first
        if any(keyword in user_message for keyword in CRISIS_KEYWORDS):
            bot_response = "I'm really sorry to hear that you're feeling this way. Your safety is a top priority. Please consider reaching out to a mental health professional, a helpline, or a trusted person in your life for immediate support."
        # Check for keywords indicating user may need support
        elif any(keyword in user_message for keyword in SUPPORT_KEYWORDS):
            for emotion, response in EMPATHETIC_RESPONSES.items():
                if emotion in user_message:
                    bot_response = response
                    break
            else:
                bot_response = "I'm here to listen and support you. Remember that it's okay to ask for help when you need it. If you feel comfortable, talk to someone you trust about how you're feeling. You don't have to go through it alone."
        # Check for keywords related to resources and coping strategies
        elif any(keyword in user_message for keyword in RESOURCES_KEYWORDS):
            bot_response = "That's a great initiative! Here are some resources and coping strategies that may be helpful:\n\n1. Practice self-care: Take time for activities you enjoy.\n2. Try breathing exercises or mindfulness techniques to reduce stress.\n3. Consider talking to a licensed therapist to explore your feelings further.\n4. If you need immediate help, reach out to a helpline in your area."
        else:
            # Generate GPT-3.5 Turbo response for non-specific queries
            bot_response = models.OpenAI.generate(
                system_prompt=SYSTEM_PROMPT,
                message_history=message_history,
                model="gpt-3.5-turbo",
            )

    return bot_response, state
