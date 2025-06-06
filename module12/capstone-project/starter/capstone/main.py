from langchain_ollama import OllamaLLM
from src.rag.document_loader import load_documents, create_vector_store
from src.intent.router import IntentRouter
from src.rag.policy_qa import PolicyRAG
from src.rag.benefits_qa import BenefitsRAG
from src.training.csv_tools import TrainingRecords
from src.orchestration.graph import create_workflow
from src.console.interface import ConsoleInterface
import os
import typer
import shutil
import hashlib

app = typer.Typer()


@app.command()
def setup():
    """Initial setup - load documents and create vector store"""
    print("Setting up Jenna...")

    # Ensure directories exist
    os.makedirs("data/policies", exist_ok=True)
    os.makedirs("data/benefits", exist_ok=True)
    os.makedirs("data/training", exist_ok=True)
    os.makedirs("data/training/snapshots", exist_ok=True)
    os.makedirs("data/training/conversation_history", exist_ok=True)

    # Load and process documents
    print("Processing documents...")
    chunks = load_documents()
    print(f"Loaded {len(chunks)} document chunks")

    # Create vector store
    print("Building vector store...")
    create_vector_store(chunks)
    print("Vector store created successfully")

    print("Setup complete! Run 'python main.py start' to launch Jenna.")


@app.command()
def start():
    """Start the Jenna HR assistant"""
    print("Starting Jenna...")

    # Initialize LLM
    print("Connecting to Ollama...")
    llm = OllamaLLM(model="gemma3finetuned:q4km")

    # Initialize components
    print("Initializing components...")
    intent_router = IntentRouter(llm)
    policy_rag = PolicyRAG(llm)
    benefits_rag = BenefitsRAG(llm)
    training_records = TrainingRecords()

    # Create workflow
    print("Building workflow...")
    workflow = create_workflow(
        intent_router, policy_rag, benefits_rag, training_records, llm
    )

    # Start console interface
    print("Launching console interface...")
    console = ConsoleInterface(workflow)
    console.run_repl()


@app.command()
def organize_documents():
    """Organize documents into policies and benefits folders"""
    print("Organizing documents...")

    # Ensure directories exist
    os.makedirs("data/policies", exist_ok=True)
    os.makedirs("data/benefits", exist_ok=True)

    # Define benefit-related keywords (expanded list for better classification)
    benefit_keywords = [
        "benefit",
        "insurance",
        "health",
        "dental",
        "vision",
        "medical",
        "401k",
        "retirement",
        "compensation",
        "bonus",
        "perks",
        "wellness",
        "assistance program",
        "gym",
        "maternity",
        "paternity",
        "parental leave",
        "disability",
        "life insurance",
    ]

    # Check if doc_library exists
    if not os.path.exists("doc_library"):
        print("doc_library not found. Skipping document organization.")
        return

    # Process each file in doc_library
    moved_count = 0
    benefit_count = 0
    policy_count = 0

    for filename in os.listdir("doc_library"):
        if filename.endswith(".txt"):
            file_path = os.path.join("doc_library", filename)

            # Read file content to determine if it's a benefit document
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read().lower()
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

            # Check if any benefit keywords are in the content
            is_benefit = any(keyword in content for keyword in benefit_keywords)

            # Also check filename for benefit keywords for better classification
            is_benefit_by_name = any(
                keyword in filename.lower() for keyword in benefit_keywords
            )

            # Classify as benefit if either content or filename suggests it's a benefit
            is_benefit = is_benefit or is_benefit_by_name

            # Copy to appropriate directory
            if is_benefit:
                destination = os.path.join("data/benefits", filename)
                shutil.copy2(file_path, destination)
                print(f"Copied {filename} to benefits directory")
                benefit_count += 1
            else:
                destination = os.path.join("data/policies", filename)
                shutil.copy2(file_path, destination)
                print(f"Copied {filename} to policies directory")
                policy_count += 1

            moved_count += 1

    print(f"Document organization complete! Organized {moved_count} documents.")
    print(f"- {benefit_count} documents classified as benefits")
    print(f"- {policy_count} documents classified as policies")


@app.command()
def cleanup_documents():
    """Remove document duplication and ensure proper organization"""
    print("Cleaning up document structure...")

    # Step 1: Ensure proper organization of documents
    organize_documents()

    # Step 2: Check for and remove duplicates between data/policies and data/benefits
    file_hashes = {}

    # Helper function to compute file hash
    def get_file_hash(filepath):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    # Identify duplicates across directories
    print("\nChecking for duplicates between policies and benefits...")

    policies_dir = "data/policies"
    benefits_dir = "data/benefits"

    # Track duplicate files to remove
    duplicates_to_remove = []

    # Check for duplicates between policies and benefits directories
    if os.path.exists(policies_dir) and os.path.exists(benefits_dir):
        policy_files = os.listdir(policies_dir)
        benefit_files = os.listdir(benefits_dir)

        # Check for filename duplicates first
        common_files = set(policy_files) & set(benefit_files)
        if common_files:
            print(
                f"Found {len(common_files)} files with the same name in both directories."
            )
            for filename in common_files:
                policy_path = os.path.join(policies_dir, filename)
                benefit_path = os.path.join(benefits_dir, filename)

                # Compare content to see if they're actually the same
                policy_hash = get_file_hash(policy_path)
                benefit_hash = get_file_hash(benefit_path)

                if policy_hash == benefit_hash:
                    print(f"  {filename} is identical in both directories")
                    # Determine which one to keep based on benefit keywords
                    with open(
                        policy_path, "r", encoding="utf-8", errors="replace"
                    ) as f:
                        content = f.read().lower()

                    # Define benefit-related keywords for decision-making
                    benefit_keywords = [
                        "benefit",
                        "insurance",
                        "health",
                        "retirement",
                        "compensation",
                    ]
                    is_benefit = any(
                        keyword in content for keyword in benefit_keywords
                    ) or any(
                        keyword in filename.lower() for keyword in benefit_keywords
                    )

                    # Keep the file in the appropriate directory, remove from the other
                    if is_benefit:
                        duplicates_to_remove.append(policy_path)
                    else:
                        duplicates_to_remove.append(benefit_path)

    # Step 3: Check for duplicates between doc_library and data directories
    if os.path.exists("doc_library"):
        print("\nChecking for duplicates between doc_library and data directories...")
        doc_library_files = [
            os.path.join("doc_library", f)
            for f in os.listdir("doc_library")
            if f.endswith(".txt")
        ]
        data_files = []

        if os.path.exists(policies_dir):
            data_files.extend(
                [
                    os.path.join(policies_dir, f)
                    for f in os.listdir(policies_dir)
                    if f.endswith(".txt")
                ]
            )

        if os.path.exists(benefits_dir):
            data_files.extend(
                [
                    os.path.join(benefits_dir, f)
                    for f in os.listdir(benefits_dir)
                    if f.endswith(".txt")
                ]
            )

        # Compute hashes for all doc_library files
        doc_library_hashes = {get_file_hash(f): f for f in doc_library_files}

        # Check data files against doc_library hashes
        for data_file in data_files:
            data_hash = get_file_hash(data_file)
            if data_hash in doc_library_hashes:
                print(
                    f"  {os.path.basename(data_file)} is duplicated in doc_library and data directories"
                )

        # Since all doc_library files should now be in data directories, suggest removing doc_library
        print(
            "\nAll documents from doc_library have been properly organized in data directories."
        )
        print(
            "The doc_library folder is now redundant and can be removed with the cleanup_doc_library command."
        )

    # Step 4: Remove identified duplicates
    if duplicates_to_remove:
        print(f"\nRemoving {len(duplicates_to_remove)} duplicate files...")
        for file_path in duplicates_to_remove:
            try:
                os.remove(file_path)
                print(f"  Removed duplicate: {file_path}")
            except Exception as e:
                print(f"  Error removing {file_path}: {e}")

    print("\nDocument cleanup complete!")
    print(
        "Run 'python main.py setup' to rebuild the vector store with the organized documents."
    )


@app.command()
def cleanup_doc_library():
    """Remove the doc_library folder after confirming all documents are properly organized"""
    if not os.path.exists("doc_library"):
        print("doc_library folder not found. No action needed.")
        return

    print("WARNING: This will permanently remove the doc_library folder.")
    print("Make sure you have run organize_documents and cleanup_documents first.")
    confirmation = input("Type 'YES' to confirm deletion: ")

    if confirmation == "YES":
        try:
            shutil.rmtree("doc_library")
            print("doc_library folder has been removed successfully.")
        except Exception as e:
            print(f"Error removing doc_library folder: {e}")
    else:
        print("Operation cancelled. No changes were made.")


if __name__ == "__main__":
    app()
