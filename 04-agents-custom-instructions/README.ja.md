![Chapter 04: Agents and Custom Instructions](images/chapter-header.png)

> **Pythonコードレビュアー、テスト専門家、セキュリティレビュアーを…1つのツールに雇えたら？**

Chapter 03では、コードレビュー・リファクタリング・デバッグ・テスト生成・git連携という重要なワークフローをマスターしました。これだけでも GitHub Copilot CLI をフル活用できますが、さらに先へ進みましょう。

これまでは Copilot CLI を汎用アシスタントとして使ってきました。エージェントを使うと、型ヒントやPEP 8を強制するコードレビュアー、pytestケースを書くテストヘルパーなど、特定のペルソナと組み込み基準を持たせることができます。同じプロンプトでも、専門的な指示を持つエージェントで処理すると、明らかに良い結果が得られることを実感できるはずです。

## 🎯 学習目標

この章を終えると、次のことができるようになります：

- 組み込みエージェントを使う：Plan（`/plan`）、Code-review（`/review`）、そして自動エージェント（Explore、Task）を理解する
- エージェントファイル（`.agent.md`）を使って専門エージェントを作成する
- ドメイン固有のタスクにエージェントを活用する
- `/agent` と `--agent` を使ってエージェントを切り替える
- プロジェクト固有の基準のためにカスタム指示ファイルを書く

> ⏱️ **目安時間**：約55分（読書20分 + ハンズオン35分）

---

## 🧩 現実世界のアナロジー：専門家を雇う

家の修理が必要なとき、「なんでも屋さん」に頼まないですよね。専門家を呼びます：

| 問題 | 専門家 | 理由 |
|------|--------|------|
| 水漏れ | 配管工 | 配管の規格に詳しく、専用工具を持っている |
| 配線工事 | 電気工事士 | 安全基準を理解し、法令に準拠している |
| 屋根の張り替え | 屋根職人 | 素材や地域の気候条件を把握している |

エージェントも同じです。汎用AIの代わりに、特定タスクに集中して正しい手順を知っているエージェントを使いましょう。指示を一度設定すれば、コードレビュー・テスト・セキュリティ・ドキュメントなど、その専門スキルが必要なときにいつでも再利用できます。

<img src="images/hiring-specialists-analogy.png" alt="Hiring Specialists Analogy - Just as you call specialized tradespeople for house repairs, AI agents are specialized for specific tasks like code review, testing, security, and documentation" width="800" />

---

# エージェントを使う

組み込みエージェントとカスタムエージェントをすぐに始めましょう。

---

## *エージェント初めて？* ここから始めよう！
エージェントを使ったことがない、作ったこともない？このコースで始めるために必要なことをまとめました。

1. **今すぐ*組み込み*エージェントを試そう：**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   これでPlanエージェントが起動し、ステップごとの実装計画を作成します。

2. **カスタムエージェントの例を見てみよう：** エージェントの指示を定義するのは簡単です。用意されている [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) ファイルを見て、パターンを確認してください。

3. **核心概念を理解しよう：** エージェントは、ジェネラリストではなくスペシャリストに相談するようなものです。「フロントエンドエージェント」はアクセシビリティとコンポーネントパターンに自動的に集中します。エージェントの指示に既に記載されているため、毎回リマインドする必要がありません。


## 組み込みエージェント

**Chapter 03 開発ワークフローで、既にいくつかの組み込みエージェントを使っていました！**
<br>`/plan` と `/review` は実は組み込みエージェントです。裏側で何が起きているのかがわかりましたね。完全なリストはこちら：

| エージェント | 起動方法 | できること |
|------------|---------|-----------|
| **Plan** | `/plan` または `Shift+Tab`（モード切替） | コーディング前にステップごとの実装計画を作成する |
| **Code-review** | `/review` | ステージ済み・未ステージの変更を、集中した実行可能なフィードバックでレビューする |
| **Init** | `/init` | プロジェクト設定ファイル（指示・エージェント）を生成する |
| **Explore** | *自動* | コードベースを探索・分析するよう Copilot に依頼したときに内部で使われる |
| **Task** | *自動* | テスト・ビルド・リント・依存関係のインストールなどのコマンドを実行する |

<br>

**組み込みエージェントの動作例** - Plan、Code-review、Explore、Task の起動例

```bash
copilot

# Planエージェントを起動して実装計画を作成する
> /plan Add input validation for book year in the book app

# Code-reviewエージェントで変更をレビューする
> /review

# ExploreエージェントとTaskエージェントは関連する場面で自動的に起動される：
> Run the test suite        # Taskエージェントが使われる

> Explore how book data is loaded    # Exploreエージェントが使われる
```

Taskエージェントについては？Taskエージェントは裏側で何が起きているかを管理・追跡し、わかりやすく整理された形式でレポートします：

| 結果 | 表示内容 |
|------|---------|
| ✅ **成功** | 簡潔なサマリー（例：「全247テスト成功」「ビルド成功」） |
| ❌ **失敗** | スタックトレース・コンパイラエラー・詳細ログを含む完全な出力 |


> 📚 **公式ドキュメント**: [GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Copilot CLI にエージェントを追加する

自分だけのエージェントをワークフローに追加するのは簡単です！一度定義すれば、あとは指示するだけ！

<img src="images/using-agents.png" alt="Four colorful AI robots standing together, each with different tools representing specialized agent capabilities" width="800"/>

## 🗂️ エージェントを追加する 

エージェントファイルは `.agent.md` 拡張子を持つマークダウンファイルです。2つのパートで構成されています：YAMLフロントマター（メタデータ）とマークダウン指示です。

> 💡 **YAMLフロントマターって何？** ファイルの先頭にある小さな設定ブロックで、`---` マーカーで囲まれています。YAMLは `key: value` のペアです。残りの部分は通常のマークダウンです。

最小限のエージェントの例：

```markdown
---
name: my-reviewer
description: Code reviewer focused on bugs and security issues
---

# Code Reviewer

You are a code reviewer focused on finding bugs and security issues.

When reviewing code, always check for:
- SQL injection vulnerabilities
- Missing error handling
- Hardcoded secrets
```

> 💡 **必須 vs 任意**: `description` フィールドは必須です。`name`・`tools`・`model` などの他のフィールドは任意です。

## エージェントファイルの置き場所

| 場所 | スコープ | 最適な用途 |
|------|---------|-----------|
| `.github/agents/` | プロジェクト固有 | プロジェクトの規約を持つチーム共有エージェント |
| `~/.copilot/agents/` | グローバル（全プロジェクト） | どこでも使う個人エージェント |

**このプロジェクトには [.github/agents/](../.github/agents/) フォルダにサンプルエージェントファイルが含まれています**。自分で書くこともできますし、既に用意されているものをカスタマイズすることもできます。

<details>
<summary>📂 このコースのサンプルエージェントを見る</summary>

| ファイル | 説明 |
|---------|------|
| `hello-world.agent.md` | 最小限の例 - ここから始めよう |
| `python-reviewer.agent.md` | Pythonコード品質レビュアー |
| `pytest-helper.agent.md` | pytestテスト専門家 |

```bash
# または個人エージェントフォルダにコピーする（全プロジェクトで利用可能）
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

コミュニティエージェントは [github/awesome-copilot](https://github.com/github/awesome-copilot) を参照してください。

</details>


## 🚀 カスタムエージェントを使う2つの方法

### インタラクティブモード
インタラクティブモードの中で、`/agent` を使ってエージェントを一覧表示し、使用するエージェントを選択します。
エージェントを選択して、そのエージェントとの会話を続けます。

```bash
copilot
> /agent
```

別のエージェントに切り替えるか、デフォルトモードに戻るには、再度 `/agent` コマンドを使います。

### プログラマティックモード

エージェントを指定して新しいセッションを直接起動します。

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **エージェントの切り替え**: `/agent` または `--agent` を使えばいつでも別のエージェントに切り替えられます。標準の Copilot CLI 体験に戻るには、`/agent` を使って **エージェントなし** を選択します。

---

# エージェントをもっと深く知る

<img src="images/creating-custom-agents.png" alt="Robot being assembled on a workbench surrounded by components and tools representing custom agent creation" width="800"/>

> 💡 **このセクションはオプションです。** 組み込みエージェント（`/plan`、`/review`）はほとんどのワークフローに十分対応できます。カスタムエージェントは、作業全体に一貫して適用したい専門知識が必要なときに作成しましょう。

以下の各トピックは独立しています。**興味のある部分から読み始めてください。すべてを一度に読む必要はありません。**

| やりたいこと | ジャンプ先 |
|---|---|
| エージェントが汎用プロンプトより優れている理由を確認する | [スペシャリスト vs 汎用](#specialist-vs-generic-see-the-difference) |
| 1つの機能で複数のエージェントを組み合わせる | [複数エージェントで作業する](#working-with-multiple-agents) |
| エージェントを整理・命名・共有する | [エージェントの整理と共有](#organizing--sharing-agents) |
| 常時オンのプロジェクトコンテキストを設定する | [Copilot 向けプロジェクト設定](#configuring-your-project-for-copilot) |
| YAMLプロパティとツールを調べる | [エージェントファイルリファレンス](#agent-file-reference) |

以下のシナリオを選択して展開してください。

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>スペシャリスト vs 汎用：違いを見てみよう</strong> - エージェントが汎用プロンプトより優れた出力を生む理由</summary>

## スペシャリスト vs 汎用：違いを見てみよう

ここでエージェントの真価が発揮されます。違いを見てみましょう：

### エージェントなし（汎用 Copilot）

```bash
copilot

> Add a function to search books by year range in the book app
```

**汎用の出力**：
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

基本的。動く。でも多くが欠けている。

---

### Python Reviewer エージェントを使った場合

```bash
copilot

> /agent
# "python-reviewer" を選択

> Add a function to search books by year range in the book app
```

**スペシャリストの出力**：
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    Search for books within a specified year range.

    Args:
        books: List of book dictionaries
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)

    Returns:
        List of books published within the year range

    Raises:
        ValueError: If start_year is greater than end_year
        TypeError: If year values are not integers
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("Year values must be integers")

    if start_year > end_year:
        raise ValueError(f"Start year ({start_year}) cannot be greater than end year ({end_year})")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**python-reviewerエージェントが自動的に含めるもの**：
- ✅ すべてのパラメータと戻り値の型ヒント
- ✅ Args/Returns/Raises を含む包括的なdocstring
- ✅ 適切なエラーハンドリングを伴う入力バリデーション
- ✅ パフォーマンス向上のためのリスト内包表記
- ✅ エッジケースの処理（年の値が欠損または無効な場合）
- ✅ PEP 8 準拠のフォーマット
- ✅ 防御的プログラミングの実践

**違い**: 同じプロンプト、劇的に良い出力。エージェントは、あなたが頼むのを忘れてしまうような専門知識を持ち込んでくれます。

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>複数エージェントで作業する</strong> - スペシャリストの組み合わせ、セッション途中の切り替え、エージェントをツールとして使う</summary>

## 複数エージェントで作業する

本当の力は、スペシャリストが1つの機能について協力するときに発揮されます。

### 例：シンプルな機能を作る

```bash
copilot

> I want to add a "search by year range" feature to the book app

# 設計にpython-reviewerを使う
> /agent
# "python-reviewer" を選択

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# テスト設計にpytest-helperへ切り替える
> /agent
# "pytest-helper" を選択

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# 両方の設計を統合する
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**重要な洞察**: あなたはスペシャリストを指揮するアーキテクトです。細部はエージェントに任せ、ビジョンはあなたが持つ。

<details>
<summary>🎬 実際の動作を見る！</summary>

![Python Reviewer Demo](images/python-reviewer-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

### エージェントをツールとして使う

エージェントが設定されていると、Copilot は複雑なタスク中にそれらをツールとして呼び出すこともできます。フルスタックの機能を依頼すると、Copilot が適切なスペシャリストエージェントに自動的に委任することがあります。

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>エージェントの整理と共有</strong> - 命名、ファイル配置、指示ファイル、チームでの共有</summary>

## エージェントの整理と共有

### エージェントの命名

エージェントファイルを作成するとき、名前が重要です。`/agent` や `--agent` の後に入力するものであり、チームメイトのエージェントリストに表示されます。

| ✅ 良い名前 | ❌ 避けるべき名前 |
|-----------|----------------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**命名規則：**
- 小文字とハイフンを使う：`my-agent-name.agent.md`
- ドメインを含める：`frontend`・`backend`・`devops`・`security`
- 必要に応じて具体的に：`react-typescript` vs 単なる `frontend`

---

### チームでの共有

エージェントファイルを `.github/agents/` に置けば、バージョン管理されます。リポジトリにプッシュすると、すべてのチームメンバーが自動的に取得できます。ただし、エージェントは Copilot がプロジェクトから読み込むファイルの一種に過ぎません。**指示ファイル**もサポートしており、`/agent` を実行しなくても、すべてのセッションに自動的に適用されます。

こう考えてください：エージェントは呼び出すスペシャリスト、指示ファイルは常に有効なチームのルールです。

### ファイルの置き場所

2つの主な場所はすでに知っています（上の[エージェントファイルの置き場所](#エージェントファイルの置き場所)を参照）。このデシジョンツリーを使って選択しましょう：

<img src="images/agent-file-placement-decision-tree.png" alt="Decision tree for where to put agent files: experimenting → current folder, team use → .github/agents/, everywhere → ~/.copilot/agents/" width="800"/>

**シンプルに始めよう：** プロジェクトフォルダに `*.agent.md` ファイルを1つ作成し、満足したら恒久的な場所に移動しましょう。

エージェントファイルの他に、Copilot は**プロジェクトレベルの指示ファイル**も自動的に読み込みます（`/agent` は不要）。`AGENTS.md`・`.instructions.md`・`/init` については、下の[Copilot 向けプロジェクト設定](#configuring-your-project-for-copilot)を参照してください。

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Copilot 向けプロジェクト設定</strong> - AGENTS.md・指示ファイル・/init のセットアップ</summary>

## Copilot 向けプロジェクト設定

エージェントはオンデマンドで呼び出すスペシャリストです。**プロジェクト設定ファイル**は異なります：Copilot はプロジェクトの規約・技術スタック・ルールを把握するため、すべてのセッションで自動的に読み込みます。`/agent` を実行する必要はなく、リポジトリで作業するすべての人にコンテキストが常に適用されます。

### /init でのクイックセットアップ

最も手早く始める方法は、Copilot に設定ファイルを生成させることです：

```bash
copilot
> /init
```

Copilot がプロジェクトをスキャンして、カスタマイズされた指示ファイルを作成します。後で編集することもできます。

### 指示ファイルの形式

| ファイル | スコープ | 備考 |
|---------|---------|------|
| `AGENTS.md` | プロジェクトルートまたはネスト | **クロスプラットフォーム標準** - Copilot や他のAIアシスタントで動作する |
| `.github/copilot-instructions.md` | プロジェクト | GitHub Copilot 固有 |
| `.github/instructions/*.instructions.md` | プロジェクト | 粒度の細かい、トピック別の指示 |
| `CLAUDE.md`・`GEMINI.md` | プロジェクトルート | 互換性のためにサポート |

> 🎯 **始めたばかり？** プロジェクト指示には `AGENTS.md` を使いましょう。他の形式は必要に応じて後から探索できます。

### AGENTS.md

`AGENTS.md` は推奨される形式です。Copilot や他のAIコーディングツールで動作する [オープンスタンダード](https://agents.md/) です。リポジトリルートに置くと Copilot が自動的に読み込みます。このプロジェクト自身の [AGENTS.md](../AGENTS.md) が実際の例です。

典型的な `AGENTS.md` には、プロジェクトのコンテキスト・コードスタイル・セキュリティ要件・テスト基準が記述されます。サンプルファイルのパターンに従って自分のものを書きましょう。

### カスタム指示ファイル（.instructions.md）

より細かい制御を求めるチームには、指示をトピック別ファイルに分割する方法があります。各ファイルは1つの関心事をカバーし、自動的に適用されます：

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **補足**: 指示ファイルはどの言語でも使えます。この例ではコースプロジェクトに合わせてPythonを使っていますが、TypeScript・Go・Rust・その他チームが使う技術に対して同様のファイルを作成できます。

**コミュニティの指示ファイルを探す**: [github/awesome-copilot](https://github.com/github/awesome-copilot) で .NET・Angular・Azure・Python・Docker などの技術に対応した既製の指示ファイルを参照できます。

### カスタム指示の無効化

Copilot にすべてのプロジェクト固有の設定を無視させたい場合（デバッグや動作比較に便利）：

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>エージェントファイルリファレンス</strong> - YAMLプロパティ・ツールエイリアス・完全な例</summary>

## エージェントファイルリファレンス

### より完全な例

上の[最小限のエージェント形式](#-エージェントを追加する)を確認しました。ここでは `tools` プロパティを使ったより包括的なエージェントを示します。`~/.copilot/agents/python-reviewer.agent.md` を作成してください：

```markdown
---
name: python-reviewer
description: Python code quality specialist for reviewing Python projects
tools: ["read", "edit", "search", "execute"]
---

# Python Code Reviewer

You are a Python specialist focused on code quality and best practices.

**Your focus areas:**
- Code quality (PEP 8, type hints, docstrings)
- Performance optimization (list comprehensions, generators)
- Error handling (proper exception handling)
- Maintainability (DRY principles, clear naming)

**Code style requirements:**
- Use Python 3.10+ features (dataclasses, type hints, pattern matching)
- Follow PEP 8 naming conventions
- Use context managers for file I/O
- All functions must have type hints and docstrings

**When reviewing code, always check:**
- Missing type hints on function signatures
- Mutable default arguments
- Proper error handling (no bare except)
- Input validation completeness
```

### YAMLプロパティ

| プロパティ | 必須 | 説明 |
|----------|------|------|
| `name` | いいえ | 表示名（デフォルトはファイル名） |
| `description` | **はい** | エージェントの役割 - Copilot がいつ提案するかを理解するために使われる |
| `tools` | いいえ | 許可するツールのリスト（省略すると全ツールが利用可能）。下のツールエイリアスを参照。 |
| `target` | いいえ | `vscode` または `github-copilot` のみに制限する |

### ツールエイリアス

`tools` リストで使用する名前：
- `read` - ファイルの内容を読み込む
- `edit` - ファイルを編集する
- `search` - ファイルを検索する（grep/glob）
- `execute` - シェルコマンドを実行する（別名：`shell`・`Bash`）
- `agent` - 他のカスタムエージェントを呼び出す

> 📖 **公式ドキュメント**: [カスタムエージェントの設定](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **VS Code のみ**: `model` プロパティ（AIモデルの選択）は VS Code では動作しますが、GitHub Copilot CLI ではサポートされていません。クロスプラットフォームのエージェントファイルにそのまま含めることは安全です。GitHub Copilot CLI は無視します。

### エージェントテンプレートをもっと見る

> 💡 **初心者へのメモ**: 以下の例はテンプレートです。**特定の技術はあなたのプロジェクトで使っているものに置き換えてください。** 重要なのは、特定の技術ではなく、エージェントの*構造*です。

このプロジェクトには [.github/agents/](../.github/agents/) フォルダに実際の例が含まれています：
- [hello-world.agent.md](../.github/agents/hello-world.agent.md) - 最小限の例、ここから始めよう
- [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) - Pythonコード品質レビュアー
- [pytest-helper.agent.md](../.github/agents/pytest-helper.agent.md) - pytestテスト専門家

コミュニティエージェントは [github/awesome-copilot](https://github.com/github/awesome-copilot) を参照してください。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

自分のエージェントを作って実際に動かしてみましょう。

---

## ▶️ 実際に試してみよう

```bash

# エージェントディレクトリを作成する（まだなければ）
mkdir -p .github/agents

# コードレビュアーエージェントを作成する
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: Senior code reviewer focused on security and best practices
---

# Code Reviewer Agent

You are a senior code reviewer focused on code quality.

**Review priorities:**
1. Security vulnerabilities
2. Performance issues
3. Maintainability concerns
4. Best practice violations

**Output format:**
Provide issues as a numbered list with severity tags:
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# ドキュメントエージェントを作成する
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: Technical writer for clear and complete documentation
---

# Documentation Agent

You are a technical writer who creates clear documentation.

**Documentation standards:**
- Start with a one-sentence summary
- Include usage examples
- Document parameters and return values
- Note any gotchas or limitations
EOF

# 使ってみよう
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# またはエージェントを切り替える
copilot
> /agent
# "documentor" を選択
> Document @samples/book-app-project/books.py
```

---

## 📝 課題

### メインチャレンジ：専門エージェントチームを作る

ハンズオンの例では `reviewer` と `documentor` エージェントを作成しました。今度は別のタスク——book appのデータバリデーション改善——にエージェントを作って使う練習をしましょう：

1. `.github/agents/` に、エージェント1つにつき1ファイル、計3つの `.agent.md` ファイルを作成する
2. エージェント内容：
   - **data-validator**：`data.json` に欠損や不正なデータ（著者が空・year=0・フィールド欠損）がないか確認する
   - **error-handler**：Pythonコードの一貫性のないエラーハンドリングをレビューし、統一されたアプローチを提案する
   - **doc-writer**：docstringとREADMEコンテンツを生成・更新する
3. book appで各エージェントを使う：
   - `data-validator` → `@samples/book-app-project/data.json` を監査する
   - `error-handler` → `@samples/book-app-project/books.py` と `@samples/book-app-project/utils.py` をレビューする
   - `doc-writer` → `@samples/book-app-project/books.py` にdocstringを追加する
4. コラボレーション：`error-handler` でエラーハンドリングのギャップを特定し、`doc-writer` で改善されたアプローチをドキュメント化する

**成功基準**: 一貫した高品質な出力を生成する3つの動作するエージェントがあり、`/agent` で切り替えられる。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**スターターテンプレート**：`.github/agents/` に1エージェントにつき1ファイルを作成する：

`data-validator.agent.md`:
```markdown
---
description: Analyzes JSON data files for missing or malformed entries
---

You analyze JSON data files for missing or malformed entries.

**Focus areas:**
- Empty or missing author fields
- Invalid years (year=0, future years, negative years)
- Missing required fields (title, author, year, read)
- Duplicate entries
```

`error-handler.agent.md`:
```markdown
---
description: Reviews Python code for error handling consistency
---

You review Python code for error handling consistency.

**Standards:**
- No bare except clauses
- Use custom exceptions where appropriate
- All file operations use context managers
- Consistent return types for success/failure
```

`doc-writer.agent.md`:
```markdown
---
description: Technical writer for clear Python documentation
---

You are a technical writer who creates clear Python documentation.

**Standards:**
- Google-style docstrings
- Include parameter types and return values
- Add usage examples for public methods
- Note any exceptions raised
```

**エージェントのテスト：**

> 💡 **補足：** `samples/book-app-project/data.json` はリポジトリのローカルコピーに既にあるはずです。もし存在しない場合は、ソースリポジトリからオリジナルバージョンをダウンロードしてください：
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# リストから "data-validator" を選択
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**ヒント：** YAMLフロントマターの `description` フィールドはエージェントが動作するために必須です。

</details>

### ボーナスチャレンジ：指示ライブラリ

オンデマンドで呼び出すエージェントを作りました。次は反対側を試してみましょう：**指示ファイル**は、`/agent` を実行しなくても Copilot がすべてのセッションで自動的に読み込みます。

`.github/instructions/` フォルダを作成し、少なくとも3つの指示ファイルを作りましょう：
- `python-style.instructions.md`：PEP 8 と型ヒントの規約を強制する
- `test-standards.instructions.md`：テストファイルに pytest の規約を強制する
- `data-quality.instructions.md`：JSONデータエントリを検証する

book appのコードで各指示ファイルをテストしましょう。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 起きること | 修正方法 |
|--------|-----------|---------|
| エージェントフロントマターに `description` がない | エージェントが読み込まれないか、発見されない | 常に YAMLフロントマターに `description:` を含める |
| エージェントのファイル場所が間違っている | 使おうとしてもエージェントが見つからない | `~/.copilot/agents/`（個人）または `.github/agents/`（プロジェクト）に置く |
| `.agent.md` の代わりに `.md` を使っている | ファイルがエージェントとして認識されない可能性がある | `python-reviewer.agent.md` のようにファイルを命名する |
| エージェントのプロンプトが長すぎる | 30,000文字の制限に達する可能性がある | エージェント定義を絞り込む；詳細な指示にはスキルを使う |

### トラブルシューティング

**エージェントが見つからない** - 以下のいずれかの場所にエージェントファイルが存在することを確認する：
- `~/.copilot/agents/`
- `.github/agents/`

利用可能なエージェントの一覧表示：

```bash
copilot
> /agent
# 利用可能なエージェントが全て表示される
```

**エージェントが指示に従わない** - プロンプトを具体的にし、エージェント定義にさらに詳細を追加する：
- バージョン付きの特定のフレームワーク・ライブラリ
- チームの規約
- コードパターンの例

**カスタム指示が読み込まれない** - プロジェクトで `/init` を実行してプロジェクト固有の指示をセットアップする：

```bash
copilot
> /init
```

または無効化されていないか確認する：
```bash
# 読み込みたい場合は --no-custom-instructions を使わない
copilot  # デフォルトでカスタム指示が読み込まれる
```

</details>

---

# まとめ

## 🔑 重要なポイント

1. **組み込みエージェント**：`/plan` と `/review` は直接呼び出す；Explore と Task は自動的に動作する
2. **カスタムエージェント**は `.agent.md` ファイルで定義されるスペシャリスト
3. **良いエージェント**は明確な専門知識・基準・出力形式を持っている
4. **マルチエージェントの連携**は専門知識を組み合わせて複雑な問題を解決する
5. **指示ファイル**（`.instructions.md`）はチームの基準を自動適用のためにエンコードする
6. **一貫した出力**は明確に定義されたエージェント指示から生まれる

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次のステップ

エージェントは *Copilot がコードにアプローチして的を絞ったアクションを取る方法*を変えます。次は**スキル**について学びます——スキルは*どのステップを*踏むかを変えます。エージェントとスキルの違いが気になりますか？Chapter 05 でそれを正面から取り上げます。

**[Chapter 05: Skills System](../05-skills/README.md)** では次のことを学びます：

- スキルがプロンプトから自動トリガーされる仕組み（スラッシュコマンド不要）
- コミュニティスキルのインストール
- SKILL.md ファイルを使ったカスタムスキルの作成
- エージェント・スキル・MCP の違い
- それぞれをいつ使うか

---

**[← Chapter 03 に戻る](../03-development-workflows/README.md)** | **[Chapter 05 へ進む →](../05-skills/README.md)**
