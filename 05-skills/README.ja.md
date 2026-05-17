![Chapter 05: Skills System](images/chapter-header.png)

> **チームのベストプラクティスを、毎回説明しなくても Copilot が自動的に適用してくれたら？**

この章では、Agent Skills について学びます。Skills とは、タスクに関連するときに Copilot が自動的に読み込む、指示のフォルダーです。エージェントが Copilot の*思考方法*を変えるのに対し、Skills は*特定のタスクの完遂方法*を Copilot に教えます。セキュリティ監査スキルを作成して Copilot がセキュリティについて質問されたときに適用させたり、一貫したコード品質を保つチーム標準のレビュー基準を構築したり、Skills が Copilot CLI・VS Code・GitHub Copilot クラウドエージェントをまたいでどのように機能するかを学びます。


## 🎯 学習目標

この章を終えると、次のことができるようになります：

- Agent Skills の仕組みと使いどころを理解する
- SKILL.md ファイルを使ってカスタムスキルを作成する
- 共有リポジトリのコミュニティスキルを活用する
- Skills・エージェント・MCP の使い分けを判断できる

> ⏱️ **目安時間**：約55分（読書20分 + ハンズオン35分）

---

## 🧩 現実世界のたとえ：電動工具

汎用ドリルは便利ですが、専用のアタッチメントを付けることで真の力を発揮します。
<img src="images/power-tools-analogy.png" alt="Power Tools - Skills Extend Copilot's Capabilities" width="800"/>


Skills も同じ仕組みです。用途に応じてドリルビットを交換するように、Copilot に Skills を追加してさまざまなタスクに対応できます：

| スキルのアタッチメント | 目的 |
|------------|---------|
| `commit` | 一貫したコミットメッセージを生成する |
| `security-audit` | OWASP の脆弱性をチェックする |
| `generate-tests` | 包括的な pytest テストを作成する |
| `code-checklist` | チームのコード品質基準を適用する |



*Skills は Copilot の機能を拡張する専用アタッチメントです*

---

# Skills の仕組み

<img src="images/how-skills-work.png" alt="Glowing RPG-style skill icons connected by light trails on a starfield background representing Copilot skills" width="800"/>

Skills とは何か、なぜ重要なのか、エージェントや MCP との違いを学びましょう。

---

## *Skills が初めての方は* ここから始めよう！

1. **すでに使えるスキルを確認する：**
   ```bash
   copilot
   > /skills list
   ```
   これで、CLI 自体に同梱されている**組み込みスキル**や、プロジェクトおよび個人フォルダーにあるスキルも含め、Copilot が検出できるすべてのスキルが表示されます。

   > 💡 **組み込みスキル**：Copilot CLI にはあらかじめスキルがインストールされています。たとえば、`customizing-copilot-cloud-agents-environment` スキルは Copilot クラウドエージェントの環境カスタマイズのガイドを提供します。インストール不要でそのまま使えます。`/skills list` を実行して利用可能なスキルを確認しましょう。

2. **実際のスキルファイルを見てみる：** 提供されている [code-checklist SKILL.md](../.github/skills/code-checklist/SKILL.md) を確認してパターンをつかんでください。YAML フロントマターとマークダウンの指示を組み合わせただけのシンプルな構造です。

3. **コアコンセプトを理解する：** Skills は、プロンプトがスキルの説明と一致したときに Copilot が*自動的に*読み込む、タスク専用の指示です。有効化の操作は不要で、自然に質問するだけで機能します。


## Skills を理解する

Agent Skills とは、指示・スクリプト・リソースを含むフォルダーで、タスクに関連するときに Copilot が**自動的に読み込み**ます。Copilot はプロンプトを読み取り、どのスキルが一致するかを確認し、該当する指示を自動的に適用します。

```bash
copilot

> Check books.py against our quality checklist
# Copilot がこれを "code-checklist" スキルに一致すると判断し
# Python 品質チェックリストを自動的に適用します

> Generate tests for the BookCollection class
# Copilot が "pytest-gen" スキルを読み込み
# 好みのテスト構造を適用します

> What are the code quality issues in this file?
# Copilot が "code-checklist" スキルを読み込み
# チームの基準に照らしてチェックします
```

> 💡 **重要なポイント**：Skills はプロンプトがスキルの説明と一致するときに**自動的にトリガー**されます。自然に質問するだけで、Copilot が関連するスキルをバックグラウンドで適用してくれます。次に学ぶように、スキルを直接呼び出すこともできます。

> 🧰 **すぐに使えるテンプレート**：[.github/skills](../.github/skills/) フォルダーに、コピー＆ペーストで試せるシンプルなスキルが用意されています。

### スラッシュコマンドによる直接呼び出し

自動トリガーが Skills の主な動作方法ですが、スキル名をスラッシュコマンドとして使い**直接呼び出す**こともできます：

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

特定のスキルを確実に使いたいときに、明示的なコントロールが可能です。

#### 1つのメッセージで複数のスキルを組み合わせる

**1つのメッセージで複数のスキルを呼び出す**こともできます。スキルのスラッシュコマンドはプロンプトの先頭だけでなく、どこに書いても構いません。2つの異なるチェックを一度に行いたいときに便利です：

```bash
> Check @samples/book-app-project/book_app.py with /code-checklist and also run /generate-tests for it

> Review the auth module /security-audit then /code-checklist the result
```

Copilot は同じ応答の中で指定された各スキルを適用するため、複数のメッセージを送る手間が省けます。

> 💡 **ヒント**：スキルのスラッシュコマンドは文の中で最も自然な位置に書いてください。先頭・中間・末尾、どこでも問題ありません。

> 📝 **Skills と Agents の呼び出しの違い**：スキルの呼び出しとエージェントの呼び出しを混同しないようにしましょう：
> - **Skills**：`/skill-name <プロンプト>`、例：`/code-checklist Check this file`
> - **Agents**：`/agent`（リストから選択）または `copilot --agent <name>`（コマンドライン）
>
> 同じ名前（例："code-reviewer"）のスキルとエージェントが両方ある場合、`/code-reviewer` と入力すると**スキル**が呼び出されます（エージェントではありません）。

### スキルが使われたかどうかを確認するには

Copilot に直接聞くことができます：

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### Skills vs エージェント vs MCP

Skills は GitHub Copilot の拡張モデルの一部にすぎません。エージェントや MCP サーバーとの比較を見てみましょう。

> *MCP についてはまだ気にしなくて大丈夫です。[Chapter 06](../06-mcp-servers/) で詳しく説明します。ここでは Skills が全体像の中でどう位置づけられるかを把握するために紹介しています。*

<img src="images/skills-agents-mcp-comparison.png" alt="Comparison diagram showing the differences between Agents, Skills, and MCP Servers and how they combine into your workflow" width="800"/>

| 機能 | 役割 | 使いどころ |
|---------|--------------|-------------|
| **Agents** | AI の思考方法を変える | 多様なタスクにわたる専門的な知識が必要なとき |
| **Skills** | タスク固有の指示を提供する | 詳細な手順が必要な、繰り返し行う特定のタスク |
| **MCP** | 外部サービスに接続する | API からリアルタイムデータが必要なとき |

幅広い専門知識にはエージェントを、特定のタスク指示にはスキルを、外部データには MCP を使いましょう。エージェントは会話の中で1つ以上のスキルを活用できます。たとえばコードチェックをエージェントに依頼すると、`security-audit` スキルと `code-checklist` スキルの両方を自動的に適用することがあります。

> 📚 **さらに詳しく**：スキルのフォーマットとベストプラクティスの完全なリファレンスは、公式ドキュメント [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills) を参照してください。

---

## 手動プロンプトから自動的な専門知識へ

スキルの作り方に入る前に、*なぜ*学ぶ価値があるかを見てみましょう。一貫性の向上を実感すれば、「どうやって作るか」もスムーズに理解できます。

### Skills 導入前：バラバラなレビュー

毎回のコードレビューで何かを忘れてしまうかもしれません：

```bash
copilot

> Review this code for issues
# 汎用レビュー - チーム固有の懸念点を見落とす可能性があります
```

あるいは、毎回長いプロンプトを書く羽目になります：

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

入力時間：**30秒以上**。一貫性：**記憶次第**。

### Skills 導入後：自動的なベストプラクティス

`code-checklist` スキルがインストールされていれば、自然に聞くだけです：

```bash
copilot

> Check the book collection code for quality issues
```

**舞台裏で何が起きているか**：
1. Copilot がプロンプト中の「code quality」と「issues」を認識する
2. スキルの説明を確認し、`code-checklist` スキルが一致すると判断する
3. チームの品質チェックリストを自動的に読み込む
4. 項目を列挙しなくてもすべてのチェックを適用する

<img src="images/skill-auto-discovery-flow.png" alt="How Skills Auto-Trigger - 4-step flow showing how Copilot automatically matches your prompt to the right skill" width="800"/>

*自然に質問するだけ。Copilot がプロンプトを適切なスキルに照合し、自動的に適用します。*

**出力例**：
```
## Code Checklist: books.py

### Code Quality
- [PASS] All functions have type hints
- [PASS] No bare except clauses
- [PASS] No mutable default arguments
- [PASS] Context managers used for file I/O
- [PASS] Functions are under 50 lines
- [PASS] Variable and function names follow PEP 8

### Input Validation
- [FAIL] User input is not validated - add_book() accepts any year value
- [FAIL] Edge cases not fully handled - empty strings accepted for title/author
- [PASS] Error messages are clear and helpful

### Testing
- [FAIL] No corresponding pytest tests found

### Summary
3 items need attention before merge
```

**違い**：チームの基準が毎回自動的に適用されるため、わざわざ入力する必要がありません。

---

<details>
<summary>🎬 実際に動く様子を見てみよう！</summary>

![Skill Trigger Demo](images/skill-trigger-demo.gif)

*デモの出力は例示です。お使いのモデル・ツール・環境によって結果は異なります。*

</details>

---

## スケールでの一貫性：チーム PR レビュースキル

チームに10項目の PR チェックリストがあるとします。スキルがなければ、開発者全員が10項目を覚えなければならず、誰かが必ず1つ忘れてしまいます。`pr-review` スキルがあれば、チーム全体で一貫したレビューが実現します：

```bash
copilot

> Can you review this PR?
```

Copilot がチームの `pr-review` スキルを自動的に読み込み、10項目すべてをチェックします：

```
PR Review: feature/user-auth

## Security ✅
- No hardcoded secrets
- Input validation present
- No bare except clauses

## Code Quality ⚠️
- [WARN] print statement on line 45 - remove before merge
- [WARN] TODO on line 78 missing issue reference
- [WARN] Missing type hints on public functions

## Testing ✅
- New tests added
- Edge cases covered

## Documentation ❌
- [FAIL] Breaking change not documented in CHANGELOG
- [FAIL] API changes need OpenAPI spec update
```

**威力**：チームメンバー全員が同じ基準を自動的に適用できます。新メンバーはチェックリストを暗記する必要がなく、スキルが代わりにやってくれます。

---

# カスタムスキルの作成

<img src="images/creating-managing-skills.png" alt="Human and robotic hands building a wall of glowing LEGO-like blocks representing skill creation and management" width="800"/>

SKILL.md ファイルから独自のスキルを構築しましょう。

---

## スキルの保存場所

スキルは `.github/skills/`（プロジェクト固有）または `~/.copilot/skills/`（ユーザーレベル）に保存されます。

### Copilot がスキルを見つける方法

Copilot はスキルを探すために以下の場所を自動的にスキャンします：

| 場所 | スコープ |
|----------|-------|
| `.github/skills/` | プロジェクト固有（git 経由でチームと共有） |
| `~/.copilot/skills/` | ユーザー固有（個人用スキル） |

### スキルの構造

各スキルは `SKILL.md` ファイルを含む専用フォルダーに保存されます。スクリプト・例・その他のリソースを任意で追加することもできます：

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # 必須：スキルの定義と指示
    ├── examples/          # 任意：Copilot が参照できるサンプルファイル
    │   └── sample.py
    └── scripts/           # 任意：スキルが使用できるスクリプト
        └── validate.sh
```

> 💡 **ヒント**：ディレクトリ名は SKILL.md フロントマターの `name`（小文字・ハイフン区切り）と一致させましょう。

### SKILL.md のフォーマット

Skills は YAML フロントマター付きのシンプルなマークダウン形式を使用します：

```markdown
---
name: code-checklist
description: Comprehensive code quality checklist with security, performance, and maintainability checks
license: MIT
---

# Code Checklist

When checking code, look for:

## Security
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure

## Performance
- N+1 query problems (running one query per item instead of one query for all items)
- Unnecessary loops or computations
- Memory leaks
- Blocking operations

## Maintainability
- Function length (flag functions > 50 lines)
- Code duplication
- Missing error handling
- Unclear naming

## Output Format
Provide issues as a numbered list with severity:
- [CRITICAL] - Must fix before merge
- [HIGH] - Should fix before merge
- [MEDIUM] - Should address soon
- [LOW] - Nice to have
```

**YAML プロパティ：**

| プロパティ | 必須 | 説明 |
|----------|----------|-------------|
| `name` | **はい** | 一意の識別子（小文字、スペースはハイフン） |
| `description` | **はい** | スキルの役割と Copilot がいつ使うべきかの説明 |
| `license` | いいえ | このスキルに適用されるライセンス |

> 📖 **公式ドキュメント**：[About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### はじめてのスキルを作ろう

OWASP Top 10 の脆弱性をチェックするセキュリティ監査スキルを構築してみましょう：

```bash
# スキルディレクトリを作成する
mkdir -p .github/skills/security-audit

# SKILL.md ファイルを作成する
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Security Audit

Perform a security audit checking for:

## Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Authentication Issues
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Sensitive Data
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Access Control
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Output
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# スキルをテストする（スキルはプロンプトに基づいて自動的に読み込まれます）
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# Copilot が "security vulnerabilities" をスキルに一致すると判断し
# OWASP チェックリストを自動的に適用します
```

**期待される出力**（実際の結果は異なります）：

```
Security Audit: book-app-project

[HIGH] Hardcoded file path (book_app.py, line 12)
  File path is hardcoded rather than configurable
  Fix: Use environment variable or config file

[MEDIUM] No input validation (book_app.py, line 34)
  User input passed directly to function without sanitization
  Fix: Add input validation before processing

✅ No SQL injection found
✅ No hardcoded credentials found
```

---

## 優れたスキル説明の書き方

SKILL.md の `description` フィールドは非常に重要です！Copilot がスキルを読み込むかどうかを判断する根拠になります：

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **ヒント**：普段どのように質問するかを反映したキーワードを含めましょう。「security review」と言うなら、説明に「security review」を含めてください。

### Skills とエージェントを組み合わせる

Skills とエージェントは連携して動作します。エージェントが専門知識を提供し、スキルが具体的な指示を提供します：

```bash
# code-reviewer エージェントで起動する
copilot --agent code-reviewer

> Check the book app for quality issues
# code-reviewer エージェントの専門知識と
# code-checklist スキルのチェックリストが組み合わさります
```

---

# Skills の管理と共有

インストール済みスキルの確認、コミュニティスキルの探し方、自分のスキルの共有方法を学びましょう。

<img src="images/managing-sharing-skills.png" alt="Managing and Sharing Skills - showing the discover, use, create, and share cycle for CLI skills" width="800" />

---

## `/skills` コマンドでスキルを管理する

`/skills` コマンドでインストール済みスキルを管理できます：

| コマンド | 機能 |
|---------|--------------|
| `/skills list` | インストール済みスキルをすべて表示する |
| `/skills info <name>` | 特定のスキルの詳細を取得する |
| `/skills add <name>` | スキルを有効化する（リポジトリやマーケットプレイスから） |
| `/skills remove <name>` | スキルを無効化またはアンインストールする |
| `/skills reload` | SKILL.md を編集した後にスキルを再読み込みする |

> 💡 **覚えておこう**：プロンプトごとにスキルを「有効化」する必要はありません。インストールされていれば、プロンプトがスキルの説明に一致したときに**自動的にトリガー**されます。これらのコマンドは使用するためではなく、どのスキルが利用可能かを管理するためのものです。

### 例：スキルを確認する

```bash
copilot

> /skills list

Available skills:
- security-audit: Security-focused code review checking OWASP Top 10
- generate-tests: Generate comprehensive unit tests with edge cases
- code-checklist: Team code quality checklist
...

> /skills info security-audit

Skill: security-audit
Source: Project
Location: .github/skills/security-audit/SKILL.md
Description: Security-focused code review checking OWASP Top 10 vulnerabilities
```

---

<details>
<summary>実際に動く様子を見てみよう！</summary>

![List Skills Demo](images/list-skills-demo.gif)

*デモの出力は例示です。お使いのモデル・ツール・環境によって結果は異なります。*

</details>

---

### `/skills reload` を使うタイミング

スキルの SKILL.md を作成または編集した後、Copilot を再起動しなくても変更を反映するには `/skills reload` を実行します：

```bash
# スキルファイルを編集する
# その後 Copilot で：
> /skills reload
Skills reloaded successfully.
```

> 💡 **知っておくと便利**：`/compact` で会話履歴を要約した後も、スキルは有効なままです。コンパクト化の後に再読み込みする必要はありません。

---

## コミュニティスキルの探し方と使い方

### プラグインを使ってスキルをインストールする

> 💡 **プラグインとは？** プラグインは、Skills・エージェント・MCP サーバー設定をまとめてバンドルできるインストール可能なパッケージです。Copilot CLI の「アプリストア」拡張のようなものです。

`/plugin` コマンドでこれらのパッケージを閲覧・インストールできます：

```bash
copilot

> /plugin list
# インストール済みプラグインを表示する

> /plugin marketplace
# 利用可能なプラグインを閲覧する

> /plugin install <plugin-name>
# マーケットプレイスからプラグインをインストールする
```

ローカルのプラグインカタログを最新の状態に保つには、以下のコマンドで更新します：

```bash
copilot plugin marketplace update
```

プラグインは複数の機能をまとめてバンドルできます。1つのプラグインに、連携して動作する関連スキル・エージェント・MCP サーバー設定が含まれることもあります。

### コミュニティスキルリポジトリ

既製のスキルはコミュニティリポジトリからも入手できます：

- **[Awesome Copilot](https://github.com/github/awesome-copilot)** - スキルのドキュメントや例を含む GitHub Copilot の公式リソース

### GitHub CLI でコミュニティスキルをインストールする

GitHub リポジトリからスキルをインストールする最も簡単な方法は `gh skill install` コマンドです（[GitHub CLI v2.90.0+](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) が必要）：

```bash
# awesome-copilot からインタラクティブにスキルを選択してインストールする
gh skill install github/awesome-copilot

# または特定のスキルを直接インストールする
gh skill install github/awesome-copilot code-checklist

# すべてのプロジェクトで使う個人用としてインストールする（ユーザースコープ）
gh skill install github/awesome-copilot code-checklist --scope user
```

> ⚠️ **インストール前に確認**：スキルをインストールする前に必ず SKILL.md を読んでください。Skills は Copilot の動作を制御するため、悪意のあるスキルが有害なコマンドの実行や予期しないコードの変更を指示する可能性があります。

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

学んだことを活かして、自分だけのスキルを構築・テストしてみましょう。

---

## ▶️ 自分で試してみよう

### さらにスキルを作ろう

以下に2つのスキルの例を示します。それぞれ異なるパターンを使っています。上の「はじめてのスキルを作ろう」と同じ `mkdir` + `cat` の手順に従うか、ファイルを適切な場所にコピー＆ペーストしてください。さらに多くの例は [.github/skills](../.github/skills) にあります。

### pytest テスト生成スキル

コードベース全体で一貫した pytest 構造を保証するスキルです：

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: Generate comprehensive pytest tests with fixtures and edge cases
---

# pytest Test Generation

Generate pytest tests that include:

## Test Structure
- Use pytest conventions (test_ prefix)
- One assertion per test when possible
- Clear test names describing expected behavior
- Use fixtures for setup/teardown

## Coverage
- Happy path scenarios
- Edge cases: None, empty strings, empty lists
- Boundary values
- Error scenarios with pytest.raises()

## Fixtures
- Use @pytest.fixture for reusable test data
- Use tmpdir/tmp_path for file operations
- Mock external dependencies with pytest-mock

## Output
Provide complete, runnable test file with proper imports.
EOF
```

### チーム PR レビュースキル

チーム全体で一貫した PR レビュー基準を強制するスキルです：

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# PR Review

Review code changes against team standards:

## Security Checklist
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] No bare except clauses
- [ ] No sensitive data in logs

## Code Quality
- [ ] Functions under 50 lines
- [ ] No print statements in production code
- [ ] Type hints on public functions
- [ ] Context managers for file I/O
- [ ] No TODOs without issue references

## Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentation
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Output Format
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

### さらに挑戦しよう

1. **スキル作成チャレンジ**：3点チェックリストを行う `quick-review` スキルを作ってみましょう：
   - bare except 節
   - 型ヒントの欠落
   - 不明瞭な変数名

   テスト方法：「Do a quick review of books.py」と質問してみましょう。

2. **スキル比較**：詳細なセキュリティレビュープロンプトを手動で書くのにかかる時間を計ってみましょう。次に「Check for security issues in this file」とだけ質問して、security-audit スキルが自動的に読み込まれるのを見てみましょう。スキルによってどれだけ時間が節約できましたか？

3. **チームスキルチャレンジ**：あなたのチームのコードレビューチェックリストについて考えてみましょう。スキルとしてエンコードできますか？スキルが常にチェックすべき3つの項目を書き出してみましょう。

**理解度の確認**：`description` フィールドが重要な理由（Copilot がスキルを読み込むかどうかを判断する根拠になる）を説明できれば、Skills を理解しています。

---

## 📝 課題

### メインチャレンジ：Book Summary スキルを作ろう

上の例では `pytest-gen` と `pr-review` スキルを作成しました。今度は全く異なる種類のスキルを練習しましょう：データからフォーマットされた出力を生成するスキルです。

1. 現在のスキルを一覧表示する：Copilot を起動して `/skills list` を実行します。`ls .github/skills/` でプロジェクトスキルを、`ls ~/.copilot/skills/` で個人スキルを確認することもできます。
2. `.github/skills/book-summary/SKILL.md` に `book-summary` スキルを作成します。このスキルはブックコレクションのフォーマットされたマークダウンサマリーを生成します。
3. スキルに含めること：
   - 明確な name と description（description はマッチングに重要！）
   - 具体的なフォーマットルール（例：タイトル・著者・年・既読ステータスのマークダウンテーブル）
   - 出力規則（例：既読ステータスに ✅/❌ を使う、年順でソートする）
4. スキルをテストする：`@samples/book-app-project/data.json Summarize the books in this collection`
5. `/skills list` でスキルが自動トリガーされるか確認する
6. `/book-summary Summarize the books in this collection` で直接呼び出してみる

**成功基準**：ブックコレクションについて質問したときに Copilot が自動的に適用する、動作する `book-summary` スキルが完成していること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**スターターテンプレート**：`.github/skills/book-summary/SKILL.md` を作成します：

```markdown
---
name: book-summary
description: Generate a formatted markdown summary of a book collection
---

# Book Summary Generator

Generate a summary of the book collection following these rules:

1. Output a markdown table with columns: Title, Author, Year, Status
2. Use ✅ for read books and ❌ for unread books
3. Sort by year (oldest first)
4. Include a total count at the bottom
5. Flag any data issues (missing authors, invalid years)

Example:
| Title | Author | Year | Status |
|-------|--------|------|--------|
| 1984 | George Orwell | 1949 | ✅ |
| Dune | Frank Herbert | 1965 | ❌ |

**Total: 2 books (1 read, 1 unread)**
```

**テスト方法：**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# スキルが description のマッチによって自動トリガーされるはずです
```

**トリガーされない場合：** `/skills reload` を実行してからもう一度質問してみましょう。

</details>

### ボーナスチャレンジ：Commit Message スキル

1. 一貫したフォーマットでコンベンショナルコミットメッセージを生成する `commit-message` スキルを作成しましょう
2. 変更をステージングして「Generate a commit message for my staged changes」と質問してテストしましょう
3. スキルをドキュメント化し、`copilot-skill` トピックを付けて GitHub で共有しましょう

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起きるか | 修正方法 |
|---------|--------------|-----|
| `SKILL.md` 以外のファイル名を使う | スキルが認識されない | ファイル名は正確に `SKILL.md` でなければなりません |
| `description` フィールドが曖昧 | スキルが自動的に読み込まれない | description はPRIMARYな検出の仕組みです。具体的なトリガーワードを使いましょう |
| フロントマターに `name` または `description` がない | スキルの読み込みに失敗する | YAML フロントマターに両方のフィールドを追加しましょう |
| フォルダーの場所が間違っている | スキルが見つからない | プロジェクト用は `.github/skills/skill-name/`、個人用は `~/.copilot/skills/skill-name/` を使いましょう |

### トラブルシューティング

**スキルが使われない** - 期待通りにスキルが使われない場合：

1. **description を確認する**：質問の仕方と一致していますか？
   ```markdown
   # 悪い例：曖昧すぎる
   description: Reviews code

   # 良い例：トリガーワードが含まれている
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **ファイルの場所を確認する**：
   ```bash
   # プロジェクトスキル
   ls .github/skills/

   # ユーザースキル
   ls ~/.copilot/skills/
   ```

3. **SKILL.md のフォーマットを確認する**：フロントマターは必須です：
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

**スキルが表示されない** - フォルダー構造を確認しましょう：
```
.github/skills/
└── my-skill/           # フォルダー名
    └── SKILL.md        # 正確に SKILL.md でなければなりません（大文字・小文字を区別）
```

スキルを作成または編集した後は `/skills reload` を実行して変更が反映されるようにしましょう。

**スキルが読み込まれるかテストする** - Copilot に直接聞いてみましょう：
```bash
> What skills do you have available for checking code quality?
# Copilot が見つけた関連スキルを説明します
```

**スキルが実際に動作しているか確認するには？**

1. **出力フォーマットを確認する**：スキルが出力フォーマット（`[CRITICAL]` タグなど）を指定している場合、応答の中にそれが含まれているか確認しましょう
2. **直接聞く**：応答を受け取った後、「Did you use any skills for that?」と質問しましょう
3. **あり/なしで比較する**：`--no-custom-instructions` を使って同じプロンプトを試し、違いを確認しましょう：
   ```bash
   # スキルあり
   copilot --allow-all -p "Review @file.py for security issues"

   # スキルなし（ベースライン比較）
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **特定のチェックを確認する**：スキルに特定のチェック（「50行を超える関数」など）が含まれている場合、それが出力に現れているか確認しましょう

</details>

---

# まとめ

## 🔑 重要なポイント

1. **Skills は自動的**：プロンプトがスキルの description に一致すると Copilot が読み込みます
2. **直接呼び出し**：スラッシュコマンドとして `/skill-name` でスキルを直接呼び出すこともできます
3. **SKILL.md フォーマット**：YAML フロントマター（name・description・任意の license）とマークダウンの指示
4. **場所が重要**：`.github/skills/` はプロジェクト・チームでの共有用、`~/.copilot/skills/` は個人用
5. **description がカギ**：普段どのように質問するかに合わせた description を書きましょう

> 📋 **クイックリファレンス**：コマンドとショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次のステップ

Skills は自動読み込みされる指示で Copilot の機能を拡張します。では、外部サービスへの接続はどうでしょうか？そこで登場するのが MCP です。

**[Chapter 06: MCP Servers](../06-mcp-servers/README.md)** では以下を学びます：

- MCP（Model Context Protocol）とは何か
- GitHub・ファイルシステム・ドキュメントサービスへの接続
- MCP サーバーの設定
- 複数サーバーを使ったワークフロー

---

**[← Chapter 04 に戻る](../04-agents-custom-instructions/README.md)** | **[Chapter 06 に進む →](../06-mcp-servers/README.md)**
