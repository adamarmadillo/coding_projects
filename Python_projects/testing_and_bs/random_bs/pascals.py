num_rows = 5
layer = [1]
lis = [layer]
for i in range(1, num_rows): # 1, 2, 3, 4 (number/len of the row being copied from)
    new_layer = []
    for j in range(i + 1): # 0, 1 -> 0, 1, 2 (indices of the row being generated/last row + 1)
        if j == 0:
            new_layer.append(layer[j])
        elif j == i:
            new_layer.append(layer[j - 1])
        else:
            new_layer.append(layer[j - 1] + layer[j])
    layer = new_layer
    lis.append(layer)

print(lis)