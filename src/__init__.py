from .intellitext import IntelliText


def main():
    it = IntelliText()
    it.listen()


if __name__ == '__main__':
    main()

__all__ = ["IntelliText"]