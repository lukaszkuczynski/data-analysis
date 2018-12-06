import pickle

def read_file():
    filename = 'data/java_posts.pickle'
    with open(filename, 'rb') as f:
        docs = pickle.load(f)
        return docs

if __name__ == "__main__":
    docs = read_file()
    print(docs)