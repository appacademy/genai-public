# Guide: Converting Fine-Tuned Gemma 3 to Q4 GGUF for Ollama on Linux



## Introduction

Welcome to Guide 2c of our Module 10 learning activity in the "Generative AI for Software Developers" course. This Linux-specific guide follows your completion of fine-tuning Gemma 3 4B using Unsloth via Google Colab (Guide 1). Now, you'll learn how to convert that fine-tuned model into a quantized Q4_K_M GGUF format for efficient deployment on Ollama running on your Linux machine. This conversion process is critical for practical AI development, allowing you to dramatically reduce model size while preserving most capabilities. For students using Windows or macOS systems, please refer to Guide 2a or Guide 2b respectively.



## Learning Outcomes

1. Understand the GGUF conversion process for LLMs.
2. Convert a Hugging Face format model to a float16 GGUF file using `llama.cpp`.
3. Quantize a float16 GGUF file to Q4_K_M GGUF using `llama.cpp` tools.
4. Import and run a custom fine-tuned model in Ollama on Linux.



## Prerequisites:

1. Access to the fine-tuned `gemma-3-finetune` model folder (merged float16, Safetensors format) created via Google Colab.
2. **Essential Build Tools:** Installed on your Linux distribution. This provides `git`, `make`, `gcc`/`g++` (C/C++ compilers), and Python tools.
    - _Debian/Ubuntu:_ Run `sudo apt update && sudo apt install build-essential git python3 python3-venv python3-pip` in your terminal.
    - _Fedora:_ Run `sudo dnf update && sudo dnf groupinstall "Development Tools" && sudo dnf install git python3 python3-pip python3-venv`.
    - _Arch Linux:_ Run `sudo pacman -Syu base-devel git python python-pip python-venv`.
    - _Other Distributions:_ Check your distribution's documentation for installing equivalent development packages.
3. **Python 3.12:** Installed on your system (usually included or installable via your package manager). Ensure it's a recent version (3.10+).
    - _Check version:_ Run `python3 --version` in Terminal.
4. **VS Code:** Installed on your Linux machine (optional, but recommended for consistency with the course).
5. **Ollama:** Installed and running on your Linux machine.



## Set Up:

This section guides you through setting up your project environment in VS Code (or your preferred terminal) on Linux.

1. **Create Project Folder:**

   - Open your Terminal or the integrated terminal in VS Code.
   - Create a new folder for this project (e.g., `~/Gemma_Conversion_Project`). Use the `mkdir` command.

```bash
mkdir ~/Gemma_Conversion_Project
cd ~/Gemma_Conversion_Project 
```

   - Create a subfolder named `convert-to-q4_k_m-gguf`. This will be your main working directory.

```bash
mkdir convert-to-q4_k_m-gguf
cd convert-to-q4_k_m-gguf 
```

   - If using VS Code, open this folder (`File` > `Open Folder...`).

2. **Place Fine-tuned Model:**

   - Locate the `gemma-3-finetune` folder you downloaded from Colab (it contains `.safetensors` files, `config.json`, etc.).
   - Copy or move (`cp -r` or `mv`) the entire `gemma-3-finetune` folder into the `./convert-to-q4_k_m-gguf` directory.

2. **Clone `llama.cpp` Repository:**

   - Ensure you are in the `./convert-to-q4_k_m-gguf` directory in your terminal.
   - Clone the `llama.cpp` repository using Git:

```bash
git clone https://github.com/ggerganov/llama.cpp 
```

   - This creates a `./convert-to-q4_k_m-gguf/llama.cpp` folder.

4. **Set Up Python Environment:**

   - In the terminal (still inside `./convert-to-q4_k_m-gguf`), create a Python virtual environment:

```bash
python3 -m venv .venv 
```

   - Activate the virtual environment:

```bash
source .venv/bin/activate 
```
	_(You should see `(.venv)` appear at the start of your terminal prompt)._

   - Install the required Python packages using the `requirements.txt` file provided by `llama.cpp`:

```bash
pip install -r llama.cpp/requirements.txt 
```
	_(This installs `torch`, `transformers`, `numpy`, `protobuf`, `sentencepiece`, `gguf`, etc.)_

5. **Build `llama.cpp`:**

   - Building on Linux using `make` is typically straightforward.
   - Navigate into the `llama.cpp` directory:

```bash
cd llama.cpp 
```

   - Compile `llama.cpp` using `make`. This command compiles the necessary tools, including `quantize` and dependencies for the Python scripts.

```bash
make 
```
	_(This process might take a few minutes. You should see compilation messages scroll by.)_

- Verify the build by checking for the `quantize` executable:

Bash

```
ls -l quantize 
```

_(You should see the `quantize` file listed with execute permissions)._

- Navigate back to your main working directory:


```bash
cd .. 
```



## Conversion Steps:

### Step 1: Convert Hugging Face Model to Float16 GGUF

1. Ensure you are in the terminal, inside your main working directory (`./convert-to-q4_k_m-gguf`), and your virtual environment (`.venv`) is activated.
   
2. Run the conversion script provided by `llama.cpp`:

```bash
python llama.cpp/convert_hf_to_gguf.py ./gemma-3-finetune --outfile gemma-3-finetune-f16.gguf --outtype f16 
```

   - `./gemma-3-finetune`: Path to your input model folder.
   - `--outfile gemma-3-finetune-f16.gguf`: Specifies the output file name.
   - `--outtype f16`: Specifies the output precision (float16).
   - This creates `gemma-3-finetune-f16.gguf` (~7.8 GB) in the current directory (`./convert-to-q4_k_m-gguf`).

3. Verify the float16 GGUF file has been created:

```bash
ls -lh gemma-3-finetune-f16.gguf 
```



### Step 2: Quantize Float16 GGUF to Q4_K_M GGUF

1. Ensure you are still in your main working directory (`./convert-to-q4_k_m-gguf`) with the virtual environment active.
   
2. Run the `quantize` binary you built earlier, providing the input (f16 GGUF) and output (Q4_K_M GGUF) filenames, and the quantization type:

```bash
./llama.cpp/quantize gemma-3-finetune-f16.gguf gemma-3-finetune-Q4_K_M.gguf Q4_K_M 
```

   - `./llama.cpp/quantize`: Path to the compiled quantization tool.
   - `gemma-3-finetune-f16.gguf`: Your input file (float16 GGUF).
   - `gemma-3-finetune-Q4_K_M.gguf`: Your desired output file name.
   - `Q4_K_M`: The target quantization type.
   - This creates `gemma-3-finetune-Q4_K_M.gguf` (~2.5-3.5 GB) in the current directory.

3. Verify the Q4_K_M GGUF file has been created:

```bash
ls -lh gemma-3-finetune-Q4_K_M.gguf 
```



### Step 3: Import into Ollama

1. Create a file named `Modelfile` (no extension) in your working directory (`./convert-to-q4_k_m-gguf`) with the following content:

```plaintext
FROM ./gemma-3-finetune-Q4_K_M.gguf 
```

2. Run the Ollama create command using a name that follows Ollama's conventions:

```bash
ollama create gemma3finetuned:q4km -f Modelfile 
```

   - If `ollama` isn't recognized, ensure Ollama is installed correctly and its binary is in your system PATH (usually handled by the installer). You might need to restart your terminal.

3. Test the newly imported model:

```bash
ollama run gemma3finetuned:q4km 
```

   - Enter a prompt (e.g., "What is the modulus operator?") to verify it works and reflects the fine-tuning.



## Troubleshooting Tips for Linux

- **`make` fails:** Ensure build tools are installed (e.g., `sudo apt install build-essential`). Check for specific errors during the `make` process—you might need other libraries depending on your distribution or optional `llama.cpp` features you enabled (though the basic `make` should be fine).

- **`command not found: python3` or `pip`:** Ensure Python 3 and pip are installed (`sudo apt install python3 python3-pip`) and in your PATH. Make sure your virtual environment is active (`source .venv/bin/activate`).

- **Permission Denied:** If you encounter permission errors running scripts or `quantize`, use `chmod +x` to grant execute permissions (e.g., `chmod +x ./llama.cpp/quantize`). Use `sudo` only for package installations, not for regular file operations unless absolutely necessary.

- **Quantization Fails:** Double-check the input/output filenames and the quantization type (`Q4_K_M`). Ensure the `gemma-3-finetune-f16.gguf` file isn't corrupted. Check available disk space with `df -h .`.

- **Ollama Command Not Recognized:** Ensure Ollama is running (check `systemctl status ollama` if installed as a service). Restart the Terminal. Verify the Ollama binary location is in your `$PATH` (check with `echo $PATH` and `which ollama`). Add it to your shell profile (`.bashrc`, `.zshrc`, etc.) if needed.



## Conclusion

Congratulations! You've successfully added model quantization to your AI developer toolkit, enabling you to deploy custom fine-tuned models in resource-constrained environments. By converting your Gemma 3 model to Q4_K_M GGUF format on your Linux machine, you've reduced its size significantly while maintaining most of its capabilities—a critical optimization for real-world AI applications. This skill complements your existing knowledge, bringing you closer to building complete, efficient AI systems that can run locally.
