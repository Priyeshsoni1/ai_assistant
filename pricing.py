MODEL_PRICING={
    "openai/gpt-oss-20b:free":{
        "input":0.03,
        "output":0.07
    },
    "gpt-4o-mini":{
        "input":0.13,
        "output":0.67        
    }
}

def calculate_cost(prompt_tokens,completion_tokens,model):
    pricing=MODEL_PRICING[model]

    input_cost=(completion_tokens*pricing["input"])/10000000
    output_cost=(prompt_tokens*pricing["output"])/1000000
    total_cost=input_cost+output_cost

    return input_cost,output_cost,total_cost
