import os
import time
from datetime import datetime
from typing import Dict, Any, List, Optional


class MarkdownWriter:
    def __init__(self, problem: str, output_dir: str = "outputs"):
        """
        Initialize the markdown writer with the problem statement

        Args:
            problem: The problem statement to solve
            output_dir: Directory to save the file
        """
        self.problem = problem
        self.start_time = time.time()
        self.sections = []
        self.timestamps = {}
        self.confidence_scores = {}
        self.output_dir = output_dir
        self.filepath = None

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"problem_solving_{timestamp}.md"
        self.filepath = os.path.join(output_dir, self.filename)

        # Initialize the file with header
        self._initialize_file()

    def _format_confidence(self, confidence: float) -> str:
        """Format confidence score with stars"""
        stars = int(confidence * 5)
        empty_stars = 5 - stars
        return f"{'★' * stars}{'☆' * empty_stars} ({confidence:.2f})"

    def _format_duration(self, seconds: float) -> str:
        """Format duration in a readable way"""
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.2f} minutes"
        else:
            hours = seconds / 3600
            return f"{hours:.2f} hours"

    def _initialize_file(self):
        """Initialize the markdown file with header and problem statement"""
        md_content = f"# Problem Solving Report\n\n"
        md_content += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"**Problem Statement:**\n\n{self.problem}\n\n"

        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"📝 Initialized markdown report: {self.filepath}")

    def add_section(self, title: str, content: str, confidence: float = None):
        """
        Add a new section to the markdown document and save immediately

        Args:
            title: The section title
            content: The section content
            confidence: Optional confidence score
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        section = {"title": title, "content": content, "timestamp": timestamp}
        self.sections.append(section)

        self.timestamps[title] = timestamp
        if confidence is not None:
            self.confidence_scores[title] = confidence

        # Save this section immediately
        self._append_section(section)

        print(f"📝 Added section '{title}' to markdown report")

    def _append_section(self, section: Dict[str, Any]):
        """Append a single section to the markdown file"""
        title = section["title"]
        content = section["content"]
        timestamp = section["timestamp"]

        md_content = f"## {title}\n\n"
        md_content += f"*Completed: {timestamp}*\n\n"
        md_content += f"{content}\n\n"

        # Append to file
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(md_content)

    def save(self) -> str:
        """
        Finalize the markdown document by adding summary information

        Returns:
            Path to the saved file
        """
        # Calculate total duration
        total_duration = time.time() - self.start_time

        # Build summary content
        md_content = f"## Workflow Summary\n\n"
        md_content += f"- **Total Duration:** {self._format_duration(total_duration)}\n"
        md_content += f"- **Sections:** {len(self.sections)}\n"

        # Append summary to file
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(md_content)

        print(f"📝 Finalized markdown report: {self.filepath}")
        return self.filepath
