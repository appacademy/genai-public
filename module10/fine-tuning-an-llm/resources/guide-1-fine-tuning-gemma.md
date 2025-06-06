# Guide 1: Fine-Tuning Gemma 3 4B with Unsloth on Google Colab



## Introduction

This guide walks you through fine-tuning the Gemma 3 4B model using Unsloth’s pre-configured `Gemma3_(4B).ipynb` notebook on Google Colab’s free tier, available via Unsloth’s GitHub repository. The notebook uses the `mlabonne/FineTome-100k` dataset (100,000 rows) and trains for 30 steps, processing approximately 240 rows of data in about 6 minutes. After fine-tuning, you’ll download the model and proceed to the appropriate OS-specific guide (Windows, Mac, or Linux) for conversion to **Q4_K_M GGUF** format and deployment on Ollama. This process runs in the cloud and is the same for all students, regardless of their computer’s operating system.



## Learning Outcomes

Upon completing this guide, you will be able to: 

1. Set up and run a pre-configured Google Colab notebook for LLM fine-tuning. 
2. Understand the basic workflow of fine-tuning using Unsloth, including loading a model, applying LoRA adapters, preparing data, and initiating training.
3. Execute Python code cells in Colab to install dependencies and run a fine-tuning process.
4. Save the fine-tuned LoRA adapters and merge them with the base model to produce a full float16 model.
5. Prepare and download the merged model files for subsequent local conversion and deployment.



## Prerequisites

- **Google Account**: For accessing Colab and Google Drive.
- **Time**: Approximately 20 to30 minutes.



**Important Note on Notebook Scope:**

The Unsloth Colab notebook (`Gemma3_(4B).ipynb`) you will use contains a complete workflow, including sections for inference testing and direct saving to GGUF formats (like Q8_0 or F16).

**For this learning activity (Guide 1), we will only execute a limited portion of the notebook:**

* **We WILL perform the following:** Installation, Model Loading & LoRA Setup, Data Prep, Training (for 30 steps), Saving LoRA adapters, and Merging/Saving the full model in float16 format to Google Drive.
* **We WILL SKIP:** The "Inference" section and the direct "GGUF / llama.cpp Conversion" sections within the Colab notebook.

Our primary goal at this stage is to fine-tune the model and prepare the merged float16 version (`gemma-3-finetune` folder) for download. The conversion to the final Q4_K_M GGUF format for Ollama will be handled locally on your machine in the OS-specific **Guide 2 (a, b, or c)**.



## Step 1: Access and Set Up the Colab Notebook

**Access the Notebook**:
- Visit Unsloth’s GitHub repository: [github.com/unslothai/unsloth](https://github.com/unslothai/unsloth).
- In the table under “Finetune for Free,” click the “Start for free” link next to “Gemma 3 (4B)” to open the `Gemma3_(4B).ipynb` notebook in Colab.
![](/_assets/activity-01-unsloth-github.png)



**Enable GPU Runtime**:

   - Click "Runtime" > "Change runtime type" > Select "GPU" (T4).
   - This ensures faster training on Colab’s free Tesla T4 GPU.
     



**Mount Google Drive**:

- Add a new code cell at the top of the notebook and run:
```python
from google.colab import drive
drive.mount('/content/drive')
```

- Follow the prompt to authenticate and mount Drive. This ensures the fine-tuned model can be saved to a persistent location.



## Step 2: Run the Notebook Up to Fine-Tuning Completion

### Run the “Installation” Section:

**Execute the cells under “Installation” and “Colab Extra Install” to install Unsloth and dependencies**:![](/_assets/activity-02-installation.png)



### Run the “Unsloth” Section:

**Execute the cells to load the Gemma 3 4B model and apply LoRA adapters**:
![](/_assets/activity-04-unsloth.png)



**Add LoRA Adaptors**:
![](/_assets/activity-05-lora-adaptors.png)



### Run the “Data Prep” Section:

Execute all cells under “Data Prep” to load and prepare the `mlabonne/FineTome-100k` dataset.

**Execute `get_chat_template` function**:
![](/_assets/activity-06-chat-templates.png)



**Load the dataset**:
![](/_assets/activity-07-load-dataset.png)

**Convert datasets to the correct format**:
![](/_assets/activity-08-convert-dataset.png)



**Apply `Gemma-3` chat template**:
![](/_assets/activity-09-apply-chat-template.png)



### Run the “Train the model” Section:

**Execute all cells under “Train the model” to fine-tune the model for 30 steps**:
![](/_assets/activity-10-train-the-model.png)



**Apply Unsloth's `train_on_completions` method**:
![](/_assets/activity-11-train-on-completions-method.png)



**Verify masking the instruction is complete**:
![](/_assets/activity-12-verify-masking.png)



**Print the masked out example**:
![](/_assets/activity-13-print-the-masked-example.png)



**Show current memory stats**:
![](/_assets/activity-14-show-memory-stats.png)



**Train the model**:
![](/_assets/activity-15-train-the-model.png)

   - Note: The 30-step process takes approximately 6 minutes (359 seconds) and processes around 240 rows of data (30 steps × 8 rows per step).
     



**Add Resource Monitoring and Disk Cleanup**:

- After the `trainer_stats = trainer.train()` cell, add and run the following to monitor disk space and clean up temporary files:
![](/_assets/activity-16-resource-monitoring-disk-cleanup.png)



**Run the memory stats cell**:
![](/_assets/activity-17-show-memory-stats.png)



Congratulations! The model has been fine-tuned.



## Step 3: Save and Merge the Fine-Tuned Model

Skip the **Inference** section and proceed to the “Saving, loading finetuned models” Section.

**Save the final model as LoRA adapters**:
![](/_assets/activity-18-save-as-lora-adapters.png)



**Merge LoRA with Base Model**:

- In the “Saving to float16 for VLLM” section, change `if False` to `if True` and update the path to save to Google Drive:
![](/_assets/activity-19-merge-lora-with-base-model.png)
- Result: Creates `gemma-3-finetune` folder (~8-10 GB) in Google Drive.



## Step 4: Download the Model:

Add a new cell, zip the folder, and save the zip file to your Google Drive with the following commands.
```bash
!zip -r /content/drive/MyDrive/gemma-3-finetune.zip /content/drive/MyDrive/gemma-3-finetune
```

- Download `gemma-3-finetune.zip` via Google Drive to your computer.
- Unzip to a directory on your computer (e.g., `path/to/gemma-3-finetune`).



#### Step 5: Proceed to OS-Specific Conversion Guide

Depending on your computer’s operating system, proceed to the appropriate guide:

- **Windows**: Guide 2a: Convert to Q4_K_M GGUF for Ollama on Windows.
- **Mac**: Guide 2b: Convert to Q4_K_M GGUF for Ollama on Mac.
- **Linux**: Guide 2c: Convert to Q4_K_M GGUF for Ollama on Linux.



---


## Troubleshooting Tips for Fine-Tuning



- **Colab Session Disconnects**:
  - Ensure you remain active during the 6-minute training run to avoid disconnection (Colab may terminate idle sessions after 20-40 minutes).
  - If disconnected before saving, restart the notebook, remount Drive, and rerun the steps.
  
  
  
- **Memory Issues in Colab**:
  - Reduce `per_device_train_batch_size` to 1 or increase `gradient_accumulation_steps` to 8.
  - Run: `!nvidia-smi` to monitor VRAM usage.
  
  
  
- **Disk Space Issues**:
  - Monitor disk space with `!df -h` before and after training.
  - Clear temporary files with `!rm -rf /root/.cache/huggingface` and `!rm -rf *.txt` if space runs low.

