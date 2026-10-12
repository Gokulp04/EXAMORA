# --------------------------------------------------
# EXAMORA - MODULE SERVICE
# --------------------------------------------------

def build_module_summary(modules):
    """
    Create a simple summary for all modules.

    Each module will contain:
    - Module number
    - Title
    - Topic count
    - Content length
    - Has content or not
    """

    summary = {}

    if not modules:
        return summary

    for module_number, module in modules.items():

        module = module or {}

        content = module.get(
            "content",
            ""
        )

        topics = module.get(
            "topics",
            []
        )

        summary[str(module_number)] = {
            "number": int(module_number),
            "title": module.get(
                "title",
                f"Module {module_number}"
            ),
            "topic_count": len(topics),
            "content_length": len(content),
            "has_content": bool(
                content.strip()
            )
        }

    return summary


# --------------------------------------------------
# CALCULATE MODULE CONTENT PERCENTAGES
# --------------------------------------------------

def calculate_module_percentages(modules):
    """
    Calculate how much content each module contains.

    Example:

        Module 1 -> 20%
        Module 2 -> 15%
        Module 3 -> 30%
        Module 4 -> 20%
        Module 5 -> 15%

    The percentage is based on the amount of
    extracted syllabus content.
    """

    # Default percentages
    # Used when no syllabus content is available.

    default_percentages = {
        str(i): 20.0
        for i in range(1, 6)
    }

    if not modules:
        return default_percentages

    content_lengths = {}

    for module_number in range(1, 6):

        key = str(module_number)

        module = modules.get(
            key,
            {}
        )

        content = module.get(
            "content",
            ""
        )

        content_lengths[key] = len(
            content.strip()
        )


    # Total content length
    total_content = sum(
        content_lengths.values()
    )


    # If syllabus has no readable text
    if total_content == 0:
        return default_percentages


    percentages = {}

    for module_number in range(1, 6):

        key = str(module_number)

        percentage = (
            content_lengths[key]
            / total_content
        ) * 100

        percentages[key] = round(
            percentage,
            1
        )


    return percentages


# --------------------------------------------------
# GET MODULE BY NUMBER
# --------------------------------------------------

def get_module_by_number(
    modules,
    module_number
):
    """
    Get a specific module from the
    complete module dictionary.
    """

    if not modules:
        return None

    key = str(module_number)

    return modules.get(
        key
    )


# --------------------------------------------------
# GET SELECTED MODULE INFORMATION
# --------------------------------------------------

def get_selected_module(
    modules,
    module_number
):
    """
    Return important information about
    the selected module.
    """

    module = get_module_by_number(
        modules,
        module_number
    )

    if not module:
        return {
            "number": module_number,
            "title": f"Module {module_number}",
            "content": "",
            "topics": [],
            "topic_count": 0,
            "content_length": 0,
            "has_content": False
        }

    content = module.get(
        "content",
        ""
    )

    topics = module.get(
        "topics",
        []
    )

    return {
        "number": int(module_number),
        "title": module.get(
            "title",
            f"Module {module_number}"
        ),
        "content": content,
        "topics": topics,
        "topic_count": len(topics),
        "content_length": len(content),
        "has_content": bool(
            content.strip()
        )
    }


# --------------------------------------------------
# COUNT AVAILABLE MODULES
# --------------------------------------------------

def count_available_modules(modules):
    """
    Count how many modules contain
    actual syllabus content.
    """

    if not modules:
        return 0

    count = 0

    for module_number in range(1, 6):

        module = modules.get(
            str(module_number),
            {}
        )

        content = module.get(
            "content",
            ""
        )

        if content.strip():
            count += 1

    return count


# --------------------------------------------------
# GET MODULES WITH CONTENT
# --------------------------------------------------

def get_available_modules(modules):
    """
    Return only modules that have
    actual content.
    """

    available = {}

    if not modules:
        return available

    for module_number in range(1, 6):

        key = str(module_number)

        module = modules.get(
            key,
            {}
        )

        content = module.get(
            "content",
            ""
        )

        if content.strip():
            available[key] = module

    return available


# --------------------------------------------------
# GET MODULE STATUS
# --------------------------------------------------

def get_module_status(
    modules,
    module_number
):
    """
    Return the current status of a module.

    Possible status:
    - ready
    - empty
    """

    module = get_module_by_number(
        modules,
        module_number
    )

    if not module:
        return "empty"

    content = module.get(
        "content",
        ""
    )

    if content.strip():
        return "ready"

    return "empty"


# --------------------------------------------------
# CREATE COMPLETE MODULE DASHBOARD DATA
# --------------------------------------------------

def create_module_dashboard_data(modules):
    """
    Prepare all information required by
    the EXAMORA module dashboard.
    """

    percentages = calculate_module_percentages(
        modules
    )

    summary = build_module_summary(
        modules
    )

    dashboard_data = []

    for module_number in range(1, 6):

        key = str(module_number)

        module_info = summary.get(
            key,
            {
                "number": module_number,
                "title": f"Module {module_number}",
                "topic_count": 0,
                "content_length": 0,
                "has_content": False
            }
        )

        dashboard_data.append({
            "number": module_number,
            "title": module_info["title"],
            "topic_count": module_info["topic_count"],
            "content_length": module_info["content_length"],
            "percentage": percentages.get(
                key,
                20.0
            ),
            "status": (
                "ready"
                if module_info["has_content"]
                else "empty"
            )
        })

    return dashboard_data