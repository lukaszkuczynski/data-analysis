import argparse
import requests
import json
import csv
from bs4 import BeautifulSoup

DEVTO_API_ARTICLES_URL = 'https://dev.to/api/articles'


def log(txt):
    print(txt)


def get_ids(args):
    tag = args.tag
    for page in range(1, args.pages+1):
        log("analyzing page %d " % page)
        url = "%s?tag=%s&page=%d" % (DEVTO_API_ARTICLES_URL, tag, page)
        resp = requests.get(url)
        body = json.loads(resp.text)
        for entry in body:
            yield entry['id']
            

def get_texts_for_ids(IDs):
    texts = []
    for id in IDs:
        url = "%s/%d" % (DEVTO_API_ARTICLES_URL, id)
        resp = requests.get(url)
        body = json.loads(resp.text)
        if not 'body_html' in body:
            log('htlm not found in %s' % body)
            continue
        soup = BeautifulSoup(body['body_html'])
        texts.append({
            'id': body['id'],
            'title': body['title'],
            'content': soup.get_text()
        })
        log("fetched docs with title '%s'" % body['title'])
    return texts    


def write_texts_to_csv(args, texts):
    output_filename = args.output
    with open(output_filename, 'w', newline='', encoding='utf8') as f:
        writer = csv.DictWriter(f, fieldnames=['id','title','content'])
        writer.writeheader()
        writer.writerows(texts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default='java')
    parser.add_argument("--pages", default=10)
    parser.add_argument("--output", default='java_posts.csv')
    args = parser.parse_args()
    ids = get_ids(args)
    texts = get_texts_for_ids(ids)
    # texts = list(texts[:3])
    write_texts_to_csv(args, texts)
    

