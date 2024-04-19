
highscore_list = []

with open("highscore_list.txt", "r", encoding="utf-8") as file:
    text = file.read()
    lines = text.splitlines()
    for line in lines:
        word = line.split(" ")
        highscore_list.append([word[0], int(word[1])])

print(lines)
print(highscore_list)


