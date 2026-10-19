from services.analysis_service import generate_questions


def generate(analysis_result):
    """
    Generate exam-oriented questions
    from the analyzed module.
    """

    return generate_questions(
        analysis_result
    )