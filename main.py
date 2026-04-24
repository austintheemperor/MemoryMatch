def size():
    width = int(input("width: "))
    height = int(input("height: "))
    return width, height
width, height = 3, 3
while (width * height) % 2 != 0:
    print("at least one value has to be positive")
    width, height = size()

key = []
visual = []
counter = 1

for i in range(1, height + 1):
    keyRow = []
    row = []
    for j in range(1, width + 1):
        counter += 1
        keyRow.append(f"{i}x{j}")
        if counter % 2 != 0:
            row.append(f"{(counter - 1)//2}")
        else:
            row.append(f"{counter//2}")
    visual.append(row)
    key.append(keyRow)

print(key)
print(visual)