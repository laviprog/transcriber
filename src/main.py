from src import log


def welcome_message() -> str:
    log.info("Welcome to python-best-template!")
    return "Hello from python-best-template!"


def main():
    print(welcome_message())


if __name__ == "__main__":
    main()
