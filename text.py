import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please set GROQ_API_KEY in the .env file.")

client = Groq(api_key=api_key)

def summarize_text():
    text = input("Enter the text to summarize:\n")

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a professional event summarizer.do not add any introduction just provide the output Your task is to convert a list of rough notes or key points into a clear, well-structured event summary in a paragraph of 300 words"},
            {"role": "user", "content": text}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        top_p=1
    )

    summary = response.choices[0].message.content.strip()
    print("\n📄 Summary:")
    print(summary)

if __name__ == "__main__":
    summarize_text()
