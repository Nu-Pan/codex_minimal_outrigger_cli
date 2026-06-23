# `app_spec`

## Summary
- cmoc のアプリケーション挙動を定める正本仕様断片群への入口。CLI 起動経路、Codex CLI 呼び出し、ログ、共通エラー処理、インデクシング、run 隔離、セッション状態、利用手順、プロンプト文面、横断的な雑則を扱う。
- 利用者が実行するサブコマンド単位の仕様へ進むための入口も含み、共通仕様から個別コマンド仕様へ読む先を切り分ける階層として位置づけられる。

## Read this when
- cmoc の CLI としての外部挙動、サブコマンドの責務、標準出力・標準エラー出力、ログ保存、エラー終了、状態遷移、git branch/worktree 操作を確認・実装・テストしたいとき。
- cmoc から Codex CLI をどう起動し、profile・環境変数・Structured Output・ログ・retry・resume・並列実行をどう扱うか判断したいとき。
- INDEX.md の自動生成・更新、実行前インデクシング、生成対象・除外対象、hash 更新判定、自動コミット範囲、排他制御を扱うとき。
- run root、repo root、work root、session branch、run branch、run worktree、セッション状態ファイル、apply 状態など、cmoc の実行単位と永続状態の関係を確認したいとき。
- 初回初期化から session fork/join、oracle 改訂・レビュー、apply fork/join、セッション終了までの標準ワークフローを把握したいとき。
- agent に渡すプロンプトや利用者向けレポートの自然言語方針、cmoc 固有概念をプロンプトへ出す境界を確認したいとき。

## Do not read this when
- oracle file と realization file の基本定義、責務分担、編集権限だけを確認したいとき。
- パスキーワードやルート種別そのものの定義だけを確認したいときは、パスモデルを定義する仕様または実装へ直接進む。
- 実装ファイルやテストファイルの具体的なコード構造、関数、クラス、helper 分割、既存挙動だけを調べたいとき。
- oracle file の品質基準、realization file の品質基準、INDEX.md エントリーの書き方そのものを確認したいだけで、cmoc のアプリケーション挙動を扱わないとき。
- 特定サブコマンドから参照される内部処理ではなく、単にソース配置やテスト配置を探しているとき。

## hash
- f42d91aca9ec1dc9aa12975814609e536b18b31d3deefd3af5a1f39b076a049e

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
