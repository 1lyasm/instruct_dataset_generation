import json
import argparse
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM


def main():
    parser = argparse.ArgumentParser(
        prog="correct",
        description="Correct writing errors in the input dataset",
    )
    parser.add_argument(
        "-d",
        "--dataset_path",
        help="Path of the dataset",
        default=os.path.join("data", "top_down.json"),
    )
    parser.add_argument(
        "-o",
        "--output_path",
        help="Path of the corrected output dataset",
        default=os.path.join("output", "corrected.json"),
    )
    arguments = parser.parse_args()

    llm = OllamaLLM(model="llama3.1:8b", num_thread=10, verbose=False)
    template = """From your input, you will
        fix writing errors and label the
        pair from one of these categories:
        "open": 'What color is orange?'
        "closed":
            'Given that  F=mg, find F if m = 10, g = 9.8'
        "extraction": 'Einstein was born in 1918.
            What year was Einstein born?'
        "summarization": 'Summarize the following passage:
            <passage>'
        "brainstorming": "Come up with an idea for a
            date"
        "classification": "Classify the following to animals
            and fruits: [list]"
        "writing": "Write a love poem"
         Your response is in valid JSON format.
         Make sure that 'instruction' and 'answer'
            is written according to the rules of
            Azerbaijani language and reads smoothly.
         Rewrite them if necessary.
         Here is the JSON:
         {instruction}
        """
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm
    answer = chain.invoke({"instruction": """{
        "instruction": "Təyinat yerinə çatmaq üçün marşrut planlayıcısı yaradın. Başlayın: Interlaken, İsveçrə\n Təyinat: Lauterbrunnen, İsveçrə",
        "answer": "Bahnhofstrasse-yə MarkTgasse-də şimal-şərqdə, Bahnhofstrasse-yə sola dönün, Bernstrasse-yə sola dönün, HauptStrasse'nin üzərinə ilk sağa dönün və sonra Murbacherstrasse'yə davam edin. Interlakenstrasse-yə sola dönün və Gewerbestrasse-yə bir qədər sağ çıxın. Lauterbrunnen üçün işarələri izləyin və sağa Zellerweg üzərinə dönün. Yolda çəngəldə Steinbridge-də sağa dönün və Lauterbrunnen'in dolama yolunu izləyin.",
        "category": "unknown"
    }"""})
    print(answer)

if __name__ == "__main__":
    main()
