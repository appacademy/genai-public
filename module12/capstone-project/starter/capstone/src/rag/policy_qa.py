from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from src.rag.document_loader import load_vector_store
import os
import re
import hashlib


class PolicyRAG:

    # TODO: Implement the PolicyRAG class to handle policy-related queries
    def __init__(self, llm, vector_store_path="data/vector_store"):
        """Initialize the Policy RAG component"""
        # TODO: 1. Define the constructor to initialize the class with LLM and vector store

        # TODO: 2. Define the prompts for different types of questions
        self.qa_prompt = ChatPromptTemplate.from_template(
            """
        You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer questions about company policies.
        
        Use ONLY the following context to answer the question. If you don't have enough information based on the context, say 
        "I don't have enough information about that in my knowledge base. Please contact HR for more details."
        
        Context:
        {context}
        
        Question: {question}
        
        Answer the question based only on the provided context. Include the source document name in your response 
        for citation purposes. Format your response in a friendly, helpful tone.
        
        When answering follow-up questions or comparing policies, make sure to use all relevant context provided.
        If the question asks for a comparison between different policies (like PTO vs maternity leave), make sure
        to address both policies in your answer with clear distinctions between them.
        
        If multiple policies are mentioned in the question, be sure to discuss each one and highlight the key 
        similarities and differences between them. Structure your answer clearly, using bullet points where appropriate.
        """
        )

        # Specialized prompt for sensitive topics like substance abuse, mental health, etc.
        self.sensitive_topic_prompt = ChatPromptTemplate.from_template(
            """
        You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer questions about company policies,
        including sensitive topics like substance abuse, mental health, or harassment policies.
        
        Use the following context to answer the question. 
        
        Context:
        {context}
        
        Question: {question}
        
        Important instructions for sensitive topics:
        1. Present information about support resources and company assistance programs first
        2. Explain the policy's protection and confidentiality provisions clearly
        3. Describe any disciplinary actions or consequences only after explaining support options
        4. Use compassionate, non-judgmental language throughout your response
        5. Emphasize that seeking help is encouraged, not penalized
        6. Include the source document name for citation
        
        For substance abuse or addiction questions specifically:
        7. Always mention Employee Assistance Program (EAP) resources if available in the context
        8. Discuss both the Wellness Program and related policies together if relevant
        9. Emphasize confidentiality and non-punitive aspects of seeking help
        10. Synthesize information from multiple documents to provide a complete answer
        11. Address how different policies and programs work together to support employees
        
        If the context doesn't specifically address the question (for example, if the Wellness Program doesn't 
        explicitly mention addiction):
        12. Acknowledge this limitation clearly: "Based on the available information, our [specific policy] documentation 
           doesn't explicitly mention [topic]. However, I can share what our policies do cover:"
        13. Provide the most relevant information you do have (e.g., smoking cessation programs, EAP resources, etc.)
        14. Offer to search across all policies: "Would you like me to search all company policies for information about [topic]?"
        15. Recommend contacting HR for more specific information
        16. Do NOT respond with only "I don't have enough information" - always try to provide some helpful direction
        
        Answer the question based on the provided context. Format your response in a friendly, supportive tone.
        """
        )

        # Specialized prompt for comparative questions
        self.comparison_prompt = ChatPromptTemplate.from_template(
            """
        You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer questions about company policies.
        
        The user has asked a comparative question about different policies. Use ONLY the following context to answer the question.
        If you don't have enough information, say "I don't have enough information about that in my knowledge base. Please contact HR for more details."
        
        Context:
        {context}
        
        Question: {question}
        
        In your answer:
        17. Address each policy mentioned in the question separately first
        18. Then provide a clear comparison highlighting key similarities and differences
        19. Use bullet points for clarity when listing features of each policy
        20. Include the source document names for citation purposes
        21. Format your response in a friendly, helpful tone
        
        IMPORTANT: When answering questions about relationships between policies (e.g., "Does maternity leave count as PTO?", "Is X part of Y?", "Does X affect Y?"):
        22. Begin your answer with a direct, explicit statement about the relationship (e.g., "No, maternity leave does NOT count against your PTO balance.")
        23. Cite the specific document section that addresses this relationship
        24. If the relationship isn't explicitly stated in the documents, acknowledge this and provide the most relevant information from both policies
        25. Explain how the policies interact in practice for employees
        
        The reader wants to understand the practical differences between these policies and how they might affect them.
        Focus on providing specific details, not general statements.
        
        For example, if comparing PTO and sick leave, explain how many days are provided for each, how they accrue,
        whether they roll over, and what the request process looks like for both.
        
        Example response for a relationship question like "Does maternity leave count against PTO?":
        "No, maternity leave does NOT count against your PTO balance. According to our Parental Leave Policy, maternity leave is a separate benefit that provides X weeks of paid leave following childbirth or adoption. This is completely separate from your PTO balance, which remains intact during your maternity leave. You will continue to accrue PTO while on maternity leave as stated in section X of the policy."
        """
        )

        # Specialized prompt for follow-up questions
        self.followup_prompt = ChatPromptTemplate.from_template(
            """
        You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer follow-up questions about company policies.
        
        Use ONLY the following context to answer the question. If you don't have enough information based on the context, say 
        "I don't have enough information about that in my knowledge base. Please contact HR for more details."
        
        Previous question: {previous_question}
        
        Context from both the current and previous conversation:
        {context}
        
        Current follow-up question: {question}
        
        Important instructions for follow-up questions:
        26. Remember that the user is referring to information from their previous question
        27. Use the combined context to provide a comprehensive answer
        28. Make sure to explain any terms or concepts that carry over from the previous exchange
        29. Include the source document name in your response for citation
        
        Answer the follow-up question based only on the provided context. Format your response in a friendly, helpful tone.
        """
        )

        self.parser = StrOutputParser()

    def _build_policy_cache(self):
        """Build a cache of policy files and their content hashes for better document matching"""
        # TODO: 1. Ensure the directories exist and load policy files

    def find_document_source(self, content):
        """Find the source document for a given content using improved matching techniques"""
        # TODO: 1. Check if the content is empty or None and handle string conversion

        # TODO: 2. Methods to find the source document

        # TODO: 5. Fallback to metadata if available

    def is_sensitive_topic(self, query):
        """Detect if the query is about a sensitive topic that needs special handling"""
        # TODO: 1. Check if the query contains any sensitive keywords

    def is_comparative_question(self, query):
        """Detect if the query is asking for a comparison between policies"""
        # TODO: 1. Check if this is a relationship question first

        # TODO: 2. Check for comparative terms in the query

        # TODO: 3. Check for multiple policy types in the query

    def is_relationship_question(self, query):
        """Detect if the query is asking about relationships between policies"""
        # TODO: 1. Check if the query contains any patterns indicating a relationship

    def is_followup_question(self, query, previous_question):
        """Detect if the query is a follow-up to the previous question"""
        # TODO: 1. Check if the query is empty or None

        # TODO: 2. Check if the query is a follow-up to the previous question

        # TODO: 3. Check if the query contains any follow-up indicators and if it is short

    def expand_query(self, query):
        """Expand the query with related terms to improve document retrieval"""
        # TODO: 1. Map of terms to their related terms for expansion

        # TODO: 2. Add related terms to the query

        # TODO: 3. Special handling for addiction/substance abuse questions about options or help

    def extract_entities_for_comparison(self, query):
        """Extract policy entities that should be compared"""
        # TODO: 1. Check for common policy entities in the query

    def get_relevant_documents(self, query, k=10):
        """Retrieve relevant policy documents for a query with enhanced retrieval for comparative questions"""
        # TODO: 1. Check if the vector store is available

        # TODO: 2. Check if this is a comparative question and create an expanded query

        # TODO: 3. Get retriever without filter to ensure we get documents, print original query, and get documents

        # TODO: 4. For comparative questions, we need a second phase of retrieval

        # TODO: 5. Additional handling for sensitive topics

        # TODO: 6. Print document information for debugging with improved filename detection

        # TODO: 7. Special handling for various query types

    def generate_response(
        self, query, documents, previous_question=None, previous_context=None
    ):
        """Generate a response based on retrieved documents with enhanced context organization"""
        # TODO: 1. Check if the documents are empty and format the response accordingly

        # TODO: 2. Iterate through the documents and extract page_content and metadata

        # TODO: 3. Organize context by policy type for comparative questions

        # TODO: 4. Select the appropriate prompt based on query type
