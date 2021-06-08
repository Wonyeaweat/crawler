import csv

def solve():
    csv.field_size_limit(500 * 1024 * 1024)  # 设置csv字段最大长度
    wordlistfile = open("./wordlist.txt", "r")
    index = open("./index.csv", "w")
    indexwriter = csv.writer(index)
    wordlist = wordlistfile.readlines()
    for word in wordlist:
        word = word.strip()
        print(word)
        csvfile = open("./data.csv", "r", newline='')
        csvreader = csv.reader(csvfile)
        writeline = [word]
        for line in csvreader:
            if len(line) > 1:
                id = line[0]
                url = line[1]
                title = line[2]
                text = line[3]
                if text.count(word) > 0:
                    writeline.append((id, title, url, text.count(word)/len(text)))
        indexwriter.writerow(writeline)


if __name__ == "__main__":
    solve()
