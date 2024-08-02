# Libraries
import ollama


def job_titles(title):
    template = """
        For the following jobs titles please give me its general title.

        be short and concise no explanation and no duplicates, no punctuation the responses should be in English.

        do not add more than one general title

        Question: {question}
        """

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": template.format(question=title),
            },
        ],
    )
    return response["message"]["content"]
