import unittest
import os
import shutil
from langchain_community.llms import Ollama
from src.rag.document_loader import load_documents, create_vector_store
from src.rag.policy_qa import PolicyRAG
from src.rag.benefits_qa import BenefitsRAG


class TestRAGPipelines(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        # Create test directories
        os.makedirs("test_data/policies", exist_ok=True)
        os.makedirs("test_data/benefits", exist_ok=True)
        os.makedirs("test_data/vector_store", exist_ok=True)

        # Create sample policy document
        with open("test_data/policies/pto_policy.txt", "w") as f:
            f.write(
                """
                Employee PTO policy sample
                This Employee PTO policy sample is ready to be tailored to your company's needs.
                
                Policy brief & purpose
                Our Employee PTO policy or paid time off policy refers to the amount of time off we offer to our employees per calendar year or month.
                
                We offer 20 days of annual PTO to our full-time, permanent employees.
                These employees can use their PTO from the beginning of the year, without having to wait to accrue it.
                
                Unused PTO may not be passed on to the next calendar year.
                """
            )

        # Create sample benefits document
        with open("test_data/benefits/401k.txt", "w") as f:
            f.write(
                """
                401(k) Retirement Plan
                
                Gem City Technologies offers a 401(k) retirement plan to help employees save for their future.
                
                Key features:
                - Company matches 100% of employee contributions up to 5% of salary
                - Immediate vesting of company match
                - Multiple investment options available
                - Employees are eligible after 90 days of employment
                """
            )

        # Process documents and create vector store
        chunks = load_documents(
            policy_dir="test_data/policies", benefits_dir="test_data/benefits"
        )
        create_vector_store(chunks, vector_store_path="test_data/vector_store")

        # Initialize LLM and RAG components
        cls.llm = Ollama(model="gemma3")
        cls.policy_rag = PolicyRAG(cls.llm, vector_store_path="test_data/vector_store")
        cls.benefits_rag = BenefitsRAG(
            cls.llm, vector_store_path="test_data/vector_store"
        )

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after all tests"""
        # Remove test directories
        shutil.rmtree("test_data", ignore_errors=True)

    def test_policy_retrieval(self):
        """Test that policy documents can be retrieved correctly"""
        query = "What's our PTO policy?"
        documents = self.policy_rag.get_relevant_documents(query)

        # Check that we got at least one document
        self.assertGreater(len(documents), 0)

        # Check that the document contains relevant information
        doc_text = documents[0].page_content.lower()
        self.assertIn("pto", doc_text)
        self.assertIn("20 days", doc_text)

    def test_benefits_retrieval(self):
        """Test that benefits documents can be retrieved correctly"""
        query = "What's our 401(k) match?"
        documents = self.benefits_rag.get_relevant_documents(query)

        # Check that we got at least one document
        self.assertGreater(len(documents), 0)

        # Check that the document contains relevant information
        doc_text = documents[0].page_content.lower()
        self.assertIn("401(k)", doc_text)
        self.assertIn("5%", doc_text)

    def test_policy_response_generation(self):
        """Test that policy responses can be generated correctly"""
        query = "What's our PTO policy?"
        documents = self.policy_rag.get_relevant_documents(query)
        response = self.policy_rag.generate_response(query, documents)

        # Check that the response contains relevant information
        self.assertIn("20 days", response)
        self.assertIn("PTO", response)

    def test_benefits_response_generation(self):
        """Test that benefits responses can be generated correctly"""
        query = "What's our 401(k) match?"
        documents = self.benefits_rag.get_relevant_documents(query)
        response = self.benefits_rag.generate_response(query, documents)

        # Check that the response contains relevant information
        self.assertIn("5%", response)
        self.assertIn("match", response)


if __name__ == "__main__":
    unittest.main()
