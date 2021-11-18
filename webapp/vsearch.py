def search4vowels(phrase: str, letters: str='aeiou') -> set:
    return set(letters).intersection(set(phrase))