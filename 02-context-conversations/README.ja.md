![Chapter 02: Context and Conversations](images/chapter-header.png)

> **AIがコードベース全体を見渡せたら、どうなるでしょう？1ファイルずつではなく。**

この章では、GitHub Copilot CLI の真の力である「コンテキスト」を解放します。`@` 記法を使ってファイルやディレクトリを参照し、Copilot CLI にコードベースを深く理解させる方法を学びます。セッションをまたいで会話を継続する方法、数日後でも作業を再開する方法、そして単一ファイルのレビューでは見逃してしまうバグをクロスファイル分析で発見する方法も紹介します。

## 🎯 学習目標

この章を終えると、次のことができるようになります：

- `@` 記法を使ってファイル・ディレクトリ・画像を参照できる
- `--resume` や `--continue` を使って前のセッションを再開できる
- [コンテキストウィンドウ](../GLOSSARY.md#context-window)の仕組みを理解できる
- 効果的なマルチターン会話ができる
- マルチプロジェクトワークフロー向けにディレクトリの権限を管理できる

> ⏱️ **目安時間**：約50分（読書20分 + ハンズオン30分）

---

## 🧩 実世界のたとえ：同僚との会話

<img src="images/colleague-context-analogy.png" alt="Context Makes the Difference - Without vs With Context" width="800"/>

*同僚と同じように、Copilot CLI は心を読む力を持っていません。情報を多く提供することで、人間も Copilot も的確なサポートができるようになります！*

バグを同僚に説明するときのことを想像してみてください：

> **コンテキストなし**：「book アプリが動かない。」

> **コンテキストあり**：「`books.py` を見て、特に `find_book_by_title` 関数を確認してほしい。大文字小文字を区別しないマッチングができていないんだ。」

Copilot CLI にコンテキストを提供するには、*`@` 記法*を使って特定のファイルを指示します。

---

# 必須：基本的なコンテキスト

<img src="images/essential-basic-context.png" alt="Glowing code blocks connected by light trails representing how context flows through Copilot CLI conversations" width="800"/>

このセクションでは、コンテキストを効果的に扱うために必要なことをすべて説明します。まずはこの基本をマスターしましょう。

---

## @ 記法

`@` 記号は、プロンプト内のファイルやディレクトリを参照するためのものです。「このファイルを見て」と Copilot CLI に伝える方法です。

> 💡 **注意**：このコースのすべての例では、リポジトリに含まれる `samples/` フォルダを使用しています。すべてのコマンドをそのまま試すことができます。

### 今すぐ試してみよう（セットアップ不要）

コンピューター上の任意のファイルで試すことができます：

```bash
copilot

# 手元にある任意のファイルを指定
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **手元にプロジェクトがない場合は？** 簡単なテストファイルを作成してみましょう：
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### 基本的な @ パターン

| パターン | 動作 | 使用例 |
|---------|------|--------|
| `@file.py` | 単一ファイルを参照 | `Review @samples/book-app-project/books.py` |
| `@folder/` | ディレクトリ内のすべてのファイルを参照 | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | 複数のファイルを参照 | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### 単一ファイルを参照する

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![File Context Demo](images/file-context-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

### 複数ファイルを参照する

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### ディレクトリ全体を参照する

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## クロスファイル・インテリジェンス

これがコンテキストを「超能力」に変える部分です。単一ファイルの分析は便利ですが、クロスファイル分析は変革的です。

<img src="images/cross-file-intelligence.png" alt="Cross-File Intelligence - comparing single-file vs cross-file analysis showing how analyzing files together reveals bugs, data flow, and patterns invisible in isolation" width="800"/>

### デモ：複数ファイルにまたがるバグを発見する

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **上級者向けオプション**：セキュリティ重視のクロスファイル分析を試したい場合は、Python セキュリティサンプルを使ってみましょう：
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![Multi-File Demo](images/multi-file-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

**Copilot CLI が発見すること**：

```
Cross-Module Analysis
=====================

1. DATA FLOW PATTERN
   book_app.py creates BookCollection instance and calls methods
   books.py defines BookCollection class and manages data persistence

   Flow: book_app.py (UI) → books.py (business logic) → data.json (storage)

2. DUPLICATE DISPLAY FUNCTIONS
   book_app.py:9-21    show_books() function
   utils.py:28-36      print_books() function

   Impact: Two nearly identical functions doing the same thing. If you update
   one (like changing the format), you must remember to update the other.

3. INCONSISTENT ERROR HANDLING
   book_app.py handles ValueError from year conversion
   books.py silently returns None/False on errors

   Pattern: No unified approach to error handling across modules
```

**なぜ重要か**：単一ファイルのレビューでは全体像が見えません。クロスファイル分析によってのみ、以下のことが明らかになります：
- **重複コード**：統合すべき箇所
- **データフローのパターン**：コンポーネントがどう連携しているか
- **アーキテクチャ上の問題**：保守性に影響する設計の問題

---

### デモ：60秒でコードベースを把握する

<img src="images/codebase-understanding.png" alt="Split-screen comparison showing manual code review taking 1 hour versus AI-assisted analysis taking 10 seconds" width="800" />

新しいプロジェクトに参加したばかり？Copilot CLI を使って素早く全体を把握しましょう。

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**得られる回答**：
```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**結果**：コードを1時間かけて読む作業が、10秒に圧縮されます。どこに集中すべきかが一目瞭然です。

---

## 実践例

### 例1：コンテキストを使ったコードレビュー

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI がファイル全体の内容を把握し、具体的なフィードバックを返す：
# "Line 49: Case-sensitive comparison may miss books..."
# "Line 29: JSON decode errors are caught but data corruption isn't logged..."

> What about @samples/book-app-project/book_app.py?

# book_app.py をレビューしつつ、books.py のコンテキストも保持したまま
```

### 例2：コードベースを理解する

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI が books.py を読み込み、BookCollection クラスを理解する

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI がディレクトリを走査してサマリーを返す

> How does the app save and load books?

# Copilot CLI がすでに見たコードをたどって答えを出す
```

<details>
<summary>🎬 マルチターン会話の実際の動作を見る！</summary>

![Multi-Turn Demo](images/multi-turn-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

### 例3：マルチファイルのリファクタリング

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI が両方のファイルを見て、重複コードをどうまとめるか提案する
```

---

## セッション管理

セッションは作業中に自動保存されます。前回のセッションを再開して、中断した箇所から続けることができます。

### セッションの自動保存

すべての会話は自動的に保存されます。通常どおり終了するだけでOKです：

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... 作業を進める ...]

> /exit
```

### 直前のセッションを再開する

```bash
# 中断した箇所から続ける
copilot --continue
```

### 特定のセッションを再開する

```bash
# インタラクティブにセッション一覧から選択する
copilot --resume

# または ID を指定して特定のセッションを再開する
copilot --resume=abc123

# またはセッションに付けた名前で再開する
copilot --resume="my book app review"
```

> 💡 **セッション ID の調べ方は？** 暗記する必要はありません。`copilot --resume`（ID なし）を実行すると、過去のセッション一覧（名前・ID・最終アクティブ日時）がインタラクティブに表示されます。選びたいものを選ぶだけです。
>
> **複数のターミナルがある場合は？** 各ターミナルウィンドウは独自のコンテキストを持つ独立したセッションです。3つのターミナルで Copilot CLI を開いていれば、3つの別セッションになります。どのターミナルからでも `--resume` を実行すれば、すべてのセッションを確認できます。`--continue` フラグはまず現在の作業ディレクトリのセッションを探し、なければ最後にアクティブだったセッションを取得します。
>
> **再起動せずにセッションを切り替えるには？** はい、できます。アクティブなセッション内から `/resume` スラッシュコマンドを使いましょう：
> ```
> > /resume
> # 切り替え先のセッション一覧が表示される
> ```

### セッションを整理する

後で見つけやすいように、セッションに意味のある名前を付けましょう。セッションの開始時に名前を付けることも、セッション内でいつでも名前を変更することもできます：

```bash
# セッション開始時に名前を付ける
copilot --name book-app-review

# またはセッション内から現在のセッション名を変更する
copilot

> /rename book-app-review
# セッションが識別しやすい名前に変更される
```

セッションに名前を付けておけば、一覧をスクロールせずに直接名前で再開できます：

```bash
copilot --resume=book-app-review
```

不要なセッションを削除するには、セッション内から `/session delete` を使います：

```bash
copilot

> /session delete            # 現在のセッションを削除
> /session delete abc123     # 特定のセッションを ID で削除
> /session delete-all        # すべてのセッションを削除（要注意！）
```

### コンテキストの確認と管理

ファイルや会話を追加していくと、Copilot CLI の[コンテキストウィンドウ](../GLOSSARY.md#context-window)が埋まっていきます。コントロールを維持するためのコマンドが複数用意されています：

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# 現在のセッションを破棄し（履歴は保存されません）、新しい会話を開始する

> /new
# 現在のセッションを終了し（履歴に保存して検索・再開が可能）、新しい会話を開始する

> /rewind
# タイムラインピッカーを開き、会話の任意の時点にロールバックできる
```

> 💡 **`/clear` と `/new` の使い分け**：`books.py` のレビューをしていて `utils.py` の話に切り替えたい場合は、先に `/new`（または履歴が不要なら `/clear`）を実行しましょう。そうしないと古いトピックのコンテキストが残り、新しいトピックへの回答が混乱する可能性があります。

> 💡 **間違えた、または別のアプローチを試したい場合は？** `/rewind`（または Esc キーを2回押す）を使うと、**タイムラインピッカー**が開き、会話の任意の時点にロールバックできます（直前だけでなく）。間違った方向に進んでしまって、最初からやり直さずに戻りたいときに便利です。

---

### 中断した箇所から再開する

<img src="images/session-persistence-timeline.png" alt="Timeline showing how GitHub Copilot CLI sessions persist across days - start on Monday, resume on Wednesday with full context restored" width="800"/>

*セッションは終了時に自動保存されます。数日後に再開しても、ファイル・問題点・進捗がすべて記憶されています。*

複数日にまたがるワークフローを想像してみましょう：

```bash
# 月曜日：最初から名前を付けて book app review を開始する
copilot --name book-app-review

> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# 修正作業を進める...

> /exit
```

```bash
# 水曜日：名前を指定して中断した箇所から正確に再開する
copilot --resume=book-app-review

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
```

**なぜこれが強力か**：数日後でも、Copilot CLI は以下を覚えています：
- 作業していたファイル
- 番号付きの問題リスト
- すでに対処した問題
- 会話のコンテキスト

再説明不要。ファイルを読み直す必要なし。そのまま作業を続けるだけです。

---

**🎉 基本はマスターしました！** `@` 記法、セッション管理（`--name`/`--continue`/`--resume`/`/rename`）、コンテキストコマンド（`/context`/`/clear`）を使えば、十分な生産性を発揮できます。以下の内容はオプションです。準備ができたら戻ってきましょう。

---

# オプション：さらに深く学ぶ

<img src="images/optional-going-deeper.png" alt="Abstract crystal cave in blue and purple tones representing deeper exploration of context concepts" width="800"/>

これらのトピックは、上記の必須内容の上に積み重なるものです。**興味のある箇所だけ選んで読んでもOKです。[練習](#practice)にスキップしても構いません。**

| 学びたいこと | ジャンプ先 |
|---|---|
| ワイルドカードパターンと上級セッションコマンド | [追加の @ パターンとセッションコマンド](#additional-patterns) |
| 複数プロンプトをまたいだコンテキストの活用 | [コンテキストを活かした会話](#context-aware-conversations) |
| トークン制限と `/compact` | [コンテキストウィンドウを理解する](#understanding-context-windows) |
| 参照するファイルの選び方 | [何を参照すべきかを選ぶ](#choosing-what-to-reference) |
| スクリーンショットやモックアップの分析 | [画像を使って作業する](#working-with-images) |

<details>
<summary><strong>追加の @ パターンとセッションコマンド</strong></summary>
<a id="additional-patterns"></a>

### 追加の @ パターン

上級者向けに、Copilot CLI はワイルドカードパターンと画像参照をサポートしています：

| パターン | 動作 |
|---------|------|
| `@folder/*.py` | フォルダ内のすべての .py ファイル |
| `@**/test_*.py` | 再帰的ワイルドカード：どこにあるテストファイルも検索 |
| `@image.png` | UI レビュー用の画像ファイル |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### セッション情報の確認

```bash
copilot

> /session
# 現在のセッションの詳細とワークスペースのサマリーを表示

> /usage
# セッションの使用状況と統計を表示
```

### セッションを共有する

```bash
copilot

> /share file ./my-session.md
# セッションを Markdown ファイルとしてエクスポート

> /share gist
# セッションを GitHub Gist として作成

> /share html
# セッションを自己完結型のインタラクティブ HTML ファイルとしてエクスポート
# チームメンバーと洗練されたセッションレポートを共有したり、参考として保存するのに便利
```

</details>

<details>
<summary><strong>コンテキストを活かした会話</strong></summary>
<a id="context-aware-conversations"></a>

### コンテキストを活かした会話

互いに積み重なるマルチターン会話こそが、本当の魔法を生み出します。

#### 例：段階的な改善

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods

Copilot CLI: "Here's the class with complete type hints..."
[型付きバージョンを表示]

> Now improve error handling

Copilot CLI: "Building on the typed version, here's improved error handling..."
[バリデーションと適切な例外処理を追加]

> Generate tests for this final version

Copilot CLI: "Based on the class with types and error handling..."
[包括的なテストを生成]
```

各プロンプトが前の作業の上に積み重なっている点に注目してください。これがコンテキストの力です。

</details>

<details>
<summary><strong>コンテキストウィンドウを理解する</strong></summary>
<a id="understanding-context-windows"></a>

### コンテキストウィンドウを理解する

基本編で `/context` と `/clear` はすでに学びました。ここでは、コンテキストウィンドウの仕組みをより深く理解しましょう。

すべての AI には「コンテキストウィンドウ」があります。これは AI が一度に考慮できるテキストの量のことです。

<img src="images/context-window-visualization.png" alt="Context Window Visualization" width="800"/>

*コンテキストウィンドウは机のようなもの：一度に置けるものには限りがあります。ファイル、会話履歴、システムプロンプトがすべてスペースを占有します。*

#### 上限に達したとき

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# ファイルや会話を追加するにつれて増えていく

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# 警告：コンテキストの上限に近づいています

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### `/compact` コマンド

コンテキストが埋まってきたけれど、会話を失いたくない場合、`/compact` が履歴を要約してトークンを解放します：

```bash
copilot

> /compact
# 会話履歴を要約してコンテキストスペースを解放する
# 重要な発見や決定事項は保持される
```

#### コンテキスト効率化のヒント

| 状況 | 操作 | 理由 |
|------|------|------|
| 新しいトピックを開始 | `/clear` | 不要なコンテキストを削除 |
| 間違った方向に進んだ | `/rewind` | 任意の時点にロールバック |
| 会話が長くなった | `/compact` | 履歴を要約してトークンを解放 |
| 特定のファイルが必要 | `@folder/` より `@file.py` | 必要なものだけ読み込む |
| 上限に近づいた | `/new` または `/clear` | 新しいコンテキストで開始 |
| 複数のトピック | トピックごとに `/rename` | 適切なセッションを再開しやすくする |

#### 大規模コードベースのベストプラクティス

1. **具体的に指定する**：`@samples/book-app-project/` より `@samples/book-app-project/books.py`
2. **トピック切り替え時はコンテキストをクリア**：フォーカスを変えるときは `/new` または `/clear`
3. **`/compact` を活用する**：会話を要約してコンテキストを解放
4. **複数のセッションを使う**：機能やトピックごとに1つのセッション

</details>

<details>
<summary><strong>何を参照すべきかを選ぶ</strong></summary>
<a id="choosing-what-to-reference"></a>

### 何を参照すべきかを選ぶ

コンテキストにおいて、ファイルによって価値は異なります。賢く選ぶコツを紹介します：

#### ファイルサイズの考慮

| ファイルサイズ | おおよその[トークン数](../GLOSSARY.md#token) | 戦略 |
|--------------|--------------------------------------|------|
| 小（100行未満） | 約500〜1,500トークン | 自由に参照 |
| 中（100〜500行） | 約1,500〜7,500トークン | 特定のファイルを参照 |
| 大（500行以上） | 7,500トークン以上 | 選択的に、特定のファイルを使用 |
| 非常に大（1000行以上） | 15,000トークン以上 | 分割またはセクションを絞り込むことを検討 |

**具体例：**
- book アプリの Python ファイル4つ合計 ≈ 2,000〜3,000トークン
- 典型的な Python モジュール（200行）≈ 3,000トークン
- Flask API ファイル（400行）≈ 6,000トークン
- package.json ≈ 200〜500トークン
- 短いプロンプト + レスポンス ≈ 500〜1,500トークン

> 💡 **コードのトークン数の簡易見積もり**：コードの行数に約15を掛けると、おおよそのトークン数になります。あくまで目安です。

#### 含めるべきもの、除外すべきもの

**高価値**（含めるべきもの）：
- エントリーポイント（`book_app.py`、`main.py`、`app.py`）
- 質問の対象となる特定のファイル
- ターゲットファイルから直接インポートされるファイル
- 設定ファイル（`requirements.txt`、`pyproject.toml`）
- データモデルやデータクラス

**低価値**（除外を検討すべきもの）：
- 生成ファイル（コンパイル済み出力、バンドルされたアセット）
- Node モジュールやベンダーディレクトリ
- 大きなデータファイルやフィクスチャ
- 質問と関係のないファイル

#### 詳細度のスペクトル

```
大まかに ────────────────────────► 詳細に
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ すべてをスキャン                     └─ 必要なものだけ
        （コンテキストを多く使う）                （コンテキストを節約）
```

**大まかに指定すべき場合**（`@samples/book-app-project/`）：
- コードベースの初期探索
- 多くのファイルにまたがるパターンの発見
- アーキテクチャのレビュー

**詳細に指定すべき場合**（`@samples/book-app-project/books.py`）：
- 特定の問題のデバッグ
- 特定ファイルのコードレビュー
- 単一の関数についての質問

#### 実践例：段階的なコンテキスト読み込み

```bash
copilot

# ステップ1：構造から始める
> @package.json What frameworks does this project use?

# ステップ2：回答に基づいて絞り込む
> @samples/book-app-project/ Show me the project structure

# ステップ3：重要な部分にフォーカス
> @samples/book-app-project/books.py Review the BookCollection class

# ステップ4：必要なときだけ関連ファイルを追加
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

この段階的なアプローチで、コンテキストをフォーカスして効率的に保てます。

</details>

<details>
<summary><strong>画像を使って作業する</strong></summary>
<a id="working-with-images"></a>

### 画像を使って作業する

`@` 記法を使って会話に画像を含めたり、**クリップボードから貼り付け**（Cmd+V / Ctrl+V）たりできます。Copilot CLI はスクリーンショット・モックアップ・図解を分析して、UI デバッグ・デザイン実装・エラー分析を手伝うことができます。

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **詳細を学ぶ**：対応フォーマット・実践的なユースケース・画像とコードを組み合わせるヒントは、[追加のコンテキスト機能](../appendices/additional-context.md#working-with-images)を参照してください。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

コンテキストとセッション管理のスキルを実際に使ってみましょう。

---

## ▶️ 自分でやってみよう

### プロジェクト全体のレビュー

このコースには直接レビューできるサンプルファイルが含まれています。copilot を起動して次のプロンプトを実行してみましょう：

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI は以下のような問題を特定します：
# - 表示関数の重複
# - 入力バリデーションの欠如
# - 一貫しないエラー処理
```

> 💡 **自分のファイルで試したい場合は？** 小さな Python プロジェクトを作成し（`mkdir -p my-project/src`）、.py ファイルをいくつか追加して、`@my-project/src/` でレビューしてみましょう。サンプルコードを作成してほしい場合は copilot に頼むこともできます！

### セッションのワークフロー

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLI がバリデーションのアプローチを提案]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# 後で中断した箇所から再開する
copilot --continue

> Generate tests for the changes we made
```

---

デモを完了したら、以下のバリエーションを試してみましょう：

1. **クロスファイルチャレンジ**：book_app.py と books.py がどのように連携しているか分析する：
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **セッションチャレンジ**：セッションを開始して `/rename my-first-session` で名前を付け、何か作業をして `/exit` で終了してから `copilot --continue` を実行する。何をしていたか覚えているか確認しましょう。

3. **コンテキストチャレンジ**：セッションの途中で `/context` を実行する。何トークン使っていますか？`/compact` を試してもう一度確認しましょう。（`/compact` について詳しくは、「さらに深く学ぶ」の[コンテキストウィンドウを理解する](#understanding-context-windows)を参照してください。）

**自己確認**：`@folder/` がファイルを1つずつ開くより強力な理由を説明できれば、コンテキストを理解できています。

---

## 📝 課題

### メインチャレンジ：データフローを追う

ハンズオン例ではコード品質のレビューと入力バリデーションを扱いました。今度は同じコンテキストスキルを別のタスクに活かし、データがアプリ内をどのように流れるかを追ってみましょう：

1. インタラクティブセッションを開始：`copilot`
2. `books.py` と `book_app.py` を一緒に参照：
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. データファイルを追加のコンテキストとして取り込む：
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. クロスファイルの改善を依頼：
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. セッションの名前を変更：`/rename data-flow-analysis`
6. `/exit` で終了し、`copilot --continue` で再開してデータフローについてフォローアップの質問をする

**成功の基準**：複数ファイルをまたいでデータを追跡し、名前付きセッションを再開し、クロスファイルの提案を得ることができた。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**始め方：**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

再開するには：`copilot --continue`

**役立つコマンド：**
- `@file.py` - 単一ファイルを参照
- `@folder/` - フォルダ内のすべてのファイルを参照（末尾の `/` に注意）
- `/context` - コンテキストの使用量を確認
- `/rename <name>` - セッションに名前を付けて簡単に再開できるようにする

</details>

### ボーナスチャレンジ：コンテキストの上限

1. `@samples/book-app-project/` で book アプリのすべてのファイルを一度に参照する
2. 異なるファイルについてさまざまな詳細な質問をする（`books.py`、`utils.py`、`book_app.py`、`data.json`）
3. `/context` を実行して使用状況を確認。どれだけ早く埋まるか？
4. `/compact` を使ってスペースを確保し、会話を続ける練習をする
5. ファイル参照をより具体的にし（例：フォルダ全体ではなく `@samples/book-app-project/books.py`）、コンテキスト使用量への影響を確認する

---

<details>
<summary>🔧 <strong>よくあるミスとトラブルシューティング</strong>（クリックして展開）</summary>

### よくあるミス

| ミス | 何が起きるか | 対処法 |
|------|------------|--------|
| ファイル名の前に `@` を忘れる | Copilot CLI が「books.py」を通常のテキストとして扱う | ファイルを参照するには `@samples/book-app-project/books.py` のように使う |
| セッションが自動で引き継がれると思い込む | 新しく `copilot` を起動すると前のコンテキストはすべて失われる | `--continue`（最後のセッション）または `--resume`（セッションを選択）を使う |
| 現在のディレクトリ外のファイルを参照する | 「Permission denied」や「File not found」のエラーが出る | `/add-dir /path/to/directory` でアクセスを許可する |
| トピックを切り替えるときに `/clear` を使わない | 古いコンテキストが新しいトピックへの回答を混乱させる | 別のタスクを始める前に `/clear` を実行する |

### トラブルシューティング

**「File not found」エラー** - 正しいディレクトリにいることを確認してください：

```bash
pwd  # 現在のディレクトリを確認
ls   # ファイルを一覧表示

# その後 copilot を起動して相対パスを使用
copilot

> Review @samples/book-app-project/books.py
```

**「Permission denied」** - ディレクトリを許可リストに追加する：

```bash
copilot --add-dir /path/to/directory

# またはセッション内から：
> /add-dir /path/to/directory
```

**コンテキストがすぐに埋まる場合**：
- ファイル参照をより具体的にする
- 異なるトピック間で `/clear` を使う
- 複数のセッションに分けて作業する

</details>

---

# まとめ

## 🔑 重要なポイント

1. **`@` 記法**：ファイル・ディレクトリ・画像のコンテキストを Copilot CLI に提供する
2. **マルチターン会話**：コンテキストが積み重なるにつれ、互いに積み上がっていく
3. **セッションの自動保存**：起動時に `--name` で名前を付け、`--resume=<name>` で名前を指定して再開、または `--continue` で直前のセッションを再開
4. **コンテキストウィンドウには上限あり**：`/clear`・`/compact`・`/context`・`/new`・`/rewind` で管理する
5. **権限フラグ**（`--add-dir`、`--allow-all`）：マルチディレクトリアクセスを制御する。賢く使おう！
6. **画像参照**（`@screenshot.png`）：UI の問題を視覚的にデバッグするのに役立つ

> 📚 **公式ドキュメント**：コンテキスト・セッション・ファイル操作の完全なリファレンスは [Use Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli) を参照してください。

> 📋 **クイックリファレンス**：コマンドとショートカットの完全一覧は [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)を参照してください。

---

## ➡️ 次のステップ

Copilot CLI にコンテキストを与える方法を習得しました。次は実際の開発タスクに活かしていきましょう。今学んだコンテキストのテクニック（ファイル参照・クロスファイル分析・セッション管理）は、次の章の強力なワークフローの土台となります。

**[Chapter 03: Development Workflows](../03-development-workflows/README.md)** では、次のことを学びます：

- コードレビューのワークフロー
- リファクタリングのパターン
- デバッグの支援
- テストの生成
- Git との連携

---

**[← Chapter 01 に戻る](../01-setup-and-first-steps/README.md)** | **[Chapter 03 に進む →](../03-development-workflows/README.md)**
