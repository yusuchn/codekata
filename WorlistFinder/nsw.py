for word in open('file'):
    word = word.strip()
    if set(word) <= set(permitted_characters):
        print(word)