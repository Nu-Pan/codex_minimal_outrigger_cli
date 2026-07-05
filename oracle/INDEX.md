# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語 Markdown 文書を集めた領域。アプリケーション仕様、branch/worktree モデル、不採用設計案、開発ルールなど、実装前に人間意図を確認する入口になる。
- 公開 CLI 挙動、状態・ログ・インデックス生成、agent call 境界、実行環境管理、実装・テストの共通作法など、実装差を避けたい外部挙動や責務境界を扱う下位文書へ進むためのまとまり。

## Read this when
- cmoc の個別機能や開発作法について、自然言語で書かれた oracle doc を探すとき。
- CLI 実行フロー、サブコマンド、共通前処理、ログ、状態管理、run 隔離、Codex CLI 呼び出し、provider 連携、branch/worktree モデルに関する正本仕様断片を確認したいとき。
- Python 実装、CLI 配置、開発環境、pytest 方針など、realization code を追加・変更する前に守るべき共通ルールを確認したいとき。
- 現行設計に対して、過去に不採用となった代替案やその理由を再検討したいとき。

## Do not read this when
- oracle file と realization file の一般的な定義、責務境界、記述標準、INDEX.md エントリー作成規則だけを確認したいとき。
- パスキーワードやルート種別の定義そのものを確認したいとき。
- 自然言語の正本仕様ではなく、oracle src、oracle test、realization code、既存テストの具体的な関数構造や内部 helper を直接調べたいとき。

## hash
- e2d2741a77e32907dc16322ef2b56ad06f765c34eef38789a55f172c5611c0b5

# `src`

## Summary
- cmoc の正本実装として、AI agent call parameter、prompt 構築、共有設定、パス表記、規範モデル、Markdown rendering helper など、複数領域から参照される基礎仕様断片を扱う。
- サブコマンドごとの AI エージェント呼び出し設定、共通規範プロンプト、ルートプレースホルダ付きパス、横断設定値、構造化文書モデルを確認する入口になる。

## Read this when
- AI エージェント呼び出し時の prompt、Structured Output schema、モデル設定、reasoning effort、cwd、ファイルアクセス権限、preflight 設定などの正本仕様断片を確認したいとき。
- agent call 用の完全なプロンプトが、役割、概要、ゴール、補助プロンプト、ファイルアクセス制限、ルーティング規則、各種標準などの部品からどう構築されるかを確認・変更したいとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard など、AI に注入する共通規範プロンプトや注入指定を確認したいとき。
- cmoc 全体で共有される設定値、パス表記規則、規範文書の構造化、Markdown rendering helper の正本実装を探すとき。
- INDEX.md エントリー生成、oracle file レビュー、fork 適用後レビュー、session join の conflict marker 解消、TUI 起動前後のパラメータ選定などで、AI agent call の入力契約と出力契約を実装・テストへ反映する前に確認したいとき。

## Do not read this when
- AI エージェント呼び出しや prompt 構築ではなく、CLI 引数処理、branch 操作、diff 取得、merge 実行、保存処理、表示整形などの実行制御実装を調べたいとき。
- 個別サブコマンドの利用者向け入出力、実行フロー、状態ファイルの仕様を探しているとき。
- 設定ファイルの読み書き、JSON 変換、init 処理、バックエンド API へ送る実リクエスト形式、具体的なモデル名解決、agent CLI 実行処理など、realization implementation 側の具体的なアルゴリズムだけを確認したいとき。
- 生成済み Markdown の内容や配置先、個別の規範本文、CLI の実行状態など、正本実装上の基礎概念や prompt 部品以外の具体的な仕様を調べているとき。

## hash
- 65b0b57aceb14bfd21b3a27e750d877af0d2a10c5ee9cfba987a0abca198dd52
