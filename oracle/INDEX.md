# `doc`

## Summary
- cmoc の正本仕様・設計判断・開発ルールを分類して置く上位文書ディレクトリ。
- アプリケーションの共通 lifecycle、実行境界、状態・ログ・feedback、サブコマンド固有契約への入口。
- 不採用となった設計・運用案と採否理由への入口。
- Python 実装、CLI 責務分担、開発環境、テスト規則・実行手順への入口。

## Read this when
- cmoc の仕様、設計判断、または開発ルールについて、どの文書群から確認を始めるか判断するとき。
- アプリケーション挙動、過去の代替案、Python/CLI 開発規約、環境、テスト手順のいずれかを調べるとき。

## Do not read this when
- 単一の実装、テスト、schema、状態データ、または個別文書の具体的内容だけを確認したいとき。
- 特定サブコマンドや個別ルールの詳細を確認するため、文書群全体を読む必要がないとき。
- INDEX.md の生成・更新規則そのものを確認したいとき。

## hash
- 1c302a7e45b505a98c9dac384bb8cbdba48442af21ddc97aa80a6768fd9bbbc8

# `src`

## Summary
- oracle 配下の入力スキーマ、agent call builder、設定・パス・prompt 構築の基盤を扱う入口。
- エディタ上書き、フィードバック観測、agent call の共通型と用途別設定、prompt と policy 注入、Codex CLI や構造化文書の処理を確認するための上位ルーティング先。

## Read this when
- oracle/src 配下で、複数の入力契約や agent call 構築領域にまたがる仕様・実装の入口を判断するとき。
- エディタ入力上書き、フィードバック報告、agent call、設定・パス・prompt 構築の正本領域を特定したいとき。

## Do not read this when
- 特定の agent call の個別 prompt、入力、結果分類、検証条件だけを確認する場合。
- エディタ上書き、フィードバック送信、collector、issue 同一性判定、remediation など個別処理の具体的挙動だけを確認する場合。
- Codex CLI sandbox、Structured Output schema、個別 CLI 機能や MCP tool の詳細な契約・実装だけを確認する場合。

## hash
- 99c23199cd94a9204f0028ba7a4a480081afca0c849d618c5b1c4a7833577cfb
