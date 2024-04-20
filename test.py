
highscore_list = []

with open("highscore_list.txt", "r", encoding="utf-8") as file:
    text = file.read()
    lines = text.splitlines()
    for line in lines:
        word = line.split(" ")
        highscore_list.append([word[0], int(word[1])])


print(highscore_list)

highscore_list.append(['Paco', 55000] )
print(highscore_list)

while True:
    bubbled = False
    for i in range(len(highscore_list)-1):  
        if highscore_list[i][1] < highscore_list[i+1][1]:
            highscore_list[i+1], highscore_list[i] = highscore_list[i], highscore_list[i+1]
            bubbled = True
            
    if not bubbled:
        break

print(highscore_list)