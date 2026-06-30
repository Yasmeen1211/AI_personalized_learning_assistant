
def extract_topics(text):

    lines = text.split("\n")

    topics = []

    for line in lines:

        line = line.strip()

        if len(line) > 4:

            topics.append(line)

    return list(dict.fromkeys(topics))[:20]
