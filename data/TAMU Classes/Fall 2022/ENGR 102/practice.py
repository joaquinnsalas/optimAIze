while True:
    try:
        num = int(input("Enter your favorite integer: "))
    except ValueError:
        print("Please enter a valid integer")
        continue
    else:
        break