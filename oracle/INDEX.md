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
- cmoc の oracle 実装群における上位入口。agent call パラメータ、prompt 構築、用途別の起動・検証定義、設定・パス・構造化文書モデルを下位要素へ振り分ける。
- agent call の呼び出し設定や用途別 builder を調べる場合は acp_builder、prompt の組み立て規則や各種ポリシーを調べる場合は prompt_builder、設定・パス解決・Markdown 構造化文書を調べる場合は other から読み始める。

## Read this when
- oracle の実装全体で、agent call 関連の責務がどの下位要素にあるかを判断するとき。
- 呼び出しパラメータ、prompt 構築、用途別起動処理、設定・パスモデルの調査開始点を決めるとき。

## Do not read this when
- 特定の prompt policy、agent call builder、設定クラス、パス解決処理、または構造化文書モデルだけを確認したい場合は、対応する下位要素を直接読むとき。
- agent call の実行結果の保存・集約や、oracle／realization 本文・INDEX.md 自体の編集方法を調べるとき。

## hash
- 4af0b7fbf24db6d6442d583b4b206d10b4771528c060ff8e984534a8ad377dc5
