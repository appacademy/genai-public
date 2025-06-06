from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load the base model
base_model_name = "unsloth/gemma-3-4b-it"
model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    device_map="cpu",  # Explicitly use CPU
    torch_dtype="float16",  # Use float16 to reduce memory usage
    low_cpu_mem_usage=True,  # Optimize for CPU memory usage
)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)

# Load the fine-tuned LoRA adapters
lora_path = "D:/source/w-repos/AppAcademy/activities/AA-GenAI-Activities/mod-10-activity-01-fine-tuning-an-llm/convert-to-q4_k_m-gguf/gemma-3"
model = PeftModel.from_pretrained(model, lora_path, device_map="cpu")

# Merge the LoRA adapters with the base model
model = model.merge_and_unload()

# Save the merged model
output_path = "D:/source/w-repos/AppAcademy/activities/AA-GenAI-Activities/mod-10-activity-01-fine-tuning-an-llm/convert-to-q4_k_m-gguf/gemma-3-finetune"
model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)

print(f"Merged model saved to {output_path}")
