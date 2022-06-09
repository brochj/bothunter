def read_words_list(filename: str) -> list:
    with open(f"{filename}.txt", "r") as file:
        return [line.rstrip() for line in file]
