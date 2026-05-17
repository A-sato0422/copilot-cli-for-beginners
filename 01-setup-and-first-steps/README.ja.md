![Chapter 01: First Steps](images/chapter-header.png)

> **AIがバグを瞬時に発見し、難解なコードを説明し、動くスクリプトを生成する様子を体験しましょう。そして GitHub Copilot CLI の3つの使い方を学びます。**

この章からいよいよ魔法が始まります！なぜ開発者たちが GitHub Copilot CLI を「いつでも呼び出せるシニアエンジニア」と表現するのか、実際に体験しましょう。AIがセキュリティバグを数秒で発見し、複雑なコードをわかりやすい日本語で説明し、動くスクリプトを即座に生成するのを目の当たりにします。そして、3つのインタラクションモード（Interactive・Plan・Programmatic）をマスターして、どのタスクにどのモードを使えばいいかを習得しましょう。

> ⚠️ **前提条件**: 先に **[Chapter 00: Quick Start](../00-quick-start/README.md)** を完了してください。以下のデモを実行する前に、GitHub Copilot CLI のインストールと認証が必要です。

## 🎯 学習目標

この章を終えると、次のことができるようになります：

- ハンズオンデモを通じて、GitHub Copilot CLI が生産性をどう向上させるかを実感する
- タスクに応じて適切なモード（Interactive・Plan・Programmatic）を選択できる
- スラッシュコマンドを使ってセッションを制御できる

> ⏱️ **目安時間**：約45分（読書15分 + ハンズオン30分）

---

# はじめての Copilot CLI 体験

<img src="images/first-copilot-experience.png" alt="モニターにコードが表示されたデスクに座る開発者と、AIアシストを表す光の粒子" width="800"/>

まずは Copilot CLI が何をできるのか、実際に試してみましょう。

---

## まずは慣れる：最初のプロンプト

インパクトのあるデモに入る前に、今すぐ試せるシンプルなプロンプトから始めましょう。**コードリポジトリは不要**です！ターミナルを開いて Copilot CLI を起動してください：

```bash
copilot
```

以下の初心者向けプロンプトを試してみましょう：

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

Python を使っていなくても大丈夫！お好みの言語について質問してみましょう。

どれほど自然に使えるかに気づくはずです。同僚に話しかけるような感覚で質問するだけです。探索が終わったら、`/exit` と入力してセッションを終了します。

**重要な気づき**：GitHub Copilot CLI は会話形式です。特別な構文を覚えなくてもすぐに使い始められます。

## 実際に動かしてみよう

なぜ開発者たちが「いつでも呼び出せるシニアエンジニア」と呼ぶのか、体験してみましょう。

> 📖 **サンプルの読み方**: `>` で始まる行は、Copilot CLI のインタラクティブセッション内で入力するプロンプトです。`>` のない行は、ターミナルで実行するシェルコマンドです。

> 💡 **サンプル出力について**: このコースで示されているサンプル出力はあくまで例示です。Copilot CLI の回答は毎回異なるため、文言・書式・詳細度はあなたの環境と異なります。正確なテキストではなく、*返ってくる情報の種類*に注目してください。

### デモ1：数秒でコードレビュー

このコースには意図的なコード品質の問題が含まれたサンプルファイルが含まれています。ローカルマシンで作業していてまだリポジトリをクローンしていない場合は、以下の `git clone` コマンドを実行し、`copilot-cli-for-beginners` フォルダに移動してから `copilot` コマンドを実行してください。

```bash
# ローカルで作業する場合、まだクローンしていなければ実行
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Copilot を起動
copilot
```

Copilot CLI のインタラクティブセッションに入ったら、以下を実行します：

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **`@` 記号は何に使う？** `@` 記号は Copilot CLI にファイルを読み込むよう指示します。詳細は Chapter 02 で学びます。今はコマンドをそのままコピーしてください。

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![Code Review Demo](images/code-review-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

**まとめ**：プロ品質のコードレビューが数秒で完了。手動レビューなら…もっと時間がかかりますよね！

---

### デモ2：難解なコードを解説させる

「このコードは何をしているんだろう？」と悩んだことはありませんか？Copilot CLI セッション内でこれを試してみましょう：

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![Explain Code Demo](images/explain-code-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

**何が起きるか**：（出力はあなたの環境で異なります）Copilot CLI がファイルを読み込み、コードを理解して、わかりやすい言葉で説明します。

```
This is a book collection management module using Python dataclasses.

Think of it like a digital bookshelf:
- Book is a dataclass - a simple way to store book information (title, author, year, read status)
- BookCollection manages the entire collection and handles saving/loading

Key components:

1. @dataclass decorator (line 8)
   - Automatically creates __init__, __repr__, etc.
   - Clean way to define data structures in Python

2. BookCollection class (line 16)
   - Maintains a list of Book objects
   - Handles persistence with JSON file I/O
   - load_books() reads from data.json
   - save_books() writes to data.json using asdict()

3. Book operations:
   - add_book() - creates and saves new books
   - find_book_by_title() - searches collection
   - mark_as_read() - updates read status
   - find_by_author() - filters by author name

Common pattern: Read from JSON → Work with Python objects → Write back to JSON
```

**まとめ**：複雑なコードを、根気強いメンターが教えてくれるように解説してくれます。

---

### デモ3：動くコードをすぐに生成

15分かけて検索しなければならないような関数も、セッション内で一発生成できます：

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 実際の動作を見る！</summary>

![Generate Code Demo](images/generate-code-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

**何が起きるか**：コピー＆ペーストしてすぐ動かせる完全な関数が数秒で生成されます。

探索が終わったらセッションを終了しましょう：

```
> /exit
```

**まとめ**：即座に結果が得られ、しかも1つの継続セッションの中でずっと作業できました。

---

# モードとコマンド

<img src="images/modes-and-commands.png" alt="Copilot CLI のモードとコマンドを表す、光るスクリーンやダイヤルが並んだSF風のコントロールパネル" width="800"/>

Copilot CLI が何をできるかを体験しました。次は、その機能を*効果的に使う方法*を理解しましょう。3つのインタラクションモードを使い分けることが鍵です。

> 💡 **補足**: Copilot CLI には、入力を待たずにタスクを進める **Autopilot** モードもあります。強力ですが、全権限の付与が必要でプレミアムリクエストを自律的に消費します。このコースでは以下の3つのモードに集中します。基本に慣れたら Autopilot も紹介します。

---

## 🧩 実世界のたとえ：外食

GitHub Copilot CLI の使い方を、外食に例えて考えてみましょう。計画から注文まで、状況ごとに適したアプローチがあります：

| モード | 外食のたとえ | 使うべき場面 |
|------|----------------|-------------|
| **Plan** | レストランへの GPS ルート案内 | 複雑なタスク - ルートを確認し、立ち寄り箇所を確認し、計画に合意してから出発する |
| **Interactive** | ウェイターとの会話 | 探索と試行錯誤 - 質問して、カスタマイズして、リアルタイムでフィードバックをもらう |
| **Programmatic** | ドライブスルーでの注文 | 素早く具体的なタスク - 環境から離れずに、すぐに結果を得る |

外食と同じように、それぞれのアプローチがいつ適しているかは自然と身につきます。

<img src="images/ordering-food-analogy.png" alt="GitHub Copilot CLI の3つの使い方 - Plan Mode（GPS ルート）、Interactive Mode（ウェイターとの会話）、Programmatic Mode（ドライブスルー）" width="800"/>

*タスクに応じてモードを選ぼう：Plan は事前に計画を立てるとき、Interactive は対話しながら作業するとき、Programmatic はすぐに結果が欲しいとき*

### どのモードから始めればいい？

**Interactive モードから始めましょう。**
- 実験しながら追加の質問ができる
- 会話を通じて自然にコンテキストが積み上がる
- `/clear` でミスを簡単に取り消せる

慣れてきたら試してみましょう：
- **Programmatic モード**（`copilot -p "<プロンプト>"`）：素早いワンオフの質問に
- **Plan モード**（`/plan`）：コーディング前により詳細な計画を立てたいとき

---

## 3つのモード

### モード1：Interactive モード（まずここから）

<img src="images/interactive-mode.png" alt="Interactive Mode - 質問に答えたり注文を調整したりできるウェイターと話す様子" width="250"/>

**向いている場面**：探索・試行錯誤・複数ターンの会話。質問に答え、フィードバックを受け取り、注文をその場で調整してくれるウェイターと話す感覚です。

インタラクティブセッションの開始：

```bash
copilot
```

ここまで見てきたように、自然に入力できるプロンプトが表示されます。利用可能なコマンドを確認するには：

```
> /help
```

**重要な気づき**：Interactive モードはコンテキストを保持します。各メッセージが前のメッセージの上に積み重なり、本物の会話のように続きます。

#### Interactive モードの例

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

各プロンプトが前の回答の上に積み重なっていることに注目してください。毎回ゼロから始めるのではなく、会話を続けているのです。

---

### モード2：Plan モード

<img src="images/plan-mode.png" alt="Plan Mode - GPS でドライブルートを事前に計画する様子" width="250"/>

**向いている場面**：実行前にアプローチを確認したい複雑なタスク。旅行前に GPS でルートを計画するイメージです。

Plan モードを使うと、コードを書く前にステップバイステップの計画を作成できます。`/plan` コマンドを使うか、**Shift+Tab** を押して Plan モードに切り替えます：

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

> 💡 **ヒント**：**Shift+Tab** でモードを切り替えられます（Interactive → Plan → Autopilot）。インタラクティブセッション中にいつでもコマンドを入力せずにモードを切り替えられます。

`--plan` フラグを使って最初から Plan モードで起動することもできます：

```bash
copilot --plan
```

**Plan モードの出力例**（実際の出力は異なります）：

```
📋 Implementation Plan

Step 1: Update the command handler in book_app.py
  - Add new elif branch for "mark" command
  - Create handle_mark_as_read() function

Step 2: Implement the handler function
  - Prompt user for book title
  - Call collection.mark_as_read(title)
  - Display success/failure message

Step 3: Update help text
  - Add "mark" to available commands list
  - Document the command usage

Step 4: Test the flow
  - Add a book
  - Mark it as read
  - Verify status changes in list output

Proceed with implementation? [Y/n]
```

**重要な気づき**：Plan モードでは、コードが書かれる前にアプローチを確認・修正できます。計画が完成したら、後で参照できるようファイルに保存するよう指示することもできます。例えば「Save this plan to `mark_as_read_plan.md`」と伝えると、計画の詳細を含む Markdown ファイルが作成されます。

> 💡 **もっと複雑なことを試したい？** `/plan Add search and filter capabilities to the book app` を試してみましょう。Plan モードはシンプルな機能からフルアプリケーションまでスケールします。

> 📚 **Autopilot モードについて**：Shift+Tab の3つ目のモードが **Autopilot** です。Autopilot モードでは、Copilot が各ステップで入力を待たずに計画全体を実行します。まるで「終わったら教えて」と同僚にタスクを任せる感覚です。通常のワークフローは「計画 → 承認 → Autopilot」の順で、まず計画を上手に書けるようになることが大切です。`copilot --autopilot` で直接 Autopilot を起動することもできます。まずは Interactive と Plan モードに慣れてから、[公式ドキュメント](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot)を参照しましょう。

---

### モード3：Programmatic モード

<img src="images/programmatic-mode.png" alt="Programmatic Mode - ウェイターと話さずに素早く注文するドライブスルーの様子" width="250"/>

**向いている場面**：自動化・スクリプト・CI/CD・単発コマンド。ウェイターと話さずに素早く注文するドライブスルーのイメージです。

インタラクションが不要な単発コマンドには `-p` フラグを使います：

```bash
# コードを生成する
copilot -p "Write a function that checks if a number is even or odd"

# 簡単なヘルプを得る
copilot -p "How do I read a JSON file in Python?"
```

**重要な気づき**：Programmatic モードはすぐに回答して終了します。会話はなく、入力 → 出力のみです。

<details>
<summary>📚 <strong>さらに進む：スクリプトでの Programmatic モード活用</strong>（クリックして展開）</summary>

慣れてきたら、シェルスクリプトで `-p` を活用できます：

```bash
#!/bin/bash
# コミットメッセージを自動生成する
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# ファイルをレビューする
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **`--allow-all` について**：このフラグはすべての権限確認をスキップし、ファイルの読み込み・コマンドの実行・URL へのアクセスを確認なしで行えるようにします。インタラクティブセッションがないため、Programmatic モード（`-p`）では必要になります。自分で書いたプロンプトに対して、信頼できるディレクトリ内でのみ使用してください。信頼できない入力や重要なディレクトリでは絶対に使用しないでください。

</details>

---

## 重要なスラッシュコマンド

Copilot CLI を使い始める上で、最初に覚えておくと便利なコマンドです：

| コマンド | 何をするか | 使うタイミング |
|---------|--------------|-------------|
| `/ask` | 会話履歴に影響しないクイック質問 | 現在のタスクを妨げずに素早く答えが欲しいとき |
| `/clear` | 会話をクリアして新しく始める | トピックを切り替えるとき |
| `/help` | 利用可能なコマンドをすべて表示 | コマンドを忘れたとき |
| `/model` | AI モデルを表示または切り替える | AI モデルを変更したいとき |
| `/plan` | コーディング前に作業計画を立てる | より複雑な機能に取り組むとき |
| `/research` | GitHub とウェブソースを使った詳細調査 | コーディング前にトピックを調査したいとき |
| `/exit` | セッションを終了する | 作業を終えたとき |

> 💡 **`/ask` と通常チャットの違い**：通常、送信したメッセージはすべて進行中の会話の一部となり、以降の回答に影響します。`/ask` は「オフレコ」のショートカットで、`/ask What does YAML mean?` のような一回限りの質問をセッションのコンテキストを汚染せずに行えます。

> 💡 **Tab補完**：スラッシュコマンドを入力中に **Tab** を押すと、コマンド名を自動補完したり、利用可能なサブコマンドや引数を順番に表示できます。コマンドの正確な名前が思い出せないときに便利です。

以上でスタート編は完了です！慣れてきたら、追加コマンドも探索してみましょう。

> 📚 **公式ドキュメント**: コマンドとフラグの完全なリストは [CLI コマンドリファレンス](https://docs.github.com/copilot/reference/cli-command-reference)を参照してください。

<details>
<summary>📚 <strong>追加コマンド一覧</strong>（クリックして展開）</summary>

> 💡 上記の基本コマンドだけで日常の多くの作業をカバーできます。より深く探索したいときのためのリファレンスです。

### エージェント環境

| コマンド | 何をするか |
|---------|--------------|
| `/agent` | 利用可能なエージェントを確認して選択する |
| `/env` | 読み込まれた環境の詳細（アクティブな instructions・MCP サーバー・スキル・エージェント・プラグイン）を表示する |
| `/init` | リポジトリの Copilot instructions を初期化する |
| `/mcp` | MCP サーバーの設定を管理する |
| `/skills` | 拡張機能のためのスキルを管理する |

> 💡 エージェントは [Chapter 04](../04-agents-custom-instructions/README.md)、スキルは [Chapter 05](../05-skills/README.md)、MCP サーバーは [Chapter 06](../06-mcp-servers/README.md) で解説します。

### モデルとサブエージェント

| コマンド | 何をするか |
|---------|--------------|
| `/delegate` | タスクを GitHub Copilot クラウドエージェントに委任する |
| `/fleet` | 複雑なタスクを並列サブタスクに分割して高速化する |
| `/model` | AI モデルを表示または切り替える |
| `/tasks` | バックグラウンドのサブエージェントとデタッチされたシェルセッションを確認する |

### コード

| コマンド | 何をするか |
|---------|--------------|
| `/diff` | 現在のディレクトリの変更を確認する |
| `/pr` | 現在のブランチのプルリクエストを操作する |
| `/research` | GitHub とウェブソースを使って詳細調査を実行する |
| `/review` | コードレビューエージェントを実行して変更を分析する |
| `/terminal-setup` | 複数行入力のサポートを有効化する（shift+enter と ctrl+enter） |

### 権限

| コマンド | 何をするか |
|---------|--------------|
| `/add-dir <directory>` | 許可リストにディレクトリを追加する |
| `/allow-all [on\|off\|show]` | すべての権限確認を自動承認する。`on` で有効化、`off` で無効化、`show` で現在の状態を確認 |
| `/yolo` | `/allow-all on` のクイックエイリアス。すべての権限確認を自動承認する |
| `/cwd`, `/cd [directory]` | 作業ディレクトリを表示または変更する |
| `/list-dirs` | 許可済みディレクトリをすべて表示する |

> ⚠️ **注意して使用**：`/allow-all` と `/yolo` は確認プロンプトをスキップします。信頼できるプロジェクトには便利ですが、信頼できないコードでは注意してください。

### セッション

| コマンド | 何をするか |
|---------|--------------|
| `/clear` | 現在のセッションを破棄（履歴は保存されない）して新しい会話を開始する |
| `/compact` | コンテキストの使用量を減らすために会話を要約する |
| `/context` | コンテキストウィンドウのトークン使用量と可視化を表示する |
| `/keep-alive` | Copilot CLI が動作中にシステムのスリープを防ぐ。ノートPCでの長時間タスクに便利 |
| `/new` | 現在のセッションを終了（検索・再開のために履歴に保存）して新しい会話を開始する |
| `/resume` | 別のセッションに切り替える（セッション ID または名前を指定可能） |
| `/rename` | 現在のセッションの名前を変更する（名前を省略すると自動生成） |
| `/rewind` | タイムラインピッカーを開いて会話の任意の以前のポイントに戻る |
| `/usage` | セッションの使用量メトリクスと統計を表示する |
| `/session` | セッション情報とワークスペースの概要を表示する。`/session delete`・`/session delete <id>`・`/session delete-all` でセッションを削除できる |
| `/share` | セッションを Markdown ファイル・GitHub Gist・スタンドアロン HTML ファイルとしてエクスポートする |

### 表示

| コマンド | 何をするか |
|---------|--------------|
| `/statusline`（または `/footer`）| セッション下部のステータスバーに表示する項目をカスタマイズする（ディレクトリ・ブランチ・進捗・コンテキストウィンドウ・クォータ） |
| `/theme` | ターミナルのテーマを表示または設定する |

### ヘルプとフィードバック

| コマンド | 何をするか |
|---------|--------------|
| `/changelog` | CLI バージョンの変更履歴を表示する |
| `/feedback` | GitHub にフィードバックを送信する |
| `/help` | 利用可能なコマンドをすべて表示する |

### クイックシェルコマンド

`!` をプレフィックスとして付けることで、AI を介さずにシェルコマンドを直接実行できます：

```bash
copilot

> !git status
# git status を AI をバイパスして直接実行

> !python -m pytest tests/
# pytest を直接実行
```

### モデルの切り替え

Copilot CLI は OpenAI・Anthropic・Google などの複数の AI モデルをサポートしています。利用可能なモデルはサブスクリプションレベルと地域によって異なります。`/model` を使ってオプションを確認し、切り替えましょう：

```bash
copilot
> /model

# 利用可能なモデルを表示して選択できる。Sonnet 4.5 を選んでみましょう。
```

> 💡 **ヒント**：モデルによって消費される「プレミアムリクエスト」の量が異なります。**1x** とマークされたモデル（Claude Sonnet 4.5 など）は優れたデフォルトです。高性能でかつ効率的です。倍率の高いモデルはプレミアムリクエストのクォータを速く消費するので、本当に必要なときのために取っておきましょう。

> 💡 **どのモデルを選べばいいかわからない？** モデルピッカーから **`Auto`** を選択すると、Copilot がセッションごとに最適なモデルを自動的に選んでくれます。モデル選択を考えたくない初心者には最適なデフォルト設定です。

</details>

---

# 練習

<img src="../images/practice.png" alt="モニターにコードが表示され、ランプ・コーヒーカップ・ヘッドフォンが置かれたハンズオン準備の整った暖かいデスク" width="800"/>

学んだことを実際に試してみましょう。

---

## ▶️ 自分で試してみよう

### インタラクティブ探索

Copilot を起動して、フォローアッププロンプトを使ってブックアプリを段階的に改善しましょう：

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### 機能を計画する

`/plan` を使って、コードを書く前に Copilot CLI に実装をマッピングさせましょう：

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# 計画を確認する
# 承認または修正する
# ステップバイステップで実装されるのを見る
```

### Programmatic モードで自動化

`-p` フラグを使えば、インタラクティブモードに入らずにターミナルから直接 Copilot CLI を実行できます。以下のスクリプトをリポジトリルートからターミナル（Copilot の外）にコピーして貼り付け、ブックアプリのすべての Python ファイルをレビューしましょう。

```bash
# ブックアプリのすべての Python ファイルをレビューする
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows)：**

```powershell
# ブックアプリのすべての Python ファイルをレビューする
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

デモを完了したら、以下のバリエーションも試してみましょう：

1. **インタラクティブチャレンジ**：`copilot` を起動してブックアプリを探索する。`@samples/book-app-project/books.py` について質問し、改善を3回連続でリクエストしてみましょう。

2. **Plan モードチャレンジ**：`/plan Add rating and review features to the book app` を実行する。計画をよく読んで、理にかなっているか確認しましょう。

3. **Programmatic チャレンジ**：`copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"` を実行する。初回で上手くいきましたか？

---

## 💡 ヒント：ウェブやモバイルから CLI セッションを操作する

GitHub Copilot CLI は**リモートセッション**をサポートしており、実際にターミナルの前にいなくても、ウェブブラウザ（デスクトップまたはモバイル）や GitHub Mobile アプリから実行中の CLI セッションを監視・操作できます。

`--remote` フラグでリモートセッションを開始します：

```bash
copilot --remote
```

Copilot CLI がリンクを表示し、QR コードへのアクセスを提供します。スマートフォンやデスクトップのブラウザタブでリンクを開くと、セッションをリアルタイムで確認し、フォローアッププロンプトの送信・計画の確認・エージェントのリモート操作ができます。セッションはユーザー固有なので、自分の Copilot CLI セッションにのみアクセスできます。

アクティブなセッション内からいつでもリモートアクセスを有効にすることもできます：

```
> /remote
```

リモートセッションの詳細は [Copilot CLI ドキュメント](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely)を参照してください。

---

## 📝 課題

### メインチャレンジ：ブックアプリのユーティリティを改善する

ハンズオンの例では `book_app.py` のレビューとリファクタリングに取り組みました。今度は別のファイル `utils.py` で同じスキルを練習しましょう：

1. インタラクティブセッションを開始：`copilot`
2. Copilot CLI にファイルを要約させる：「Summarize @samples/book-app-project/utils.py and explain what each function in this file does」
3. 入力バリデーションを追加させる：「Add validation to `get_user_choice()` so it handles empty input and non-numeric entries」
4. エラーハンドリングを改善させる：「What happens if `get_book_details()` receives an empty string for the title? Add guards for that.」
5. ドキュメント文字列を追加させる：「Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values」
6. プロンプト間でコンテキストがどう引き継がれるかを観察する。各改善は前の改善の上に積み重なります
7. `/exit` で終了する

**達成基準**：複数ターンの会話を通じて構築された、入力バリデーション・エラーハンドリング・ドキュメント文字列が追加された改善版 `utils.py` ができているはずです。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**試してみるサンプルプロンプト：**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**よくある問題：**
- Copilot CLI が確認の質問をしてきたら、自然に答えるだけでOK
- コンテキストは引き継がれるので、各プロンプトは前の続きから始まります
- やり直したい場合は `/clear` を使いましょう

</details>

### ボーナスチャレンジ：モードを比較する

例では検索機能に `/plan` を、バッチレビューに `-p` を使いました。今度は1つの新しいタスクで3つのモードすべてを試してみましょう：`BookCollection` クラスに `list_by_year()` メソッドを追加する。

1. **Interactive**：`copilot` → メソッドの設計と構築をステップバイステップで依頼する
2. **Plan**：`/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programmatic**：`copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**振り返り**：どのモードが一番自然に感じられましたか？それぞれをいつ使いますか？

---

<details>
<summary>🔧 <strong>よくあるミスとトラブルシューティング</strong>（クリックして展開）</summary>

### よくあるミス

| ミス | 何が起きるか | 対処法 |
|---------|--------------|-----|
| `/exit` の代わりに `exit` と入力する | Copilot CLI が「exit」をコマンドではなくプロンプトとして扱う | スラッシュコマンドは必ず `/` から始める |
| 複数ターンの会話に `-p` を使う | 各 `-p` の呼び出しは独立していて、以前の呼び出しを記憶していない | 文脈を積み重ねる会話にはインタラクティブモード（`copilot`）を使う |
| `$` や `!` を含むプロンプトをクォートで囲まない | Copilot CLI が見る前にシェルが特殊文字を解釈してしまう | プロンプトをクォートで囲む：`copilot -p "What does $HOME mean?"` |
| 実行中のタスクをキャンセルするために Esc を1回押す | 誤動作防止のため、Esc1回では処理中の作業はキャンセルされない | Copilot CLI が処理中のときは **Esc を2回** 押してキャンセル |

### トラブルシューティング

**「Model not available」**：サブスクリプションにすべてのモデルが含まれていない可能性があります。`/model` を使って利用可能なモデルを確認してください。

**「Context too long」**：会話でコンテキストウィンドウをすべて使い切っています。`/clear` でリセットするか、新しいセッションを開始してください。

**「Rate limit exceeded」**：数分待ってから再試行してください。バッチ操作には間隔を置いた Programmatic モードの使用を検討してください。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **Interactive モード**は探索と試行錯誤向け - コンテキストが引き継がれます。その時点まで話した内容を覚えている人との会話のようなものです。
2. **Plan モード**は通常、より複雑なタスク向けです。実装前に確認しましょう。
3. **Programmatic モード**は自動化向けです。インタラクションは不要です。
4. **基本コマンド**（`/ask`・`/help`・`/clear`・`/plan`・`/research`・`/model`・`/exit`）で日常の大半の用途をカバーできます。

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)を参照してください。

---

## ➡️ 次のステップ

3つのモードを理解したところで、次は Copilot CLI にコードのコンテキストを伝える方法を学びましょう。

**[Chapter 02: Context and Conversations](../02-context-conversations/README.md)** では以下を学びます：

- ファイルやディレクトリを参照する `@` 構文
- `--resume` と `--continue` によるセッション管理
- コンテキスト管理が Copilot CLI を本当に強力にする仕組み

---

**[← コースホームに戻る](../README.md)** | **[Chapter 02 へ進む →](../02-context-conversations/README.md)**
