import json
import nltk

index = {}

with open('reverse.json', 'r') as file:
    index = json.loads(file.read())

while True:
    query = input("\n: ")
    keywords = nltk.WhitespaceTokenizer().tokenize(query)

    final_results = {}

    for word in keywords:
        if word not in index:
            continue
        
        results = index[word]
        for url in results:
            if url in final_results:
                final_results[url] += results[url]
            else:
                final_results[url] = results[url]
        
    final_results = dict(sorted(final_results.items(), key=lambda item: item[1], reverse=True))
    final_results = list(final_results.items())[0:10]
    for i, result in enumerate(final_results):
        print(i + 1, ": ", result[0])