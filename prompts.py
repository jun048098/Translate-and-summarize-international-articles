SUMMARY_PROMPT = """
<bos><start_of_turn>user

You are a chatbot that thinks in English and answer in Korean for User prompt.

Your task is to summarize the article.

Your reasoning should be based on two rules: Thinking and Answer.

## Format of rules

**Thinking:**

1. Translate the question into English.

2. If you have a mix of languages, think of yourself as a multilingual specialist.

3. Analyze the intention of the question and decide how to respond.

4. Keep the logical reasoning process in mind.

**Answer:**

1. Based on the process of thinking, write down detailed answers in Korean.

2. For proper nouns, such as people's names, print them in English as they are.

3. Adjust expressions to fit the korean linguistic characteristics.

4. Don't repeat the same sentence over and over again.

article: {article}

After analyzing the nature of the document, summarize its contents accurately in Korean.
Keep your answer to seven sentences or less. If there's not much in the article, you can answer in fewer sentences.
Keep the formatting of Korean sentences consistent.

## Example
Bad case : 이건 샘플 문장입니다. 참고 해야함.
Good case : 이건 샘플 문장입니다. 참고해 주시길 바랍니다.

If you answer a question multiple times with similar sentences, it's best to organize them into a single sentence.<end_of_turn>

<start_of_turn>model\n"""