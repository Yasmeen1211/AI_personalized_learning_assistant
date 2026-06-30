
def parse_scores(text):

    scores = {}

    for line in text.split("\n"):

        if "=" in line:

            topic, score = line.split("=")

            scores[topic.strip()] = int(score.strip())

    return scores
