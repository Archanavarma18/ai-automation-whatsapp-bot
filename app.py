from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq

app = Flask(__name__)

client = Groq(api_key="")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():

    incoming_msg = request.values.get('Body', '').strip()

    response = MessagingResponse()
    msg = response.message()

    try:
        ai_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a funny helpful WhatsApp assistant."
                },
                {
                    "role": "user",
                    "content": incoming_msg
                }
            ]
        )

        reply = ai_response.choices[0].message.content

    except Exception as e:
        reply = f"Error: {str(e)}"

    msg.body(reply)

    return str(response)

if __name__ == "__main__":
    app.run(debug=False)