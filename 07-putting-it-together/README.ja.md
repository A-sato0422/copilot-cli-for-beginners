![Chapter 07: Putting It All Together](images/chapter-header.png)

> **これまで学んだすべてがここで結集します。アイデアからマージ済みPRまでを、1つのセッションで実現しましょう。**

この章では、これまで学んできたことをすべて組み合わせて、完全なワークフローを構築します。マルチエージェント連携を使った機能開発、コミット前にセキュリティ問題を検出するプリコミットフックの設定、CI/CDパイプラインへのCopilot統合、そして機能のアイデアから1つのターミナルセッションでマージ済みPRまでを実現します。ここで、GitHub Copilot CLI は真の「力の乗数」となります。

> 💡 **Note**: この章では、これまで学んだすべてを組み合わせる方法を紹介します。**エージェント、スキル、MCPがなくても生産的に作業できます（もちろんあると非常に便利ですが）。** コアワークフロー — 記述・計画・実装・テスト・レビュー・リリース — は第00〜03章の組み込み機能だけで動作します。

## 🎯 学習目標

この章を終えると、次のことができるようになります：

- エージェント、スキル、MCP (Model Context Protocol) を統合されたワークフローに組み合わせる
- マルチツールアプローチで完全な機能を構築する
- フックを使った基本的な自動化を設定する
- プロフェッショナルな開発のベストプラクティスを実践する

> ⏱️ **目安時間**：約75分（読書15分 + ハンズオン60分）

---

## 🧩 現実世界のアナロジー：オーケストラ

<img src="images/orchestra-analogy.png" alt="Orchestra Analogy - Unified Workflow" width="800"/>

交響楽団にはさまざまなパートがあります：
- **弦楽器**は基盤を提供します（コアワークフローのように）
- **金管楽器**はパワーを加えます（専門知識を持つエージェントのように）
- **木管楽器**は色彩を加えます（機能を拡張するスキルのように）
- **打楽器**はリズムを刻みます（外部システムへ接続するMCPのように）

それぞれのパートだけでは音に限界があります。しかし、優れた指揮のもとで合わさることで、壮大な音楽が生まれます。

**それがこの章で学ぶことです！**<br>
*オーケストラを指揮する指揮者のように、エージェント・スキル・MCPを統合されたワークフローへと指揮します*

まずは、コードの変更・テスト生成・レビュー・PR作成をすべて1つのセッションで行うシナリオを見ていきましょう。

---

## アイデアからマージ済みPRまでを1セッションで

エディタ・ターミナル・テストランナー・GitHub UIを切り替えながらコンテキストを失い続ける代わりに、すべてのツールを1つのターミナルセッションに集約できます。このパターンについては、後述の[統合パターン](#統合パターン-上級者向け)セクションで詳しく説明します。

```bash
# インタラクティブモードでCopilotを起動
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilotが大まかなプランを作成...

# PYTHON-REVIEWER エージェントに切り替え
> /agent
# "python-reviewer" を選択

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# python-reviewerエージェントが以下を生成：
# - メソッドのシグネチャと戻り値の型
# - リスト内包表記を使ったフィルタ実装
# - 空のコレクションに対するエッジケース処理

# PYTEST-HELPER エージェントに切り替え
> /agent
# "pytest-helper" を選択

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# pytest-helperエージェントが以下を生成：
# - 空コレクション用テストケース
# - 既読・未読が混在する場合のテストケース
# - すべて既読の場合のテストケース

# 実装
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# テスト
> Generate comprehensive tests for the new feature

# 以下のような複数のテストが生成されます：
# - ハッピーパス（3テスト）— 正しいフィルタリング、既読の除外、未読の包含
# - エッジケース（4テスト）— 空コレクション、全既読、全未読、1冊のみ
# - パラメータ化（5ケース）— @pytest.mark.parametrize を使った既読/未読比率の変化
# - 統合（4テスト）— mark_as_read、remove_book、add_book、データ整合性との連携

# 変更をレビュー
> /review

# レビューが通ったら、/pr を使って現在のブランチのプルリクエストを操作
> /pr [view|create|fix|auto]

# またはCopilotに自然な言葉でドラフト作成を依頼することも可能
> Create a pull request titled "Feature: Add list unread books command"
```

**従来のアプローチ**：エディタ・ターミナル・テストランナー・ドキュメント・GitHub UIを行き来する。切り替えのたびにコンテキストが失われ、摩擦が生じます。

**重要な気づき**：あなたはアーキテクトとしてスペシャリストたちを指揮しました。詳細はスペシャリストが担い、ビジョンはあなたが担います。

> 💡 **さらに発展させるには**：このような大規模なマルチステッププランには、`/fleet` を試してみましょう。独立したサブタスクをCopilotに並列実行させられます。詳細は[公式ドキュメント](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet)を参照してください。

---

# 追加ワークフロー

<img src="images/combined-workflows.png" alt="People assembling a colorful giant jigsaw puzzle with gears, representing how agents, skills, and MCP combine into unified workflows" width="800"/>

第04〜06章を完了した上級者向けに、エージェント・スキル・MCPがいかに効果を高めるかを示すワークフローを紹介します。

## 統合パターン

すべてを組み合わせるためのメンタルモデルです：

<img src="images/integration-pattern.png" alt="The Integration Pattern - A 4-phase workflow: Gather Context (MCP), Analyze and Plan (Agents), Execute (Skills + Manual), Complete (MCP)" width="800"/>

---

## ワークフロー1：バグ調査と修正

全ツール統合による実践的なバグ修正：

```bash
copilot

# フェーズ1：GitHubからバグを理解する（MCPが提供）
> Get the details of issue #1

# 判明：「find_by_authorが部分名で動作しない」

# フェーズ2：ベストプラクティスを調査（Webおよびソースを含む深い調査）
> /research Best practices for Python case-insensitive string matching

# フェーズ3：関連コードを見つける
> @samples/book-app-project/books.py Show me the find_by_author method

# フェーズ4：専門家の分析を得る
> /agent
# "python-reviewer" を選択

> Analyze this method for issues with partial name matching

# エージェントが特定：メソッドが部分文字列マッチではなく完全一致を使用している

# フェーズ5：エージェントの指示に従って修正
> Implement the fix using lowercase comparison and 'in' operator

# フェーズ6：テストを生成
> /agent
# "pytest-helper" を選択

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# フェーズ7：コミットとPR
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## ワークフロー2：コードレビューの自動化（オプション）

> 💡 **このセクションはオプションです。** プリコミットフックはチームにとって便利ですが、生産性を上げるために必須ではありません。始めたばかりの方はスキップして構いません。
>
> ⚠️ **パフォーマンスに関する注意**：このフックはステージングされた各ファイルに対して `copilot -p` を呼び出すため、1ファイルあたり数秒かかります。大きなコミットの場合は、重要なファイルだけに絞るか、`/review` を使って手動でレビューすることを検討してください。

**gitフック**とは、Gitが特定のタイミング（例：コミット直前）に自動的に実行するスクリプトです。これを使ってコードの自動チェックを行えます。コミットに対して自動的にCopilotレビューを実行する方法は以下のとおりです：

```bash
# プリコミットフックを作成
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# ステージングされたファイルを取得（Pythonファイルのみ）
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # タイムアウトを使ってハングを防止（1ファイルあたり60秒）
    # --allow-all はファイルの読み書きを自動承認し、フックを無人実行可能にします。
    # これは自動化スクリプトのみで使用してください。インタラクティブセッションではCopilotに許可を求めさせましょう。
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # タイムアウト発生を確認
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> ⚠️ **macOSユーザー向け**：macOSには `timeout` コマンドがデフォルトで含まれていません。`brew install coreutils` でインストールするか、タイムアウトガードなしのシンプルな呼び出しに置き換えてください。

> 📚 **公式ドキュメント**：完全なフックAPIについては [Use hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) と [Hooks configuration reference](https://docs.github.com/copilot/reference/hooks-configuration) を参照してください。
>
> 💡 **組み込みの代替手段**：Copilot CLIにはプリコミットなどのイベントで自動的に実行できる組み込みフックシステム（`copilot hooks`）も備わっています。上記の手動gitフックは完全なコントロールを提供し、組み込みシステムは設定がよりシンプルです。どちらが自分のワークフローに合うか上記のドキュメントで確認しましょう。

これで毎回のコミットに簡易セキュリティレビューが実行されます：

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# 出力例：
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## ワークフロー3：新しいコードベースへのオンボーディング

新しいプロジェクトに参加するとき、コンテキスト・エージェント・MCPを組み合わせて素早くキャッチアップできます：

```bash
# インタラクティブモードでCopilotを起動
copilot

# フェーズ1：コンテキストを使って全体像を把握
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# フェーズ2：特定のフローを理解する
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# フェーズ3：エージェントで専門的な分析を得る
> /agent
# "python-reviewer" を選択

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# フェーズ4：取り組む課題を見つける（MCPがGitHubアクセスを提供）
> List open issues labeled "good first issue"

# フェーズ5：コントリビュートを始める
> Pick the simplest open issue and outline a plan to fix it
```

このワークフローは `@` コンテキスト・エージェント・MCPを1つのオンボーディングセッションに組み合わせており、この章の前半で紹介した統合パターンそのものです。

---

# ベストプラクティスと自動化

ワークフローをより効果的にするためのパターンと習慣です。

---

## ベストプラクティス

### 1. 分析の前にコンテキストを収集する

分析を依頼する前に必ずコンテキストを集めましょう：

```bash
# 良い例
> Get the details of issue #42
> /agent
# python-reviewer を選択
> Analyze this issue

# 効果が低い例
> /agent
# python-reviewer を選択
> Fix login bug
# エージェントがイシューのコンテキストを持っていない
```

### 2. エージェント・スキル・カスタム命令の違いを理解する

それぞれのツールには得意な場面があります：

```bash
# エージェント：明示的に起動する専門ペルソナ
> /agent
# python-reviewer を選択
> Review this authentication code for security issues

# スキル：プロンプトがスキルの説明と一致したときに自動起動するモジュール機能
# （まず作成が必要 — 第05章参照）
> Generate comprehensive tests for this code
# テスト用スキルが設定されていれば自動的に起動する

# カスタム命令（.github/copilot-instructions.md）：切り替えや起動なしに
# すべてのセッションに常時適用されるガイダンス
```

> 💡 **ポイント**：エージェントもスキルもコードの分析と生成の両方ができます。本当の違いは**起動方法**にあります — エージェントは明示的（`/agent`）、スキルは自動（プロンプトマッチ）、カスタム命令は常時オンです。

### 3. セッションを集中させる

`/rename` でセッションにラベルを付け（履歴から探しやすくなります）、`/exit` でクリーンに終了しましょう：

```bash
# 良い例：1セッションに1機能
> /rename list-unread-feature
# list unread の作業
> /exit

copilot
> /rename export-csv-feature
# CSV エクスポートの作業
> /exit

# 効果が低い例：すべてを1つの長いセッションで処理する
```

### 4. Copilotでワークフローを再利用可能にする

ワークフローをwikiに記録するだけでなく、Copilotが活用できるようリポジトリに直接組み込みましょう：

- **カスタム命令**（`.github/copilot-instructions.md`）：コーディング規約・アーキテクチャルール・ビルド/テスト/デプロイ手順の常時オンガイダンス。すべてのセッションで自動的に適用されます。
- **プロンプトファイル**（`.github/prompts/`）：チームで共有できる再利用可能なパラメータ化プロンプト — コードレビュー・コンポーネント生成・PR説明のテンプレートのようなものです。
- **カスタムエージェント**（`.github/agents/`）：専門ペルソナ（セキュリティレビュアーやドキュメントライターなど）をエンコードし、チームの誰でも `/agent` で起動できます。
- **カスタムスキル**（`.github/skills/`）：関連するときに自動起動するステップバイステップのワークフロー手順をパッケージ化します。

> 💡 **メリット**：新しいチームメンバーがあなたのワークフローを無料で手に入れられます — 誰かの頭の中に閉じ込められることなく、リポジトリに組み込まれています。

---

## ボーナス：プロダクション向けパターン

これらのパターンはオプションですが、プロフェッショナルな環境で非常に役立ちます。

### PRの説明文ジェネレーター

```bash
# 包括的なPR説明を生成
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### CI/CDとの統合

既存のCI/CDパイプラインを持つチーム向けに、GitHub Actionsを使ってすべてのプルリクエストに対してCopilotレビューを自動化できます。レビューコメントの自動投稿や重大な問題のフィルタリングも含まれます。

> 📖 **詳細はこちら**：完全なGitHub Actionsワークフロー、設定オプション、トラブルシューティングのヒントについては [CI/CD Integration](../appendices/ci-cd-integration.md) を参照してください。

---

# 実践

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

完全なワークフローを実践してみましょう。

---

## ▶️ 自分でやってみよう

デモを終えたら、以下のバリエーションを試してみましょう：

1. **エンドツーエンドチャレンジ**：小さな機能（例：「未読本の一覧表示」または「CSVへのエクスポート」）を選んでください。完全なワークフローを使います：
   - `/plan` で計画を立てる
   - エージェントでデザイン（python-reviewer、pytest-helper）
   - 実装する
   - テストを生成する
   - PRを作成する

2. **自動化チャレンジ**：「コードレビューの自動化」ワークフローのプリコミットフックを設定してください。意図的なファイルパス脆弱性を含むコミットを作成してみましょう。ブロックされますか？

3. **あなたのプロダクションワークフロー**：自分がよく行う作業のための独自ワークフローを設計してください。チェックリストとして書き出しましょう。スキル・エージェント・フックで自動化できる部分はどこでしょうか？

**自己確認**：エージェント・スキル・MCPがどのように連携するか、そしてそれぞれをいつ使うべきかを同僚に説明できれば、このコースを完了したと言えます。

---

## 📝 課題

### メインチャレンジ：エンドツーエンドの機能開発

ハンズオン例では「未読本の一覧表示」機能の構築を行いました。次は別の機能で完全なワークフローを練習しましょう：**出版年の範囲で本を検索する**：

1. Copilotを起動してコンテキストを収集：`@samples/book-app-project/books.py`
2. `/plan` で計画：`/plan Add a "search by year" command that lets users find books published between two years`
3. `BookCollection` に `find_by_year_range(start_year, end_year)` メソッドを実装する
4. `book_app.py` に、ユーザーに開始年と終了年を入力させる `handle_search_year()` 関数を追加する
5. テストを生成：`@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. `/review` でレビューする
7. READMEを更新：`@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. コミットメッセージを生成する

作業しながらワークフローを記録しましょう。

**成功基準**：計画・実装・テスト・ドキュメント・レビューを含めて、Copilot CLIを使ってアイデアからコミットまでの機能開発を完了できた。

> 💡 **ボーナス**：第04章でエージェントを設定済みの場合は、カスタムエージェントを作成して活用してみましょう。例えば、実装レビュー用のエラーハンドラーエージェントや、READMEの更新用のドキュメントライターエージェントなどです。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**この章の冒頭にある [「アイデアからマージ済みPRまで」](#アイデアからマージ済みprまでを1セッションで) 例のパターンに従ってください。** 主なステップは以下のとおりです：

1. `@samples/book-app-project/books.py` でコンテキストを収集する
2. `/plan Add a "search by year" command` で計画を立てる
3. メソッドとコマンドハンドラを実装する
4. エッジケース（無効な入力、空の結果、逆順の範囲）を含むテストを生成する
5. `/review` でレビューする
6. `@samples/book-app-project/README.md` でREADMEを更新する
7. `-p` でコミットメッセージを生成する

**考慮すべきエッジケース：**
- ユーザーが「2000」と「1990」（逆順の範囲）を入力した場合は？
- 範囲に一致する本がない場合は？
- ユーザーが数値以外の入力をした場合は？

**重要なのは完全なワークフローを練習すること**：アイデア → コンテキスト → 計画 → 実装 → テスト → ドキュメント → コミット。

</details>

---

<details>
<summary>🔧 <strong>よくあるミス</strong>（クリックして展開）</summary>

| ミス | 何が起きるか | 対処法 |
|------|-------------|--------|
| いきなり実装に飛びつく | 後から修正コストが高い設計上の問題を見落とす | まず `/plan` でアプローチを考え抜く |
| 1つのツールだけを使う | 遅く、不十分な結果になる | 組み合わせる：分析にエージェント → 実行にスキル → 統合にMCP |
| コミット前にレビューしない | セキュリティ問題やバグが紛れ込む | 常に `/review` を実行するか、[プリコミットフック](#ワークフロー2コードレビューの自動化オプション)を使う |
| ワークフローをチームと共有しない | 各自が車輪を再発明する | 共有のエージェント・スキル・命令としてパターンを記録する |

</details>

---

# まとめ

## 🔑 重要なポイント

1. **統合 > 孤立**：ツールを組み合わせて最大の効果を引き出す
2. **コンテキストを先に**：分析の前に必要なコンテキストを集める
3. **エージェントは分析、スキルは実行**：適切なツールを適切な場面で使う
4. **繰り返しを自動化**：フックとスクリプトで効果を倍増させる
5. **ワークフローを記録する**：共有できるパターンはチーム全体を助ける

> 📋 **クイックリファレンス**：コマンドとショートカットの完全な一覧は [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## 🎓 コース修了！

おめでとうございます！あなたが学んだこと：

| 章 | 学習内容 |
|----|---------|
| 00 | Copilot CLI のインストールとクイックスタート |
| 01 | 3つのインタラクションモード |
| 02 | `@` 構文によるコンテキスト管理 |
| 03 | 開発ワークフロー |
| 04 | 専門化されたエージェント |
| 05 | 拡張可能なスキル |
| 06 | MCPによる外部接続 |
| 07 | 統合されたプロダクションワークフロー |

あなたは今、GitHub Copilot CLI を開発ワークフローの真の「力の乗数」として活用する準備が整いました。

## ➡️ 次のステップ

学びはここで終わりません：

1. **毎日実践する**：実際の作業でCopilot CLIを使う
2. **カスタムツールを構築する**：自分のニーズに合ったエージェントとスキルを作成する
3. **知識を共有する**：チームがこれらのワークフローを採用するのを手伝う
4. **最新情報をチェックする**：GitHub Copilotのアップデートで新機能を把握する

### リソース

- [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Community Skills](https://github.com/topics/copilot-skill)

---

**よくできました！さあ、素晴らしいものを作りましょう。**

**[← 第06章に戻る](../06-mcp-servers/README.md)** | **[コースホームに戻る →](../README.md)**
