import unittest

from services.analysis_service import (
    analyze_module,
    generate_questions,
    create_study_plan,
    create_revision,
    calculate_readiness
)


class TestStudyPlanner(unittest.TestCase):

    def setUp(self):

        self.module = {
            "number": 1,
            "title": "Machine Learning",

            "content": """
            Machine Learning is a branch of
            Artificial Intelligence.

            Supervised learning uses labelled data.
            Classification is used for predicting
            categories.

            Regression is used for predicting
            continuous values.

            Evaluation techniques are used to
            measure model performance.

            Applications of Machine Learning
            are used in many real world systems.
            """,

            "topics": [
                "Machine Learning",
                "Supervised Learning",
                "Classification",
                "Regression",
                "Evaluation Techniques",
                "Applications of Machine Learning"
            ]
        }


    def test_analysis(self):

        result = analyze_module(
            self.module
        )

        self.assertGreater(
            result["topic_count"],
            0
        )

        self.assertGreaterEqual(
            result["coverage_score"],
            0
        )

        self.assertLessEqual(
            result["coverage_score"],
            100
        )


    def test_topic_scores(self):

        result = analyze_module(
            self.module
        )

        for topic in result["topics"]:

            self.assertGreaterEqual(
                topic["score"],
                35
            )

            self.assertLessEqual(
                topic["score"],
                100
            )


    def test_question_generation(self):

        result = analyze_module(
            self.module
        )

        questions = generate_questions(
            result
        )

        self.assertGreater(
            len(questions),
            0
        )

        for question in questions:

            self.assertIn(
                "question",
                question
            )

            self.assertIn(
                "marks",
                question
            )


    def test_study_plan(self):

        result = analyze_module(
            self.module
        )

        plan = create_study_plan(
            result,
            3
        )

        self.assertGreater(
            len(plan),
            0
        )


    def test_revision(self):

        result = analyze_module(
            self.module
        )

        revision = create_revision(
            result
        )

        self.assertGreater(
            len(revision),
            0
        )


    def test_readiness(self):

        result = analyze_module(
            self.module
        )

        readiness = calculate_readiness(
            result,
            3
        )

        self.assertGreaterEqual(
            readiness,
            0
        )

        self.assertLessEqual(
            readiness,
            98
        )


if __name__ == "__main__":
    unittest.main()