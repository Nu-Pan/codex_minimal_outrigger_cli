# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語で書かれた文書群への入口。アプリケーションレベルの CLI 挙動、git branch / worktree モデル、不採用設計判断、開発時の横断規則を扱う。
- 利用者に見える仕様、外部 agent 制御、状態管理、作業隔離、ログ、ルーティング文書生成、実装・テスト方針などを、目的別の仕様文書へ選んで読みに行くための階層。

## Read this when
- cmoc の CLI 外部挙動、サブコマンド、状態遷移、stdout / stderr、終了コード、ログ、git branch / worktree 操作の正本仕様を確認したいとき。
- Codex CLI 呼び出し、agent prompt、Structured Output、retry / resume、ファイルアクセス制限、並列実行など、外部 agent の起動・制御・記録に関する仕様を調べるとき。
- session branch、run branch、session home branch、fork / join commit、run ごとの linked worktree 隔離など、cmoc の branch / commit / worktree モデルを確認するとき。
- INDEX.md の生成・更新、hash 更新、インデクシング、自動コミット、排他制御、ルーティング文書の意味情報を扱うとき。
- Python 実装、CLI 構成、共通処理の配置、開発環境、pytest 方針など、realization code を追加・修正・検証する前の横断的な開発規則を確認したいとき。
- memory、kaizen、作業計画レビュー、改善案の自動注入など、採用しなかった設計案の背景や不採用理由を確認したいとき。

## Do not read this when
- oracle file、realization file、path keyword、root model など、cmoc 全体の基礎概念だけを確認したいときは、それらを定義するより直接の仕様や実装へ進む。
- 実装ファイルやテストファイルの責務、既存関数、helper 分割、具体的なコード構造だけを調べたいときは、realization 側の対象領域へ進む。
- 個別の AgentCallParameters のフィールド値、profile 本文、sandbox 設定、argv の詳細だけを確認したいときは、parameter builder 側を読む。
- 特定サブコマンドの詳細仕様だけが必要で、対象サブコマンドが分かっているときは、この階層全体ではなく該当する下位仕様へ直接進む。
- INDEX.md エントリー作成の品質基準、oracle / realization の一般標準、またはパス表記の基本定義だけを確認したいときは、アプリケーション仕様文書ではなく標準文書や基礎定義を読む。

## hash
- e034f2c522d389ace4b172846346c9a6944a9d5de6b2b47dd764f364709833fb

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
