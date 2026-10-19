import re


# --------------------------------------------------
# DETECT MODULES FROM SYLLABUS
# --------------------------------------------------

def detect_modules(text):
    """
    Detect Module / Unit / Chapter sections
    from the uploaded syllabus text.

    EXAMORA supports up to 5 modules.
    """

    text = text or ""

    # Normalize text
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    modules = {}

    # Detect patterns such as:
    # MODULE 1
    # Module - 1
    # Module: 1
    # UNIT 1
    # UNIT - 1
    # CHAPTER 1

    pattern = re.compile(
        r"""
        (?P<header>
            (?:module|unit|chapter)
            \s*
            [-:.\s]*
            (?P<number>[1-5])
            \b
            [^\n]*
        )
        (?P<content>
            .*?
        )
        (?=
            (?:module|unit|chapter)
            \s*
            [-:.\s]*
            [1-5]
            \b
            |
            \Z
        )
        """,
        re.IGNORECASE | re.DOTALL | re.VERBOSE
    )

    matches = pattern.finditer(text)

    for match in matches:

        number = int(
            match.group("number")
        )

        header = match.group(
            "header"
        ).strip()

        content = match.group(
            "content"
        ).strip()

        # Clean excessive spaces
        content = re.sub(
            r"\s+",
            " ",
            content
        ).strip()

        # Extract title from heading
        title = extract_module_title(
            header,
            number
        )

        # Extract possible topics
        topics = extract_topics(
            content
        )

        modules[str(number)] = {
            "number": number,
            "title": title,
            "content": content[:15000],
            "topics": topics
        }

    # --------------------------------------------------
    # ALWAYS RETURN MODULE 1 TO MODULE 5
    # --------------------------------------------------

    for number in range(1, 6):

        key = str(number)

        if key not in modules:
            modules[key] = {
                "number": number,
                "title": f"Module {number}",
                "content": "",
                "topics": []
            }

    # Maintain correct order
    return {
        str(number): modules[str(number)]
        for number in range(1, 6)
    }


# --------------------------------------------------
# EXTRACT MODULE TITLE
# --------------------------------------------------

def extract_module_title(header, number):
    """
    Extract a meaningful title from a module heading.

    Example:
        MODULE 1 - INTRODUCTION TO AI

    becomes:

        Introduction To AI
    """

    if not header:
        return f"Module {number}"

    # Remove MODULE / UNIT / CHAPTER + number
    title = re.sub(
        r"^(module|unit|chapter)"
        r"\s*[-:.\s]*"
        r"\d+",
        "",
        header,
        flags=re.IGNORECASE
    )

    # Remove unwanted separators
    title = title.strip(
        " -:.\t"
    )

    if not title:
        return f"Module {number}"

    # Limit title length
    title = title[:100]

    return title


# --------------------------------------------------
# EXTRACT TOPICS
# --------------------------------------------------

def extract_topics(content):
    """
    Extract possible topic names from module content.

    This is a rule-based first stage.
    Later EXAMORA AI analysis can improve this.
    """

    if not content:
        return []

    # Try multiple separators
    parts = re.split(
        r"\n+|"
        r"[.;]+|"
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

        # Ignore very short text
        if len(topic) < 4:
            continue

        # Ignore very long paragraphs
        if len(topic) > 150:
            continue

        # Ignore pure numbers
        if topic.isdigit():
            continue

        topics.append(topic)

    # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    unique_topics = []
    seen = set()

    for topic in topics:

        key = topic.lower()

        if key not in seen:
            seen.add(key)
            unique_topics.append(topic)

    return unique_topics[:50]


# --------------------------------------------------
# GET SINGLE MODULE
# --------------------------------------------------

def get_module(modules, module_number):
    """
    Return one selected module.
    """

    if not modules:
        return None

    key = str(module_number)

    return modules.get(key)


# --------------------------------------------------
# CHECK WHETHER MODULE HAS CONTENT
# --------------------------------------------------

def module_has_content(module):
    """
    Check whether the selected module
    actually contains syllabus content.
    """

    if not module:
        return False

    content = module.get(
        "content",
        ""
    )

    return bool(
        content and content.strip()
    )


# --------------------------------------------------
# COUNT MODULE TOPICS
# --------------------------------------------------

def count_module_topics(module):
    """
    Return the number of detected topics.
    """

    if not module:
        return 0

    topics = module.get(
        "topics",
        []
    )

    return len(topics)