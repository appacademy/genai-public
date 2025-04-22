import time
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from models.prompt_template import PromptTemplate
from models.prompt_test import PromptTest


class PromptLab:
    """Main workbench for creating, testing, and optimizing prompts."""

    def __init__(self):
        self.prompt_templates = {}
        self.test_results = {}
        self.tester = PromptTest()

    def add_prompt_template(self, template: PromptTemplate, name: str):
        """Add a prompt template to the workbench."""
        if not template.validate():
            raise ValueError("Prompt template is missing required components")
        self.prompt_templates[name] = template
        return name

    def test_prompt(
        self, template_name: str, test_queries: List[str]
    ) -> Dict[str, Any]:
        """Test a specific prompt template."""
        if template_name not in self.prompt_templates:
            raise ValueError(f"Template '{template_name}' not found")

        template = self.prompt_templates[template_name]
        result = self.tester.test_prompt(template, test_queries)

        result_id = f"{template_name}_v{template.version}_{result['prompt_id']}"
        self.test_results[result_id] = result["results"]

        return {"result_id": result_id, "results": result["results"]}

    def compare_prompts(
        self, template_a_name: str, template_b_name: str, test_queries: List[str]
    ) -> Dict[str, Any]:
        """Compare two prompt templates."""
        if (
            template_a_name not in self.prompt_templates
            or template_b_name not in self.prompt_templates
        ):
            raise ValueError("One or both template names not found")

        template_a = self.prompt_templates[template_a_name]
        template_b = self.prompt_templates[template_b_name]

        result = self.tester.run_ab_test(
            template_a,
            template_b,
            test_queries,
            a_label=f"{template_a_name} v{template_a.version}",
            b_label=f"{template_b_name} v{template_b.version}",
        )

        comparison_id = (
            f"compare_{template_a_name}_vs_{template_b_name}_{result['comparison_id']}"
        )
        self.test_results[comparison_id] = result["comparison"]

        return {"comparison_id": comparison_id, "comparison": result["comparison"]}

    def generate_report(self, result_id: str) -> str:
        """Generate a detailed report of test results."""
        if result_id not in self.test_results:
            raise ValueError(f"Result ID '{result_id}' not found")

        result = self.test_results[result_id]

        # Check if this is a comparison or a single test
        if "a" in result and "b" in result:
            return self._generate_comparison_report(result)
        else:
            return self._generate_test_report(result)

    def _generate_test_report(self, result: Dict[str, Any]) -> str:
        """Generate a report for a single prompt test."""
        template = PromptTemplate.from_dict(result["prompt_template"])

        report = [
            "# Prompt Test Report",
            f"Generated: {time.ctime(result['timestamp'])}",
            f"Model: {result['model']}",
            "\n## Prompt Template (v{0})".format(template.version),
            "```",
            template.get_full_prompt(),
            "```",
            "\n## Performance Metrics",
        ]

        for metric, value in result["metrics"].items():
            report.append(f"- {metric.replace('_', ' ').title()}: {value:.2f}")

        report.append("\n## Sample Responses")

        for i, resp in enumerate(result["responses"][:3]):  # Show first 3 responses
            report.append(f"\n### Query {i+1}:")
            report.append(f"```\n{resp['query']}\n```")
            report.append("\nResponse:")
            report.append(
                f"```\n{resp.get('response', 'Error: ' + resp.get('error', 'Unknown error'))}\n```"
            )
            report.append(
                f"Tokens: {resp.get('tokens_used', 'N/A')}, Time: {resp.get('response_time', 'N/A'):.2f}s"
            )

        return "\n".join(report)

    def _generate_comparison_report(self, comparison: Dict[str, Any]) -> str:
        """Generate a report for an A/B test comparison."""
        report = [
            "# A/B Test Comparison Report",
            f"Generated: {time.ctime(comparison['timestamp'])}",
            f"\n## {comparison['a']['label']} vs {comparison['b']['label']}",
            "\n## Metrics Comparison",
        ]

        # Compare metrics
        metrics_table = [
            "| Metric | "
            + comparison["a"]["label"]
            + " | "
            + comparison["b"]["label"]
            + " | Difference |",
            "|--------|-------|-------|------------|",
        ]

        a_metrics = comparison["a"]["metrics"]
        b_metrics = comparison["b"]["metrics"]

        all_metrics = set(list(a_metrics.keys()) + list(b_metrics.keys()))

        for metric in all_metrics:
            a_value = a_metrics.get(metric, "N/A")
            b_value = b_metrics.get(metric, "N/A")

            if isinstance(a_value, (int, float)) and isinstance(b_value, (int, float)):
                diff = b_value - a_value
                diff_str = f"{diff:+.2f}"
            else:
                diff_str = "N/A"

            a_str = (
                f"{a_value:.2f}" if isinstance(a_value, (int, float)) else str(a_value)
            )
            b_str = (
                f"{b_value:.2f}" if isinstance(b_value, (int, float)) else str(b_value)
            )

            metrics_table.append(
                f"| {metric.replace('_', ' ').title()} | {a_str} | {b_str} | {diff_str} |"
            )

        report.extend(metrics_table)

        # Sample comparison
        report.append("\n## Sample Response Comparison")

        for i, comp in enumerate(
            comparison["per_query_comparison"][:2]
        ):  # Show first 2 comparisons
            report.append(f"\n### Query {i+1}:")
            report.append(f"```\n{comp['query']}\n```")

            report.append(f"\n**{comparison['a']['label']}**:")
            report.append(f"```\n{comp['a_response']}\n```")
            report.append(f"Tokens: {comp['a_tokens']}, Time: {comp['a_time']:.2f}s")

            report.append(f"\n**{comparison['b']['label']}**:")
            report.append(f"```\n{comp['b_response']}\n```")
            report.append(f"Tokens: {comp['b_tokens']}, Time: {comp['b_time']:.2f}s")

        # Recommendation
        report.append("\n## Recommendation")

        a_score = sum(
            a_metrics.get(m, 0)
            for m in a_metrics
            if isinstance(a_metrics.get(m), (int, float))
        )
        b_score = sum(
            b_metrics.get(m, 0)
            for m in b_metrics
            if isinstance(b_metrics.get(m), (int, float))
        )

        if a_score > b_score:
            report.append(
                f"Based on the metrics, **{comparison['a']['label']}** appears to perform better overall."
            )
        elif b_score > a_score:
            report.append(
                f"Based on the metrics, **{comparison['b']['label']}** appears to perform better overall."
            )
        else:
            report.append(
                "Both prompts perform similarly based on the metrics analyzed."
            )

        return "\n".join(report)

    def visualize_comparison(self, comparison_id: str):
        """Create visualizations for A/B test results."""
        if comparison_id not in self.test_results:
            raise ValueError(f"Comparison ID '{comparison_id}' not found")

        comparison = self.test_results[comparison_id]

        if "a" not in comparison or "b" not in comparison:
            raise ValueError("This result is not a comparison")

        a_metrics = comparison["a"]["metrics"]
        b_metrics = comparison["b"]["metrics"]

        # Get common metrics
        common_metrics = set(a_metrics.keys()).intersection(set(b_metrics.keys()))
        common_metrics = [
            m
            for m in common_metrics
            if isinstance(a_metrics[m], (int, float))
            and isinstance(b_metrics[m], (int, float))
        ]

        if not common_metrics:
            raise ValueError("No comparable metrics found")

        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))

        x = range(len(common_metrics))
        width = 0.35

        a_values = [a_metrics[m] for m in common_metrics]
        b_values = [b_metrics[m] for m in common_metrics]

        ax.bar(
            [i - width / 2 for i in x], a_values, width, label=comparison["a"]["label"]
        )
        ax.bar(
            [i + width / 2 for i in x], b_values, width, label=comparison["b"]["label"]
        )

        ax.set_ylabel("Value")
        ax.set_title("Metric Comparison")
        ax.set_xticks(x)
        ax.set_xticklabels([m.replace("_", " ").title() for m in common_metrics])
        ax.legend()

        plt.tight_layout()

        # Create per-query comparison if available
        if comparison.get("per_query_comparison"):
            # Extract tokens and time data
            queries = [
                f"Q{i+1}" for i in range(len(comparison["per_query_comparison"]))
            ]
            a_tokens = [comp["a_tokens"] for comp in comparison["per_query_comparison"]]
            b_tokens = [comp["b_tokens"] for comp in comparison["per_query_comparison"]]
            a_times = [comp["a_time"] for comp in comparison["per_query_comparison"]]
            b_times = [comp["b_time"] for comp in comparison["per_query_comparison"]]

            # Create tokens comparison
            fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

            x = range(len(queries))

            ax1.bar(
                [i - width / 2 for i in x],
                a_tokens,
                width,
                label=comparison["a"]["label"],
            )
            ax1.bar(
                [i + width / 2 for i in x],
                b_tokens,
                width,
                label=comparison["b"]["label"],
            )
            ax1.set_ylabel("Tokens")
            ax1.set_title("Tokens Used per Query")
            ax1.set_xticks(x)
            ax1.set_xticklabels(queries)
            ax1.legend()

            # Create time comparison
            ax2.bar(
                [i - width / 2 for i in x],
                a_times,
                width,
                label=comparison["a"]["label"],
            )
            ax2.bar(
                [i + width / 2 for i in x],
                b_times,
                width,
                label=comparison["b"]["label"],
            )
            ax2.set_ylabel("Time (s)")
            ax2.set_title("Response Time per Query")
            ax2.set_xticks(x)
            ax2.set_xticklabels(queries)
            ax2.legend()

            plt.tight_layout()

        return plt

    def get_improvement_suggestions(self, result_id: str) -> Dict[str, Any]:
        """Generate suggestions for improving a prompt based on test results."""
        if result_id not in self.test_results:
            raise ValueError(f"Result ID '{result_id}' not found")

        result = self.test_results[result_id]

        # If this is a comparison, suggest improvements based on the better performing prompt
        if "a" in result and "b" in result:
            a_score = sum(
                v
                for k, v in result["a"]["metrics"].items()
                if isinstance(v, (int, float))
            )
            b_score = sum(
                v
                for k, v in result["b"]["metrics"].items()
                if isinstance(v, (int, float))
            )

            better_label = (
                result["a"]["label"] if a_score >= b_score else result["b"]["label"]
            )
            worse_label = (
                result["b"]["label"] if a_score >= b_score else result["a"]["label"]
            )

            suggestions = {
                "summary": f"{better_label} outperformed {worse_label}.",
                "recommendations": [
                    "Consider adopting the structure and approach from the better-performing prompt.",
                    "Look at specific metrics to identify areas of improvement.",
                ],
            }
            return suggestions

        # For single prompt tests, suggest improvements based on metrics
        template = PromptTemplate.from_dict(result["prompt_template"])
        metrics = result["metrics"]

        suggestions = {
            "summary": "Based on the test results, here are some potential improvements:",
            "recommendations": [],
        }

        # Add specific recommendations based on metrics
        if metrics.get("format_adherence", 1.0) < 0.8:
            suggestions["recommendations"].append(
                "The responses aren't consistently following the requested format. "
                "Make the format instructions more explicit and consider adding an example."
            )

        if not template.examples or len(template.examples) == 0:
            suggestions["recommendations"].append(
                "Adding examples could improve response quality and consistency."
            )

        if not template.constraints:
            suggestions["recommendations"].append(
                "Consider adding constraints to better guide the response content and format."
            )

        if template.instruction and len(template.instruction.split()) < 10:
            suggestions["recommendations"].append(
                "The instruction is quite brief. Consider expanding it to be more specific about what you want."
            )

        # If no specific issues found, add general improvement suggestions
        if not suggestions["recommendations"]:
            suggestions["recommendations"] = [
                "Try adding more context to improve response relevance.",
                "Make instructions more specific to get more precise outputs.",
                "Consider testing a few-shot approach if currently using zero-shot.",
                "Experiment with different response formats to find the most effective structure.",
            ]

        return suggestions
