from llms import OllamaGenerator
from main import search_title

q_map = {
    "How does message compression affect data flow in Kafka?": [
        "What impact does compressing messages have on Kafka's data throughput?",
        # "In Kafka, how does enabling compression influence data transmission?",
        # "How is Kafka’s data flow affected when message compression is used?",
        # "What are the effects of using message compression on Kafka performance?",
        # "Does compressing Kafka messages change how data moves through the system?",
        # "How does Kafka handle data flow when compression is turned on?",
        # "What role does message compression play in Kafka’s streaming efficiency?",
        # "How does enabling compression alter Kafka’s data pipeline behavior?",
        # "What changes occur in Kafka data transfer when compression is applied?",
        # "How does Kafka’s data handling differ with and without message compression?",
    ]
}

for q, sep in q_map.items():
    print(f"{q}:")
    print("Possible resp:")
    res = search_title(q)
    tab = "\t"
    print(f"Top 5 results for {q}:")
    for i, r in enumerate(res):
        score = r.get("_score", 0) - 1  #  converting to --> [-1, 1] scale again
        r = r.get("_source", {})
        print(tab, f"{i}. {r['title']}: Score: {score}")

    for i, s in enumerate(sep):
        res = search_title(s)
        print(tab, f"Top 5 results for {s}:")
        res_text = ""
        for i, r in enumerate(res):
            score = r.get("_score", 0) - 1  #  converting to --> [-1, 1] scale again
            r = r.get("_source", {})
            print(tab, tab, f"{i}. {r['title']}: Score: {score}")

    print(r)

    ollama = OllamaGenerator("deepseek-r1:32b", str(r))
    print(ollama.get_response("1", "What impact does compressing messages have on Kafka's data throughput?"))
    print()
