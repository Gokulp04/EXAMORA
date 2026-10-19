import unittest

from services.syllabus_service import (
    detect_modules,
    extract_module_title,
    module_has_content,
    count_module_topics
)

from services.module_service import (
    calculate_module_percentages,
    get_selected_module,
    count_available_modules
)


class TestModuleServices(unittest.TestCase):

    def setUp(self):

        self.syllabus = """
        MODULE 1 - Introduction to AI

        Artificial Intelligence basics.
        Intelligent agents.
        Problem solving.

        MODULE 2 - Machine Learning

        Supervised learning.
        Unsupervised learning.
        Regression and classification.

        MODULE 3 - Deep Learning

        Neural networks.
        Deep learning architecture.

        MODULE 4 - NLP

        Natural language processing.
        Text processing.

        MODULE 5 - Applications

        AI applications.
        Real world examples.
        """

    def test_detect_five_modules(self):

        modules = detect_modules(
            self.syllabus
        )

        self.assertEqual(
            len(modules),
            5
        )

        self.assertIn(
            "1",
            modules
        )

        self.assertIn(
            "5",
            modules
        )


    def test_module_title(self):

        title = extract_module_title(
            "MODULE 2 - Machine Learning",
            2
        )

        self.assertEqual(
            title,
            "Machine Learning"
        )


    def test_module_has_content(self):

        modules = detect_modules(
            self.syllabus
        )

        module_1 = modules["1"]

        self.assertTrue(
            module_has_content(
                module_1
            )
        )


    def test_module_topics(self):

        modules = detect_modules(
            self.syllabus
        )

        module_2 = modules["2"]

        self.assertGreater(
            count_module_topics(
                module_2
            ),
            0
        )


    def test_module_percentages(self):

        modules = detect_modules(
            self.syllabus
        )

        percentages = (
            calculate_module_percentages(
                modules
            )
        )

        total = sum(
            percentages.values()
        )

        self.assertAlmostEqual(
            total,
            100.0,
            places=1
        )


    def test_selected_module(self):

        modules = detect_modules(
            self.syllabus
        )

        selected = get_selected_module(
            modules,
            2
        )

        self.assertEqual(
            selected["number"],
            2
        )

        self.assertTrue(
            selected["has_content"]
        )


    def test_available_modules(self):

        modules = detect_modules(
            self.syllabus
        )

        count = count_available_modules(
            modules
        )

        self.assertEqual(
            count,
            5
        )


if __name__ == "__main__":
    unittest.main()