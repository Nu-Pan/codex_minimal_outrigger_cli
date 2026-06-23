# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語の markdown ドキュメントとして書かれた仕様群への入口。アプリケーションとしての CLI 挙動、Codex CLI 呼び出し、ログ、エラー処理、インデクシング、run 隔離、セッション状態、利用手順、プロンプト文面、git branch/worktree モデル、開発規則、採用しなかった設計案の理由を扱う。
- 実装やテストの正本コードではなく、人間が所有する意図・判断・境界条件を文章で確認するための領域であり、利用者に見える挙動、開発時の共通規則、設計上の non-goal を読む先へ分岐する上位入口として位置づけられる。

## Read this when
- cmoc の CLI としての外部挙動、サブコマンドの責務、標準出力・標準エラー出力、ログ、エラー終了、状態遷移、git branch/worktree 操作を確認・実装・テストしたいとき。
- cmoc が Codex CLI をどう起動し、profile、環境変数、Structured Output、ログ、retry、resume、並列実行、プロンプト文面をどう扱うか判断したいとき。
- INDEX.md の自動生成・更新、実行前インデクシング、生成対象・除外対象、hash 更新判定、自動コミット範囲、排他制御を扱うとき。
- run root、repo root、work root、session branch、run branch、run worktree、セッション状態ファイル、apply 状態など、cmoc の実行単位と永続状態の関係を確認したいとき。
- 通常の local branch から session branch を作り、run ごとに run branch と linked worktree を分離する git モデルや、cmoc-managed branch の命名・merge 関係を確認したいとき。
- Python 実装、CLI 構成、共通処理配置、開発環境、依存追加、pytest による自動テスト範囲など、realization code を追加・修正・検証する前に共通開発規則を確認したいとき。
- AI memory、kaizen 自動注入、作業計画レビュー、apply での独立した計画立案ステップなど、一般には有効に見える設計案を cmoc が採用しない理由を確認したいとき。

## Do not read this when
- oracle file と realization file の基本定義、所有者、編集権限、正本仕様断片としての扱いだけを確認したいとき。
- パスキーワードやルート種別そのものの定義だけを確認したいときは、パスモデルを定義する仕様または実装へ直接進む。
- プログラミング言語や設定ファイルで書かれた正本実装、または正本テストの具体的な構造・関数・期待値を確認したいとき。
- realization implementation や realization test の現在のコード構造、関数、クラス、helper 分割、既存挙動だけを調べたいとき。
- oracle file の品質基準、realization file の品質基準、INDEX.md エントリーの書き方そのものを確認したいだけで、cmoc の自然言語仕様群に含まれる具体的なアプリケーション挙動・開発規則・設計判断を扱わないとき。
- 特定サブコマンドから参照される仕様ではなく、単にソース配置やテスト配置を探しているとき。

## hash
- 3a130d7c84766e719251b28be7de5abb81dd22a5a8f5fe46bf18bba51fb9eb94

# `src`

## Summary
- cmoc の正本仕様断片のうち、実装言語・設定ファイルで記述された oracle source 群を収める領域。AI agent 呼び出し仕様、基礎データ構造、設定仕様など、realization implementation が従うべき実装寄りの正本断片への入口になる。
- 自然言語仕様を主とする oracle doc やテスト仕様を主とする oracle test ではなく、cmoc 内部の型、変換、設定、プロンプト構築など、実装として表現された正本仕様を確認するための階層。
- 下位要素として、agent 呼び出しパラメータと共通 prompt 部品を扱う領域、パスモデル・構造化文書・規範モデルなどの基礎 helper を扱う領域、リポジトリ単位の設定値と Codex CLI 向け値の対応を扱う領域へ分岐する。

## Read this when
- cmoc の realization implementation を作る前に、根拠となる実装形式の正本仕様断片を探したいとき。
- AI agent 呼び出し時の role、summary、goal、補助 prompt、ファイルアクセスモード、モデル種別、reasoning effort、Structured Output 契約などを確認したいとき。
- cmoc 内部で共有される基礎概念、共通データ構造、ルートトークン付きパス表記、実パス解決、構造化文書の Markdown 描画、規範断片モデルを確認したいとき。
- 開発対象リポジトリごとの設定 JSON、既定値、制御上限値、Codex CLI に渡すモデル名や reasoning effort 名への対応を確認したいとき。
- oracle doc の抽象的な説明だけではなく、実装・設定ファイルとして表された正本仕様断片を起点に、対応する realization code の方針を判断したいとき。

## Do not read this when
- 自然言語の正本仕様文書そのものを読み、概念定義、標準、仕様判断の文章を確認したいとき。
- oracle test として表されたテスト仕様や、期待される検証観点を確認したいとき。
- 実際に編集すべき realization implementation や realization test のコード、CLI 実装、git 操作、端末 UI、状態ファイル処理を探しているとき。
- リポジトリ全体のルーティング方針や、oracle / realization の一般定義だけを確認したいとき。
- INDEX.md エントリーの文面そのものを生成・確認したいだけで、下位の正本仕様断片を読む必要がないとき。

## hash
- 098eb3abd15f08ad3c5efe22cbcc979f1c8807db8834e98b6b5f020369ba864a
