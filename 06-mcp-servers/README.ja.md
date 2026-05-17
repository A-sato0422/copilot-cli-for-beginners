![Chapter 06: MCP Servers](images/chapter-header.png)

> **Copilot が GitHub のイシューを読んで、データベースを確認して、PR を作成できたら？しかもすべてターミナルから？**

ここまで、Copilot が扱えるのはあなたが直接渡したもの（`@` で参照したファイル、会話履歴、自身のトレーニングデータ）だけでした。でも、Copilot が自ら GitHub リポジトリを確認したり、プロジェクトのファイルを参照したり、ライブラリの最新ドキュメントを調べたりできたらどうでしょう？

それを実現するのが MCP（Model Context Protocol）です。Copilot を外部サービスに接続して、リアルタイムのデータにアクセスできるようにする仕組みです。Copilot が接続する各サービスを「MCP サーバー」と呼びます。この章では、いくつかの接続を設定して、Copilot が格段に便利になる様子を体験します。

> 💡 **MCP をすでに知っている方へ**: [クイックスタート](#-use-the-built-in-github-mcp) に進んで動作確認とサーバー設定を始めましょう。

## 🎯 学習目標

この章を終えると、次のことができるようになります：

- MCP とは何か、なぜ重要かを理解する
- `/mcp` コマンドで MCP サーバーを管理する
- GitHub、ファイルシステム、ドキュメント用の MCP サーバーを設定する
- book app プロジェクトで MCP を活用したワークフローを使う
- カスタム MCP サーバーをいつ・どのように構築するかを知る（オプション）

> ⏱️ **目安時間**：約50分（読書15分 + ハンズオン35分）

---

## 🧩 現実世界のたとえ：ブラウザ拡張機能

<img src="images/browser-extensions-analogy.png" alt="MCP Servers are like Browser Extensions" width="800"/>

MCP サーバーをブラウザの拡張機能のように考えましょう。ブラウザ単体でもウェブページは表示できますが、拡張機能を使うと追加のサービスと連携できます：

| ブラウザ拡張機能 | 接続先 | MCP での対応 |
|-----------------|--------|------------|
| パスワードマネージャー | パスワード保管庫 | **GitHub MCP** → リポジトリ・イシュー・PR |
| Grammarly | 文章解析サービス | **Context7 MCP** → ライブラリドキュメント |
| ファイルマネージャー | クラウドストレージ | **Filesystem MCP** → ローカルプロジェクトファイル |

拡張機能がなくてもブラウザは使えますが、あればパワフルなツールになります。MCP サーバーも同じです。GitHub のイシューを読んで、ファイルシステムを探索して、最新ドキュメントを取得するなど、Copilot をリアルなデータソースに接続します。

***MCP サーバーは Copilot と外の世界（GitHub、リポジトリ、ドキュメントなど）をつなぐ***

> 💡 **重要なポイント**：MCP なしでは、Copilot は `@` で明示的に共有したファイルしか見られません。MCP があれば、プロジェクトを自ら探索し、GitHub リポジトリを確認し、ドキュメントを調べることができます。すべて自動で。

---

<img src="images/quick-start-mcp.png" alt="Power cable connecting with bright electrical spark surrounded by floating tech icons representing MCP server connections" width="800"/>

# クイックスタート：30秒で MCP を体験

## 組み込みの GitHub MCP を使ってみよう
何も設定しなくても、今すぐ MCP を体験できます。
GitHub MCP サーバーはデフォルトで含まれています。試してみましょう：

```bash
copilot
> List the recent commits in this repository
```

Copilot が実際のコミットデータを返してきたら、MCP が動いています。GitHub MCP サーバーがあなたの代わりに GitHub にアクセスしているのです。ただし GitHub は *1つのサーバー* にすぎません。この章では、さらに多くのサーバー（ファイルシステムへのアクセス、最新ドキュメント、その他）を追加して、Copilot をもっと活用できるようにします。

---

## `/mcp show` コマンド

`/mcp show` を使うと、設定されている MCP サーバーとその有効/無効の状態を確認できます：

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **GitHub サーバーしか表示されない？** それで正常です！追加の MCP サーバーをまだ追加していなければ、GitHub だけが表示されます。次のセクションで追加します。

> 📚 **MCP 管理コマンドをすべて確認したい？** チャット内のスラッシュコマンド `/mcp` か、ターミナルから直接 `copilot mcp` を使ってサーバーを管理できます。この章末の[コマンドリファレンス](#-additional-mcp-commands)を参照してください。

<details>
<summary>🎬 実際の動作を見る！</summary>

![MCP Status Demo](images/mcp-status-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

---

## MCP があると何が変わる？

MCP があることで、実際にこれだけ違いが出ます：

**MCP なし：**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**MCP あり：**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP によって、Copilot が実際の開発環境を認識できるようになります。

> 📚 **公式ドキュメント**：[MCP について](https://docs.github.com/copilot/concepts/context/mcp) — GitHub Copilot での MCP の仕組みを詳しく解説しています。

---

# MCP サーバーの設定

<img src="images/configuring-mcp-servers.png" alt="Hands adjusting knobs and sliders on a professional audio mixing board representing MCP server configuration" width="800"/>

MCP の動作を確認したところで、追加サーバーを設定しましょう。サーバーを追加する方法は2つあります：**組み込みレジストリから追加**（最も簡単 — CLI で対話形式に設定）か、**設定ファイルを手動で編集**（より柔軟）。迷ったらレジストリから始めましょう。

---

## レジストリから MCP サーバーをインストールする

CLI には MCP サーバーの組み込みレジストリがあり、人気サーバーを対話形式でインストールできます。JSON の編集は不要です。

```bash
copilot

> /mcp search
```

Copilot が利用可能なサーバーの一覧を表示します。選択すると、CLI が必要な設定（API キー、パスなど）を案内してくれ、自動的に設定ファイルに追加されます。

> 💡 **レジストリを使う理由**：最も簡単に始められる方法です。npm パッケージ名やコマンド引数、JSON の構造を知らなくても大丈夫。CLI がすべて処理してくれます。

---

## MCP 設定ファイル

MCP サーバーの設定は `~/.copilot/mcp-config.json`（ユーザーレベル、全プロジェクトに適用）または `.mcp.json`（プロジェクトレベル、プロジェクトのルートに配置）に記述します。上で `/mcp search` を使った場合、CLI がすでにこのファイルを作成または更新しています。カスタマイズのためにも、フォーマットを理解しておきましょう。

> ⚠️ **注意**：`.vscode/mcp.json` は MCP 設定ソースとしてサポートされなくなりました。既存の `.vscode/mcp.json` がある場合は、プロジェクトルートの `.mcp.json` に移行してください。古い設定ファイルが検出されると、CLI が移行のヒントを表示します。

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*ほとんどの MCP サーバーは npm パッケージとして配布され、`npx` コマンドで実行します。*

<details>
<summary>💡 <strong>JSON が初めての方へ</strong>：各フィールドの意味をクリックして確認</summary>

| フィールド | 意味 |
|-----------|------|
| `"mcpServers"` | すべての MCP サーバー設定のコンテナ |
| `"server-name"` | 任意の名前（例："github"、"filesystem"） |
| `"type": "local"` | サーバーをローカルマシンで実行する |
| `"command": "npx"` | 実行するプログラム（npx は npm パッケージを実行） |
| `"args": [...]` | コマンドに渡す引数 |
| `"tools": ["*"]` | このサーバーのすべてのツールを許可する |

**JSON の重要なルール：**
- 文字列にはダブルクォート `"` を使う（シングルクォートは不可）
- 最後の項目の後にカンマを付けない
- ファイルは有効な JSON でなければならない（不安な場合は [JSON バリデーター](https://jsonlint.com/) を使用）

</details>

---

## MCP サーバーの追加

GitHub MCP サーバーは組み込みで、設定は不要です。以下は追加できるサーバーの一覧です。**興味があるものを選ぶか、順番に進めましょう。**

| やりたいこと | 移動先 |
|------------|--------|
| Copilot にプロジェクトファイルを参照させる | [Filesystem サーバー](#filesystem-server) |
| 最新のライブラリドキュメントを取得する | [Context7 サーバー](#context7-server-documentation) |
| オプションの機能（カスタムサーバー、web_fetch）を試す | [さらに進む](#beyond-the-basics) |

<details>
<summary><strong>Filesystem サーバー</strong> — Copilot にプロジェクトファイルを探索させる</summary>
<a id="filesystem-server"></a>

### Filesystem サーバー

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **`.` パスについて**：`.` は「カレントディレクトリ」を意味します。Copilot は起動した場所を基準にファイルにアクセスできます。Codespace ではワークスペースのルートになります。必要であれば `/workspaces/copilot-cli-for-beginners` のような絶対パスも使えます。

これを `~/.copilot/mcp-config.json` に追加して Copilot を再起動してください。

</details>

<details>
<summary><strong>Context7 サーバー</strong> — 最新のライブラリドキュメントを取得する</summary>
<a id="context7-server-documentation"></a>

### Context7 サーバー（ドキュメント）

Context7 は、人気フレームワークやライブラリの最新ドキュメントへのアクセスを Copilot に提供します。古くなっているかもしれないトレーニングデータに頼るのではなく、実際の最新ドキュメントを取得します。

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **API キー不要**
- ✅ **アカウント不要**
- ✅ **コードはローカルに残る**

これを `~/.copilot/mcp-config.json` に追加して Copilot を再起動してください。

</details>

<details>
<summary><strong>さらに進む</strong> — カスタムサーバーとウェブアクセス（オプション）</summary>
<a id="beyond-the-basics"></a>

上記のコアサーバーに慣れたら試せるオプションの追加機能です。

### Microsoft Learn MCP サーバー

これまで紹介したすべての MCP サーバー（filesystem、Context7）はローカルマシンで実行されます。しかし MCP サーバーはリモートでも動作できます。つまり、Copilot CLI に URL を指定するだけで、あとは自動で処理されます。`npx` も Python も不要で、ローカルプロセスも、インストールする依存関係もありません。

[Microsoft Learn MCP サーバー](https://github.com/microsoftdocs/mcp)はその良い例です。Copilot CLI に公式 Microsoft ドキュメント（Azure、Microsoft Foundry をはじめとする AI トピック、.NET、Microsoft 365 など）への直接アクセスを提供し、モデルのトレーニングデータに頼らず、ドキュメントを検索・取得したり、公式コードサンプルを見つけたりできます。

- ✅ **API キー不要**
- ✅ **アカウント不要**
- ✅ **ローカルインストール不要**

**`/plugin install` でクイックインストール：**

JSON 設定ファイルを手動で編集する代わりに、1つのコマンドでインストールできます：

```bash
copilot

> /plugin install microsoftdocs/mcp
```

これにより、サーバーと関連するエージェントスキルが自動的に追加されます。インストールされるスキルには以下が含まれます：

- **microsoft-docs**：概念、チュートリアル、事実の調査
- **microsoft-code-reference**：API の調査、コードサンプル、トラブルシューティング
- **microsoft-skill-creator**：Microsoft テクノロジーに関するカスタムスキルを生成するメタスキル

**使い方：**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 詳細：[Microsoft Learn MCP サーバー概要](https://learn.microsoft.com/training/support/mcp-get-started)

### `web_fetch` を使ったウェブアクセス

Copilot CLI には任意の URL からコンテンツを取得できる組み込みの `web_fetch` ツールが含まれています。ターミナルを離れることなく、README や API ドキュメント、リリースノートを取り込むのに便利です。MCP サーバーは不要です。

アクセスできる URL は `~/.copilot/config.json`（Copilot の全般設定）で制御できます。これは `~/.copilot/mcp-config.json`（MCP サーバーの定義）とは別のファイルです。

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**使い方：**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### カスタム MCP サーバーを構築する

自分の API やデータベース、社内ツールに Copilot を接続したいですか？Python でカスタム MCP サーバーを構築できます。既製サーバー（GitHub、filesystem、Context7）がほとんどのユースケースをカバーしているため、これは完全にオプションです。

📖 book app を例にした完全なウォークスルーは [カスタム MCP サーバーガイド](mcp-custom-server.md) を参照してください。

📚 さらなる背景については、[MCP for Beginners コース](https://github.com/microsoft/mcp-for-beginners) を参照してください。

</details>

<a id="complete-configuration-file"></a>

### 完全な設定ファイル

filesystem サーバーと Context7 サーバーを含む完全な `mcp-config.json` です：

> 💡 **注意**：GitHub MCP は組み込みです。設定ファイルに追加する必要はありません。

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

グローバルに使う場合は `~/.copilot/mcp-config.json` として保存し、プロジェクト固有の設定にする場合はプロジェクトルートに `.mcp.json` として保存してください。

---

# MCP サーバーを使う

MCP サーバーの設定ができたところで、実際に何ができるか見てみましょう。

<img src="images/using-mcp-servers.png" alt="Using MCP Servers - Hub-and-spoke diagram showing a Developer CLI connected to GitHub, Filesystem, Context7, and Custom/Web Fetch servers" width="800" />

---

## サーバーの使用例

**試したいサーバーを選ぶか、順番に進めましょう。**

| 試したいこと | 移動先 |
|------------|--------|
| GitHub リポジトリ・イシュー・PR | [GitHub サーバー](#github-server-built-in) |
| プロジェクトファイルの参照 | [Filesystem サーバーの使い方](#filesystem-server-usage) |
| ライブラリドキュメントの検索 | [Context7 サーバーの使い方](#context7-server-usage) |
| カスタムサーバー・Microsoft Learn MCP・web_fetch の使い方 | [さらに進む（使い方）](#beyond-the-basics-usage) |

<details>
<summary><strong>GitHub サーバー（組み込み）</strong> — リポジトリ・イシュー・PR などにアクセス</summary>
<a id="github-server-built-in"></a>

### GitHub サーバー（組み込み）

GitHub MCP サーバーは**組み込み**です。Copilot にログイン済みであれば（初回セットアップ時に実施）、すでに使えます。設定は不要です！

> 💡 **動かない場合**：`/login` を実行して GitHub で再認証してください。

<details>
<summary><strong>Dev コンテナでの認証</strong></summary>

- **GitHub Codespaces**（推奨）：認証は自動です。`gh` CLI が Codespace のトークンを引き継ぎます。操作は不要です。
- **ローカル Dev コンテナ（Docker）**：コンテナ起動後に `gh auth login` を実行し、Copilot を再起動してください。

**認証のトラブルシューティング：**
```bash
# 認証されているか確認
gh auth status

# 認証されていない場合はログイン
gh auth login

# GitHub MCP が接続されているか確認
copilot
> /mcp show
```

</details>

| 機能 | 例 |
|------|-----|
| **リポジトリ情報** | コミット・ブランチ・コントリビューターを確認 |
| **イシュー** | イシューの一覧表示・作成・検索・コメント |
| **プルリクエスト** | PR の確認・差分・作成・ステータス確認 |
| **コード検索** | リポジトリ全体でコードを検索 |
| **Actions** | ワークフローの実行状況とステータスを確認 |

```bash
copilot

# このリポジトリの最近のアクティビティを確認
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# リポジトリの構造を探索
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# リポジトリ全体でコードパターンを検索
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **自分のフォークで作業している場合**：このコースリポジトリをフォークしていれば、イシューの作成やプルリクエストなどの書き込み操作も試せます。後の演習で練習しましょう。

> ⚠️ **結果が表示されない場合**：GitHub MCP はリモートリポジトリ（github.com 上）に対して動作し、ローカルファイルだけではありません。リポジトリにリモートがあることを確認してください：`git remote -v` で確認できます。

</details>

<details>
<summary><strong>Filesystem サーバー</strong> — プロジェクトファイルを参照・分析する</summary>
<a id="filesystem-server-usage"></a>

### Filesystem サーバー

設定済みであれば、filesystem MCP は Copilot が自動的に使えるツールを提供します：

```bash
copilot

> How many Python files are in the book-app-project directory?

Found 3 Python files in samples/book-app-project/:
- book_app.py
- books.py
- utils.py

> What's the total size of the data.json file?

samples/book-app-project/data.json: 2.4 KB

> Find all functions that don't have type hints in the book app

Found 2 functions without type hints:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

</details>

<details>
<summary><strong>Context7 サーバー</strong> — ライブラリドキュメントを調べる</summary>
<a id="context7-server-usage"></a>

### Context7 サーバー

```bash
copilot

> What are the best practices for using pytest fixtures?

From pytest Documentation:

Fixtures - Use fixtures to provide a fixed baseline for tests:

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # フィクスチャは引数として自動的に渡される
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# Copilot が公式の pytest パターンを把握しているので
# samples/book-app-project/tests/test_books.py に適用できる
```

</details>

<details>
<summary><strong>さらに進む</strong> — カスタムサーバーと web_fetch の使い方</summary>
<a id="beyond-the-basics-usage"></a>

### さらに進む

**カスタム MCP サーバー**：[カスタム MCP サーバーガイド](mcp-custom-server.md) で book-lookup サーバーを構築した場合、ブックコレクションを直接クエリできます：

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**：[Microsoft Learn MCP サーバー](#microsoft-learn-mcp-server)をインストールした場合、公式 Microsoft ドキュメントを直接参照できます：

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**：組み込みの `web_fetch` ツールで任意の URL からコンテンツを取得できます：

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## マルチサーバーワークフロー

「これがあったら二度と手放せない」と開発者が言う理由を示すワークフローです。各例では、1つのセッションで複数の MCP サーバーを組み合わせています。

<img src="images/issue-to-pr-workflow.png" alt="Issue to PR Workflow using MCP - Shows the complete flow from getting a GitHub issue through creating a pull request" width="800"/>

*完全な MCP ワークフロー：GitHub MCP がリポジトリデータを取得し、Filesystem MCP がコードを見つけ、Context7 MCP がベストプラクティスを提供し、Copilot が分析を担当する*

以下の各例は独立しています。**興味のあるものを選ぶか、すべて読んでみましょう。**

| 見たいもの | 移動先 |
|-----------|--------|
| 複数サーバーの連携 | [マルチサーバー探索](#multi-server-exploration) |
| イシューから PR まで1セッションで | [Issue-to-PR ワークフロー](#issue-to-pr-workflow) |
| プロジェクトのクイックヘルスチェック | [ヘルスダッシュボード](#health-dashboard) |

<details>
<summary><strong>マルチサーバー探索</strong> — filesystem・GitHub・Context7 を1セッションで組み合わせる</summary>
<a id="multi-server-exploration"></a>

#### 複数の MCP サーバーで book app を探索する

```bash
copilot

# ステップ1：filesystem MCP で book app を探索
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# ステップ2：GitHub MCP で最近の変更を確認
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# ステップ3：Context7 MCP でベストプラクティスを調べる
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# ステップ4：改善提案をまとめる
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 MCP ワークフローの実際の動作を見る！</summary>

![MCP Workflow Demo](images/mcp-workflow-demo.gif)

*デモの出力は変わります。モデル・ツール・回答は、ここで示されているものと異なります。*

</details>

**結果**：コード探索 → 履歴の確認 → ベストプラクティスの調査 → 改善計画。**1つのターミナルセッションから、3つの MCP サーバーを組み合わせて実現。**

</details>

<details>
<summary><strong>Issue-to-PR ワークフロー</strong> — ターミナルを離れずに GitHub イシューからプルリクエストまで</summary>
<a id="issue-to-pr-workflow"></a>

#### Issue-to-PR ワークフロー（自分のリポジトリで）

書き込み権限がある自分のフォークやリポジトリで最もよく機能します：

> 💡 **今すぐ試せなくても大丈夫**。読み取り専用クローンの場合は、課題で練習します。今は流れを理解するために読み進めましょう。

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot が add_book() に年のバリデーションを実装]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Add year validation to book app
```

**コピペゼロ。コンテキストスイッチゼロ。ターミナル1つで完結。**

</details>

<details>
<summary><strong>ヘルスダッシュボード</strong> — 複数サーバーでプロジェクトのクイックヘルスチェック</summary>
<a id="health-dashboard"></a>

#### book app ヘルスダッシュボード

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory

Book App Health Report
======================

📊 Functions Found:
- books.py: 8 methods in BookCollection (all have type hints ✓)
- book_app.py: 6 functions (4 have type hints, 2 missing)
- utils.py: 3 functions (1 has type hints, 2 missing)

🧪 Test Coverage:
- test_books.py: 8 test functions covering BookCollection
- Missing: no tests for book_app.py CLI functions
- Missing: no tests for utils.py helper functions

📝 Recent Activity:
- 3 commits in the last week
- Most recent: added test fixtures

Recommendations:
- Add type hints to utils.py functions
- Add tests for book_app.py CLI handlers
- All files well-sized (<100 lines) - good structure!
```

**結果**：複数のデータソースを数秒で集約。手動でやれば、grep の実行・行数のカウント・git log の確認・テストファイルの参照が必要で、15分以上かかる作業です。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

**🎉 基本をマスターしました！** MCP を理解し、サーバーの設定方法を学び、実際のワークフローを体験しました。今度は自分で試してみましょう。

---

## ▶️ 実際に試してみよう

あなたの番です！以下の演習を実施して、book app プロジェクトで MCP サーバーを練習しましょう。

### 演習1：MCP の状態を確認する

まず、利用可能な MCP サーバーを確認します：

```bash
copilot

> /mcp show
```

GitHub サーバーが有効として表示されるはずです。表示されない場合は `/login` を実行して認証してください。

---

### 演習2：Filesystem MCP で book app を探索する

filesystem サーバーを設定済みであれば、book app を探索してみましょう：

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**期待される結果**：Copilot が `book_app.py`、`books.py`、`utils.py` と各ファイルの関数を一覧表示します。

> 💡 **filesystem MCP をまだ設定していない？** 上記の[完全な設定](#complete-configuration-file)セクションから設定ファイルを作成してください。その後 Copilot を再起動します。

---

### 演習3：GitHub MCP でリポジトリ履歴を照会する

組み込みの GitHub MCP を使って、このコースリポジトリを探索しましょう：

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**期待される結果**：Copilot が GitHub リモートからの最近のコミットメッセージとブランチ名を表示します。

> ⚠️ **Codespace を使っている場合**：自動的に動作します。認証は引き継がれます。ローカルクローンの場合は `gh auth status` でログイン済みか確認してください。

---

### 演習4：複数の MCP サーバーを組み合わせる

filesystem と GitHub MCP を1つのセッションで組み合わせてみましょう：

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**期待される結果**：Copilot が JSON ファイルを読み込み（filesystem MCP）、"The Hobbit"、"1984"、"Dune"、"To Kill a Mockingbird"、"Mysterious Book" の5冊を一覧表示し、その後 GitHub のコミット履歴を照会します。

**自己チェック**：「リポジトリのコミット履歴を確認して」が、手動で `git log` を実行して出力をプロンプトに貼り付けるよりも優れている理由を説明できれば、MCP を理解できています。

---

## 📝 課題

### メインチャレンジ：book app MCP 探索

book app プロジェクトで MCP サーバーを組み合わせて練習しましょう。以下のステップを1つの Copilot セッションで実施してください：

1. **MCP の動作確認**：`/mcp show` を実行し、少なくとも GitHub サーバーが有効であることを確認する
2. **filesystem MCP の設定**（未設定の場合）：filesystem サーバーの設定で `~/.copilot/mcp-config.json` を作成する
3. **コードの探索**：filesystem サーバーを使うよう Copilot に依頼する：
   - `samples/book-app-project/books.py` のすべての関数を一覧表示する
   - `samples/book-app-project/utils.py` で型ヒントが欠けている関数を確認する
   - `samples/book-app-project/data.json` を読み込み、データ品質の問題を特定する（ヒント：最後のエントリを確認）
4. **リポジトリアクティビティの確認**：GitHub MCP を使うよう Copilot に依頼する：
   - `samples/book-app-project/` のファイルに関連する最近のコミットを一覧表示する
   - オープン中のイシューやプルリクエストがあるか確認する
5. **サーバーの組み合わせ**：1つのプロンプトで Copilot に依頼する：
   - `samples/book-app-project/tests/test_books.py` のテストファイルを読み込む
   - テスト済みの関数と `books.py` のすべての関数を比較する
   - 不足しているテストカバレッジをまとめる

**成功の基準**：filesystem と GitHub MCP のデータを1つの Copilot セッションでシームレスに組み合わせられ、各 MCP サーバーが回答に何を提供したかを説明できること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**ステップ1：MCP の確認**
```bash
copilot
> /mcp show
# "github" が有効として表示されるはず
# 表示されない場合は: /login を実行
```

**ステップ2：設定ファイルの作成**

上記の[完全な設定](#complete-configuration-file)セクションの JSON を使って `~/.copilot/mcp-config.json` として保存してください。

**ステップ3：確認すべきデータ品質の問題**

`data.json` の最後の書籍エントリ：
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
著者が空で、年が 0 になっています。これがデータ品質の問題です！

**ステップ5：テストカバレッジの比較**

`test_books.py` のテストがカバーしているのは：`add_book`、`mark_as_read`、`remove_book`、`get_unread_books`、`find_book_by_title`。`load_books`、`save_books`、`list_books` などの関数には直接のテストがありません。`book_app.py` の CLI 関数と `utils.py` のヘルパーにはテストがまったくありません。

**MCP が動作しない場合**：設定ファイルを編集した後に Copilot を再起動してください。

</details>

### ボーナスチャレンジ：カスタム MCP サーバーを構築する

さらに深く進みたい方は、[カスタム MCP サーバーガイド](mcp-custom-server.md) に従って、任意の API に接続する独自の MCP サーバーを Python で構築しましょう。

---

<details>
<summary>🔧 <strong>よくあるミスとトラブルシューティング</strong>（クリックして展開）</summary>

### よくあるミス

| ミス | 何が起きるか | 解決方法 |
|-----|------------|---------|
| GitHub MCP が組み込みであることを知らない | 手動でインストール・設定しようとする | GitHub MCP はデフォルトで含まれています。試しに「このリポジトリの最近のコミットを一覧表示して」と入力してみてください |
| 設定の場所を間違える | MCP 設定を見つけられない・編集できない | ユーザーレベルの設定は `~/.copilot/mcp-config.json`、プロジェクトレベルはプロジェクトルートの `.mcp.json` |
| 設定ファイルの JSON が無効 | MCP サーバーの読み込みに失敗する | `/mcp show` で設定を確認し、JSON の構文を検証する |
| MCP サーバーの認証を忘れる | 「認証失敗」エラーが発生する | 一部の MCP は個別の認証が必要です。各サーバーの要件を確認してください |

### トラブルシューティング

**「MCP server not found」** — 以下を確認してください：
1. npm パッケージが存在するか：`npm view @modelcontextprotocol/server-github`
2. 設定が有効な JSON か
3. サーバー名が設定と一致しているか

`/mcp show` を使って現在の設定を確認してください。

**「GitHub authentication failed」** — 組み込みの GitHub MCP は `/login` の認証情報を使います。試してみてください：

```bash
copilot
> /login
```

これで GitHub との再認証が行われます。問題が続く場合は、GitHub アカウントがアクセスしているリポジトリに必要な権限を持っているか確認してください。

**「MCP server failed to start」** — サーバーのログを確認してください：
```bash
# サーバーコマンドを手動で実行してエラーを確認
npx -y @modelcontextprotocol/server-github
```

**MCP ツールが使えない** — サーバーが有効になっているか確認してください：
```bash
copilot

> /mcp show
# サーバーが一覧に表示されて有効になっているか確認
```

サーバーが無効になっている場合は、以下の[追加 `/mcp` コマンド](#-additional-mcp-commands)で再度有効にする方法を確認してください。

</details>

---

<details>
<summary>📚 <strong>追加の MCP コマンド</strong>（クリックして展開）</summary>
<a id="-additional-mcp-commands"></a>

MCP サーバーを管理する方法は2つあります：**チャットセッション内でスラッシュコマンドを使う**か、**ターミナルから直接 `copilot mcp` コマンドを使う**（チャットセッションは不要）。

### オプション1：スラッシュコマンド（チャットセッション内）

`copilot` を起動した後、以下のコマンドが使えます：

| コマンド | 何をするか |
|---------|----------|
| `/mcp show` | 設定済みの MCP サーバーとその状態をすべて表示する |
| `/mcp add` | 新しいサーバーを追加するための対話形式のセットアップ |
| `/mcp edit <server-name>` | 既存のサーバー設定を編集する |
| `/mcp enable <server-name>` | 無効なサーバーを有効にする（セッションをまたいで持続する） |
| `/mcp disable <server-name>` | サーバーを無効にする（セッションをまたいで持続する） |
| `/mcp delete <server-name>` | サーバーを永続的に削除する |
| `/mcp auth <server-name>` | OAuth を使う MCP サーバーで再認証する（例：アカウントを切り替えた後） |

### オプション2：`copilot mcp` コマンド（ターミナルから）

チャットセッションを開始せずに、ターミナルから直接 MCP サーバーを管理できます：

```bash
# 設定済みの MCP サーバーをすべて一覧表示
copilot mcp list

# サーバーを有効にする
copilot mcp enable filesystem

# サーバーを無効にする
copilot mcp disable context7
```

> 💡 **どちらを使うべき？** チャットセッション中は `/mcp` スラッシュコマンドを使いましょう。セッションを開始する前にサーバー設定をすばやく確認・変更したい場合は `copilot mcp` をターミナルから使いましょう。

このコースでは `/mcp show` だけで十分な場面がほとんどです。他のコマンドは、複数のサーバーを管理するようになると便利になります。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **MCP** は Copilot を外部サービス（GitHub、ファイルシステム、ドキュメント）に接続する
2. **GitHub MCP は組み込み** — 設定不要、`/login` するだけ
3. **filesystem と Context7** は `~/.copilot/mcp-config.json` で設定する
4. **マルチサーバーワークフロー** は1つのセッションで複数のデータソースを組み合わせる
5. **2つの管理方法**：チャット内では `/mcp` スラッシュコマンド、ターミナルから直接 `copilot mcp` を使う
6. **カスタムサーバー** で任意の API に接続できる（オプション、付録ガイドで解説）

> 📋 **クイックリファレンス**：コマンドとショートカットの完全な一覧は [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次のステップ

モード・コンテキスト・ワークフロー・エージェント・スキル・MCP、すべての構成要素が揃いました。あとはこれらをすべて組み合わせるだけです。

**[Chapter 07: Putting It All Together](../07-putting-it-together/README.md)** では、以下を学びます：

- エージェント・スキル・MCP を統合したワークフローへの組み合わせ方
- アイデアからマージ済み PR までの完全な機能開発
- フックによる自動化
- チーム環境でのベストプラクティス

---

**[← Chapter 05 に戻る](../05-skills/README.md)** | **[Chapter 07 へ進む →](../07-putting-it-together/README.md)**
