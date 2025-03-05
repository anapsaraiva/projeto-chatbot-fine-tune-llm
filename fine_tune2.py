from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

dataset = load_dataset("json", data_files="dataset.jsonl", split="train")

subset_size = 100  # Número de amostras para teste inicial
small_dataset = dataset.shuffle(seed=42).select(range(subset_size))

model_name = "EleutherAI/gpt-neo-125M"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token  

def tokenize_function(examples):
    texts = []
    for i in range(len(examples["context"])):
        text = (
            f"Contexto: {examples['context'][i]}\n"
            f"Pergunta: {examples['question'][i]}\n"
            f"Resposta: {examples['answer'][i]}\n"
        )
        texts.append(text)
    
    tokenized = tokenizer(
        texts,
        truncation=True,
        padding="max_length",
        max_length=512,
    )
    
    tokenized["labels"] = tokenized["input_ids"].copy()
    
    return tokenized

tokenized_small_dataset = small_dataset.map(tokenize_function, batched=True)

print(f"Tamanho do dataset reduzido: {len(tokenized_small_dataset)}")

# Argumentos de treinamento
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",          
    learning_rate=5e-5,
    per_device_train_batch_size=2,  
    gradient_accumulation_steps=2, 
    num_train_epochs=2,             
    weight_decay=0.01,
    save_total_limit=2,
    save_strategy="epoch",         
    logging_dir="./logs",           
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    use_cpu=True,     
    greater_is_better=False,              
    gradient_checkpointing=False,   
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_small_dataset,    
    eval_dataset=tokenized_small_dataset,       
)

trainer.train()

model.save_pretrained("./fine-tuned-model")
tokenizer.save_pretrained("./fine-tuned-model")
