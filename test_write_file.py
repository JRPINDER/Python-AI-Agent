from functions.write_file import writefile

def main():
    print(writefile("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(writefile("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(writefile("calculator", "/tmp/temp.txt", "this should not be allowed"))

if __name__ == "__main__":
    main()

