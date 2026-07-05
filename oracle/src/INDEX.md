# `oracle`

## Summary
- cmoc の正本実装のうち、AI agent call parameter、prompt 構築、共有設定・パス表記・規範モデル・Markdown rendering helper など、複数領域の実装やテストが参照する基礎仕様断片を扱う領域。
- サブコマンドごとの AI エージェント呼び出し設定、共通規範プロンプトの組み立て、ルートプレースホルダ付きパスの扱い、横断的な設定値や構造化文書モデルを確認するための入口になる。

## Read this when
- cmoc が AI エージェントを呼び出す際の prompt、Structured Output schema、モデル設定、reasoning effort、cwd、ファイルアクセス権限、preflight 設定などの正本仕様断片を確認したいとき。
- agent call 用の完全なプロンプトが、役割・概要・ゴール・補助プロンプト・ファイルアクセス制限・ルーティング規則・各種標準などの部品からどう構築されるかを確認・変更したいとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard など、AI に注入する共通規範プロンプトやその注入指定を確認したいとき。
- cmoc 全体で共有される設定値、パス表記規則、規範文書の構造化、または Markdown rendering helper の正本実装を探すとき。
- INDEX.md エントリー生成、oracle file レビュー、fork 適用後レビュー、session join の conflict marker 解消、TUI 起動前後のパラメータ選定など、AI agent call の入力契約と出力契約を実装・テストへ反映する前に確認したいとき。

## Do not read this when
- AI エージェント呼び出しや prompt 構築ではなく、CLI 引数処理、branch 操作、diff 取得、merge 実行、保存処理、表示整形などの実行制御実装を調べたいとき。
- 個別サブコマンドの利用者向け入出力、実行フロー、状態ファイルの仕様を探しているとき。
- 設定ファイルの読み書き処理、JSON 変換処理、init 処理、バックエンド API へ送る実リクエスト形式、具体的なモデル名解決、agent CLI 実行処理など realization implementation 側の具体的なアルゴリズムだけを確認したいとき。
- 生成済み Markdown の内容や配置先、個別の規範本文、CLI の実行状態など、正本実装上の基礎概念や prompt 部品以外の具体的な仕様を調べているとき。

## hash
- 1f0bad8be1e8d1745d307119dacb2880c4990fbc65cb3f3e81dbf107780935cd
