with open("Word_extractor/temp_input.txt", encoding="utf-8", errors="replace") as file:
    text_input = file.read()

for i in ("\n", ".", "/", ",", "(", ")", ":", ";"):
    text_input = text_input.replace(i, " ")
text_input = text_input.lower()

full_word_list = text_input.split(" ")
cleared_list = list(dict.fromkeys(full_word_list))

keep_list = []
i = 0
while i < len(cleared_list):
    keep = input(f"(y/n/h)Keep: {cleared_list[i]}\n")
    if keep == "y":
        keep_list.append(cleared_list[i])
        i += 1
    elif keep == "h":
        keep_list.append(input(f"New word:\n"))
    elif keep == "n":
        i += 1
    elif keep == "q":
        break

with open("Word_extractor/word_list.txt", "w") as file:
    for word in keep_list:
        file.write(word + ", ")