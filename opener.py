import sys
file = sys.argv[1]

try:
    with open(file) as f:
        content = f.read()

    print(content)
    new = input("Write> ")
    with open(file, "w") as f:
        f.write(new)
except Exception as e:
    print(e)