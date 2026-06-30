# Context Relevance
def evaluate_system(query, answer, schedule, topics, quiz):

    # Context Relevance
    context_relevance = len(query.split()) / 10

    # Plan Completeness
    plan_completeness = len(schedule) /5

    # Quiz Quality
    quiz_quality = len(quiz.split("\n")) / 10

    # Normalize (0 to 1)
    context_relevance = round(min(context_relevance, 1), 2)
    plan_completeness = round(min(plan_completeness, 1), 2)
    quiz_quality = round(min(quiz_quality, 1), 2)

    return {
        "context_relevance": context_relevance,
        "plan_completeness": plan_completeness,
        "quiz_quality": quiz_quality
    }







