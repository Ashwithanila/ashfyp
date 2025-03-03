import os
from dotenv import load_dotenv
from groq import Groq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

def ask_ai(combined_input: str) -> str:
    """
    Generates fitness advice based on user profile, question, and notes using the Groq API.
    Now expecting only one combined input, which will reduce error.
    """
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found in environment variables. Please set it."
        )

    # Initialize Groq client
    client = Groq(api_key=GROQ_API_KEY)

    try:
        prompt = PromptTemplate(
            input_variables=["combined_input"],
            template="""You are a highly experienced personal trainer and dietitian, an expert in health, nutrition, and fitness. 
            Use the following user profile, question, and notes to provide a personalized and accurate response. 
            Relevant details that must be included, are the profile and what question that has been asked.

            Combined Inputs:{combined_input}

            Response:"""
        )

        messages = [{"role": "user", "content": prompt.format(combined_input=combined_input)}]

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Or another supported Groq model
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Example usage
    os.environ['GROQ_API_KEY'] = "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"  # Replace with your actual Groq API key
    example_profile = "30 years old, male, wants to build muscle, has a knee injury"
    example_question = "What exercises can I do to build my chest without putting strain on my knees?"
    example_notes = "The user hates bicep curls and cannot do hammer curls due to injury."
    combined = f"Profile: {example_profile}\nQuestion: {example_question}\nNotes {example_notes}"
    advice = ask_ai(combined)
    print(f"Example Advice:\n{advice}")