def identify_weak_topics(score_dict):

    results = []

    for topic, score in score_dict.items():

        if score <= 40:

            category = "Weak"
            reason = (
                "Low score. Requires strong focus "
                "and repeated revision."
            )

        elif score < 75:

            category = "Medium"
            reason = (
                "Average performance. "
                "Needs additional practice."
            )

        else:

            category = "Strong"
            reason = (
                "Good understanding of the topic."
            )

        results.append({

            "topic": topic,
            "score": score,
            "category": category,
            "reason": reason
        })

    return results