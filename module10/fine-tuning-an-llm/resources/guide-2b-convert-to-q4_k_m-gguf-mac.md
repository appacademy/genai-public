# Guide: Converting Fine-Tuned Gemma 3 to Q4 GGUF for Ollama on macOS



## Introduction

Welcome to Guide 2b of our Module 10 learning activity in the "Generative AI for Software Developers" course. This macOS-specific guide follows your completion of fine-tuning Gemma 3 4B using Unsloth via Google Colab (Guide 1). Now, you'll learn how to convert that fine-tuned model into a quantized Q4_K_M GGUF format for efficient deployment on Ollama running on your Mac. This conversion process is critical for practical AI development, allowing you to dramatically reduce model size while preserving most capabilities. For students using Windows or Linux systems, please refer to Guide 2a or Guide 2c respectively.



## Learning Outcomes

1. Understand the GGUF conversion process for LLMs.
2. Convert a Hugging Face format model to a float16 GGUF file using `llama.cpp`.
3. Quantize a float16 GGUF file to Q4_K_M GGUF using `llama.cpp` tools.
4. Import and run a custom fine-tuned model in Ollama on macOS.



## Prerequisites:

1. Access to the fine-tuned `gemma-3-finetune` model folder (merged float16, Safetensors format) created via Google Colab.
2. **Xcode Command Line Tools:** Installed on your Mac. This provides essential build tools like `git`, `make`, and `clang`.
   - _Check installation:_ Open Terminal (`Applications` > `Utilities` > `Terminal`) and run `xcode-select -p`. If it shows a path, you likely have them.
   - _Install if needed:_ Run `xcode-select --install` in Terminal and follow the prompts.
3. **Python 3.12:** Installed on your Mac. (macOS usually comes with Python 3, but ensure it's a recent version like 3.10+).
   - _Check version:_ Run `python3 --version` in Terminal.
   - _Install if needed:_ Download from python.org or use a package manager like Homebrew (`brew install python`).
4. **VS Code:** Installed on your Mac.
5. **Ollama:** Installed and running on your Mac.



## Set Up:

This section guides you through setting up your project environment in VS Code on your Mac.

1. **Create Project Folder:**
   
   - Open VS Code.
   - Create a new folder for this project (e.g., `~/Documents/Gemma_Conversion_Project`). Use Finder or the `mkdir` command in the Terminal.
   - Open this folder in VS Code (`File` > `Open Folder...`).
   - Create a subfolder named `convert-to-q4_k_m-gguf`. This will be your main working directory.

2. **Place Fine-tuned Model:**
   
   - Locate the `gemma-3-finetune` folder you downloaded from Colab (it contains `.safetensors` files, `config.json`, etc.).
   - Copy or move the entire `gemma-3-finetune` folder into the `./convert-to-q4_k_m-gguf` directory within your project folder.

3. **Clone `llama.cpp` Repository:**
   
   - Open the integrated terminal in VS Code (`Terminal` > `New Terminal`).
   - Navigate into your working directory:

```bash
cd convert-to-q4_k_m-gguf 
```

   - Clone the `llama.cpp` repository using Git:


```bash
git clone https://github.com/ggerganov/llama.cpp 
```

   - This creates a `./convert-to-q4_k_m-gguf/llama.cpp` folder.

4. **Set Up Python Environment:**

   - In the VS Code terminal (still inside `./convert-to-q4_k_m-gguf`), create a Python virtual environment:


```bash
python3 -m venv .venv 
```
   - Activate the virtual environment:

```bash
source .venv/bin/activate 
```
	_(You should see `(.venv)` appear at the start of your terminal prompt)._

- Install the required Python packages:


```bash
pip install -r llama.cpp/requirements.txt 
```
	_(This installs `torch`, `transformers`, `numpy`, `protobuf`, `sentencepiece`, `gguf`, etc., specified by `llama.cpp`)_

5. **Build `llama.cpp`:**

   - Unlike the Windows guide which used prebuilt binaries due to build complexity, building on macOS is usually straightforward with `make`.
   - Navigate into the `llama.cpp` directory:


```bash
cd llama.cpp 
```

   - Compile `llama.cpp` using `make`. This command compiles the necessary tools, including `quantize` and `convert_hf_to_gguf.py`'s dependencies.


```bash
make 
```

	_(This process might take a few minutes. You should see compilation messages scroll by.)_

   - _(Optional: For Apple Silicon Macs (M1/M2/M3), you can enable Metal GPU support for potentially faster _inference_ (though quantization is CPU-bound) by running `make LLAMA_METAL=1` instead. For this guide, the standard `make` is sufficient.)_

   - Verify the build by checking for the `quantize` executable:

```bash
ls -l quantize 
```

	   _(You should see the `quantize` file listed with execute permissions)._

   - Navigate back to your main working directory:


```bash
cd .. 
```



## Conversion Steps:

### Step 1: Convert Hugging Face Model to Float16 GGUF

1. Ensure you are in the VS Code terminal, inside your main working directory (`./convert-to-q4_k_m-gguf`), and your virtual environment (`.venv`) is activated.

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

   - If `ollama` isn't recognized, ensure Ollama is installed correctly and its directory is in your system PATH (usually handled automatically on Mac). You might need to restart your terminal or VS Code.

3. Test the newly imported model:

   
```bash
ollama run gemma3finetuned:q4km 
```
   - Enter a prompt (e.g., "What is the modulus operator?") to verify it works and reflects the fine-tuning.



## Troubleshooting Tips for macOS

- **`make` fails:** Ensure Xcode Command Line Tools are installed (`xcode-select --install`). Check for specific errors during the `make` process—you might need additional libraries (though usually not required for basic CPU builds).

- **`command not found: python3` or `pip`:** Ensure Python 3 is installed and in your PATH. Use `python3` and `pip3` if needed. Make sure your virtual environment is active (`source .venv/bin/activate`).

- **Permission Denied:** If you encounter permission errors running scripts or `quantize`, use `chmod +x` to grant execute permissions (e.g., `chmod +x ./llama.cpp/quantize`). You generally shouldn't need `sudo`.

- **Quantization Fails:** Double-check the input/output filenames and the quantization type (`Q4_K_M`). Ensure the `gemma-3-finetune-f16.gguf` file isn't corrupted.

- **Ollama Command Not Recognized:** Ensure Ollama is running. Restart the Terminal or VS Code. If installed via download, the path might need to be added manually (check Ollama documentation). If installed via Homebrew, ensure `brew` paths are correctly configured in your shell profile (`.zshrc` or `.bash_profile`).



## Conclusion

Congratulations! You've successfully added model quantization to your AI developer toolkit, enabling you to deploy custom fine-tuned models in resource-constrained environments. By converting your Gemma 3 model to Q4_K_M GGUF format on your Mac, you've reduced its size significantly while maintaining most of its capabilities—a critical optimization for real-world AI applications. This skill complements your existing knowledge, bringing you closer to building complete, efficient AI systems that can run locally.
