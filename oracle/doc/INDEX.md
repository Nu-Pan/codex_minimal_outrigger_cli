# `app_spec`

## Summary
- cmoc のアプリケーションとしての外部挙動と横断実行規則を扱う正本仕様断片のまとまり。利用者ワークフロー、CLI サブコマンド、セッション・apply 状態、run 隔離、Codex CLI 呼び出し、ログ、エラー、補完、インデクシング、プロンプト規範などを確認する入口になる。
- 個別サブコマンドの引数、事前条件、状態遷移、branch/worktree 操作、Codex CLI や agent call に委ねる境界、stdout・report・終了コードの仕様へ進むための領域。
- cmoc が作業対象リポジトリをどの前提で扱い、実行中の状態・ログ・生成物・補完プローブ・INDEX 更新・プロンプト文面をどう制御するかを、実装差を避けたい範囲で定める。

## Read this when
- cmoc の利用者向け CLI 挙動、標準ワークフロー、サブコマンドの呼び出し順、引数、事前条件、正常系・失敗系、出力、終了コードを実装・修正・テストするとき。
- session の開始・終了・破棄、apply の開始・取込・破棄、oracle review、初期化、明示インデクシング、AI Agent CLI/TUI 起動など、サブコマンド単位の正本仕様を探すとき。
- セッション状態ファイル、apply 状態、run 用 branch/worktree、作業隔離、作業対象リポジトリの前提、管理 branch 上の変更範囲など、複数サブコマンドにまたがる制御モデルを確認するとき。
- cmoc から Codex CLI を呼び出す方法、profile・環境変数・stdin・stdout/stderr・Structured Output・retry/resume・quota 待機・並列実行・編集禁止領域の扱いを確認するとき。
- サブコマンド実行中のコンソール出力、ログファイル、時間・パス表記、共通エラー処理、補完プローブ時の副作用抑制、INDEX.md 自動生成・更新のタイミングを扱うとき。
- agent に渡すプロンプトや人間向けレポートの文面で、cmoc 固有概念をどう解決して渡すか、日本語と英語識別子をどう使い分けるかを判断するとき。

## Do not read this when
- oracle file と realization file の基本定義、編集主体、正本性、責務分担だけを確認したいときは、基礎概念を扱う文書を読む。
- パスキーワードや root 種別そのものの定義、パス解決の実装詳細だけを確認したいときは、パスモデルの仕様または実装へ直接進む。
- 個別の Codex CLI 呼び出しごとの具体的な AgentCallParameter、builder の引数構築、schema 定義そのものを確認したいだけなら、対応する builder や schema 実装を読む。
- realization file の分割、抽象化、依存追加、テスト肥大化抑制など、実装品質基準だけを判断したいときは、realization 向けの規範を読む。
- 特定の実装ファイル、テストファイル、helper のコード構造、既存挙動、内部関数名を調べたいだけなら、対象の realization implementation または realization test へ進む。
- 通常の git 操作一般、任意 branch の汎用 merge、join 済み結果の rollback、旧サブコマンド互換など、現行 cmoc のアプリ仕様が対象外としている機能を探しているとき。

## hash
- 05dc9c9ba9708ac26f1b583161188fa7f34ac1303c69e012441476df848f5507

# `branch_model.md`

## Summary
- cmoc が通常の local branch から session branch を作り、run ごとに session branch から run branch と linked worktree を分離して扱う git branch / commit / worktree モデルを定義する。
- repository default branch を特別扱いせず、session fork 時点の local branch を session home branch として扱う方針、cmoc-managed branch の命名規則、fork / join commit の用語を確認する入口になる。

## Read this when
- cmoc session fork / join や run 系サブコマンドが、どの branch を作成し、どの branch を分岐元・merge 先として扱うべきかを確認したいとき。
- cmoc-managed branch、session branch、session home branch、run branch、apply / review などのサブコマンド別 branch 名の関係を実装・テストする前。
- run の作業内容を session branch や repo root から隔離するための branch / linked worktree の責務、命名規則、commit 用語を確認したいとき。
- repository default branch、local branch、remote-tracking branch が cmoc 管理対象かどうか、また default branch を特別扱いしないことを確認したいとき。

## Do not read this when
- oracle file と realization file の責務分担、正本仕様断片としての扱い、INDEX.md エントリー作成基準を確認したいだけのとき。
- path キーワードや repo root / run root / work root の一般的な定義を確認したいとき。
- git branch / commit / worktree の cmoc 用語ではなく、CLI 出力形式、設定項目、永続状態、実装品質基準、テスト肥大化抑制の一般方針を調べたいとき。

## hash
- 3548445dc5441fa2e2e774ba8b45d8bdaaf363b110f5e8a3f4704bdac6cdf3af

# `considered_alternative`

## Summary
- 採用しなかった設計案とその理由を集めた、正本仕様断片内の不採用判断の入口。
- 対象は、AI の記憶・改善案の自動注入、作業計画を人間がレビューする workflow、apply 系処理で修正点リストアップ後に独立した計画立案ステップを置く案など、cmoc が採らない方向性の設計根拠である。
- 採用済み仕様の詳細ではなく、なぜ特定の代替案を避け、oracle、INDEX、ログ、実行成果物、次回の修正点リストアップなどを軸にした設計へ寄せるのかを確認するためのルーティング対象である。

## Read this when
- cmoc の設計で、一般的には有効に見える workflow、memory、kaizen、作業計画、計画レビューなどの案を採用しない理由を確認したいとき。
- AI が過去の実行結果、失敗分析、改善案、継続指示を後続実行へ自動で引き継ぐ仕組みを追加すべきか判断しているとき。
- 人間と AI の責務分担として、人間が作業計画をレビューする方式ではなく、人間が正本仕様断片を編集し AI が実装可能性を評価して追従する方式の背景を確認したいとき。
- apply 系の処理設計で、修正点リストアップ後に独立した作業計画生成ステップを挟む案や、そのトークン消費削減効果を検討しているとき。
- oracle 以外に暗黙仕様や準仕様レイヤーが増えること、または人間の認知負荷を増やす共同管理対象ができることを避ける判断根拠を確認したいとき。

## Do not read this when
- 採用済みの CLI 入出力、状態遷移、具体的なサブコマンド挙動を確認したいとき。
- oracle file、realization file、INDEX、ログ、実行成果物の一般的な定義、配置、生成手順を確認したいだけのとき。
- 個別の kaizen 文面、レビュー観点、改善提案の中身を設計したいだけで、後続実行への自動注入可否を扱わないとき。
- 修正点リストアップそのものの仕様や、リストアップ内容を具体的に充実させる方法を探しているとき。
- 実装ファイル、テスト、補助ファイルの具体的な変更方針やコード上の責務境界を調べたいとき。

## hash
- 1ad6daf0acaae977b28c2cbee5e1760cf36356b75d12c6cf142e4f3d962482f2

# `dev_rule`

## Summary
- cmoc の開発時に従う横断的な規則群への入口。Python 実装の書き方、CLI 構成と共通処理の配置、開発環境、テスト方針を扱う正本仕様断片をまとめている。
- 個別機能の利用者向け仕様ではなく、realization code を追加・修正・検証するときの共通判断基準を確認するための領域である。

## Read this when
- Python の実装またはテストを追加・変更する前に、型ヒント、import、docstring、コメント、ログ、非公開識別子などの基本的な書き方を確認したいとき。
- CLI 引数解釈、エントリーポイント、サブコマンド本体、複数サブコマンドで使う共通処理の配置方針を判断したいとき。
- 開発環境、Python 仮想環境、pip、依存追加、ファイルエンコード、ファイル名・ディレクトリ名の命名規則を確認したいとき。
- pytest による自動テストを追加・変更し、Codex CLI や LLM の挙動ではなく、決定論的な制御ロジックとして検証してよい範囲を判断したいとき。
- コードレビューや実装修正で、実装・テスト全体に共通する品質基準や責務分離の基準を確認したいとき。

## Do not read this when
- 個別サブコマンドの外部仕様、入出力 schema、保存状態、エラー条件など、利用者に見える機能仕様を確認したいとき。
- path キーワード、oracle file と realization file の関係、正本仕様断片の扱い、INDEX.md 生成基準など、リポジトリ全体の基本概念を確認したいとき。
- 特定の実装ファイル、テストファイル、既存関数のシグネチャ、内部ロジック、現在のテスト期待値を探したいとき。
- Codex CLI や LLM の実際の応答品質、プロンプト品質、生成結果の妥当性を評価したいとき。

## hash
- c1fea811a659d60c1026cb0cff145c59f0af412ed0e06fbdc61402924b088a7f
