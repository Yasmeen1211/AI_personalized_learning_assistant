import streamlit as st
from datetime import date
import mlflow

from utils.file_parser import parse_uploaded_file

from utils.extract_scores import extract_scores_with_llm
from evaluation.custom_eval import evaluate_system

from rag.vector_store import build_vector_store

from workflow.langgraph_flow import graph
from agents.quiz_agent import generate_quiz

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Study Planner",
    layout="wide"
)

st.title(
    "AI Personalized Learning and Study Planner"
)

# -----------------------------------
# FILE UPLOADS
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload Notes [Pdf/TXT]",
    type=["pdf", "txt"]
)

score_file = st.file_uploader(
    "Upload Topic and Result [Image/PDF/TXT]",
    type=["pdf", "txt", "png", "jpg", "jpeg"]
)

# -----------------------------------
# EXAM DATE
# -----------------------------------

exam_date = st.date_input(
    "Exam Date",
    value=date.today()
)

# -----------------------------------
# STUDY HOURS
# -----------------------------------

study_hours = st.slider(
    "Study Hours Per Day",
    1,
    12,
    7
)

# -----------------------------------
# MLFLOW
# -----------------------------------

mlflow.set_experiment(
    "AI_Study_Planner"
)

# -----------------------------------
# MAIN EXECUTION
# -----------------------------------

if uploaded_file and score_file:

    # -------------------------------
    # PARSE FILES
    # -------------------------------

    syllabus_text = parse_uploaded_file(
        uploaded_file
    )

    raw_score_text = parse_uploaded_file(
        score_file
    )

    # -------------------------------
    # EXTRACT SCORES
    # -------------------------------

    score_dict = extract_scores_with_llm(
        raw_score_text
    )

    st.subheader(
        "Extracted Scores"
    )

    st.json(score_dict)

    # -------------------------------
    # BUILD VECTOR STORE
    # -------------------------------

    build_vector_store(
        syllabus_text
    )

    # -------------------------------
    # RUN LANGGRAPH
    # -------------------------------

    with mlflow.start_run():

        result = graph.invoke({

            "syllabus_text": syllabus_text,

            "score_dict": score_dict,

            "exam_date": exam_date,

            "study_hours": study_hours
        })

        # ---------------------------
        # LOGGING
        # ---------------------------

        mlflow.log_param(
            "study_hours",
            study_hours
        )

        mlflow.log_metric(
            "weak_topics_count",
            len(
                result.get(
                    "weak_topics",
                    []
                )
            )
        )
        

    # -------------------------------
    # WEAK TOPICS
    # -------------------------------

    st.header(
        "Weak Topic Analysis"
    )

    st.json(
        result.get(
            "weak_topics",
            []
        )
    )

    # -------------------------------
    # TIMETABLE
    # -------------------------------

    st.header(
        "Study Timetable"
    )

    schedule = result.get(
        "schedule",
        []
    )

    for day in schedule:

        st.subheader(
            day["date"]
        )

        for item in day["schedule"]:

            st.write(

                f"• {item['topic']} "

                f"({item['category']}) - "

                f"{item['hours']} hrs - "

                f"{item['task']}"
            )

    # -------------------------------
    # RESOURCES
    # -------------------------------

    st.header("Recommended Resources")

    resources = result.get(
        "resources",
        {}
    )

    for topic, content in resources.items():

        with st.expander(topic):

            st.write(content)

    # -------------------------------
    # QUIZ
    # -------------------------------

    # st.header(
    #     "Quiz"
    # )

    # st.write(
    #     result.get(
    #         "quiz",
    #         ""
    #     )
    # )
#     '''st.header("Quiz")
#     weak_topics = result.get("weak_topics", [])
#     selected_topic = st.selectbox(
#         "Select Topic",
#         [x["topic"] for x in weak_topics]
#     )

    # --------------------------------
# QUIZ GENERATOR
# --------------------------------

    st.header("Quiz Generator")
    weak_topics = result.get("weak_topics", [])
    selected_topic = st.selectbox(
        "Select Topic",
        [x["topic"] for x in weak_topics]
    )

    # Display quiz
   
    # quiz = generate_quiz(selected_topic)
    # # Split using Answer:
    # quiz_parts = quiz.split("Answer:")
    # for i in range(len(quiz_parts) - 1):

    #     question_block = quiz_parts[i].strip()
    
    # # Remove any trailing answer from the question_block
    # # (in case the generator added something)
    #     lines = question_block.split("\n")
    #     clean_lines = [line for line in lines if not line.strip().startswith("**Correct") 
    #                and not line.strip().startswith("Show Answer")]
    #     question_block = "\n".join(clean_lines).strip()
    #     answer_lines = quiz_parts[i + 1].strip().split("\n")
    #     answer_text = next((line for line in answer_lines if line.strip()), "").strip()
    #     st.write(question_block)

    #     with st.expander("Show Answer"):

    #         st.success(answer_text)
    
    # topics = result.get("topics", [])

    # weak_topics = result.get("weak_topics", [])
    # schedule = result.get("schedule", [])
    # explanation = result.get("explanation", "")

    # # Example inputs for evaluation
    # query = "Study plan for selected topics"
    # answer = explanation
    # quiz = generate_quiz("Artificial Intelligence")
    #     # or your selected topic
    # metrics=evaluate_system(query,answer,schedule,topics,quiz)
    quiz = generate_quiz(selected_topic)
    lines = quiz.split("\n")

    question_lines = []
    answer_text = ""
    for line in lines:
        stripped = line.strip()
        # Skip lines that are part of "Correct/Show Answer" formatting
        if stripped.startswith("**Correct") or stripped.startswith("Show Answer"):
            continue
        # If line is empty, skip
        if not stripped:
            continue
        # Detect answer line (after "Answer:" or standalone answer)
        if stripped.startswith("Answer:"):
            answer_text = stripped[len("Answer:"):].strip()
            # Display question first
            st.write("\n".join(question_lines))
            # Show answer in expander
            with st.expander("Show Answer"):
                st.success(answer_text)
            # Reset for next question
            question_lines = []
            answer_text = ""
            continue
        # Otherwise, accumulate question lines
        question_lines.append(stripped)
        
    # If any leftover lines after loop (last question without Answer:)
    if question_lines:
        st.write("\n".join(question_lines))
    st.success("Study Plan Generated Successfully!")
        
        