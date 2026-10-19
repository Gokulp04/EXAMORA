from services.analysis_service import analyze_module


def analyze(module):
    """
    Analyze the selected module and return
    topic importance and preparation scores.
    """

    return analyze_module(module)