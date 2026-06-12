import os
from groq import Groq
from dotenv import load_dotenv

# .env file load karein
load_dotenv()

# API Key check karne ke liye validation
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("[CRITICAL WARNING]: .env file mein GROQ_API_KEY nahi mili!")

# Groq client initialize karein
client = Groq(api_key=api_key)

SYSTEM_PROMPT = """
You are the automated AI conversational assistant for "Bread & Butter" Restaurant. Your role is to assist customers warmly, naturally, and professionally.

**OPERATIONAL RULES:**
1. **Language:** Respond in English or Mixed Urdu/English (Roman Urdu) depending on how the customer speaks to you.
2. **Tone:** Welcoming, polite, and helpful.
3. **Brevity:** Keep your responses clear, short, and structured using emojis.

**VERIFIED BREAD & BUTTER DATA:**
* **Desi Mains:** Karahi (PKR 800 - 2,500), Nihari (PKR 800 - 2,500), Haleem (PKR 800 - 2,500), Sajji (PKR 800 - 2,500)
* **Grills & BBQ:** Seekh Kebab (PKR 600 - 1,800), Chicken Tikka (PKR 600 - 1,800), Malai Boti (PKR 600 - 1,800)
* **Burgers & Wraps:** Special Burger (PKR 400 - 900), Crispy Wrap (PKR 400 - 900), Club Sandwich (PKR 400 - 900)
* **Rice Dishes:** Biryani (PKR 350 - 1,200), Pulao (PKR 350 - 1,200), Fried Rice (PKR 350 - 1,200)
* **Deals & Combos:** Family Deal (PKR 1,200 - 4,500), Couple Deal (PKR 1,200 - 4,500), Student Special (PKR 1,200 - 4,500)
* **Beverages & Desserts:** Lassi (PKR 150 - 500), Shakes (PKR 150 - 500), Zarda (PKR 150 - 500), Gulab Jamun (PKR 150 - 500), Fresh Bakery (PKR 150 - 500)

* **Delivery:** Lahore, Karachi, Islamabad within 30-45 mins. Surcharge PKR 100. Free on orders above PKR 1,500.
* **Reservations:** Tables for 2-20 guests. 2 hours advance notice required. Deposit for 10+ guests.
* **Payments:** Cash on Delivery (COD), JazzCash, EasyPaisa, Debit/Credit Cards.
* **Deals:** Updated every Monday. Follow @breadnbutter.
* **Order Tracking:** Share Order ID or registered phone number.
* **Cancellations:** Allowed within 5 minutes via call.
"""

def get_bot_response(user_message: str) -> str:
    if not user_message or user_message.strip() == "":
        return "👋 Welcome to Bread & Butter! How can I help you today? 😊"

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Updated model identifier
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.6,
            max_tokens=250
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"\n[!!! ASAL ERROR YAHAN HAI !!!]: {e}\n")
        
        return (
            "🤔 Hmm, I am having a bit of trouble connecting to my brain right now.\n\n"
            "✅ Don't worry, a live team member from Bread & Butter will assist you shortly!"
        )