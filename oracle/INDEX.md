# `doc`

## Summary
- cmoc の自然言語で書かれた正本仕様断片をまとめる領域。利用者向けの CLI 挙動、サブコマンド、Codex CLI 呼び出し、ログ、エラー処理、状態管理、インデクシング、run 隔離、利用手順、git branch / commit / worktree モデル、採用しなかった設計案、実装・テスト・開発環境の共通規則を扱う。
- 実装やテストの変更前に、確認すべき正本仕様断片を、外部挙動、git/session/run モデル、設計判断の背景、開発規則のどれとして読むべきか切り分けるための入口になる。

## Read this when
- cmoc の機能仕様や開発規則について、自然言語で書かれた正本仕様断片から読む対象を探したいとき。
- CLI サブコマンド、実行時状態、ログ、エラー処理、Codex CLI 呼び出し、プロンプト、インデクシング、run 隔離、利用ワークフローなど、利用者に見える挙動や実行時の共通規約を確認したいとき。
- session、run、apply、review に関わる branch、commit、linked worktree の用語、命名、分岐元、merge 先、隔離境界を確認したいとき。
- AI-generated kaizen の自動注入、作業計画レビュー、apply 系 orchestration など、採用しなかった workflow や設計案の理由を確認したいとき。
- Python 実装、CLI 構成、共通処理の配置、開発環境、依存追加、pytest によるテスト方針など、realization code を書く前の共通規則を確認したいとき。

## Do not read this when
- oracle file と realization file の定義、責務分担、正本仕様断片としての一般原則、INDEX.md エントリーの作成基準だけを確認したいとき。
- path キーワードや root model の定義そのものを確認したいとき。
- 自然言語仕様ではなく、AgentCallParameter builder、path model、その他のプログラム・設定として書かれた正本実装断片の詳細を直接確認したいとき。
- 既存 realization code の具体的な関数、クラス、テスト期待値、現在の内部ロジックを探したいとき。
- 読むべき個別の正本仕様断片がすでに特定できており、その本文だけを確認すればよいとき。

## hash
- 03fb4564493232bce219e069fbbb919261f75f6ea9f83caa7fe2d695312a543b

# `src`

## Summary
- cmoc の正本仕様断片のうち、プログラミング言語や設定ファイルとして書かれた仕様実装をまとめる階層。AI エージェント呼び出しパラメータ構築、標準プロンプト部品、共通基礎型、パス語彙、構造化 Markdown 生成、リポジトリ単位設定の仕様へ進む入口になる。
- サブコマンド別に AI へ渡す role、summary、goal、補助文脈、ファイルアクセス権限、モデル種別、reasoning effort、Structured Output schema の対応を確認するための領域である。
- CLI の実行制御そのものや git 操作そのものではなく、それらの処理から参照される正本仕様断片、共通値、標準文面、保存される設定構造を確認するための階層である。

## Read this when
- cmoc の処理が AI エージェントを呼び出す場面で、呼び出しパラメータ、prompt 構成、補助文脈、権限モード、モデル種別、reasoning effort、Structured Output schema の仕様を確認したいとき。
- apply fork、review oracle、indexing、session join、tui などの AI 呼び出しで、どの標準文面や入力情報を組み込み、どの応答契約を期待するかを調べたいとき。
- ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、oracle standard、realization standard、review / apply / index entry 向け standard を prompt 部品としてどう構築するかを確認したいとき。
- cmoc 内部で共有される論理モデル種別、reasoning effort、ファイルアクセスモード、AgentCallParameter、root token と実パスの変換、構造化文書レンダリング、規範文書のデータ構造を確認したいとき。
- 開発対象リポジトリごとに永続化される設定の構造、既定値、Codex CLI 向けのモデル・reasoning effort 対応、apply fork や review oracle の処理上限を確認したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、プロセス制御、git branch・merge・diff・patch 操作、永続状態の読み書き、端末 UI 描画など、AI 呼び出しパラメータ構築以外の実行フロー本体を調べたいとき。
- oracle doc の自然言語仕様本文、oracle test のテスト仕様、または realization 側の実装・テストを直接確認したいとき。
- 個別の patch 内容、merge conflict の意味的な統合判断、所見の妥当性、実装修正方針など、対象ファイル本文や差分そのものを読んで判断する作業をしたいとき。
- 設定ファイルの実行時ロード・保存処理、JSON 変換実装、設定同期コマンドの制御フローだけを確認したいとき。
- INDEX.md 全体のルーティング文書としての書き方やエントリー品質基準だけを確認したい場合で、prompt 部品としての組み込み仕様を読む必要がないとき。

## hash
- 721648fe44fd811a8a25a71e331cb9c156af1a89696628a9ea6fd7f89e782d25
