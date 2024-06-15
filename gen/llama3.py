import transformers
import torch

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
    )

messages = [
    {"role": "system", "content": "You are a gifted writer and keen observer of the human race."},
    {"role": "user", "content": "Write a long essay about 'meaning' for humans across history."},
    ]

prompt = pipeline.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True,
        )

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
    ]

outputs = pipeline(
    prompt,
    max_new_tokens=6144,
    eos_token_id=terminators,
    do_sample=True,                 # do beam search and generate alternatives
    temperature=0.6,
    top_p=0.9,
    )
print(outputs[0]["generated_text"][len(prompt):])
