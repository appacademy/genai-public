from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from src.rag.document_loader import load_vector_store
import os
import re
import hashlib


class BenefitsRAG:

    def __init__(self, llm, vector_store_path="data/vector_store"):
        """Initialize the Benefits RAG component"""
        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Define the class constructor, initialize the vector store, and build the benefit cache

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 2. Standard QA prompt for general benefit questions

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 3. Specialized prompt for sensitive topics like mental health, disabilities, etc.

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 4. Specialized prompt for comparative questions

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 5. Specialized prompt for follow-up questions

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 6. Initialize the output parser for the response

    def _build_benefit_cache(self):
        """Build a cache of benefit files and their content hashes for better document matching"""
        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Read all benefit files from the specified directories

    def find_document_source(self, content):
        """Find the source document for a given content using improved matching techniques"""
        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Check if the content is empty or None

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 2. Handle both string content and document objects/dictionaries

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 3. If we still don't have content as a string, convert it

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 4. Methods to find the document source

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 5. Fallback to metadata if available

    def is_sensitive_topic(self, query):
        """Detect if the query is about a sensitive topic that needs special handling"""
        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Check for specific sensitive keywords in the query

    def is_comparative_question(self, query):
        """Detect if the query is asking for a comparison between benefits"""
        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Check if this is a relationship question first

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 2. Check for comparative terms in the query

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 3. Check for specific benefit types in the query

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 4. Check if multiple benefit types are mentioned in the query

    def is_relationship_question(self, query):
        """Detect if the query is asking about relationships between benefits"""
        query_lower = query.lower()

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Check for specific patterns in the query

    def is_followup_question(self, query, previous_question):
        """Detect if the query is a follow-up to the previous question"""
        if not previous_question:
            return False

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Check for pronouns and demonstratives that reference previous content

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 2. Check if the query contains any follow-up indicators and if it is a short query

    def expand_query(self, query):
        """Expand the query with related terms to improve document retrieval"""
        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. map of terms to their related terms for expansion

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 2. Add related terms to the query and return the expanded query

    def extract_entities_for_comparison(self, query):
        """Extract benefit entities that should be compared"""
        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Check for common benefit entities

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 2. Check for each entity type in the query and return the found entities

    def get_relevant_documents(self, query, k=10):
        """Retrieve relevant benefits documents for a query with enhanced retrieval for comparative questions"""
        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Check if the vector store is available

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 2. Check if this is a comparative question and expand the query

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 3. Get retriever without filter to ensure we get documents and print debug info

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 4. Try to get documents using the expanded query

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 5. For comparative questions, we need a second phase of retrieval

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 6. Additional handling for sensitive topics

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 7. Print document information for debugging with improved filename detection

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 8. Implement special handling for various query types

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 9. Filter to benefit documents manually if needed, add extra blank lines, and return

    def generate_response(
        self, query, documents, previous_question=None, previous_context=None
    ):
        """Generate a response based on retrieved documents with enhanced context organization"""
        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 1. Check if the documents are empty

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 2. Format context from documents with improved source information and grouping

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 3. If this is a comparative question, organize context by benefit type

        # TODO: Implement the BenefitsRAG class to handle benefits-related queries
        # 4. Select the appropriate prompt based on query type
