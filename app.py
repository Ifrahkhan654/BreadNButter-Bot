import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from responses import get_bot_response

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

def send_instagram_message(recipient_id, text_to_send):
    """
    Sends a POST request to the Meta Graph API 
    to dispatch the bot's reply back to the Instagram user.
    """
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text_to_send}
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"[SUCCESS] Reply successfully sent to user: {recipient_id}")
        else:
            print(f"[ERROR] Meta API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[EXCEPTION] Failed to send message due to: {str(e)}")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. GET Request: Handles Meta Webhook Verification
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("[INFO] Webhook successfully verified by Meta.")
                return challenge, 200
            else:
                print("[WARNING] Verification failed: Token mismatch.")
                return "Verification token mismatch", 403
                
    # 2. POST Request: Handles Incoming Instagram DMs
    elif request.method == 'POST':
        data = request.json
        
        if data.get('object') == 'instagram':
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    
                    # Process message events
                    if 'message' in messaging_event:
                        message_data = messaging_event['message']
                        sender_id = messaging_event['sender']['id']
                        
                        # Guardrail: Skip if the message is an echo (sent by the bot itself)
                        if message_data.get('is_echo'):
                            print("[INFO] Echo detected. Skipping to prevent loop.")
                            continue
                            
                        # Extract and process the text content
                        if 'text' in message_data:
                            user_text = message_data['text']
                            print(f"[RECEIVE] Message from {sender_id}: {user_text}")
                            
                            # Get response string from logic file
                            bot_reply = get_bot_response(user_text)
                            
                            # Dispatch the reply via Meta Graph API
                            send_instagram_message(sender_id, bot_reply)
                            
        return "EVENT_RECEIVED", 200

if __name__ == '__main__':
    # Start the local development server on port 5000
    app.run(port=5000, debug=True)