import re
def extract_scores_with_llm(raw_text):

    score_dict = {}

    lines = raw_text.split("\n")

    for line in lines:

        line = line.strip()

        if "=" in line:

            parts = line.split("=")

            if len(parts) == 2:

                topic = parts[0].strip()

                score_text = parts[1].strip()

                numbers = re.findall(r"\d+", score_text)

                if numbers:

                    score = int(numbers[0])

                    score_dict[topic] = score

    return score_dict