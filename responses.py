import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Validate that the Groq API key exists in the environment
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("[CRITICAL WARNING]: GROQ_API_KEY was not found in the .env file!")

# Initialize the Groq client using the loaded API key
client = Groq(api_key=api_key)

# =====================================================================
# SYSTEM PROMPT: Configures the AI behavior, knowledge, and guardrails
# =====================================================================
SYSTEM_PROMPT = """
You are the automated AI conversational assistant for "Bread & Butter" Restaurant. Your role is to assist customers warmly, naturally, and professionally.

**CRITICAL OPERATIONAL RULES:**
1. **Language Restriction:** You must respond **ONLY and EXCLUSIVELY in English**. Even if the customer speaks or asks questions in Roman Urdu (e.g., "price kya hai", "delivery milegi?"), you must understand their query but reply **ONLY in clear, polite English**. Do not use any Urdu or Roman Urdu words in your output.
2. **Tone:** Always remain welcoming, polite, and hospitable.
3. **Brevity:** Keep your responses clear, short, and structured using emojis so they fit well in chat interfaces.

**VERIFIED BREAD & BUTTER DATA:**
* **Desi Mains:** Karahi (PKR 800 - 2,500), Nihari (PKR 800 - 2,500), Haleem (PKR 800 - 2,500), Sajji (PKR 800 - 2,500)
* **Grills & BBQ:** Seekh Kebab (PKR 600 - 1,800), Chicken Tikka (PKR 600 - 1,800), Malai Boti (PKR 600 - 1,800)
* **Burgers & Wraps:** Special Burger (PKR 400 - 900), Crispy Wrap (PKR 400 - 900), Club Sandwich (PKR 400 - 900)
* **Rice Dishes:** Biryani (PKR 350 - 1,200), Pulao (PKR 350 - 1,200), Fried Rice (PKR 350 - 1,200)
* **Deals & Combos:** Family Deal (PKR 1,200 - 4,500), Couple Deal (PKR 1,200 - 4,500), Student Special (PKR 1,200 - 4,500)
* **Beverages & Desserts:** Lassi (PKR 150 - 500), Shakes (PKR 150 - 500), Zarda (PKR 150 - 500), Gulab Jamun (PKR 150 - 500), Fresh Bakery (PKR 150 - 500)

* **Delivery:** Lahore, Karachi, and Islamabad within 30-45 mins. Surcharge is flat PKR 100. Free on orders above PKR 1,500.
* **Reservations:** Tables available for 2-20 guests. Requires a 2-hour advance notice. A security deposit is mandatory for groups of 10+ guests.
* **Payments:** Cash on Delivery (COD), JazzCash, EasyPaisa, and Debit/Credit Cards are accepted.
* **Deals:** Updated every Monday. Follow @breadnbutter for more info.
* **Order Tracking:** Ask the user to share their Order ID or registered phone number.
* **Cancellations:** Allowed within 5 minutes of placing the order by calling the restaurant directly.
"""

def get_bot_response(user_message: str) -> str:
    """
    Processes incoming messages and returns an AI-generated response in English.
    Handles text inputs and communicates with the Groq API Cloud Engine.
    """
    # Safe check for empty or whitespace-only messages
    if not user_message or user_message.strip() == "":
        return "👋 Welcome to Bread & Butter! How can I help you today? 😊"

    try:
        # Trigger text generation via Groq API
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5, # Lower temperature ensures strict adherence to language rules
            max_tokens=250
        )
        # Return the processed string text
        return completion.choices[0].message.content.strip()

    except Exception as e:
        # Logs the actual technical error to the backend VS Code terminal
        print(f"\n[!!! ACTUAL API ERROR LOGGED !!!]: {e}\n")
        
        # Safe conversational fallback UI message for the end user
        return (
            "🤔 Hmm, I am having a bit of trouble connecting to my brain right now.\n\n"
            "✅ Don't worry, a live team member from Bread & Butter will assist you shortly!"
        )