from rag.retriever import retrieve_topic_content

from llm.groq_model import generate_response


def generate_quiz(topic):

    retrieved_content = retrieve_topic_content(topic)

    prompt = f"""
    You are an AI quiz generator.

    Topic:
    {topic}

    Study Material:
    {retrieved_content}

    Generate:

    - 5 MCQ questions
    - Each question should have 4 options
    - Mention correct answer separately

    Format exactly like this:

    Q1. Question
    
    A. Option

    B. Option

    C. Option

    D. Option

    Answer: 
    
    Keep questions beginner-friendly.
    """

    response = generate_response(prompt)

    return response

