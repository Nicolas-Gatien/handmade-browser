import nltk
import os
from supabase import create_client, Client
from dotenv import load_dotenv

def search(query) -> list[str]:
    load_dotenv()

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    keywords = nltk.WhitespaceTokenizer().tokenize(query)

    final_results = {}

    for word in keywords:
        res = (
            supabase
            .table("index")
            .select("*")
            .eq("keyword", word)
            .execute()
        )

        if len(res.data) == 0:
            continue

        for result in res.data:
            word = result['keyword']
            url = result['url']
            score = result['score']
        
            if url in final_results:
                final_results[url] += score
            else:
                final_results[url] = score
        
    final_results = dict(sorted(final_results.items(), key=lambda item: item[1], reverse=True))
    final_results = list(final_results.items())[0:10]
    
    return final_results