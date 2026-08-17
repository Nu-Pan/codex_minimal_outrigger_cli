# `doc`

## Summary
- cmoc の正本文書を領域別に案内する入口。アプリケーション仕様、branch・commit・worktree のモデル、採用しなかった代替案、開発ルールを扱い、対象に応じて各下位文書へ進むためのルーティングを提供する。

## Read this when
- cmoc の正本仕様・設計資料・開発規約の入口を特定するとき
- アプリケーション挙動、branch model、設計上の代替案、Python・CLI・環境・テスト規約のいずれかを調査するとき
- 個別文書へ進む前に、対象領域の文書群を選びたいとき

## Do not read this when
- 対象の個別仕様や設計・テスト文書が既に特定できており、上位の文書群一覧を確認する必要がないとき
- 具体的な実装配置やCLI実装の責務だけを確認するとき
- テストの実行手順だけを確認するとき

## hash
- d3a45a15649b4ef42e8e396b06429e61af3b733a0a83bad0571cbe8c5f3ad94c

# `src`

## Summary
- AI コーディングエージェント呼び出しに渡す AgentCallParameter、完全 prompt、パスコンテキスト、cmoc 設定、構造化文書の基盤実装を集約する領域。
- agent call の論理モデル・推論強度・ファイルアクセスモード・Structured Output・cwd・indexing preflight を定義し、prompt_builder で policy と作業目的を統合した prompt を構築する。
- 処理別の呼び出しパラメータ生成を調査・変更する際は `acp_builder`、prompt の共通構成や規定を調査・変更する際は `prompt_builder`、パス解決・設定・構造化文書の共通モデルを確認する際は `other` が下位要素への入口となる。

## Read this when
- AgentCallParameter の共通契約、モデル・推論・アクセス制御、agent call cwd、Structured Output、indexing preflight の定義を調査・変更するとき
- 複数の cmoc 処理で共有される完全 prompt の構築順序、placeholder 統合、policy の組み込みを確認するとき
- 処理別の ACP builder と prompt builder、パスモデル、cmoc 設定、構造化文書モデルの責務分担を確認するとき

## Do not read this when
- agent call の実行制御、終了結果の処理、または TUI の起動だけを調査するときは、対応する実行側・TUI 側の下位要素を直接読む
- Codex CLI が受理する具体的なモデル名や sandbox 解決仕様だけを確認するときは、realization 実装または指定された oracle 文書を読む
- 個別処理の prompt policy、Structured Output schema、または処理固有の通常フローだけを調査するときは、対応する下位要素を直接読む

## hash
- 09a58a58b3fed24ab0b9cdcee17d73d2b5a0eeef46ed2be349cfe8eba9839184
