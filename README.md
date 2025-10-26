# 🤖 Multi-Speaker Chatbot Conversation App

A **Streamlit-based application** that simulates a multi-speaker conversation between
different AI personalities and roles.
Each chatbot responds dynamically based on its **role**, **personality**, and
**conversation topic**, creating entertaining and dramatic dialogues!

---

## 🌟 Features

- 🧠 **Multiple AI speakers** — create up to 5 distinct chatbots that talk to each other.
- 🎭 **Dynamic roles and personalities** — each bot has a unique purpose and attitude.
- 🌍 **Multi-language output** — responses can be generated in multiple languages (including English, French, Japanese, Simplified & Traditional Chinese, and more).
- 😆 **Dramatic and entertaining tone** — bots express strong personalities for lively, character-driven conversations.
- 💬 **Conversation rounds** — control how many turns each speaker takes.
- 🧍‍♂️ **Custom emojis/avatars** — each speaker's messages are labeled with a unique emoji matching their role.
- 🔄 **Multiple LLM providers** — supports OpenAI, Anthropic, Google Gemini, Groq, Grok, and OpenRouter.
- 📝 **Initial messages** — set custom starting messages for each speaker.
- 🔄 **Conversation history** — maintains context throughout the conversation.

---

## 🧩 App Structure

### **Main File: `app.py`**
The Streamlit UI:
- Lets you configure the number of speakers, their roles, personalities, and starting
messages.
- Displays conversation results with emojis and formatting.
- Supports multilingual output selection.

### **Core Logic**
| File | Purpose |
|------|----------|
| `utils/conversation_generator.py` | Generates the conversation flow between chatbots. |
| `llm/llm_service.py` | Handles interaction with multiple LLM providers (OpenAI, Anthropic, Google, Groq, etc.). |
| `constants/constants.py` | Stores configuration lists for models, roles, personalities, languages, and role avatars. |
| `utils/tools.py` | Utility functions for role emoji mapping. |
| `config/logging_config.py` | Logging configuration for the application. |

---

## ⚙️ How It Works

1. **Select the number of speakers** (2-5) and confirm.

2. **Set the conversation topic** and number of rounds.

3. **Select the output language** for responses.

4. **Configure each speaker:**
   - Name
   - Role (e.g., *Analyst, Comedian, Philosopher, Visionary, etc.*)
   - Personality (e.g., *Sarcastic, Argumentative, Friendly, etc.*)
   - Model (choose from available LLMs: GPT-4o-mini, Claude, Gemini, Llama, etc.)
   - Initial message

5. Click **Submit All Speakers** → then **Start Conversation**.

6. Watch your custom bots interact dramatically with role-specific emojis!

---

## 🌐 Supported Languages. Add more language in constants/constants.py LANGUAGES

- English
- Español (Spanish)
- Français (French)
- Deutsch (German)
- Português (Portuguese)
- Italiano (Italian)
- Русский (Russian)
- العربية (Arabic)
- हिन्दी (Hindi)
- বাংলা (Bengali)
- اردو (Urdu)
- Türkçe (Turkish)
- ภาษาไทย (Thai)
- Tiếng Việt (Vietnamese)
- Indonesia (Indonesian)
- 简体中文 (Simplified Chinese)
- 繁體中文 (Traditional Chinese)
- 日本語 (Japanese)
- 한국어 (Korean)

---

## 🧠 Example

**Topic:** *Should humans trust AI to make ethical decisions?*

| Speaker | Role | Personality | Sample Response |
|----------|------|-------------|-----------------|
| 🧠 Philosopher | Sarcastic | “Ah yes, because machines are *so* good at empathy.” |
| 🤖 Analyst | Professional | “Statistically, AI makes fewer mistakes, but ethics isn’t
about error rates.” |
| 😜 Comedian | Absurdist | “As long as my toaster doesn’t file taxes, I’m fine!” |

---

## 🚀 Run the App

```bash
uv run streamlit run app.py
```

### Prerequisites
- Python 3.10+
- API keys for your chosen LLM providers (OpenAI, Anthropic, Google, Groq, etc.)
- Environment variables set in `.env` file:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `GOOGLE_API_KEY`
  - `GROQ_API_KEY`
  - `GROK_API_KEY`
  - `OPENROUTER_API_KEY`

### Install dependencies
```bash
uv sync
```

### Environment Setup
Create a `.env` file in the project root with your API keys:
```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
GROQ_API_KEY=your_groq_key_here
GROK_API_KEY=your_grok_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
```
