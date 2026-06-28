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
- oracle src 配下の正本実装断片を束ねる入口。自然言語仕様やテストではなく、Python 実装・設定形式で書かれた oracle file を対象に、cmoc の基礎型、設定モデル、agent call parameter と prompt 構築仕様などを確認するための階層。
- 下位には、共有される値オブジェクトや path model、構造化文書生成などの基盤領域、リポジトリ単位の設定仕様領域、AI エージェント呼び出し時の role・summary・goal・権限・モデル設定・Structured Output 契約を定める領域がある。
- realization 実装やテストを直接読む前に、実装差を避けたい型・変換・設定値・AI 呼び出し境界の正本仕様を探すための入口になる。

## Read this when
- cmoc の実装で使う基本型、root token と実パスの相互変換、規範モデル、Markdown レンダリング、リポジトリ設定、AI エージェント呼び出しパラメータのいずれかについて正本仕様断片を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の意味や path 変換、git worktree 判定に関わる仕様を調べたいとき。
- 設定ファイルに保存される項目、既定値、Enum 値、Codex CLI・apply fork・review oracle 向け設定の構造を確認したいとき。
- AI に渡す prompt の構成、標準文書の注入条件、ファイルアクセスモード、モデル種別、reasoning effort、Structured Output schema など、AI 呼び出しの入出力境界を追いたいとき。
- realization code の変更前に、実装側が合わせるべきプログラム形式の正本仕様断片が oracle src 側に存在するかを確認したいとき。

## Do not read this when
- 自然言語で書かれた仕様文書、設計方針、一般基準、用語定義そのものを確認したいとき。
- oracle test に書かれた期待挙動やテストケースを確認したいとき。
- CLI 引数解析、git 操作、ファイル編集、永続状態更新、TUI 描画などの realization 実装本体を調べたいだけのとき。
- 実装から生成・修正される realization file の具体的なコード配置やテスト実装を探しているとき。
- 対象が AI 呼び出し境界、基盤型、path model、設定仕様のいずれにも関係せず、より直接の oracle doc または realization code が読む先として分かっているとき。

## hash
- 0d6988af7c21ab82b64b2ab740faa7d633f51d555093c128966c3c5023bf24ac
