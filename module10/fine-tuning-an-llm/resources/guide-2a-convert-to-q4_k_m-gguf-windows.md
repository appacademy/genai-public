# Guide: Converting Fine-Tuned Gemma 3 to Q4 GGUF for Ollama on Windows



## Introduction

Welcome to Guide 2a of our Module 10 learning activity in the "Generative AI for Software Developers" course. This Windows-specific guide follows your completion of fine-tuning Gemma 3 4B using Unsloth via Google Colab (Guide 1). Now, you'll learn how to convert that fine-tuned model into a quantized Q4_K_M GGUF format for efficient deployment on Ollama running on your Windows machine. This conversion process is critical for practical AI development, allowing you to dramatically reduce model size while preserving most capabilities. For students using Mac or Linux systems, please refer to Guide 2b or Guide 2c respectively, which follow the same core principles adapted for your operating system.



## Learning Outcomes

1. Understand the GGUF conversion process for LLMs.
2. Convert a Hugging Face format model to a float16 GGUF file.
3. Quantize a float16 GGUF file to Q4_K_M GGUF using llama.cpp tools.
4. Import and run a custom fine-tuned model in Ollama.



## Prerequisites:

1. Access to the fine-tuned `gemma-3-finetune` model folder (merged float16, Safetensors format) created via Google's Colab.
2. Git installed on your Windows machine.
3. Python 3.12 installed on your Windows machine.
4. VS Code installed on your Windows machine.
5. Ollama installed and running on your Windows machine.



## Set Up:

This section guides you through setting up your project environment in VS Code.

1. **Create Project Folder:**

   - Open VS Code.
   - Create a new folder for this project, for example, `Gemma_Conversion_Project`.
   - Open this folder in VS Code (`File` > `Open Folder...`).
   - Create a subfolder named `convert-to-q4_k_m-gguf`. This will be your main working directory.

2. **Place Fine-tuned Model:**
   
   - Locate the `gemma-3-finetune` folder you obtained after fine-tuning and merging in Colab (it should contain `.safetensors` files, `config.json`, etc.).
   - Copy or move the entire `gemma-3-finetune` folder into the `.\convert-to-q4_k_m-gguf` directory.
  
3. **Clone `llama.cpp` Repository:**
   
   - Open the integrated terminal in VS Code (`Terminal` > `New Terminal`).
   - Navigate into your working directory if not already there:

```bash
cd .\convert-to-q4_k_m-gguf 
```

   - Clone the `llama.cpp` repository using Git:

```bash
git clone https://github.com/ggerganov/llama.cpp 
```

   - This creates a `.\convert-to-q4_k_m-gguf\llama.cpp` folder.

4. **Set Up Python Environment:**
   
   - In the VS Code terminal (still inside `.\convert-to-q4_k_m-gguf`), create a Python virtual environment:

```bash
python -m venv .venv 
```

   - Activate the virtual environment:

```bash
.\.venv\Scripts\activate 
```

   - Install the required Python packages, ensuring you install the CPU version of PyTorch:

```bash
pip install transformers 
pip install torch --index-url https://download.pytorch.org/whl/cpu 
```

5. **Prepare Prebuilt `llama.cpp` Binaries:**
   
   - Download a prebuilt Windows binary release from the `llama.cpp` GitHub releases page. Based on the conversation, the `b5150` build for AVX2 (`llama-b5150-bin-win-avx2-x64.zip`) is a good choice as it contains the necessary files.
   - Extract the downloaded `.zip` archive to a temporary location.
   - Create the necessary subdirectories within your `llama.cpp` folder:

```
mkdir .\llama.cpp\build\Release 
```

   - From the extracted archive, find `llama-quantize.exe` and move it into the `.\llama.cpp\build\Release` directory, renaming it to `quantize.exe`.
   - From the extracted archive, find `llama.dll` and copy it into the same `.\llama.cpp\build\Release` directory.
   - Copy any other DLLs that `quantize.exe` might need (like `ggml.dll`, `ggml-base.dll`, `ggml-cpu.dll` found in the archive) into the `.\llama.cpp\build\Release` directory as well. This prevents "missing DLL" errors.



## Conversion Steps:

### Step 1: Convert Hugging Face Model to Float16 GGUF

1. Ensure you are in the VS Code terminal, inside the `.\convert-to-q4_k_m-gguf\llama.cpp` directory, and your virtual environment (`.venv`) is activated.
2. Navigate to the `llama.cpp` directory if needed:
   
```bash
cd .\convert-to-q4_k_m-gguf\llama.cpp 
```

3. Run the conversion script (using the script name identified from the repository listing):
   
```bash
python convert_hf_to_gguf.py --outtype f16 --outfile gemma-3-finetune-f16.gguf ..\gemma-3-finetune 
```

   - _Note:_ We use `..\gemma-3-finetune` to point to the model folder one level up from the current `llama.cpp` directory.
   - This creates `gemma-3-finetune-f16.gguf` (~7.8 GB) inside the `.\convert-to-q4_k_m-gguf\llama.cpp` directory.

4. (Recommended) Move the generated GGUF file to your main working directory (`.\convert-to-q4_k_m-gguf`) for easier access:
   
```bash
move gemma-3-finetune-f16.gguf ..\ 
```



### Step 2: Quantize Float16 GGUF to Q4_K_M GGUF

1. Navigate back to your main working directory:
   
```bash
cd .. 
```

- (Your path should now be `...\convert-to-q4_k_m-gguf`)


2. Run the `quantize.exe` binary using the relative path to the executable and the GGUF file:

```bash
.\llama.cpp\build\Release\quantize gemma-3-finetune-f16.gguf gemma-3-finetune-Q4_K_M.gguf Q4_K_M 
```

   - This reads `gemma-3-finetune-f16.gguf` from the current directory.
   - It creates `gemma-3-finetune-Q4_K_M.gguf` (~2.5-3.5 GB) in the current directory.
   - Use `Q4_K_M` as the quantization type.  

3. Verify the Q4_K_M file has been created:

```bash
dir gemma-3-finetune-Q4_K_M.gguf 
```



### Step 3: Import into Ollama

1. Create a file named `Modelfile` (no extension) in your working directory (`.\convert-to-q4_k_m-gguf`) with the following content:

```plaintext
FROM ./gemma-3-finetune-Q4_K_M.gguf 
```

2. Run the Ollama create command using a name that follows Ollama's conventions:
   
```bash
ollama create gemma3finetuned:q4km -f Modelfile 
```

   - If `ollama` isn't recognized, ensure Ollama is installed correctly and its directory is in your system PATH, or use the full path to `ollama.exe`.

3. Test the newly imported model:
   
```bash
ollama run gemma3finetuned:q4km 
```

   - Enter a prompt (e.g., "What is the modulus operator?") to verify it works and reflects the fine-tuning.



## Troubleshooting Tips for Windows

**Quantization Fails**:

- Ensure all DLLs are in `llama.cpp\build\Release`.
- Run the VS Code terminal as administrator: Close VS Code, right-click the VS Code icon, select “Run as administrator,” and reopen the project.

**Ollama Command Not Recognized**:

- Ensure Ollama is installed and added to your system PATH (April 2, 2025, 13:24). If not, reinstall Ollama or specify the full path to the `ollama` executable (e.g., `C:\path\to\ollama.exe create ...`).

**Python Package Issues**:

- If a package fails to install, ensure you’re in the virtual environment (`venv\Scripts\activate`) and try reinstalling: `pip install torch transformers peft gguf protobuf numpy typing-extensions jinja2 safetensors`.



## Conclusion

Congratulations! You've successfully added model quantization to your AI developer toolkit, enabling you to deploy custom fine-tuned models in resource-constrained environments. By converting your Gemma 3 model to Q4_K_M GGUF format, you've reduced its size by approximately 60-70% while maintaining most of its capabilities—a critical optimization for real-world AI applications. This skill complements your existing knowledge of vector databases, LangChain, and LangGraph, bringing you closer to building complete, efficient AI systems that can run locally on standard hardware.
