import os
#from llama_cpp import Llama
from openai import OpenAI


# def llama_endpoint(text: str):
#     model = Llama(
#         model_path='gemma-2-9b-it-Q4_K_M.gguf', #다운로드받은 모델의 위치
#         n_ctx=512,
#         n_gpu_layers= -1        # Number of model layers to offload to GPU
#     )
#     output = model(
#       text, # Prompt
#       max_tokens=512, # Generate up to 32 tokens, set to None to generate up to the end of the context window
#       stop=["<|eot_id|>"], # Stop generating just before the model would generate a new question
#       echo=True # Echo the prompt back in the output
#     )
#     return output['choices'][0]['text'][len(text):]

system_prompt = """
You are a chatbot that thinks in English and answer in Korean for User prompt.

Your task is to summarize the article.

Your reasoning should be based on two rules: Thinking and Answer.

## Format of rules

**Thinking:**

1. Translate the question into English.

2. Analyze the intention of the question and decide how to respond.

3. If you have a mix of languages, think of yourself as a multilingual specialist.

4. Keep the logical reasoning process in mind.

**Answer:**

1. Based on the process of thinking, write down detailed answers in Korean.

2. For proper nouns, such as people's names, print them in English as they are.

3. Adjust expressions to fit the korean linguistic characteristics.

4. Don't repeat the same sentence over and over again.<end_of_turn>"""


def vllm_endpoint(text: str, news: bool=True):
    client = OpenAI(
        base_url=os.environ.get("RUNPOD_BASE_URL"),
        api_key=os.environ.get("RUNPOD_API_KEY"),
    )
    if news:

        prompt = f"""
        article: {text}

        After analyzing the article, summarize its contents accurately in Korean.
        If you answer a question multiple times with similar sentences, it's best to organize them into a single sentence.
        On the very first line, write the title of article.
        Try to limit the number of sentences in your summary to fifteen or so.
        All sentences must be complete and end with a dot (.).

        ### Example
        모든 문장은 다음과 같이 완성된 상태로 끝나야 합니다. 중간에 끊어지지 않도록 합니다."""
    else:
        prompt = text
    response = client.chat.completions.create(
    model="google/gemma-2-9b-it",
    messages=[{"role": "user", "content": system_prompt},
              {"role": "assistant", "content": "당신의 요청을 이해했습니다. Thinking과 Answer 규칙에 근거해서 article을 요약하겠습니다. 저에게 요약해야 할 article을 제공해 주세요."},
              {"role": "user", "content":prompt}],
    temperature=0,
    # max_tokens=4096,
    )
    # return response.choices[0].message.content
    return response


if __name__ == "__main__":
    print(vllm_endpoint("안녕하세요?"))