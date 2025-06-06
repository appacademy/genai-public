import unittest
from unittest.mock import MagicMock, patch
from langchain_community.llms import Ollama
from src.intent.router import IntentRouter
from src.rag.policy_qa import PolicyRAG
from src.rag.benefits_qa import BenefitsRAG
from src.training.csv_tools import TrainingRecords
from src.orchestration.graph import create_workflow, GraphState


class TestOrchestration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        # Create mock components
        cls.llm = MagicMock()
        cls.intent_router = MagicMock()
        cls.policy_rag = MagicMock()
        cls.benefits_rag = MagicMock()
        cls.training_records = MagicMock()

        # Create workflow
        cls.workflow = create_workflow(
            cls.intent_router,
            cls.policy_rag,
            cls.benefits_rag,
            cls.training_records,
            cls.llm,
        )

    def setUp(self):
        """Reset mocks before each test"""
        self.intent_router.classify.reset_mock()
        self.policy_rag.get_relevant_documents.reset_mock()
        self.policy_rag.generate_response.reset_mock()
        self.benefits_rag.get_relevant_documents.reset_mock()
        self.benefits_rag.generate_response.reset_mock()
        self.training_records.get_employee_record.reset_mock()
        self.training_records.create_snapshot.reset_mock()
        self.training_records.enroll_in_course.reset_mock()
        self.training_records.update_completion.reset_mock()
        self.training_records.enroll_mandatory_courses.reset_mock()

    def test_policy_query_routing(self):
        """Test that policy queries are routed correctly"""
        # Set up mock intent router to return policy_q intent
        self.intent_router.classify.return_value = {"intent": "policy_q"}

        # Set up mock policy RAG
        mock_docs = [MagicMock()]
        self.policy_rag.get_relevant_documents.return_value = mock_docs
        self.policy_rag.generate_response.return_value = "This is our PTO policy..."

        # Create input state
        input_state = GraphState(user_input="What's our PTO policy?")

        # Run workflow
        result = self.workflow.invoke(input_state)

        # Check that intent router was called
        self.intent_router.classify.assert_called_once_with("What's our PTO policy?")

        # Check that policy RAG was called
        self.policy_rag.get_relevant_documents.assert_called_once()
        self.policy_rag.generate_response.assert_called_once()

        # Check that benefits RAG was not called
        self.benefits_rag.get_relevant_documents.assert_not_called()
        self.benefits_rag.generate_response.assert_not_called()

        # Check that training records were not accessed
        self.training_records.get_employee_record.assert_not_called()
        self.training_records.enroll_in_course.assert_not_called()

        # Check result
        self.assertEqual(result.response, "This is our PTO policy...")

    def test_benefits_query_routing(self):
        """Test that benefits queries are routed correctly"""
        # Set up mock intent router to return benefit_q intent
        self.intent_router.classify.return_value = {"intent": "benefit_q"}

        # Set up mock benefits RAG
        mock_docs = [MagicMock()]
        self.benefits_rag.get_relevant_documents.return_value = mock_docs
        self.benefits_rag.generate_response.return_value = "Our 401(k) match is 5%..."

        # Create input state
        input_state = GraphState(user_input="What's our 401(k) match?")

        # Run workflow
        result = self.workflow.invoke(input_state)

        # Check that intent router was called
        self.intent_router.classify.assert_called_once_with("What's our 401(k) match?")

        # Check that benefits RAG was called
        self.benefits_rag.get_relevant_documents.assert_called_once()
        self.benefits_rag.generate_response.assert_called_once()

        # Check that policy RAG was not called
        self.policy_rag.get_relevant_documents.assert_not_called()
        self.policy_rag.generate_response.assert_not_called()

        # Check that training records were not accessed
        self.training_records.get_employee_record.assert_not_called()
        self.training_records.enroll_in_course.assert_not_called()

        # Check result
        self.assertEqual(result.response, "Our 401(k) match is 5%...")

    def test_training_lookup_routing(self):
        """Test that training lookup requests are routed correctly"""
        # Set up mock intent router to return train_lookup intent
        self.intent_router.classify.return_value = {"intent": "train_lookup"}

        # Set up mock training records
        mock_record = MagicMock()
        mock_record.__len__.return_value = 2
        mock_record.iterrows.return_value = [
            (
                0,
                {
                    "course_id": "TEST-101",
                    "course_name": "Test Course 1",
                    "status": "Completed",
                    "completion_date": "2025-04-01",
                    "due_date": None,
                },
            ),
            (
                1,
                {
                    "course_id": "TEST-102",
                    "course_name": "Test Course 2",
                    "status": "Enrolled",
                    "completion_date": None,
                    "due_date": "2025-05-01",
                },
            ),
        ]
        self.training_records.get_employee_record.return_value = mock_record
        self.training_records.create_snapshot.return_value = (
            "training/snapshots/employee_snapshot.csv"
        )

        # Create input state
        input_state = GraphState(user_input="Show my training record")

        # Run workflow
        result = self.workflow.invoke(input_state)

        # Check that intent router was called
        self.intent_router.classify.assert_called_once_with("Show my training record")

        # Check that training records were accessed
        self.training_records.get_employee_record.assert_called_once()
        self.training_records.create_snapshot.assert_called_once()

        # Check that RAG components were not called
        self.policy_rag.get_relevant_documents.assert_not_called()
        self.benefits_rag.get_relevant_documents.assert_not_called()

        # Check result
        self.assertIn("training record", result.response)
        self.assertIn("snapshot", result.response)

    def test_training_enroll_routing(self):
        """Test that training enrollment requests are routed correctly"""
        # Set up mock intent router to return train_enroll intent with args
        self.intent_router.classify.return_value = {
            "intent": "train_enroll",
            "args": {"course_id": "SEC-230"},
        }

        # Set up mock training records
        self.training_records.enroll_in_course.return_value = (
            True,
            "Successfully enrolled in SEC-230",
        )

        # Create input state
        input_state = GraphState(user_input="Enroll me in SEC-230")

        # Run workflow
        result = self.workflow.invoke(input_state)

        # Check that intent router was called
        self.intent_router.classify.assert_called_once_with("Enroll me in SEC-230")

        # Check that training enrollment was called
        self.training_records.enroll_in_course.assert_called_once()

        # Check that other components were not called
        self.policy_rag.get_relevant_documents.assert_not_called()
        self.benefits_rag.get_relevant_documents.assert_not_called()
        self.training_records.update_completion.assert_not_called()

        # Check result
        self.assertIn("enrolled", result.response)
        self.assertIn("SEC-230", result.response)

    def test_training_update_routing(self):
        """Test that training update requests are routed correctly"""
        # Set up mock intent router to return train_update intent with args
        self.intent_router.classify.return_value = {
            "intent": "train_update",
            "args": {"course_id": "AI-201"},
        }

        # Set up mock training records
        self.training_records.update_completion.return_value = (
            True,
            "Marked AI-201 as completed",
        )

        # Create input state
        input_state = GraphState(user_input="I finished AI-201")

        # Run workflow
        result = self.workflow.invoke(input_state)

        # Check that intent router was called
        self.intent_router.classify.assert_called_once_with("I finished AI-201")

        # Check that training update was called
        self.training_records.update_completion.assert_called_once()

        # Check that other components were not called
        self.policy_rag.get_relevant_documents.assert_not_called()
        self.benefits_rag.get_relevant_documents.assert_not_called()
        self.training_records.enroll_in_course.assert_not_called()

        # Check result
        self.assertIn("completed", result.response)
        self.assertIn("AI-201", result.response)

    def test_mandatory_training_routing(self):
        """Test that mandatory training requests are routed correctly"""
        # Set up mock intent router to return train_mandatory intent
        self.intent_router.classify.return_value = {"intent": "train_mandatory"}

        # Set up mock training records
        self.training_records.enroll_mandatory_courses.return_value = [
            ("HR-001", True, "Successfully enrolled"),
            ("HR-002", True, "Successfully enrolled"),
            ("SEC-010", True, "Successfully enrolled"),
        ]

        # Create input state
        input_state = GraphState(user_input="Sign me up for all mandatory courses")

        # Run workflow
        result = self.workflow.invoke(input_state)

        # Check that intent router was called
        self.intent_router.classify.assert_called_once_with(
            "Sign me up for all mandatory courses"
        )

        # Check that mandatory enrollment was called
        self.training_records.enroll_mandatory_courses.assert_called_once()

        # Check that other components were not called
        self.policy_rag.get_relevant_documents.assert_not_called()
        self.benefits_rag.get_relevant_documents.assert_not_called()

        # Check result
        self.assertIn("mandatory training", result.response)
        self.assertIn("HR-001", result.response)

    def test_fallback_routing(self):
        """Test that unrelated queries are routed to fallback"""
        # Set up mock intent router to return fallback intent
        self.intent_router.classify.return_value = {"intent": "fallback"}

        # Create input state
        input_state = GraphState(user_input="What's the weather today?")

        # Run workflow
        result = self.workflow.invoke(input_state)

        # Check that intent router was called
        self.intent_router.classify.assert_called_once_with("What's the weather today?")

        # Check that no other components were called
        self.policy_rag.get_relevant_documents.assert_not_called()
        self.benefits_rag.get_relevant_documents.assert_not_called()
        self.training_records.get_employee_record.assert_not_called()

        # Check result
        self.assertIn("sorry", result.response.lower())
        self.assertIn("help", result.response.lower())


if __name__ == "__main__":
    unittest.main()
