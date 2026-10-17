import sys

def anal(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    pocet_bodiek = text.count('.')

    print(f"Pocet slov koniacich bodkov: {pocet_bodiek}")
    print(f"Pocet viet: {pocet_bodiek}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_dots.py <textfile>")
        sys.exit(1)
    anal(sys.argv[1])
