import time
import re
import uuid
from typing import List, Dict, Any
from services.ollama_service import OllamaService


class PromptTest:
    """Framework for testing and comparing prompt variations."""

    def __init__(self, model: str = "gemma:3-4b"):
        self.model = model
        self.results = {}
        self.ollama_service = OllamaService()

    def test_prompt(
        self, prompt_template, test_queries: List[str], prompt_id: str = None
    ) -> Dict[str, Any]:
        """Test a prompt template against a set of queries."""
        if not prompt_id:
            prompt_id = str(uuid.uuid4())

        results = {
            "prompt_template": prompt_template.to_dict(),
            "model": self.model,
            "timestamp": time.time(),
            "responses": [],
            "metrics": {},
        }

        full_prompt = prompt_template.get_full_prompt()

        for query in test_queries:
            query_prompt = f"{full_prompt}\n\n# Input\n{query}"

            start_time = time.time()
            try:
                response = self.ollama_service.generate(
                    prompt=query_prompt,
                    model=self.model,
                    temperature=0.7,
                    force_real_llm=False,  # Allow fallback to mock if the model isn't found
                )

                response_text = response.get("response", "")

                results["responses"].append(
                    {
                        "query": query,
                        "response": response_text,
                        "tokens_used": response.get("estimated_total_tokens", 0),
                        "response_time": response.get(
                            "response_time", time.time() - start_time
                        ),
                        "completion_tokens": response.get(
                            "estimated_completion_tokens", 0
                        ),
                        "prompt_tokens": response.get("estimated_prompt_tokens", 0),
                    }
                )
            except Exception as e:
                results["responses"].append(
                    {
                        "query": query,
                        "error": str(e),
                        "response_time": time.time() - start_time,
                    }
                )

        # Calculate overall metrics
        results["metrics"] = self.calculate_metrics(
            [r.get("response", "") for r in results["responses"] if "response" in r],
            expected_format=prompt_template.response_format,
        )

        self.results[prompt_id] = results
        return {"prompt_id": prompt_id, "results": results}

    def run_ab_test(
        self,
        prompt_a,
        prompt_b,
        test_queries: List[str],
        a_label: str = "Prompt A",
        b_label: str = "Prompt B",
    ) -> Dict[str, Any]:
        """Run a comparison test between two prompt variations."""
        test_a = self.test_prompt(prompt_a, test_queries)
        test_b = self.test_prompt(prompt_b, test_queries)

        comparison_id = f"ab_{test_a['prompt_id']}_{test_b['prompt_id']}"

        comparison = {
            "comparison_id": comparison_id,
            "timestamp": time.time(),
            "a": {
                "label": a_label,
                "prompt_id": test_a["prompt_id"],
                "metrics": test_a["results"]["metrics"],
            },
            "b": {
                "label": b_label,
                "prompt_id": test_b["prompt_id"],
                "metrics": test_b["results"]["metrics"],
            },
            "per_query_comparison": [],
        }

        # Compare individual query results
        for i, query in enumerate(test_queries):
            a_response = (
                test_a["results"]["responses"][i]
                if i < len(test_a["results"]["responses"])
                else None
            )
            b_response = (
                test_b["results"]["responses"][i]
                if i < len(test_b["results"]["responses"])
                else None
            )

            if (
                a_response
                and b_response
                and "response" in a_response
                and "response" in b_response
            ):
                query_comparison = {
                    "query": query,
                    "a_response": a_response["response"],
                    "b_response": b_response["response"],
                    "a_tokens": a_response.get("tokens_used", 0),
                    "b_tokens": b_response.get("tokens_used", 0),
                    "a_time": a_response.get("response_time", 0),
                    "b_time": b_response.get("response_time", 0),
                }
                comparison["per_query_comparison"].append(query_comparison)

        self.results[comparison_id] = comparison
        return {"comparison_id": comparison_id, "comparison": comparison}

    def calculate_metrics(
        self, responses: List[str], expected_format: str = None
    ) -> Dict[str, float]:
        """Calculate quality metrics for a set of responses."""
        metrics = {}

        # 1. Average response length (in characters)
        if responses:
            avg_length = sum(len(r) for r in responses) / len(responses)
            metrics["avg_length"] = avg_length

            # 2. Response consistency (standard deviation of lengths)
            if len(responses) > 1:
                variance = sum((len(r) - avg_length) ** 2 for r in responses) / len(
                    responses
                )
                metrics["length_std_dev"] = variance**0.5
            else:
                metrics["length_std_dev"] = 0

        # 3. Format adherence (if expected format specified)
        if expected_format:
            format_indicators = [
                "numbered list",
                "bullet points",
                "json",
                "table",
                "paragraph",
                "steps",
                "pros and cons",
                "markdown",
                "code block",
            ]

            expected_formats = []
            for indicator in format_indicators:
                if indicator.lower() in expected_format.lower():
                    expected_formats.append(indicator)

            format_adherence_scores = []
            for response in responses:
                score = 0
                for fmt in expected_formats:
                    if fmt == "numbered list" and re.search(
                        r"^\s*\d+\.", response, re.MULTILINE
                    ):
                        score += 1
                    elif fmt == "bullet points" and re.search(
                        r"^\s*[\*\-\•]", response, re.MULTILINE
                    ):
                        score += 1
                    elif fmt == "json" and re.search(
                        r"^\s*\{.*\}\s*$", response, re.DOTALL
                    ):
                        score += 1
                    elif fmt == "code block" and re.search(r"```", response):
                        score += 1
                    elif fmt == "markdown" and re.search(r"#|==|--|\*\*|__", response):
                        score += 1

                if expected_formats:
                    format_adherence_scores.append(score / len(expected_formats))

            if format_adherence_scores:
                metrics["format_adherence"] = sum(format_adherence_scores) / len(
                    format_adherence_scores
                )

        return metrics
