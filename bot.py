import requests
import discord

# =========================================================
# NOVA AI - FREE FIRE SENSITIVITY ASSISTANT
# =========================================================

DISCORD_BOT_TOKEN = "MTU0Mzk3ODc1ODE3ODg2NTIyNA.GWhR9y.z8Hi5j1LqLZ4_ieiCTkCuud8s1nX0Gy6_1qqaw"
GEMINI_API_KEY = "AIzaSyBMOUtdOIF1vVfTHGp6DrnnOX2-FQERLzw"

GEMINI_MODEL = "gemini-2.5-flash"

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are Nova AI, a friendly Free Fire gaming assistant.

Your main job is to help users with:
- Free Fire sensitivity
- Device-specific sensitivity
- HUD/control suggestions
- Headshot practice
- Recoil-control tips
- General gaming settings
- Android/device optimization suggestions

Never guarantee headshots or claim that a setting is
universally perfect. Give practical starting settings
that users can test and adjust.

Be friendly, natural and concise.
"""

# =========================================================
# DISCORD
# =========================================================

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


# =========================================================
# GEMINI
# =========================================================

def ask_gemini(user_message, username):

    prompt = f"""
The user's Discord display name is: {username}

When replying, naturally address the user by their name
when appropriate. Do not force their name into every sentence.

User message:
{user_message}
"""

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{GEMINI_MODEL}:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    payload = {
        "system_instruction": {
            "parts": [
                {
                    "text": SYSTEM_PROMPT
                }
            ]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 700
        }
    }

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            print("Gemini API Error:", response.text)

            return (
                f"Sorry {username}, AI service mein "
                "abhi problem aa rahi hai. Thodi der baad try karo."
            )

        data = response.json()

        candidates = data.get("candidates", [])

        if not candidates:
            return (
                f"Sorry {username}, mujhe abhi proper "
                "AI response nahi mila."
            )

        parts = candidates[0].get(
            "content", {}
        ).get("parts", [])

        text = "".join(
            part.get("text", "")
            for part in parts
        ).strip()

        if not text:
            return (
                f"Sorry {username}, mujhe abhi response nahi mila."
            )

        return text

    except requests.exceptions.Timeout:

        return (
            f"Sorry {username}, AI response mein timeout ho gaya."
        )

    except Exception as e:

        print("Error:", e)

        return (
            f"Sorry {username}, Nova AI ko response "
            "generate karne mein problem aa gayi."
        )


# =========================================================
# BOT ONLINE
# =========================================================

@bot.event
async def on_ready():

    print("----------------------------------")
    print("Nova AI is ONLINE")
    print(f"Bot: {bot.user}")
    print("----------------------------------")


# =========================================================
# MESSAGE HANDLER
# =========================================================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    # User का Discord display name
    username = message.author.display_name

    # =====================================================
    # DM
    # =====================================================

    if isinstance(message.channel, discord.DMChannel):

        async with message.channel.typing():

            reply = ask_gemini(
                message.content,
                username
            )

        if len(reply) <= 2000:

            await message.reply(reply)

        else:

            for i in range(0, len(reply), 1900):

                await message.channel.send(
                    reply[i:i + 1900]
                )

        return

    # =====================================================
    # SERVER
    # =====================================================

    if bot.user in message.mentions:

        clean_message = message.content

        clean_message = clean_message.replace(
            f"<@{bot.user.id}>",
            ""
        )

        clean_message = clean_message.replace(
            f"<@!{bot.user.id}>",
            ""
        )

        clean_message = clean_message.strip()

        if not clean_message:

            clean_message = "Hello Nova AI"

        async with message.channel.typing():

            reply = ask_gemini(
                clean_message,
                username
            )

        if len(reply) <= 2000:

            await message.reply(reply)

        else:

            for i in range(0, len(reply), 1900):

                await message.channel.send(
                    reply[i:i + 1900]
                )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    if DISCORD_BOT_TOKEN == "PASTE_DISCORD_BOT_TOKEN_HERE":

        print("ERROR: Discord Bot Token add karo.")

    elif GEMINI_API_KEY == "PASTE_GEMINI_API_KEY_HERE":

        print("ERROR: Gemini API Key add karo.")

    else:

        bot.run(DISCORD_BOT_TOKEN)