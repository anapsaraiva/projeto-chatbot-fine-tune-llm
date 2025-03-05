from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./fine-tuned-model")
tokenizer = AutoTokenizer.from_pretrained("./fine-tuned-model")

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def generate_response(query, context):
    if not context or len(context) == 0:
        return "Não encontrei informações suficientes no repositório para responder sua pergunta."

    context_text = "\n".join([str(doc) if doc is not None else "" for doc in context])

    input_text = (
        f"Contexto: {context_text}\n"
        f"Pergunta: {query}\n"
        f"Resposta:"
    )
  
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding=True)

    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=256,  
        num_return_sequences=1,
        pad_token_id=tokenizer.pad_token_id,
        no_repeat_ngram_size=2,  
        do_sample=False,  
        num_beams=5,  
        early_stopping=True,  # Parar a geração quando a resposta estiver completa
        repetition_penalty=1.5, 
        temperature=0.2,  
        top_k=50,  
        top_p=0.9,
    )

    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extrair apenas a parte da resposta após "Resposta:"
    response_start = full_response.find("Resposta:") + len("Resposta:")
    answer = full_response[response_start:].strip()

    return answer
