
from datetime import datetime, timedelta
import math

def generate_schedule(topics, weak_topics, exam_date, study_hours):

    today = datetime.today().date()

    total_days = (exam_date - today).days

    if total_days <= 0:
        total_days = 1

    weak = [x["topic"] for x in weak_topics if x["category"] == "Weak"]
    medium = [x["topic"] for x in weak_topics if x["category"] == "Medium"]
    strong = [x["topic"] for x in weak_topics if x["category"] == "Strong"]

    all_topics = weak + medium + strong

    total_topics = len(all_topics)

    topics_per_day = math.ceil(total_topics / total_days)

    schedule = []

    topic_index = 0

    for day in range(total_days):

        current_date = today + timedelta(days=day)

        day_plan = {
            "date": str(current_date),
            "schedule": []
        }

        todays_topics = []

        for _ in range(topics_per_day):

            if topic_index < total_topics:

                todays_topics.append(all_topics[topic_index])

                topic_index += 1

        if total_days > total_topics and weak:

            todays_topics.append(weak[day % len(weak)])

        remaining_hours = study_hours

        for topic in todays_topics:

            if topic in weak:

                category = "Weak"
                allocated = round(study_hours * 0.45 / max(len(todays_topics),1),1)

            elif topic in medium:

                category = "Medium"
                allocated = round(study_hours * 0.30 / max(len(todays_topics),1),1)

            else:

                category = "Strong"
                allocated = round(study_hours * 0.20 / max(len(todays_topics),1),1)

            remaining_hours -= allocated

            day_plan["schedule"].append({

                "topic": topic,
                "category": category,
                "hours": allocated,
                "task": "Study + Practice"
            })

        if remaining_hours > 0:

            day_plan["schedule"].append({

                "topic": "Quiz + Revision",
                "category": "Practice",
                "hours": round(remaining_hours,1),
                "task": "MCQs + Active Recall"
            })

        schedule.append(day_plan)

    return schedule
