import pandas as pd

def read_file():
    filename = 'python_posts.csv'
    df = pd.read_csv(filename, encoding='utf8')
    print(df.describe())

if __name__ == "__main__":
    read_file()
#     docs = read_file()
#     print(docs)