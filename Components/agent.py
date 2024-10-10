# Components/agent.py

import ollama
from IPython.display import display, Markdown

def generate_question(city):
    """
    Generates a list of top 10 questions a first-time traveler might ask about visiting the city.
    """
    prompt = f"""
    As a travel guide expert, generate a list of the top 10 questions that a first-time traveler might ask about visiting {city}.
    Please provide only the questions, numbered 1 to 10, without any additional descriptions.
    """
    try:
        response = ollama.chat(model="llama3.2", messages=[{'role':'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error generating questions: {e}"

def display_question_with_markdown(city):
    """
    Displays the generated questions in a markdown format.
    """
    questions_text = generate_question(city)
    markdown_output = f"### Top 10 Questions for First-Time Travelers to {city}:\n\n{questions_text}"
    display(Markdown(markdown_output))
