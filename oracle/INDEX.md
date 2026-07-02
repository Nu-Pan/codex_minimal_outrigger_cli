# `doc`

## Summary
- cmoc の自然言語による正本仕様断片を集める領域。アプリケーション仕様、branch/worktree モデル、開発規則、不採用設計案など、実装差を避けたい人間意図を文書として確認する入口になる。
- 利用者向け挙動や実行基盤の個別仕様へ進む領域と、realization code を変更する際の横断的な開発規則へ進む領域、不採用案の背景を確認する領域を分けて扱う。

## Read this when
- cmoc の CLI 挙動、run/session、git branch/worktree、Codex CLI 呼び出し、状態、ログ、エラー、インデクシングなどの正本仕様断片を探すとき。
- Python 実装・テスト・CLI 構成・開発環境など、realization code を追加または修正する前に従うべき開発規則を確認したいとき。
- 新機能や workflow 変更の前に、過去に検討されたが採用されなかった設計案と、その不採用理由を確認したいとき。
- 対象がアプリケーション外部仕様、branch モデル、開発規則、不採用案のどれに属するかを切り分けたいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー生成基準だけを確認したいとき。
- パスキーワードや repo root / run root / work root などの体系そのものを確認したいだけのとき。
- realization implementation や realization test の具体的な既存コード、内部 helper、現在のテスト期待値を調べたいとき。
- agent call の個別 prompt builder や parameter schema の正本実装だけを確認したいとき。

## hash
- 13d029d63537483e9dddd92b1e1b14bc087d9878ab0d55ef43c7aed9f91ff048

# `src`

## Summary
- AI Agent 呼び出しパラメータ、Structured Output schema、完全プロンプト構築、標準文書パーツ、設定・パス表記・構造化文書モデルを定義する正本実装断片の領域。
- cmoc の各ワークフローが AI Agent に渡す role、summary、goal、file access mode、prompt、schema、およびそれらを組み立てる共通部品を確認する入口になる。

## Read this when
- AI Agent 呼び出しで使う論理モデルクラス、reasoning effort、ファイルアクセスモード、AgentCallParameter の構造を正本仕様断片として確認または変更したいとき。
- cmoc の indexing、TUI、apply fork、review oracle、session join、ファイルアクセス規則違反リカバリで生成されるプロンプトや Structured Output schema を確認したいとき。
- 完全プロンプトの構成、静的プロンプトと動的プロンプトの分離、標準文書の注入条件、placeholder mapping、ファイルアクセス規則のプロンプト化を確認したいとき。
- oracle/realization の基本、oracle standard、realization standard、review standard、apply review standard、index entry standard、routing rule など、Agent 向けプロンプトに入る規範本文の正本実装断片を確認したいとき。
- cmoc の設定項目と既定値、論理モデル名や reasoning effort の設定表現、apply fork や review oracle の処理予算設定を確認したいとき。
- ルートパスプレースホルダ、絶対パス解決、プレースホルダ付きパス表記、git worktree root との関係、構造化文書や規範モデルの Markdown 整形を確認したいとき。

## Do not read this when
- AI Agent 呼び出しのプロセス起動、ログ保存、結果処理、エラー処理、git 操作、branch 操作、状態管理など、正本実装断片ではなく realization implementation 側の実行フローを追いたいとき。
- CLI 引数解析、サブコマンドの制御、設定ファイルの読み書き、JSON 変換、Codex CLI へ渡す実際のコマンド列を調べたいとき。
- 正本仕様断片としてのプロンプト・schema・モデル定義ではなく、特定の作業ディレクトリで読むべきファイルや生成済み INDEX.md の内容だけを知りたいとき。
- oracle file の自然言語ドキュメントだけを読み、Python や JSON で表現された正本実装断片の構造を確認する必要がないとき。
- realization code や realization test の実装不具合、テスト追加、リファクタリング対象を探しており、AgentCallParameter やプロンプト構築の正本定義に触れる必要がないとき。

## hash
- d92de2b8b4cbbd262fc8e241ac3691022c7278ede9c5a1826e436409606c9c46
