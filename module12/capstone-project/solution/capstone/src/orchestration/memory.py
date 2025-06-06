from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import datetime
import json
import os


class Conversation:
    """Class to store and manage conversation history with enhanced features"""

    def __init__(
        self,
        max_history_items=10,
        history_folder="training/conversation_history",
        log_folder="logs",
    ):
        """Initialize conversation history manager"""
        self.conversation_history = []
        self.max_history_items = max_history_items
        self.history_folder = history_folder
        self.log_folder = log_folder

        # Create folders if they don't exist
        os.makedirs(history_folder, exist_ok=True)
        os.makedirs(log_folder, exist_ok=True)

        # Initialize relevance scoring metrics
        self.topic_keywords = {
            "policy": [
                "policy",
                "policies",
                "procedure",
                "rule",
                "guideline",
                "compliance",
            ],
            "benefit": [
                "benefit",
                "benefits",
                "insurance",
                "coverage",
                "compensation",
                "perks",
            ],
            "pto": ["pto", "vacation", "time off", "leave", "holiday", "break"],
            "health": ["health", "medical", "doctor", "treatment", "wellness", "care"],
            "retirement": ["401k", "retirement", "pension", "savings", "future"],
            "training": [
                "training",
                "course",
                "development",
                "learning",
                "education",
                "skill",
            ],
        }

    def add_interaction(
        self,
        question: str,
        response: str,
        context: List[Dict[str, Any]],
        intent: Dict[str, Any],
        conversation_topic: str = None,
    ):
        """Add a new interaction to the conversation history"""
        # Generate a timestamp
        timestamp = datetime.datetime.now().isoformat()

        # Detect topics if not provided
        detected_topics = (
            conversation_topic if conversation_topic else self.detect_topics(question)
        )

        # Calculate relevance score for this interaction (0-100 scale)
        relevance_score = self.calculate_context_relevance(question, context)

        # Extract key entities from question and response
        entities = self.extract_entities(question, response)

        # Create interaction summary
        summary = self.summarize_interaction(question, response, detected_topics)

        # Create the interaction object
        interaction = {
            "timestamp": timestamp,
            "question": question,
            "response": response,
            "context_ids": (
                [self._get_context_id(ctx) for ctx in context] if context else []
            ),
            "intent": intent,
            "topics": detected_topics,
            "relevance_score": relevance_score,
            "entities": entities,
            "summary": summary,
        }

        # Add to history
        self.conversation_history.append(interaction)

        # Trim history if it exceeds max size
        if len(self.conversation_history) > self.max_history_items:
            self.conversation_history = self.conversation_history[
                -self.max_history_items :
            ]

        # Log the interaction
        self._log_interaction(interaction)

        return interaction

    def get_previous_interactions(self, count=3, topic_filter=None, min_relevance=None):
        """Get previous interactions, with optional filtering"""
        filtered_history = self.conversation_history

        # Apply topic filter if provided
        if topic_filter:
            filtered_history = [
                interaction
                for interaction in filtered_history
                if topic_filter in interaction.get("topics", [])
            ]

        # Apply relevance filter if provided
        if min_relevance is not None:
            filtered_history = [
                interaction
                for interaction in filtered_history
                if interaction.get("relevance_score", 0) >= min_relevance
            ]

        # Return the most recent items up to count
        return filtered_history[-count:]

    def detect_topics(self, text):
        """Detect topics in text based on keywords"""
        if not text:
            return []

        text_lower = text.lower()
        detected_topics = []

        for topic, keywords in self.topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)

        return detected_topics

    def calculate_context_relevance(self, query, context):
        """Calculate relevance score between query and retrieved context"""
        if not query or not context:
            return 0

        # Simple implementation based on term overlap
        query_terms = set(query.lower().split())

        total_score = 0
        for ctx in context:
            # Get content text from context
            content = (
                ctx.get("page_content", "")
                if isinstance(ctx, dict)
                else getattr(ctx, "page_content", "")
            )

            if content:
                # Count overlapping terms
                content_terms = set(content.lower().split())
                overlap = len(query_terms.intersection(content_terms))

                # Calculate score (0-100)
                ctx_score = min(100, int((overlap / max(1, len(query_terms))) * 100))
                total_score += ctx_score

        # Average the scores
        avg_score = int(total_score / max(1, len(context)))
        return avg_score

    def extract_entities(self, question, response):
        """Extract key entities from question and response"""
        entities = {"policies": [], "benefits": [], "dates": [], "numbers": []}

        # Handle case where either might be None
        question = question or ""
        response = response or ""

        # Simple keyword-based extraction
        text = question + " " + response
        text_lower = text.lower()

        # Extract policies
        policy_keywords = ["policy", "procedure", "guideline", "rule"]
        for keyword in policy_keywords:
            if keyword in text_lower:
                idx = text_lower.find(keyword)
                if idx >= 0:
                    # Try to extract policy name by looking at surrounding words
                    start = max(0, idx - 20)
                    end = min(len(text_lower), idx + 30)
                    policy_fragment = text[start:end]
                    entities["policies"].append(policy_fragment.strip())

        # Extract benefits
        benefit_keywords = [
            "insurance",
            "medical",
            "dental",
            "vision",
            "401k",
            "retirement",
        ]
        for keyword in benefit_keywords:
            if keyword in text_lower:
                entities["benefits"].append(keyword)

        # Simple number detection
        import re

        # Find numbers in text
        numbers = re.findall(r"\b\d+\b", text)
        entities["numbers"] = numbers[:5]  # Limit to first 5 numbers

        # Simple date detection for common formats
        date_patterns = [
            r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",  # MM/DD/YYYY
            r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",  # MM-DD-YYYY
            r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b",  # January 1, 2025
        ]

        for pattern in date_patterns:
            dates = re.findall(pattern, text, re.IGNORECASE)
            if dates:
                entities["dates"].extend(dates)

        # Remove duplicates while preserving order
        for key in entities:
            entities[key] = list(dict.fromkeys(entities[key]))

        return entities

    def summarize_interaction(self, question, response, topics):
        """Create a summary of the interaction"""
        # Handle null values
        if not question:
            question = ""
        if not response:
            response = ""
        if not topics:
            topics = ["general"]

        # Simple summary creation - in a real system this could use an actual summarization model
        summary = (
            f"Question about {', '.join(topics) if topics else 'general HR topics'}"
        )

        # Add word count
        question_words = len(question.split())
        response_words = len(response.split())
        summary += f". {question_words} word question, {response_words} word response"

        return summary

    def save_conversation_snapshot(self, employee_id="anonymous"):
        """Save the current conversation history to disk"""
        if not self.conversation_history:
            return None

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.history_folder}/{employee_id}_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(self.conversation_history, f, indent=2)

        return filename

    def _get_context_id(self, context):
        """Generate a consistent ID for a context item"""
        if not context:
            return None

        # Try to get content and source
        if isinstance(context, dict):
            content = context.get("page_content", "")
            source = context.get("metadata", {}).get("source", "unknown")
        else:
            content = getattr(context, "page_content", "")
            source = getattr(getattr(context, "metadata", {}), "source", "unknown")

        # Create a fingerprint using the first 50 chars of content
        content_id = content[:50].strip().replace("\n", " ")
        return f"{source}:{content_id}"

    def _log_interaction(self, interaction):
        """Log the interaction to a file"""
        date = datetime.datetime.now().strftime("%Y%m%d")
        log_file = f"{self.log_folder}/conversation_{date}.log"

        with open(log_file, "a") as f:
            f.write(f"\n--- {interaction['timestamp']} ---\n")
            f.write(f"QUERY: {interaction['question']}\n")
            f.write(f"TOPICS: {interaction['topics']}\n")
            f.write(f"INTENT: {interaction['intent']}\n")
            f.write(f"RELEVANCE: {interaction['relevance_score']}\n")
            f.write(f"RESPONSE: {interaction['response']}\n")
            f.write(f"SUMMARY: {interaction['summary']}\n")
            f.write(f"ENTITIES: {json.dumps(interaction['entities'])}\n")


# Simple conversation diagnostics tool for debugging
class ConversationDiagnostics:
    """Tools for diagnosing conversation quality and debugging issues"""

    def __init__(self, log_folder="logs"):
        self.log_folder = log_folder
        os.makedirs(log_folder, exist_ok=True)

    def log_query_processing(
        self,
        query,
        expanded_query=None,
        is_followup=False,
        is_comparative=False,
        is_sensitive=False,
        detected_entities=None,
        document_count=0,
    ):
        """Log detailed query processing information"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{self.log_folder}/query_processing_{datetime.datetime.now().strftime('%Y%m%d')}.log"

        with open(log_file, "a") as f:
            f.write(f"\n--- {timestamp} ---\n")
            f.write(f"ORIGINAL QUERY: {query}\n")
            if expanded_query:
                f.write(f"EXPANDED QUERY: {expanded_query}\n")
            f.write(f"QUERY TYPE: {'Follow-up' if is_followup else 'New'}\n")
            f.write(f"COMPARATIVE: {is_comparative}\n")
            f.write(f"SENSITIVE: {is_sensitive}\n")
            if detected_entities:
                f.write(f"DETECTED ENTITIES: {detected_entities}\n")
            f.write(f"DOCUMENTS RETRIEVED: {document_count}\n")

    def log_context_retrieval(self, retrieval_time, documents, relevance_score=None):
        """Log information about context retrieval"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{self.log_folder}/retrieval_{datetime.datetime.now().strftime('%Y%m%d')}.log"

        with open(log_file, "a") as f:
            f.write(f"\n--- {timestamp} ---\n")
            f.write(f"RETRIEVAL TIME: {retrieval_time:.3f}s\n")
            f.write(f"DOCUMENT COUNT: {len(documents)}\n")
            if relevance_score is not None:
                f.write(f"RELEVANCE SCORE: {relevance_score}\n")

            # Log document sources
            sources = []
            for doc in documents:
                if hasattr(doc, "metadata") and "source" in doc.metadata:
                    sources.append(doc.metadata["source"])
                elif (
                    isinstance(doc, dict)
                    and "metadata" in doc
                    and "source" in doc["metadata"]
                ):
                    sources.append(doc["metadata"]["source"])

            if sources:
                f.write(f"DOCUMENT SOURCES: {sources}\n")

    def create_conversation_report(self, conversation_history):
        """Create a report analyzing conversation quality"""
        if not conversation_history:
            return "No conversation history to analyze."

        # Calculate metrics
        total_interactions = len(conversation_history)
        avg_relevance = (
            sum(item.get("relevance_score", 0) for item in conversation_history)
            / total_interactions
        )

        topics_count = {}
        for item in conversation_history:
            for topic in item.get("topics", []):
                topics_count[topic] = topics_count.get(topic, 0) + 1

        # Generate report
        report = f"Conversation Analysis Report\n"
        report += f"==========================\n\n"
        report += f"Total interactions: {total_interactions}\n"
        report += f"Average relevance score: {avg_relevance:.1f}/100\n\n"

        report += f"Topic distribution:\n"
        for topic, count in topics_count.items():
            percentage = (count / total_interactions) * 100
            report += f"  - {topic}: {count} ({percentage:.1f}%)\n"

        # Add some sample interactions
        report += f"\nSample interactions:\n"
        for i, item in enumerate(conversation_history[-3:]):
            question = item.get("question", "No question")
            response = item.get("response", "No response")
            topics = item.get("topics", [])
            relevance = item.get("relevance_score", 0)

            # Format response with safe slicing
            response_preview = (
                response[:100] + "..." if response and len(response) > 100 else response
            )

            report += f"\n{i+1}. Q: {question}\n"
            report += f"   R: {response_preview}\n"
            report += f"   Topics: {topics}\n"
            report += f"   Relevance: {relevance}\n"

        return report


# Conversation memory for storing and retrieving conversation state
class ConversationMemory:
    """Enhanced conversation memory component for maintaining state across interactions"""

    def __init__(self):
        self.conversation = Conversation()
        self.diagnostics = ConversationDiagnostics()
        self.current_topic = None
        self.topic_switching_detected = False
        self.conversation_summary = ""
        self.key_entities = {
            "policies": [],
            "benefits": [],
            "training": [],
            "dates": [],
        }

    def update(self, state):
        """Update memory with new state information"""
        # Extract key information from state - supporting both state objects and dictionaries
        # This allows compatibility with both workflow and test script usage
        if isinstance(state, dict):
            # Handle dictionary state (used in test scripts)
            question = state.get("user_input", "")
            response = state.get("response", "")
            context = state.get("context", [])
            intent = state.get("intent", {})
            conversation_topic = state.get("conversation_topic", "general")
        else:
            # Handle state object (used in workflow)
            question = state.user_input
            response = state.response
            context = state.context
            intent = state.intent
            conversation_topic = state.conversation_topic

        # Detect topic switching
        if (
            self.current_topic
            and conversation_topic
            and self.current_topic != conversation_topic
        ):
            self.topic_switching_detected = True
        self.current_topic = conversation_topic

        # Add interaction to history
        interaction = self.conversation.add_interaction(
            question, response, context, intent, conversation_topic
        )

        # Update entity tracking
        for entity_type, entities in interaction["entities"].items():
            if entity_type in self.key_entities:
                self.key_entities[entity_type].extend(entities)
                # Remove duplicates while preserving order
                self.key_entities[entity_type] = list(
                    dict.fromkeys(self.key_entities[entity_type])
                )

        # Update conversation summary
        self._update_conversation_summary()

        return self

    def get_relevant_history(self, query, topic=None, count=3):
        """Get relevant conversation history for the current query"""
        # If topic switching was detected, prioritize recent history
        if self.topic_switching_detected:
            return self.conversation.get_previous_interactions(count=count)

        # Otherwise, try to get topic-relevant history with good relevance
        topic_filter = topic or self.current_topic
        relevant_history = self.conversation.get_previous_interactions(
            count=count, topic_filter=topic_filter, min_relevance=50
        )

        # Fall back to recent history if no relevant history found
        if not relevant_history:
            relevant_history = self.conversation.get_previous_interactions(count=count)

        return relevant_history

    def get_summary(self):
        """Get a summary of the conversation so far"""
        return self.conversation_summary

    def get_key_entities(self):
        """Get key entities extracted from the conversation"""
        return self.key_entities

    def save_snapshot(self, employee_id="anonymous"):
        """Save a snapshot of the conversation history"""
        return self.conversation.save_conversation_snapshot(employee_id)

    def generate_diagnostics_report(self):
        """Generate a report with conversation diagnostics"""
        return self.diagnostics.create_conversation_report(
            self.conversation.conversation_history
        )

    def _update_conversation_summary(self):
        """Update the conversation summary based on recent interactions"""
        # Get recent history
        recent_history = self.conversation.get_previous_interactions(count=5)

        if not recent_history:
            self.conversation_summary = "No conversation history."
            return

        # Build summary
        summary = "Conversation Summary:\n"

        # Add topic information
        all_topics = []
        for interaction in recent_history:
            all_topics.extend(interaction.get("topics", []))

        # Count topics and get top 3
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        top_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_topics:
            summary += (
                "Main topics: "
                + ", ".join(f"{topic}" for topic, _ in top_topics)
                + "\n"
            )

        # Summarize recent interactions
        summary += f"Recent interactions: {len(recent_history)}\n"
        for i, interaction in enumerate(recent_history):
            summary += f"{i+1}. {interaction.get('summary', 'Interaction')}\n"

        self.conversation_summary = summary
