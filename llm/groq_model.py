import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
print(os.getenv("GROQ_API_KEY"))
def generate_response(prompt):

    try:

        response = client.chat.completions.create(

            # model="llama-3.3-70b-versatile",
            model="llama-3.1-8b-instant",
            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an AI Personalized Learning Assistant."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq API Error: {str(e)}"
