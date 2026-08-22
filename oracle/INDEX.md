# `doc`

## Summary
- cmoc の正本仕様と開発ルールを集約する oracle 文書群への入口。CLI・workflow・branch／worktree・feedback・ログ・状態管理などの app_spec と、Python 実装、設計、開発環境、テスト要件・実行手順に関する dev_rule を、作業内容に応じて選択するための上位ルーティング対象。considered_alternative では採用しなかった設計・作業方式の理由を確認できる。

## Read this when
- cmoc の CLI や workflow の正本仕様を調査し、関連する app_spec 文書の入口を選ぶとき
- session fork、run の隔離、branch・commit・worktree の用語や責務を確認するとき
- 現行設計で採用しなかった作業方式や仕様案の理由を比較するとき
- Python 実装の規約、CLI の配置、開発環境、テスト要件、テスト実行手順を確認するとき

## Do not read this when
- 特定の app_spec や dev_rule の詳細だけを確認する場合は、対象文書を直接読む
- 実装コード、realization、テストコードの具体的な内容だけを調べる場合
- 既存 INDEX.md の内容やインデックス生成処理だけを確認する場合

## hash
- ab8242c8ccd61aef50a181ef0823429af722e2abbdb464e8a02a5a7e69c2ca3a

# `src`

## Summary
- cmoc の agent call パラメータ、feedback 入力、設定・パス・構造化 Markdown、prompt と各種ポリシーを構築する実装群。
- acp_builder は用途別の agent 起動設定、feedback 判定、index entry 生成、oracle・realization 操作、review、session、TUI の prompt を扱う入口。
- feedback は人間向け feedback issue の入力契約を定義し、other は設定値・root path 解決・構造化文書ノードを提供する。prompt_builder は完全な agent prompt、editor 入力、oracle・realization・file access・routing・feedback などの共通ポリシーを組み立てる。

## Read this when
- cmoc の agent call 構築と prompt 生成の実装構成を横断して確認するとき
- 用途別の agent 起動パラメータ、feedback 入力、oracle review、realization 操作の入口を確認するとき
- prompt に適用される設定・パス・アクセス制約・routing policy の組み立てを調査するとき

## Do not read this when
- 特定の用途の agent call builder や特定の policy の詳細だけを確認したいときは、対応する下位ディレクトリまたはファイルを直接読む
- Codex CLI の実行処理や、oracle・realization の正本仕様そのものを確認したいときは、実行側実装または oracle 文書を読む

## hash
- 1dda10400d887c2daa12c7cda4a71019c3f88a468d6dabddc508f71f189f7d75
