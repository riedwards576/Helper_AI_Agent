from functions.run_python import run_python_file

if __name__ == "__main__":
    print("Test 1: calculator/.")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Test 2: calculator/pkg")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Test 3: calculator/bin")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Test 4: calculator/bin")
    print(run_python_file("calculator", "nonexistent.py"))
    print()