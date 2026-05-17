![Chapter 03: Development Workflows](images/chapter-header.png)

> **AIが、あなたが気づいていないバグまで発見してくれるとしたら？**

この章では、GitHub Copilot CLI が毎日の開発ルーティンに欠かせない相棒になります。テスト、リファクタリング、デバッグ、Git など、すでに使っているワークフローの中で活用していきましょう。

## 🎯 学習目標

この章を終えると、次のことができるようになります：

- Copilot CLI を使って包括的なコードレビューを行う
- レガシーコードを安全にリファクタリングする
- AI の助けを借りて問題をデバッグする
- テストを自動生成する
- Copilot CLI を Git ワークフローと統合する

> ⏱️ **目安時間**：約60分（読書15分 + ハンズオン45分）

---

## 🧩 実世界のたとえ：大工のワークフロー

大工はツールの使い方を知っているだけでなく、仕事ごとに*ワークフロー*を持っています：

<img src="images/carpenter-workflow-steps.png" alt="Craftsman workshop showing three workflow lanes: Building Furniture (Measure, Cut, Assemble, Finish), Fixing Damage (Assess, Remove, Repair, Match), and Quality Check (Inspect, Test Joints, Check Alignment)" width="800"/>

同じように、開発者もタスクごとにワークフローを持っています。GitHub Copilot CLI はそれぞれのワークフローを強化し、日々のコーディング作業をより効率的・効果的にしてくれます。

---

# 5つのワークフロー

<img src="images/five-workflows.png" alt="Five glowing neon icons representing code review, testing, debugging, refactoring, and git integration workflows" width="800"/>

以下の各ワークフローは独立しています。今の状況に合ったものを選んで試してみましょう。すべて順番にこなす必要はありません。

---

## 自分に合ったルートを選ぼう

この章では、開発者がよく使う5つのワークフローを紹介します。**ただし、一度に全部読む必要はありません！** 各ワークフローは折りたたみセクションとして独立しています。今のプロジェクトに合ったものを選んで試しましょう。残りはいつでも後で戻って確認できます。

<img src="images/five-workflows-swimlane.png" alt="Five Development Workflows: Code Review, Refactoring, Debugging, Test Generation, and Git Integration shown as horizontal swimlanes" width="800"/>

| やりたいこと | ジャンプ先 |
|---|---|
| マージ前にコードをレビューしたい | [ワークフロー1：コードレビュー](#workflow-1-code-review) |
| 散らかったコードやレガシーコードを整理したい | [ワークフロー2：リファクタリング](#workflow-2-refactoring) |
| バグを追跡して修正したい | [ワークフロー3：デバッグ](#workflow-3-debugging) |
| コードのテストを生成したい | [ワークフロー4：テスト生成](#workflow-4-test-generation) |
| よりよいコミットとPRを書きたい | [ワークフロー5：Git 統合](#workflow-5-git-integration) |
| コーディング前にリサーチしたい | [クイックヒント：計画やコーディング前にリサーチしよう](#quick-tip-research-before-you-plan-or-code) |
| バグ修正ワークフローを端から端まで見たい | [総まとめ：バグ修正ワークフロー](#putting-it-all-together-bug-fix-workflow) |

**以下のワークフローをクリックして展開し**、GitHub Copilot CLI がその領域でどのように開発プロセスを強化できるかを確認しましょう。

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>ワークフロー1：コードレビュー</strong> - ファイルのレビュー、/review エージェントの使用、重要度別チェックリストの作成</summary>

<img src="images/code-review-swimlane-single.png" alt="Code review workflow: review, identify issues, prioritize, generate checklist." width="800"/>

### 基本のレビュー

この例では `@` 記号を使ってファイルを参照し、Copilot CLI がそのファイルの内容に直接アクセスしてレビューできるようにしています。

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![Code Review Demo](images/code-review-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

### 入力バリデーションのレビュー

プロンプトに気にするカテゴリを列挙して、特定の観点（ここでは入力バリデーション）に絞ったレビューを依頼しましょう。

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### プロジェクト全体のクロスファイルレビュー

`@` でディレクトリ全体を参照すると、Copilot CLI がプロジェクト内の全ファイルを一度にスキャンできます。

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### インタラクティブなコードレビュー

複数ターンの会話でより深く掘り下げましょう。最初に広めのレビューを依頼し、その後セッションを再起動せずにフォローアップの質問ができます。

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI が詳細なレビューを提供する

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI が空文字列・特殊文字の潜在的な問題を示す

> Create a checklist of all issues found, prioritized by severity

# Copilot CLI が重要度順のアクションアイテムを生成する
```

### レビューチェックリストテンプレート

出力を特定のフォーマット（ここでは重要度別に分類したマークダウンチェックリスト）で構造化するよう Copilot CLI に依頼しましょう。Issue にそのまま貼り付けられます。

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Git の変更を理解する（/review の前に重要）

`/review` コマンドを使う前に、git の2種類の変更を理解しておきましょう：

| 変更の種類 | 意味 | 確認方法 |
|-------------|---------------|------------|
| **ステージ済みの変更** | `git add` で次のコミットにマークしたファイル | `git diff --staged` |
| **未ステージの変更** | 変更したがまだ add していないファイル | `git diff` |

```bash
# クイックリファレンス
git status           # ステージ済みと未ステージ両方を表示
git add file.py      # ファイルをコミット用にステージ
git diff             # 未ステージの変更を表示
git diff --staged    # ステージ済みの変更を表示
```

### /review コマンドを使う

`/review` コマンドは組み込みの **code-review エージェント** を呼び出します。このエージェントはステージ済み・未ステージの変更を高いシグナル対ノイズ比で分析するよう最適化されています。自由形式のプロンプトを書く代わりに、スラッシュコマンドで特化した組み込みエージェントを起動しましょう。

```bash
copilot

> /review
# ステージ済み/未ステージの変更に対して code-review エージェントを呼び出す
# 焦点を絞った実用的なフィードバックを提供する

> /review Check for security issues in authentication
# 特定の観点を指定してレビューを実行する
```

> 💡 **ヒント**: code-review エージェントは保留中の変更がある場合に最も効果的です。`git add` でファイルをステージしておくと、より焦点を絞ったレビューができます。

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>ワークフロー2：リファクタリング</strong> - コードの再構造化、関心の分離、エラーハンドリングの改善</summary>

<img src="images/refactoring-swimlane-single.png" alt="Refactoring workflow: assess code, plan changes, implement, verify behavior." width="800"/>

### シンプルなリファクタリング

> **まずこれを試してみよう：** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

まずは簡単な改善から始めましょう。ブックアプリで試してみてください。各プロンプトは `@` ファイル参照と具体的なリファクタリング指示を組み合わせているので、Copilot CLI が何を変更すればよいかを正確に把握できます。

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **リファクタリング初心者の方へ：** 複雑な変換に取り組む前に、型ヒントの追加や変数名の改善などシンプルなリクエストから始めましょう。

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![Refactor Demo](images/refactor-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

### 関心の分離

1つのプロンプトで複数のファイルを `@` で参照すると、Copilot CLI がリファクタリングの一環としてファイル間でコードを移動できます。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### エラーハンドリングの改善

関連する2つのファイルを提供し、横断的な関心事を説明することで、Copilot CLI が両方に対して一貫した修正を提案できます。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### ドキュメントの追加

各 docstring に何を含めるべきかを箇条書きで細かく指定しましょう。

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### テストを使った安全なリファクタリング

複数ターンの会話で2つの関連するリクエストを連続して行います。まずテストを生成し、そのテストをセーフティネットとしてリファクタリングを行います。

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# まずテストを取得する

> Now refactor the BookCollection class to use a context manager for file operations

# テストによって動作が保たれていることを確認しながら安心してリファクタリングできる
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>ワークフロー3：デバッグ</strong> - バグの追跡、セキュリティ監査、複数ファイルにまたがる問題のトレース</summary>

<img src="images/debugging-swimlane-single.png" alt="Debugging workflow: understand error, locate root cause, fix, test." width="800"/>

### シンプルなデバッグ

> **まずこれを試してみよう：** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

まず何がおかしいかを説明しましょう。バグ入りのブックアプリで試せる一般的なデバッグパターンをご紹介します。各プロンプトは `@` ファイル参照と明確な症状の説明を組み合わせているので、Copilot CLI がバグを特定して診断できます。

```bash
copilot

# パターン：「X を期待していたが Y になった」
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# パターン：「予期しない動作」
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# パターン：「間違った結果」
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **デバッグのヒント**：*症状*（見えているもの）と*期待値*（本来こうなるべき動作）を説明しましょう。Copilot CLI があとは解決してくれます。

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![Fix Bug Demo](images/fix-bug-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

### 「バグ探偵」- AI が関連バグも発見する

ここでコンテキストを考慮したデバッグが真価を発揮します。バグ入りブックアプリでこのシナリオを試してみましょう。`@` でファイル全体を渡し、ユーザーが報告した症状だけを説明します。Copilot CLI は根本原因を追跡し、近くにある別のバグまで発見することがあります。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**Copilot CLI が行うこと**：
```
Root Cause: Line 80 uses exact match (==) instead of partial match (in).

Line 80: return [b for b in self.books if b.author == author]

The find_by_author function requires an exact match. Searching for "Tolkien"
won't find books by "J.R.R. Tolkien".

Fix: Change to case-insensitive partial match:
return [b for b in self.books if author.lower() in b.author.lower()]
```

**なぜ重要か**：Copilot CLI はファイル全体を読み込み、バグレポートのコンテキストを理解し、明確な説明とともに具体的な修正を提示します。

> 💡 **ボーナス**：Copilot CLI がファイル全体を分析するため、あなたが聞いていない*別の問題*も発見することがあります。たとえば、著者検索の修正中に `find_book_by_title` の大文字・小文字バグにも気づくかもしれません！

### 実世界のセキュリティサイドバー

自分のコードのデバッグも重要ですが、本番アプリのセキュリティ脆弱性を理解することはさらに重要です。次の例を試してみましょう：見慣れないファイルに Copilot CLI を向けて、セキュリティ問題を監査させます。

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

このファイルは本番アプリで実際に見られるセキュリティパターンを示しています。

> 💡 **よく登場するセキュリティ用語：**
> - **SQL インジェクション**：ユーザー入力がデータベースクエリに直接挿入され、攻撃者が悪意あるコマンドを実行できる状態
> - **パラメータ化クエリ**：安全な代替手段 - プレースホルダー（`?`）がユーザーデータと SQL コマンドを分離する
> - **レースコンディション**：2つの操作が同時に発生して互いに干渉する状態
> - **XSS（クロスサイトスクリプティング）**：攻撃者がウェブページに悪意あるスクリプトを注入する攻撃

---

### エラーを理解する

スタックトレースを `@` ファイル参照とともにプロンプトに直接貼り付けると、Copilot CLI がエラーをソースコードにマッピングできます。

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### テストケースを使ったデバッグ

正確な入力と観察された出力を説明することで、Copilot CLI が推論できる具体的・再現可能なテストケースを提供します。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### コードをまたいで問題をトレースする

複数のファイルを参照して、Copilot CLI にファイルをまたいだデータの流れを追わせ、問題の発生源を特定させましょう。

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### データの問題を理解する

データファイルと、それを読み込むコードファイルを一緒に参照することで、Copilot CLI がエラーハンドリング改善の提案をする際に全体像を把握できます。

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>ワークフロー4：テスト生成</strong> - 包括的なテストとエッジケースを自動生成</summary>

<img src="images/test-gen-swimlane-single.png" alt="Test Generation workflow: analyze function, generate tests, include edge cases, run." width="800"/>

> **まずこれを試してみよう：** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### 「テスト爆発」- 2件のテストが15件以上に

手動でテストを書くと、開発者は通常2〜3件の基本的なテストを作ります：
- 有効な入力のテスト
- 無効な入力のテスト
- エッジケースのテスト

Copilot CLI に包括的なテストの生成を依頼したらどうなるか見てみましょう！このプロンプトは `@` ファイル参照と構造化された箇条書きを組み合わせて、Copilot CLI を徹底的なテストカバレッジへと誘導します：

```bash
copilot

> @samples/book-app-project/books.py Generate comprehensive pytest tests. Include tests for:
> - Adding books
> - Removing books
> - Finding by title
> - Finding by author
> - Marking as read
> - Edge cases with empty data
```

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![Test Generation Demo](images/test-gen-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

**得られるもの**：15件以上の包括的なテストが含まれます：

```python
class TestBookCollection:
    # ハッピーパス
    def test_add_book_creates_new_book(self):
        ...
    def test_list_books_returns_all_books(self):
        ...

    # 検索操作
    def test_find_book_by_title_case_insensitive(self):
        ...
    def test_find_book_by_title_returns_none_when_not_found(self):
        ...
    def test_find_by_author_partial_match(self):
        ...
    def test_find_by_author_case_insensitive(self):
        ...

    # エッジケース
    def test_add_book_with_empty_title(self):
        ...
    def test_remove_nonexistent_book(self):
        ...
    def test_mark_as_read_nonexistent_book(self):
        ...

    # データの永続化
    def test_save_books_persists_to_json(self):
        ...
    def test_load_books_handles_missing_file(self):
        ...
    def test_load_books_handles_corrupted_json(self):
        ...

    # 特殊文字
    def test_add_book_with_unicode_characters(self):
        ...
    def test_find_by_author_with_special_characters(self):
        ...
```

**結果**：30秒で、1時間かけて考え書くようなエッジケーステストが手に入ります。

---

### ユニットテスト

1つの関数を対象に、テストしたい入力カテゴリを列挙することで、Copilot CLI が焦点を絞った徹底的なユニットテストを生成します。

```bash
copilot

> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### テストの実行

ツールチェーンについてわかりやすい言葉で Copilot CLI に質問してみましょう。適切なシェルコマンドを生成してくれます。

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI が回答する：
# cd samples/book-app-project && python -m pytest tests/
# または詳細出力：python -m pytest tests/ -v
# print 文を表示するには：python -m pytest tests/ -s
```

### 特定のシナリオのテスト

ハッピーパスを超えた高度または複雑なシナリオを列挙して、Copilot CLI に網羅的なテストを生成させましょう。

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### 既存ファイルへのテスト追加

単一の関数に対して*追加の*テストを依頼することで、Copilot CLI が既存のテストを補完する新しいケースを生成します。

```bash
copilot

> @samples/book-app-project/books.py
> Generate additional tests for the find_by_author function with edge cases:
> - Author name with hyphens (e.g., "Jean-Paul Sartre")
> - Author with multiple first names
> - Empty string as author
> - Author name with accented characters
```

</details>

---

<a id="workflow-5-git-integration"></a>
<details>
<summary><strong>ワークフロー5：Git 統合</strong> - コミットメッセージ、PR 説明文、/pr、/delegate、/diff</summary>

<img src="images/git-integration-swimlane-single.png" alt="Git Integration workflow: stage changes, generate message, commit, create PR." width="800"/>

> 💡 **このワークフローは Git の基本的な知識（ステージング・コミット・ブランチ）を前提としています。** Git が初めての方は、まず他の4つのワークフローを試してみましょう。

### コミットメッセージを生成する

> **まずこれを試してみよう：** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — 変更をステージしてからこのコマンドを実行すると、Copilot CLI がコミットメッセージを書いてくれます。

この例では `-p` インラインプロンプトフラグとシェルのコマンド置換を使い、`git diff` の出力を Copilot CLI に直接パイプして1ショットでコミットメッセージを生成します。`$(...)` 構文は括弧内のコマンドを実行し、その出力を外側のコマンドに挿入します。

```bash

# 変更内容を確認する
git diff --staged

# [Conventional Commit](../GLOSSARY.md#conventional-commit) 形式でコミットメッセージを生成する
# （"feat(books): add search" や "fix(data): handle empty input" のような構造化されたメッセージ）
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# 出力例："feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors"
```

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![Git Integration Demo](images/git-integration-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

### 変更内容を説明する

`git show` の出力を `-p` プロンプトにパイプして、最新コミットのわかりやすい要約を取得します。

```bash
# このコミットは何を変更したか？
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### PR の説明文

`git log` の出力と構造化されたプロンプトテンプレートを組み合わせて、完全なプルリクエストの説明文を自動生成します。

```bash
# ブランチの変更から PR 説明文を生成する
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### インタラクティブモードで現在のブランチに /pr を使う

Copilot CLI のインタラクティブモードでブランチを操作している場合、`/pr` コマンドを使ってプルリクエストを操作できます。`/pr` を使うと、PR の表示・新規作成・修正、またはブランチの状態に基づいて Copilot CLI に自動判断させることができます。

```bash
copilot

> /pr [view|create|fix|auto]
```

### プッシュ前のレビュー

`-p` プロンプト内で `git diff main..HEAD` を使い、ブランチの全変更に対してプッシュ前のクイックチェックを行います。

```bash
# プッシュ前の最終確認
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### バックグラウンドタスクへの /delegate

`/delegate` コマンドは作業を GitHub Copilot クラウドエージェントに引き渡します。`/delegate` スラッシュコマンド（または `&` ショートカット）を使って、明確に定義されたタスクをバックグラウンドエージェントにオフロードしましょう。

```bash
copilot

> /delegate Add input validation to the login form

# または & プレフィックスショートカットを使う：
> & Fix the typo in the README header

# Copilot CLI が：
# 1. 変更を新しいブランチにコミットする
# 2. ドラフトプルリクエストを開く
# 3. GitHub 上でバックグラウンドで作業する
# 4. 完了したらレビューを依頼する
```

他の作業に集中しながら完了させたい、明確に定義されたタスクに最適です。

### /diff でセッションの変更を確認する

`/diff` コマンドは現在のセッション中に行ったすべての変更を表示します。コミットする前に Copilot CLI が変更したすべての内容を視覚的な diff で確認するために使いましょう。

```bash
copilot

# 変更を加えた後...
> /diff

# このセッションで変更されたすべてのファイルの視覚的な diff を表示する
# コミット前のレビューに最適
```

</details>

---

## クイックヒント：計画やコーディング前にリサーチしよう

ライブラリを調査したり、ベストプラクティスを理解したり、見慣れないトピックを探索したりする必要があるときは、コードを書く前に `/research` を使って深い調査を行いましょう：

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot が GitHub リポジトリやウェブソースを検索し、参考文献付きのまとめを返します。新しい機能を始める前に調査して、より情報に基づいた意思決定をするときに便利です。結果を `/share` で共有することもできます。

> 💡 **ヒント**：`/research` は `/plan` の*前*に使うと効果的です。アプローチをリサーチしてから実装を計画しましょう。

---

## 総まとめ：バグ修正ワークフロー

報告されたバグを修正するための完全なワークフローです：

```bash

# 1. バグレポートを理解する
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. 問題をデバッグして修正する（同じセッションを継続）
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. 修正のテストを生成する
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# インタラクティブセッションを終了する

> /exit

# 4. git add を実行する

# git diff --staged が機能するように変更をステージする
git add .

# 5. コミットメッセージを生成する
copilot -p "Generate commit message for: $(git diff --staged)"

# 出力例："fix(books): support partial author name search"

# 6. 変更をコミットする（任意）

git commit -m "<生成されたメッセージを貼り付ける>"
```

### バグ修正ワークフローのまとめ

| ステップ | アクション | Copilot コマンド |
|------|--------|-----------------|
| 1 | バグを理解する | `> [バグを説明] @relevant-file.py Analyze the likely cause` |
| 2 | 分析と修正 | `> Show me the function and fix the issue` |
| 3 | テストを生成する | `> Generate tests for [specific scenarios]` |
| 4 | 変更をステージする | `git add .` |
| 5 | コミットメッセージを生成する | `copilot -p "Generate commit message for: $(git diff --staged)"` |
| 6 | 変更をコミットする | `git commit -m "<生成されたメッセージを貼り付ける>"` |

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

これらのワークフローを実際に適用してみましょう。

---

## ▶️ 自分で試してみよう

デモを完了したら、次のバリエーションを試してみましょう：

1. **バグ探偵チャレンジ**：`samples/book-app-buggy/books_buggy.py` の `mark_as_read` 関数のデバッグを Copilot CLI に依頼してみましょう。なぜ1冊だけでなくすべての本が既読になってしまうのかを説明してくれましたか？

2. **テストチャレンジ**：ブックアプリの `add_book` 関数のテストを生成してみましょう。あなたが思いつかなかったエッジケースを Copilot CLI がいくつ含めるかを数えてみましょう。

3. **コミットメッセージチャレンジ**：ブックアプリのファイルに何か小さな変更を加え、ステージして（`git add .`）から実行します：
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   あなたが素早く書いたメッセージより良いメッセージでしたか？

**自己チェック**：「このバグをデバッグして」が「バグを見つけて」より強力な理由（コンテキストが重要！）を説明できれば、開発ワークフローを理解しています。

---

## 📝 課題

### メインチャレンジ：リファクタリング・テスト・シップ

ハンズオンの例では `find_book_by_title` とコードレビューに焦点を当てました。今度は `book-app-project` の別の関数で同じワークフロースキルを練習してみましょう：

1. **レビュー**：`books.py` の `remove_book()` をエッジケースと潜在的な問題についてレビューするよう Copilot CLI に依頼します：
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **リファクタリング**：大文字・小文字を区別しないマッチングや、本が見つからない場合に有用なフィードバックを返すなど、エッジケースに対応するよう `remove_book()` を改善するよう Copilot CLI に依頼します
3. **テスト**：改善された `remove_book()` 関数のための pytest テストを生成します。以下をカバーしてください：
   - 存在する本を削除する
   - 大文字・小文字を区別しないタイトルマッチング
   - 存在しない本は適切なフィードバックを返す
   - 空のコレクションから削除する
4. **レビュー**：変更をステージして `/review` を実行し、残っている問題がないか確認します
5. **コミット**：Conventional Commit メッセージを生成します：
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**各ステップのサンプルプロンプト：**

```bash
copilot

# ステップ1：レビュー
> @samples/book-app-project/books.py Review the remove_book() function. What edge cases are not handled?

# ステップ2：リファクタリング
> Improve remove_book() to use case-insensitive matching and return a clear message when the book isn't found. Show me the before and after code.

# ステップ3：テスト
> Generate pytest tests for the improved remove_book() function, including:
> - Removing a book that exists
> - Case-insensitive matching ("dune" should remove "Dune")
> - Book not found returns appropriate response
> - Removing from an empty collection

# ステップ4：レビュー
> /review

# ステップ5：コミット
> Generate a conventional commit message for this refactor
```

**ヒント：** `remove_book()` を改善した後、Copilot CLI に「このファイルの他の関数でも同じ改善が役立つものはありますか？」と聞いてみましょう。`find_book_by_title()` や `find_by_author()` にも同様の変更を提案するかもしれません。

</details>

### ボーナスチャレンジ：Copilot CLI でアプリケーションを作る

> 💡 **注意**：この GitHub Skills 演習では Python ではなく **Node.js** を使用します。練習する GitHub Copilot CLI のテクニック（Issue の作成・コードの生成・ターミナルからのコラボレーション）はどの言語にも応用できます。

この演習では、Node.js 電卓アプリを構築しながら GitHub Copilot CLI を使って Issue を作成し、コードを生成し、ターミナルからコラボレーションする方法を学びます。CLI のインストール・テンプレートとエージェントの使用・反復的なコマンドライン駆動の開発を練習します。

##### <img src="../images/github-skills-logo.png" width="28" align="center" /> [「Copilot CLI でアプリケーションを作成する」Skills 演習を始める](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>よくあるミスとトラブルシューティング</strong>（クリックして展開）</summary>

### よくあるミス

| ミス | 起きること | 対処法 |
|---------|--------------|-----|
| 「Review this code」のような漠然としたプロンプトを使う | 具体的な問題を見逃した一般的なフィードバック | 具体的に：「Review for SQL injection, XSS, and auth issues」 |
| コードレビューに `/review` を使わない | 最適化された code-review エージェントを使い損ねる | シグナル対ノイズ比の高い出力に調整された `/review` を使う |
| コンテキストなしに「バグを見つけて」と頼む | Copilot CLI がどのバグを経験しているかわからない | 症状を説明する：「Users report X happens when Y」 |
| フレームワークを指定せずにテストを生成する | 間違った構文やアサーションライブラリを使う可能性がある | 指定する：「Generate tests using Jest」または「using pytest」 |

### トラブルシューティング

**レビューが不完全に見える** - 何を探すべきかをより具体的に指定しましょう：

```bash
copilot

# これの代わりに：
> Review @samples/book-app-project/book_app.py

# こう試しましょう：
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**テストがフレームワークに合わない** - フレームワークを指定しましょう：

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**リファクタリングで動作が変わってしまう** - 動作を保つよう Copilot CLI に依頼しましょう：

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---
