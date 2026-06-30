from typing import TypedDict

from langgraph.graph import StateGraph

from agents.knowledge_agent import extract_topics
from agents.weak_topic_agent import identify_weak_topics
from agents.study_planner_agent import generate_schedule
from agents.resource_agent import recommend_resources
from agents.quiz_agent import generate_quiz



# -------------------------------
# STATE
# -------------------------------

class StudyState(TypedDict):

    syllabus_text: str

    score_dict: dict

    exam_date: object

    study_hours: int

    topics: list

    weak_topics: list

    schedule: list

    resources: dict

    quiz: str


# -------------------------------
# KNOWLEDGE AGENT
# -------------------------------

def knowledge_node(state):

    topics = extract_topics(
        state["syllabus_text"]
    )

    state["topics"] = topics

    return state


# -------------------------------
# WEAK TOPIC AGENT
# -------------------------------

def weak_topic_node(state):

    weak_topics = identify_weak_topics(
        state["score_dict"]
    )

    state["weak_topics"] = weak_topics

    return state


# -------------------------------
# STUDY PLANNER AGENT
# -------------------------------

def planner_node(state):

    schedule = generate_schedule(

        state["topics"],

        state["weak_topics"],

        state["exam_date"],

        state["study_hours"]
    )

    state["schedule"] = schedule

    return state


# -------------------------------
# RESOURCE AGENT
# -------------------------------

def resource_node(state):

    resources = {}

    for item in state["weak_topics"]:

        topic = item["topic"]

        resources[topic] = recommend_resources(topic)

    state["resources"] = resources

    return state



# -------------------------------
# QUIZ AGENT
# -------------------------------

def quiz_node(state):

    if len(state["weak_topics"]) > 0:

        topic = state["weak_topics"][0]["topic"]

        quiz_data = generate_quiz(topic)

    else:

        quiz_data = []

    state["quiz"] = quiz_data

    return state


# -------------------------------
# BUILD GRAPH
# -------------------------------

builder = StateGraph(StudyState)

builder.add_node(
    "knowledge",
    knowledge_node
)

builder.add_node(
    "weak_topics",
    weak_topic_node
)

builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "resources",
    resource_node
)

builder.add_node(
    "quiz",
    quiz_node
)


# -------------------------------
# FLOW
# -------------------------------

builder.set_entry_point("knowledge")

builder.add_edge("knowledge","weak_topics")

builder.add_edge("weak_topics","planner")

builder.add_edge("planner","resources")

builder.add_edge("resources","quiz")

# -------------------------------
# COMPILE GRAPH
# -------------------------------

graph = builder.compile()
