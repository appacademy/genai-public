import unittest
from langchain_community.llms import Ollama
from src.intent.router import IntentRouter


class TestIntentRouter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the LLM and intent router once for all tests
        cls.llm = Ollama(model="gemma3")
        cls.router = IntentRouter(cls.llm)

    def test_policy_intent(self):
        """Test that policy questions are correctly classified"""
        query = "What's our PTO policy?"
        result = self.router.classify(query)
        self.assertEqual(result["intent"], "policy_q")

    def test_benefit_intent(self):
        """Test that benefit questions are correctly classified"""
        query = "Tell me about our 401(k) match"
        result = self.router.classify(query)
        self.assertEqual(result["intent"], "benefit_q")

    def test_training_lookup_intent(self):
        """Test that training lookup requests are correctly classified"""
        query = "Show my training record"
        result = self.router.classify(query)
        self.assertEqual(result["intent"], "train_lookup")

    def test_training_enroll_intent(self):
        """Test that training enrollment requests are correctly classified"""
        query = "Enroll me in SEC-230"
        result = self.router.classify(query)
        self.assertEqual(result["intent"], "train_enroll")
        self.assertEqual(result["args"]["course_id"], "SEC-230")

    def test_training_update_intent(self):
        """Test that training update requests are correctly classified"""
        query = "I finished AI-201 yesterday"
        result = self.router.classify(query)
        self.assertEqual(result["intent"], "train_update")
        self.assertEqual(result["args"]["course_id"], "AI-201")

    def test_mandatory_training_intent(self):
        """Test that mandatory training requests are correctly classified"""
        query = "Sign me up for all mandatory courses"
        result = self.router.classify(query)
        self.assertEqual(result["intent"], "train_mandatory")

    def test_fallback_intent(self):
        """Test that unrelated queries are routed to fallback"""
        query = "What's the weather today?"
        result = self.router.classify(query)
        self.assertEqual(result["intent"], "fallback")


if __name__ == "__main__":
    unittest.main()
