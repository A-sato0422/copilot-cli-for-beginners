def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if not choice:
            print("入力が空です。1〜5の数字を入力してください。")
        elif not choice.isdigit():
            print(f"「{choice}」は無効な入力です。数字を入力してください。")
        elif choice not in {"1", "2", "3", "4", "5"}:
            print(f"「{choice}」は範囲外です。1〜5の数字を入力してください。")
        else:
            return choice


def get_book_details():
    """対話形式でユーザーから書籍情報を取得する。

    標準入力からタイトル・著者名・出版年を順に読み取る。
    タイトルが空の場合は再入力を促す。
    出版年が数値に変換できない場合は 0 をデフォルト値として使用する。

    Parameters
    ----------
    なし（引数は受け取らない）

    Returns
    -------
    tuple[str, str, int]
        (title, author, year) の3要素タプル。

        - title (str): 書籍タイトル。空文字は許容されない。
        - author (str): 著者名。空文字の場合もそのまま返す。
        - year (int): 出版年。無効な入力の場合は 0 を返す。

    Examples
    --------
    >>> # ユーザーが "Python入門", "山田太郎", "2024" と入力した場合
    >>> title, author, year = get_book_details()
    >>> print(title, author, year)
    Python入門 山田太郎 2024
    """
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("タイトルは必須です。空にすることはできません。")

    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books):
    """
    本のコレクションを整形して標準出力に表示する。

    Args:
        books (list[dict]): 表示する本の辞書リスト。
                            各辞書は 'title'、'author'、'year' キーを持つことを想定。

    Returns:
        None
    """
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
