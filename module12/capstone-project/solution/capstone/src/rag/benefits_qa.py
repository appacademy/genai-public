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
        self.llm = llm
        try:
            self.vector_store = load_vector_store(vector_store_path)
        except FileNotFoundError:
            # If vector store doesn't exist yet, we'll initialize with empty retriever
            # It will be populated later during setup
            self.vector_store = None

        # Build a content cache of benefit files for better matching
        self.benefit_files = {}
        self.benefit_content_hashes = {}
        self._build_benefit_cache()

        # Standard QA prompt for general benefit questions
        self.qa_prompt = ChatPromptTemplate.from_template(
            """
        You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer questions about employee benefits.
        
        Use ONLY the following context to answer the question. If you don't have enough information based on the context, say 
        "I don't have enough information about that in my knowledge base. Please contact HR for more details."
        
        Context:
        {context}
        
        Question: {question}
        
        Answer the question based only on the provided context. Include the source document name in your response 
        for citation purposes. Format your response in a friendly, helpful tone.
        
        When answering follow-up questions or comparing policies, make sure to use all relevant context provided.
        If the question asks for a comparison between different benefits or policies, make sure
        to address all relevant aspects in your answer with clear distinctions between them.
        
        If multiple benefits are mentioned in the question, be sure to discuss each one and highlight the key 
        similarities and differences between them. Structure your answer clearly, using bullet points where appropriate.
        """
        )

        # Specialized prompt for sensitive topics like mental health, disabilities, etc.
        self.sensitive_topic_prompt = ChatPromptTemplate.from_template(
            """
        You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer questions about employee benefits,
        including sensitive topics like mental health resources, disability accommodations, or wellness programs.
        
        Use the following context to answer the question.
        
        Context:
        {context}
        
        Question: {question}
        
        Important instructions for sensitive topics:
        1. Present information about support resources and company assistance programs first
        2. Explain the benefits' protection and confidentiality provisions clearly
        3. Describe eligibility and enrollment processes in clear terms
        4. Use compassionate, non-judgmental language throughout your response
        5. Emphasize that seeking help is encouraged and supported
        6. Include the source document name for citation
        
        For substance abuse, addiction, or mental health questions specifically:
        1. Always mention Employee Assistance Program (EAP) resources if available in the context
        2. Discuss both the Wellness Program and related policies together if relevant
        3. Emphasize confidentiality and non-punitive aspects of seeking help
        4. Synthesize information from multiple documents to provide a complete answer
        5. Address how different benefits and programs work together to support employees
        
        If the context doesn't specifically address the question (for example, if the Wellness Program doesn't 
        explicitly mention addiction):
        1. Acknowledge this limitation clearly: "Based on the available information, our [specific policy] documentation 
           doesn't explicitly mention [topic]. However, I can share what our policies do cover:"
        2. Provide the most relevant information you do have (e.g., smoking cessation programs, EAP resources, etc.)
        3. Offer to search across all policies: "Would you like me to search all company policies for information about [topic]?"
        4. Recommend contacting HR for more specific information
        5. Do NOT respond with only "I don't have enough information" - always try to provide some helpful direction
        
        Answer the question based on the provided context. Format your response in a friendly, supportive tone.
        """
        )

        # Specialized prompt for comparative questions
        self.comparison_prompt = ChatPromptTemplate.from_template(
            """
        You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer questions about employee benefits.
        
        The user has asked a comparative question about different benefits. Use ONLY the following context to answer the question.
        If you don't have enough information, say "I don't have enough information about that in my knowledge base. Please contact HR for more details."
        
        Context:
        {context}
        
        Question: {question}
        
        In your answer:
        1. Address each benefit mentioned in the question separately first
        2. Then provide a clear comparison highlighting key similarities and differences
        3. Use bullet points for clarity when listing features of each benefit
        4. Include the source document names for citation purposes
        5. Format your response in a friendly, helpful tone
        
        IMPORTANT: When answering questions about relationships between benefits or policies (e.g., "Does maternity leave count as PTO?", "Is X part of Y?", "Does X affect Y?"):
        1. Begin your answer with a direct, explicit statement about the relationship (e.g., "No, maternity leave does NOT count against your PTO balance.")
        2. Cite the specific document section that addresses this relationship
        3. If the relationship isn't explicitly stated in the documents, acknowledge this and provide the most relevant information from both benefits
        4. Explain how the benefits interact in practice for employees
        
        The reader wants to understand the practical differences between these benefits and how they might affect them.
        Focus on providing specific details such as coverage amounts, eligibility requirements, enrollment periods,
        and usage processes.
        
        Example response for a relationship question like "Does maternity leave count against PTO?":
        "No, maternity leave does NOT count against your PTO balance. According to our Parental Leave Policy, maternity leave is a separate benefit that provides X weeks of paid leave following childbirth or adoption. This is completely separate from your PTO balance, which remains intact during your maternity leave. You will continue to accrue PTO while on maternity leave as stated in section X of the policy."
        """
        )

        # Specialized prompt for follow-up questions
        self.followup_prompt = ChatPromptTemplate.from_template(
            """
        You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer follow-up questions about employee benefits.
        
        Use ONLY the following context to answer the question. If you don't have enough information based on the context, say 
        "I don't have enough information about that in my knowledge base. Please contact HR for more details."
        
        Previous question: {previous_question}
        
        Context from both the current and previous conversation:
        {context}
        
        Current follow-up question: {question}
        
        Important instructions for follow-up questions:
        1. Remember that the user is referring to information from their previous question
        2. Use the combined context to provide a comprehensive answer
        3. Make sure to explain any terms or concepts that carry over from the previous exchange
        4. Include the source document name in your response for citation
        
        Answer the follow-up question based only on the provided context. Format your response in a friendly, helpful tone.
        """
        )

        self.parser = StrOutputParser()

    def _build_benefit_cache(self):
        """Build a cache of benefit files and their content hashes for better document matching"""
        for benefit_dir in ["data/benefits", "data/policies"]:
            if os.path.exists(benefit_dir):
                for benefit_file in os.listdir(benefit_dir):
                    if not benefit_file.endswith(".txt"):
                        continue

                    file_path = os.path.join(benefit_dir, benefit_file)
                    try:
                        with open(
                            file_path, "r", encoding="utf-8", errors="replace"
                        ) as f:
                            content = f.read()
                            self.benefit_files[benefit_file] = content

                            # Create content hashes of different lengths for partial matching
                            content_lower = content.lower()
                            for length in [100, 200, 300, 500]:
                                if len(content_lower) >= length:
                                    content_start = content_lower[:length]
                                    hash_key = hashlib.md5(
                                        content_start.encode()
                                    ).hexdigest()
                                    self.benefit_content_hashes[hash_key] = benefit_file
                    except Exception as e:
                        print(f"Error reading {benefit_file}: {e}")

    def find_document_source(self, content):
        """Find the source document for a given content using improved matching techniques"""
        if not content:
            return "Unknown"

        # Handle both string content and document objects/dictionaries
        if isinstance(content, dict):
            # It's a dictionary - extract page_content
            content = content.get("page_content", "")
        elif hasattr(content, "page_content"):
            # It's a Document object
            content = content.page_content

        # If we still don't have content as a string, convert it
        if not isinstance(content, str):
            content = str(content)

        content_lower = content.lower()

        # Method 1: Check if the content is directly in a benefit file
        for benefit_file, file_content in self.benefit_files.items():
            if content_lower in file_content.lower():
                return benefit_file

        # Method 2: Check content hashes for partial matching
        for length in [100, 200, 300]:
            if len(content_lower) >= length:
                content_start = content_lower[:length]
                hash_key = hashlib.md5(content_start.encode()).hexdigest()
                if hash_key in self.benefit_content_hashes:
                    return self.benefit_content_hashes[hash_key]

        # Method 3: Check for matching first paragraph
        first_paragraph = (
            content_lower.split("\n\n")[0]
            if "\n\n" in content_lower
            else content_lower[:200]
        )
        for benefit_file, file_content in self.benefit_files.items():
            if first_paragraph in file_content.lower():
                return benefit_file

        # Method 4: Try to match based on benefit name in content
        for benefit_file in self.benefit_files.keys():
            benefit_name = (
                os.path.splitext(benefit_file)[0]
                .lower()
                .replace("-", " ")
                .replace("_", " ")
            )
            if benefit_name in content_lower[:300]:
                return benefit_file

            # Special handling for common benefit types
            if "benefit" in benefit_file.lower() and "benefit" in content_lower[:300]:
                return benefit_file
            if "health" in benefit_file.lower() and "health" in content_lower[:300]:
                return benefit_file
            if (
                "insurance" in benefit_file.lower()
                and "insurance" in content_lower[:300]
            ):
                return benefit_file

        # Fallback to metadata if available
        metadata_source = getattr(content, "metadata", {}).get("source_file", "")
        if metadata_source:
            return metadata_source

        # Final fallback to best guess based on content keywords
        if "health" in content_lower[:500] or "medical" in content_lower[:500]:
            return "Employee-Benefits-and-Perks-1.txt"
        if "dental" in content_lower[:500] or "vision" in content_lower[:500]:
            return "Employee-Benefits-and-Perks-1.txt"
        if "401k" in content_lower[:500] or "retirement" in content_lower[:500]:
            return "Employee-Benefits-and-Perks-1.txt"
        if "wellness" in content_lower[:500] or "mental health" in content_lower[:500]:
            return "Employee-Wellness-Program-Policy.txt"

        return "Employee-Benefits-and-Perks-1.txt"  # Better than "Unknown"

    def is_sensitive_topic(self, query):
        """Detect if the query is about a sensitive topic that needs special handling"""
        sensitive_keywords = [
            "mental health",
            "depression",
            "anxiety",
            "wellness",
            "disability",
            "accommodation",
            "medical condition",
            "illness",
            "injury",
            "stress",
            "burnout",
            "therapy",
            "counseling",
            "eap",
            "assistance program",
            "leave of absence",
            "family leave",
            "pregnancy",
            "maternity",
            "paternity",
            "life insurance",
            "death benefit",
        ]
        return any(keyword in query.lower() for keyword in sensitive_keywords)

    def is_comparative_question(self, query):
        """Detect if the query is asking for a comparison between benefits"""
        # Check if this is a relationship question first
        if self.is_relationship_question(query):
            return True

        comparative_terms = [
            "compare",
            "comparison",
            "contrast",
            "difference",
            "different",
            "versus",
            " vs ",
            " or ",
            "better",
            "worse",
            "preferred",
            "choose between",
            "similarities",
            "similar",
            "same as",
        ]

        # Check for comparative terms
        if any(term in query.lower() for term in comparative_terms):
            return True

        # Check for multiple benefit types in the query
        benefit_types = [
            "health",
            "dental",
            "vision",
            "medical",
            "insurance",
            "life insurance",
            "disability",
            "retirement",
            "401k",
            "pension",
            "wellness",
            "gym",
            "reimbursement",
            "tuition",
            "education",
            "parental",
            "maternity",
            "paternity",
            "leave",
            "vacation",
            "pto",
        ]

        found_types = [benefit for benefit in benefit_types if benefit in query.lower()]
        return len(found_types) > 1

    def is_relationship_question(self, query):
        """Detect if the query is asking about relationships between benefits"""
        query_lower = query.lower()

        # Pattern 1: "Does X count against Y"
        count_patterns = [
            "count against",
            "counts against",
            "counted against",
            "counting against",
            "use my",
            "uses my",
            "using my",
            "part of",
            "included in",
            "separate from",
            "affect my",
            "affects my",
            "impact my",
            "impacts my",
        ]

        if any(pattern in query_lower for pattern in count_patterns):
            return True

        # Pattern 2: "Is X separate from Y"
        if "separate" in query_lower and any(
            benefit in query_lower
            for benefit in [
                "pto",
                "vacation",
                "leave",
                "time off",
                "maternity",
                "paternity",
                "parental",
            ]
        ):
            return True

        # Pattern 3: Direct questions about relationships
        relationship_patterns = [
            "how does .* relate to",
            "how do .* relate to",
            "connection between .* and",
            "relationship between .* and",
            "how .* works with",
        ]

        for pattern in relationship_patterns:
            if re.search(pattern, query_lower):
                return True

        return False

    def is_followup_question(self, query, previous_question):
        """Detect if the query is a follow-up to the previous question"""
        if not previous_question:
            return False

        # Check for pronouns and demonstratives that reference previous content
        followup_indicators = [
            "it",
            "this",
            "that",
            "they",
            "them",
            "those",
            "their",
            "its",
            "these",
            "the benefit",
            "the plan",
            "the coverage",
            "the policy",
            "the document",
            "tell me more",
            "explain",
            "elaborate",
            "clarify",
            "what about",
            "how about",
            "how does",
            "how do",
        ]

        # Check if the query contains any follow-up indicators
        if any(indicator in query.lower() for indicator in followup_indicators):
            return True

        # Check if the query is very short (likely a follow-up)
        if len(query.split()) <= 5:
            return True

        return False

    def expand_query(self, query):
        """Expand the query with related terms to improve document retrieval"""
        expanded_query = query

        # Map of terms to their related terms for expansion
        term_expansions = {
            "health": "medical healthcare insurance wellness doctor",
            "dental": "dentist teeth orthodontic dental insurance",
            "vision": "eye glasses contacts vision insurance optometrist",
            "retirement": "401k pension retirement plan savings future",
            "parental": "maternal paternity maternity leave baby child",
            "disability": "short-term long-term disability insurance ada",
            "leave": "time off absence pto vacation holiday",
            "vacation": "time off pto leave holiday break",
            "wellness": "fitness health gym mental physical wellbeing",
            "mental health": "counseling therapy eap stress burnout assistance",
            "life insurance": "death benefit survivor dependent coverage term",
        }

        # Add related terms to the query
        for term, expansion in term_expansions.items():
            if term in query.lower() and not all(
                exp in query.lower() for exp in expansion.split()
            ):
                expanded_query += f" {expansion}"

        return expanded_query

    def extract_entities_for_comparison(self, query):
        """Extract benefit entities that should be compared"""
        # Common benefit entities to look for
        benefit_entities = {
            "health": ["health", "healthcare", "medical", "insurance"],
            "dental": ["dental", "teeth", "dentist"],
            "vision": ["vision", "eye", "glasses", "contacts"],
            "retirement": ["retirement", "401k", "pension", "savings"],
            "parental": ["parental", "maternity", "paternity", "baby", "child"],
            "disability": ["disability", "ada", "accommodation"],
            "leave": ["leave", "time off", "pto", "vacation"],
            "wellness": ["wellness", "fitness", "gym", "wellbeing"],
            "mental health": ["mental health", "counseling", "therapy", "eap"],
            "life insurance": ["life insurance", "death benefit", "survivor"],
        }

        found_entities = []

        # Look for each entity type in the query
        for entity_type, keywords in benefit_entities.items():
            if any(keyword in query.lower() for keyword in keywords):
                found_entities.append(entity_type)

        return found_entities

    def get_relevant_documents(self, query, k=10):
        """Retrieve relevant benefits documents for a query with enhanced retrieval for comparative questions"""
        if not self.vector_store:
            return []

        # Check if this is a comparative question
        is_comparative = self.is_comparative_question(query)

        # Create expanded query for better retrieval
        expanded_query = self.expand_query(query)

        # Get retriever without filter to ensure we get documents
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k if not is_comparative else k * 2
            },  # Get more docs for comparative questions
        )

        # Print original and expanded query for debugging
        if expanded_query != query:
            print(f"\nOriginal query: '{query}'")
            print(f"Expanded query: '{expanded_query}'")

        # Try to get documents using the expanded query
        docs = retriever.invoke(expanded_query)

        # For comparative questions, we need a second phase of retrieval
        if is_comparative:
            entities = self.extract_entities_for_comparison(query)
            if len(entities) > 1:
                print(f"Detected comparative question about: {', '.join(entities)}")

                # Create individual queries for each entity
                entity_docs = []
                for entity in entities:
                    entity_query = f"{entity} benefit"
                    entity_docs.extend(retriever.invoke(entity_query))

                # Add these entity-specific docs to our results
                docs.extend(entity_docs)

                # Remove duplicates while preserving order
                seen = set()
                unique_docs = []
                for doc in docs:
                    doc_id = doc.page_content[
                        :100
                    ]  # Use first 100 chars as a simple ID
                    if doc_id not in seen:
                        seen.add(doc_id)
                        unique_docs.append(doc)

                docs = unique_docs[
                    : k + 5
                ]  # Limit to slightly more than k to have enough context

        # Additional handling for sensitive topics
        if self.is_sensitive_topic(query):
            # Try to find relevant sensitive topic documents
            sensitive_topic_keywords = [
                keyword
                for keyword in [
                    "mental health",
                    "wellness",
                    "disability",
                    "accommodation",
                    "leave",
                    "counseling",
                    "assistance program",
                    "life insurance",
                ]
                if keyword in query.lower()
            ]

            if sensitive_topic_keywords:
                for keyword in sensitive_topic_keywords:
                    topic_docs = retriever.invoke(keyword)
                    docs.extend(topic_docs)

                # Remove duplicates
                seen = set()
                unique_docs = []
                for doc in docs:
                    doc_id = doc.page_content[:100]
                    if doc_id not in seen:
                        seen.add(doc_id)
                        unique_docs.append(doc)

                docs = unique_docs[: k + 5]

        # Print document information for debugging with improved filename detection
        print(f"\nRetrieved {len(docs)} documents for query: '{query}'")
        for i, doc in enumerate(docs):
            # Use the improved document source finder
            file_match = self.find_document_source(doc.page_content)

            source_type = doc.metadata.get("source", "Unknown")
            print(f"  Doc {i+1}: {file_match} (Type: {source_type})")

            # Replace "First 100 chars:" with "Preview:"
            preview = doc.page_content[:100].replace(chr(10), " ")
            if len(doc.page_content) > 100:
                preview += "..."
            print(f"  Preview: {preview}")

        # Special handling for various query types

        # Health benefit queries
        if any(term in query.lower() for term in ["health", "medical", "insurance"]):
            print("  Health benefit query detected, returning all documents")
            print("\n")
            return docs

        # Mental health queries
        if (
            "mental health" in query.lower()
            or "wellness" in query.lower()
            or "eap" in query.lower()
        ):
            print("  Mental health/wellness query detected, returning all documents")
            print("\n")
            return docs

        # Retirement benefit queries
        if (
            "retirement" in query.lower()
            or "401k" in query.lower()
            or "pension" in query.lower()
        ):
            print("  Retirement benefit query detected, returning all documents")
            print("\n")
            return docs

        # Comparative queries need documents from multiple categories
        if is_comparative:
            print("  Comparative query detected, returning all documents")
            print("\n")
            return docs

        # Filter to benefit documents manually if needed
        benefit_docs = [doc for doc in docs if doc.metadata.get("source") == "benefit"]

        # Add extra blank lines for readability before Jenna's response
        print("\n")

        # If no benefit docs found, return all docs instead of an empty list
        return benefit_docs if benefit_docs else docs

    def generate_response(
        self, query, documents, previous_question=None, previous_context=None
    ):
        """Generate a response based on retrieved documents with enhanced context organization"""
        if not documents:
            return "I don't have enough information about that in my knowledge base. Please contact HR for more details."

        # Format context from documents with improved source information and grouping
        formatted_docs = []
        doc_by_benefit = {}  # Group documents by benefit type

        for doc in documents:
            # Use the improved document source finder
            file_match = self.find_document_source(doc.page_content)

            # For comparative questions, group by benefit type
            if self.is_comparative_question(query):
                benefit_type = (
                    file_match.split("-")[0] if "-" in file_match else file_match
                )
                if benefit_type not in doc_by_benefit:
                    doc_by_benefit[benefit_type] = []
                doc_by_benefit[benefit_type].append(
                    f"Document: {file_match}\n{doc.page_content}"
                )
            else:
                formatted_docs.append(f"Document: {file_match}\n{doc.page_content}")

        # For comparative questions, organize context by benefit type
        if self.is_comparative_question(query) and doc_by_benefit:
            for benefit_type, docs in doc_by_benefit.items():
                formatted_docs.append(f"--- {benefit_type} BENEFIT INFORMATION ---")
                formatted_docs.extend(docs)

        context = "\n\n".join(formatted_docs)

        # Select the appropriate prompt based on query type
        if self.is_followup_question(query, previous_question) and previous_question:
            print("  Using specialized follow-up question prompt")
            # For follow-up questions, include the previous question in the prompt
            chain = self.followup_prompt | self.llm | self.parser
            response = chain.invoke(
                {
                    "context": context,
                    "question": query,
                    "previous_question": previous_question,
                }
            )
        elif self.is_comparative_question(query):
            print("  Using specialized comparative question prompt")
            chain = self.comparison_prompt | self.llm | self.parser
            response = chain.invoke({"context": context, "question": query})
        elif self.is_sensitive_topic(query):
            print("  Using specialized sensitive topic prompt")
            chain = self.sensitive_topic_prompt | self.llm | self.parser
            response = chain.invoke({"context": context, "question": query})
        else:
            print("  Using standard QA prompt")
            chain = self.qa_prompt | self.llm | self.parser
            response = chain.invoke({"context": context, "question": query})

        return response
