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
- cmoc の agent call パラメータと prompt 生成を支える実装群をまとめたソースディレクトリ。共通のモデル・推論強度・ファイルアクセス契約、パス・設定モデル、構造化 Markdown、prompt の完成処理と policy、用途別 builder、feedback 入力を扱う下位要素への入口である。
- `acp_builder` は用途別 agent call parameter、`prompt_builder` は placeholder・policy・prompt 本文、`other` は設定・パス・構造化文書、`feedback` は feedback 入力形式を担う。各領域の実装や Structured Output の詳細を調べる際は、対応する下位ディレクトリから読み始める。

## Read this when
- agent call の共通パラメータ契約や、用途別 builder の責務分担を確認するとき。
- prompt の組み立て、placeholder、アクセス制約、routing、oracle・realization policy、feedback policy の実装入口を横断して調べるとき。
- cmoc の設定・パス解決・構造化 Markdown ノードの実装配置を確認するとき。

## Do not read this when
- 特定用途の agent call parameter や Structured Output の詳細だけを確認したいときは、対応する `acp_builder` の下位ディレクトリを直接読む。
- prompt policy や prompt 部品の個別実装だけを確認したいときは、対応する `prompt_builder` の下位ディレクトリを直接読む。
- Codex CLI の実行制御や、生成後の feedback の保存・集約を確認したいときは、対応する実行側・collector 側の対象を直接読む。

## hash
- 91c1e10c0778e56cb8ec5173c2a6ef40e595db352a392179b9c7a5de613c0337
