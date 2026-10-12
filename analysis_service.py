import re


# --------------------------------------------------
# IMPORTANT KEYWORDS
# --------------------------------------------------

IMPORTANT_KEYWORDS = [
    "algorithm",
    "architecture",
    "application",
    "applications",
    "classification",
    "comparison",
    "concept",
    "definition",
    "difference",
    "evaluation",
    "example",
    "implementation",
    "learning",
    "method",
    "model",
    "optimization",
    "process",
    "regression",
    "technique",
    "types",
    "advantages",
    "disadvantages",
    "working",
]


# --------------------------------------------------
# STOP WORDS
# --------------------------------------------------

STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "this",
    "that",
    "are",
    "was",
    "were",
    "into",
    "using",
    "use",
    "about",
    "their",
    "have",
    "has",
    "will",
    "can",
    "also",
    "than",
    "which",
    "what",
    "when",
    "where",
    "how",
    "module",
    "unit",
    "chapter",
    "introduction",
}


# --------------------------------------------------
# ANALYZE SELECTED MODULE
# --------------------------------------------------

def analyze_module(module):
    """
    Analyze only the selected module.

    EXAMORA calculates:
    - Topic importance
    - Topic score
    - Priority
    - Coverage
    - Overall importance
    """

    if not module:
        return {
            "title": "Selected Module",
            "topics": [],
            "coverage_score": 0,
            "importance_score": 0,
            "topic_count": 0,
            "content_chars": 0,
        }

    content = module.get(
        "content",
        ""
    )

    topics = module.get(
        "topics",
        []
    )

    # If topics are not already detected,
    # create topics from the content.
    if not topics and content:
        topics = extract_topics_from_content(
            content
        )

    scored_topics = []

    for index, topic in enumerate(topics):

        score = calculate_topic_score(
            topic,
            index,
            len(topics)
        )

        priority = get_priority(
            score
        )

        stars = get_stars(
            score
        )

        scored_topics.append({
            "name": topic,
            "score": score,
            "priority": priority,
            "stars": stars
        })

    # Highest priority topics first
    scored_topics.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # --------------------------------------------------
    # COVERAGE SCORE
    # --------------------------------------------------

    topic_count = len(
        scored_topics
    )

    if topic_count == 0:
        coverage = 0
    else:
        coverage = min(
            100,
            round(
                topic_count / 8 * 100
            )
        )

    # --------------------------------------------------
    # IMPORTANCE SCORE
    # --------------------------------------------------

    if scored_topics:

        importance = round(
            sum(
                topic["score"]
                for topic in scored_topics
            )
            / len(scored_topics)
        )

    else:
        importance = 0

    return {
        "title": module.get(
            "title",
            "Selected Module"
        ),
        "topics": scored_topics,
        "coverage_score": coverage,
        "importance_score": importance,
        "topic_count": topic_count,
        "content_chars": len(content),
    }


# --------------------------------------------------
# EXTRACT TOPICS FROM CONTENT
# --------------------------------------------------

def extract_topics_from_content(content):
    """
    Extract possible topics from raw study material.
    """

    if not content:
        return []

    parts = re.split(
        r"\n+|[.;]+|"
        r"\s+[•●▪◦]\s+|"
        r"\s+-\s+",
        content
    )

    topics = []

    for part in parts:

        topic = re.sub(
            r"\s+",
            " ",
            part
        ).strip(
            " -•●▪◦:;"
        )

        if len(topic) < 4:
            continue

        if len(topic) > 150:
            continue

        if topic.isdigit():
            continue

        topics.append(topic)

    # Remove duplicates
    unique_topics = []
    seen = set()

    for topic in topics:

        key = topic.lower()

        if key not in seen:
            seen.add(key)
            unique_topics.append(topic)

    return unique_topics[:50]


# --------------------------------------------------
# CALCULATE TOPIC SCORE
# --------------------------------------------------

def calculate_topic_score(
    topic,
    index,
    total_topics
):
    """
    Calculate importance score for a topic.

    Score is based on:
    - Important academic keywords
    - Topic length
    - Position
    """

    text = topic.lower()

    score = 45

    # --------------------------------------------------
    # KEYWORD SCORE
    # --------------------------------------------------

    keyword_matches = 0

    for keyword in IMPORTANT_KEYWORDS:

        if keyword in text:
            keyword_matches += 1

    score += keyword_matches * 5

    # --------------------------------------------------
    # LENGTH BONUS
    # --------------------------------------------------

    if len(topic) >= 30:
        score += 5

    if len(topic) >= 60:
        score += 5

    # --------------------------------------------------
    # POSITION BONUS
    # --------------------------------------------------

    if total_topics > 0:

        position_ratio = (
            index / total_topics
        )

        if position_ratio < 0.25:
            score += 10

        elif position_ratio < 0.50:
            score += 5

    # Keep score between 35 and 100
    score = max(
        35,
        min(100, score)
    )

    return round(score)


# --------------------------------------------------
# GET PRIORITY
# --------------------------------------------------

def get_priority(score):

    if score >= 85:
        return "Very High"

    if score >= 70:
        return "High"

    if score >= 55:
        return "Medium"

    return "Low"


# --------------------------------------------------
# GET STAR RATING
# --------------------------------------------------

def get_stars(score):

    if score >= 85:
        return 5

    if score >= 70:
        return 4

    if score >= 55:
        return 3

    if score >= 40:
        return 2

    return 1


# --------------------------------------------------
# GENERATE EXAM QUESTIONS
# --------------------------------------------------

def generate_questions(result):
    """
    Generate exam-oriented questions from
    analyzed topics.
    """

    topics = result.get(
        "topics",
        []
    )

    questions = []

    question_templates = [
        (
            "Explain {} with a suitable example.",
            16
        ),
        (
            "Discuss the important concepts involved in {}.",
            13
        ),
        (
            "Explain the working of {}.",
            10
        ),
        (
            "Differentiate the important approaches related to {}.",
            10
        ),
        (
            "Write a detailed note on {}.",
            5
        ),
        (
            "What is {}?",
            2
        ),
    ]

    for index, topic in enumerate(
        topics[:15]
    ):

        template, marks = (
            question_templates[
                index
                % len(question_templates)
            ]
        )

        question = template.format(
            topic["name"]
        )

        questions.append({
            "question": question,
            "marks": marks,
            "priority": topic.get(
                "priority",
                "Medium"
            ),
            "topic": topic["name"]
        })

    return questions


# --------------------------------------------------
# CREATE SMART STUDY PLAN
# --------------------------------------------------

def create_study_plan(
    result,
    hours
):
    """
    Create a study plan based on:
    - Available study time
    - Topic importance
    """

    topics = result.get(
        "topics",
        []
    )

    if not topics:

        return [
            {
                "time": "Start",
                "topic": (
                    "Upload study material "
                    "for the selected module."
                ),
                "focus": "Preparation"
            }
        ]

    try:
        hours = float(hours)
    except (
        TypeError,
        ValueError
    ):
        hours = 2.0

    total_minutes = max(
        30,
        int(hours * 60)
    )

    selected_topics = topics[:10]

    weights = [
        max(
            1,
            topic["score"]
        )
        for topic in selected_topics
    ]

    total_weight = sum(
        weights
    )

    plan = []

    used_minutes = 0

    for index, topic in enumerate(
        selected_topics
    ):

        # Calculate proportional time
        minutes = round(
            (
                total_minutes
                * topic["score"]
                / total_weight
            ) / 5
        ) * 5

        minutes = max(
            10,
            minutes
        )

        # Prevent exceeding available time
        remaining = (
            total_minutes
            - used_minutes
        )

        if remaining <= 0:
            break

        minutes = min(
            minutes,
            remaining
        )

        if index < len(
            selected_topics
        ) * 0.6:

            focus = "Learn + Recall"

        else:

            focus = "Revise + Practice"

        plan.append({
            "time": f"{minutes} min",
            "topic": topic["name"],
            "focus": focus,
            "priority": topic.get(
                "priority",
                "Medium"
            )
        })

        used_minutes += minutes

    return plan


# --------------------------------------------------
# CREATE QUICK REVISION
# --------------------------------------------------

def create_revision(result):
    """
    Create quick revision points for
    the most important topics.
    """

    topics = result.get(
        "topics",
        []
    )

    revision = []

    for topic in topics[:10]:

        topic_name = topic["name"]

        revision.append({
            "topic": topic_name,
            "point": (
                f"Focus on definition, "
                f"core concept, working, "
                f"example, advantages and "
                f"applications of "
                f"{topic_name}."
            ),
            "priority": topic.get(
                "priority",
                "Medium"
            )
        })

    return revision


# --------------------------------------------------
# CALCULATE READINESS SCORE
# --------------------------------------------------

def calculate_readiness(
    result,
    hours
):
    """
    Calculate an overall exam readiness score.
    """

    coverage = result.get(
        "coverage_score",
        0
    )

    importance = result.get(
        "importance_score",
        0
    )

    try:
        hours = float(hours)
    except (
        TypeError,
        ValueError
    ):
        hours = 2.0

    time_score = min(
        100,
        hours * 10
    )

    readiness = (
        coverage * 0.45
        + importance * 0.35
        + time_score * 0.20
    )

    return min(
        98,
        max(
            0,
            round(readiness)
        )
    )