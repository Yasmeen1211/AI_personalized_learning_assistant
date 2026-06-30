from rag.retriever import retrieve_topic_content

from llm.groq_model import generate_response

def recommend_resources(topic):

   retrieved_content = retrieve_topic_content(

        topic
    )

   prompt = f"""

   You are an AI Study Assistant.

   Topic:
   {topic}

   Retrieved Notes:
   {retrieved_content}

   Generate:

   1. Give a simple brief explanation of the topic.
   2. Give key concepts in Notes from the uploaded notes.
   3. Recommended external learning resources links
      with direct valid links.

   Include:
    - YouTube tutorials
    - Free courses
    - Documentation
   
   Keep response concise and student friendly.
   """

   response = generate_response(prompt)

   return response