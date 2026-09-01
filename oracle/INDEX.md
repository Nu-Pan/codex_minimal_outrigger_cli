# `doc`

## Summary
- cmoc の正本仕様と開発規則を、アプリケーション挙動、branch・worktree 分離、検討済み代替案、Python 実装・環境・テストの領域へ案内する上位文書群の入口。
- アプリケーション仕様では CLI、session／run、Codex 呼び出し、ログ、feedback、通知、文書分類などの個別仕様へ進み、dev_rule では実装・環境・テストの開発規則へ進む。
- branch・commit・worktree による session／run の隔離モデルと、採用しなかった設計案の判断理由を確認するための入口を含む。

## Read this when
- cmoc の正本仕様全体から、対象の挙動・設計判断・開発規則に対応する下位文書を探すとき
- CLI、session／run、Codex、feedback、ログ、通知、INDEX、branch／worktree 分離など、複数領域にまたがる仕様の所在や境界を確認するとき
- Python 実装規約、開発環境、テスト規則・実行手順を確認するとき
- 現行方針ではなく、不採用となった設計案や作業方式の理由を調べるとき

## Do not read this when
- 特定の CLI サブコマンド、Codex 呼び出し、session／run、feedback、ログ、通知などの詳細な挙動だけを確認したいときは、対応する app_spec 配下の個別仕様を直接読む
- branch model の具体的な操作契約だけを確認したいときは、branch model の本文を直接読む
- Python の実装・環境・テストに関する具体的な規則だけを確認したいときは、対応する dev_rule 配下の文書を直接読む
- 採用済み機能の仕様や realization の具体的な実装・テスト内容を調べるときは、該当する正本仕様または realization／test を直接読む

## hash
- 48cde22103429c2c8d2414b0cb6017f336ba9f39fe1bfc38ef07e0231630e149

# `src`

## Summary
- cmoc の正本ソースを構成する階層で、設定・パスモデル・構造化文書モデル、agent call パラメータ、prompt 構築、入力契約を扱う。
- agent call の実行側へ渡す構築定義と、用途別の prompt policy・feedback・editor input・TUI などの下位領域への入口となる。

## Read this when
- cmoc の設定値、Codex call パラメータ、agent call の cwd とパス placeholder、構造化文書モデルを確認するとき。
- 完全 prompt の構築や policy の組み合わせ、agent call 入力契約、feedback・editor input handoff の形式を調べるとき。
- 下位の acp_builder、prompt_builder、other など、特定の oracle ソース領域へ進む起点を判断するとき。

## Do not read this when
- 実際の CLI 実行、session join の競合解消、TUI 起動、oracle や realization 本文の編集処理を確認したいとき。
- 特定の用途における具体的な prompt policy、agent call パラメータ、JSON Schema の詳細を確認したいときは、対応する下位対象を直接読むとき。
- cmoc の意味仕様や一般的な開発規定を確認したいときは、対応する oracle/doc または dev_rule の正本を読むとき。

## hash
- 591e6af7937d26eff09b85f86d6d3b5d3ea10092d5872e3222118477a515abf0
