from services.analysis_service import create_study_plan


def plan(analysis_result, hours):
    """
    Create a personalized study plan
    based on topic importance and available time.
    """

    return create_study_plan(
        analysis_result,
        hours
    )