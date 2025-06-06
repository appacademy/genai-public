# Activity: Fine-tuning Gemma 3 4B and Converting to GGUF for Ollama



## Introduction

In this hands-on activity, you'll learn how to fine-tune Google's Gemma 3 4B Large Language Model and optimize it for local deployment. You'll start by using Unsloth on Google Colab to perform efficient LoRA (Low-Rank Adaptation) fine-tuning, which allows you to customize a powerful LLM with minimal computational resources. Then, you'll convert your fine-tuned model to a quantized format (GGUF) that dramatically reduces its size while preserving most capabilities. Finally, you'll deploy your optimized model locally using Ollama, enabling high-performance inference on consumer hardware. This workflow represents a practical, production-ready approach to customizing foundation models for specific applications.



## Learning Objectives

By completing this activity, you will be able to:

1. Apply efficient LoRA fine-tuning techniques to customize a large language model
2. Use Unsloth to accelerate training and reduce resource requirements
3. Convert a fine-tuned model from Hugging Face format to GGUF format
4. Apply quantization to reduce model size while maintaining performance
5. Deploy a custom fine-tuned model locally using Ollama



## Time Estimate

120 minutes



## Prerequisites

1. Google account (for Colab access)
2. Python 3.12
3. Git
4. VS Code or similar code editor
5. Ollama installed on your local machine
6. At least 10GB of free disk space
7. Basic understanding of LLMs and fine-tuning concepts



## Setup Instructions

### Step 1: Prepare for Colab

1. Ensure you have a Google account to access Google Colab
2. Have sufficient free space in your Google Drive (at least 10GB) for saving the fine-tuned model



### Step 2: Install Ollama

If you haven't already installed Ollama:

1. Visit [ollama.ai](https://ollama.ai) and download the installer for your operating system
2. Run the installer and follow the instructions
3. Verify Ollama is working by running `ollama run gemma:2b` in your terminal



## Activity Tasks

### Task 1: Fine-Tune Gemma 3 4B with Unsloth on Google Colab

In this task, you'll use Google Colab's free tier with Unsloth to efficiently fine-tune the Gemma 3 4B model on a sample dataset. This process is platform-independent and will be performed in the cloud regardless of your local operating system.

**Overview of the process:**
- Access and set up the Unsloth Gemma 3 notebook in Google Colab
- Configure the GPU runtime and mount Google Drive
- Install Unsloth and set up the Gemma 3 4B model with LoRA adapters
- Prepare the training data using the mlabonne/FineTome-100k dataset
- Fine-tune the model for approximately 30 steps (~6 minutes)
- Save and merge the fine-tuned model
- Download the model to your local machine

**Complete instructions:** Please follow the detailed step-by-step guide in **Guide 1: Fine-Tuning Gemma 3 4B with Unsloth on Google Colab**. This guide includes specific instructions, code snippets, and explanations for each step of the process.  [guide-1-fine-tuning-gemma.md](resources/guide-1-fine-tuning-gemma.md) 



### Task 2: Convert Fine-Tuned Gemma 3 to Q4 GGUF for Ollama

In this task, you'll convert your fine-tuned model to a quantized GGUF format for efficient local deployment with Ollama. The specific steps vary depending on your operating system.

**Overview of the process:**
- Create a project structure for the conversion process
- Set up the necessary tools and environment for conversion
- Convert the Hugging Face format model to float16 GGUF
- Quantize the float16 GGUF to Q4_K_M GGUF (reducing size by ~70%)
- Import the quantized model into Ollama
- Test the deployed model with sample queries

**Complete instructions:** Please follow the detailed guide specific to your operating system:

- **Windows users:** Follow **Guide 2a: Convert to Q4_K_M GGUF for Ollama on Windows**  [guide-2a-convert-to-q4_k_m-gguf-windows.md](resources/guide-2a-convert-to-q4_k_m-gguf-windows.md) 
- **Mac users:** Follow **Guide 2b: Convert to Q4_K_M GGUF for Ollama on Mac**  [guide-2b-convert-to-q4_k_m-gguf-mac.md](resources/guide-2b-convert-to-q4_k_m-gguf-mac.md) 
- **Linux users:** Follow **Guide 2c: Convert to Q4_K_M GGUF for Ollama on Linux**  [guide-2c-convert-to-q4_k_m-gguf-linux.md](resources/guide-2c-convert-to-q4_k_m-gguf-linux.md) 

Each guide contains platform-specific commands, troubleshooting advice, and detailed explanations tailored to your operating system.



## Conclusion

By completing this activity, you've mastered a complete workflow for customizing foundation models and deploying them efficiently on local hardware. The fine-tuning process with LoRA demonstrates how to adapt powerful LLMs with minimal computational resources, while the conversion and quantization techniques show how to optimize these models for practical deployment.

Your fine-tuned, quantized model is now approximately 70% smaller than the original while maintaining most of its capabilities. This approach enables you to create specialized AI assistants that can run efficiently on standard hardware without requiring constant cloud connectivity or expensive GPU resources—a critical skill for developing practical AI applications in resource-constrained environments.