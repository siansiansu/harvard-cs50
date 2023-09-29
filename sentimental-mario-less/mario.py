from cs50 import get_int


def helper(n):
    res = ""
    for i in range(1, n + 1):
        res += "#"
    return res


def helper2(n):
    res = ""
    for i in range(n):
        res += " "
    return res


height = 0
while height < 1 or height > 8:
    height = get_int("Height: ")

for i in range(1, height + 1):
    print(helper2(height - i) + helper(i))
