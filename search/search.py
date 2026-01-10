import nltk
import sqlite3

con = sqlite3.connect('handmade.db')
cur = con.cursor()

index = {}

while True:
    query = input("\n: ")
    keywords = nltk.WhitespaceTokenizer().tokenize(query)

    final_results = {}

    for word in keywords:
        res = cur.execute('SELECT * FROM webIndex WHERE keyword = ?', (word,)).fetchall()
        if len(res) == 0:
            continue

        for result in res:
            word = result[0]
            url = result[1]
            score = result[2]
        
            if url in final_results:
                final_results[url] += score
            else:
                final_results[url] = score
        
    final_results = dict(sorted(final_results.items(), key=lambda item: item[1], reverse=True))
    final_results = list(final_results.items())[0:10]
    for i, result in enumerate(final_results):
        print(i + 1, ": ", result[0])