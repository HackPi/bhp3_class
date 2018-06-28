import queue
import requests
import threading

THREADS = 50
TARGET = "http://testphp.vulnweb.com"
WORDLIST = "/Users/jtimarnold/Downloads/SVNDigger/all.txt"
EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"

def get_words(resume=None):
    
    def extend_words(word):
        if "." in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')

        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')
    
    with open(WORDLIST) as f:
        raw_words = f.read()

    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            else:
                if word == resume:
                    found_resume = True
                    print(f'Resuming wordlist from: {resume}')
        else:
            extend_words(word)
    return words

def dir_find(words):
    while not words.empty():
        word = words.get()
        url = f'{TARGET}{word}'
        headers = {'User-Agent': AGENT}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            if r.status_code == 404:
                print('.', end='')
            else:
                print(f'{r.status_code} => {url}')
        else:
            print(f'\nSuccess ({r.status_code}: {url})')

if __name__ == '__main__':
    #popup_help_screen.php
    words = get_words()
    for _ in range(THREADS):
        t = threading.Thread(target=dir_find, args=(words,))
        t.start()
