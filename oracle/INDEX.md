# `doc`

## Summary
- cmoc の正本仕様ドキュメントを領域別にまとめたディレクトリ。アプリケーション共通仕様、branch・commit・worktree、開発規則、不採用案などへの入口として機能する。

## Read this when
- 複数の正本仕様から、調査・変更対象の文書を選ぶとき
- Codex 呼び出し、ログ、prompt、session／run、branch、worktree、CLI、Python 開発、テストなどの仕様の入口を探すとき
- 現行仕様ではなく、採用されなかった設計案やその理由を確認するとき

## Do not read this when
- 対象の仕様文書がすでに特定できており、その本文へ直接進めるとき
- 実装やテストの具体的な内容だけを確認するとき
- Python 環境構築、CLI 設計、テスト実行など、対応する個別の開発規則文書が明確なとき

## hash
- f264ab1af6f26b43de171eb799f1d7adb6386371322f465a6b5c66013e301048

# `src`

## Summary
- cmoc の agent call 用正本ソースを集約する領域です。共通パラメータ、用途別の呼び出し構築、Structured Output schema、prompt の組み立て、パス・設定・構造化文書モデル、feedback 入力契約を扱います。各用途の builder、規範、構造化モデルの実装へ進む入口です。

## Read this when
- agent call のモデル、推論強度、ファイルアクセス、作業 root、Structured Output を確認するとき。
- indexing、oracle review、realization、feedback、TUI など用途別の agent call 構築を調査・変更するとき。
- prompt の共通部品、oracle・realization の規範、ルーティング規則、パス解決、構造化文書の変換を確認するとき。

## Do not read this when
- 実際の agent call の実行制御、CLI・TUI の上位フロー、または通常の realization 実装を調査するとき。
- 正本仕様そのもの、feedback の保存・集約、または通常のテスト実装だけを確認するとき。
- 特定の用途やモデルの責務が明らかな場合は、この領域全体ではなく該当する下位実装へ直接進むとき。

## hash
- 6016abd0b4858f5c22dba8192d514c2b6a7a820e28bb7bfc0f82c7b818fb52dd
