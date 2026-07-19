# `doc`

## Summary
- cmoc のアプリケーション仕様を収録するディレクトリ。CLI 補完、ログ、エラー処理、プロンプト、managed ollama、session/run、branch・commit・worktree、サブコマンドなど、利用者向け挙動と主要 workflow の正本仕様への入口。
- 現行仕様そのものに加え、branch model や realization refactor に関する不採用案、開発規則への導線も含む。

## Read this when
- cmoc の利用者向け挙動、CLI 実行条件、出力・ログ、状態管理、プロンプト、サービス管理、session/run、branch・worktree、サブコマンドの正本仕様の所在を確認するとき。
- 複数のアプリケーション仕様にまたがる workflow や、読むべき個別仕様・開発規則の入口を判断するとき。
- realization refactor の作業方式や検査方式について、採用・不採用の理由を確認するとき。

## Do not read this when
- 具体的な機能の詳細仕様が特定できる場合は、このディレクトリ全体ではなく対応する個別仕様ファイルを直接読む。
- 開発環境、設計・テスト規則、oracle/realization の共通定義、または具体的な実装詳細だけを確認するときは、対応する専用文書や実装本文を直接読む。
- 現在の realization refactor state や agent 呼び出し経路など、現行の refactor 運用仕様だけを確認するときは、不採用案の記録ではなく現行仕様の直接の参照先を読む。

## hash
- 5534e702758742152e7d16a0938e43b1a4a3907273b4cd7105d4ad7c69b0acd1

# `src`

## Summary
- 参照可能な正本ソース本文を含まない空の入口ディレクトリです。正本ソースの有無を確認するために使用します。

## Read this when
- このディレクトリに参照可能な正本ソースが存在するか確認するとき。

## Do not read this when
- 実装仕様や処理内容を確認したいとき。

## hash
- d8568a23bb49ca22feeeb7515fdb87fd40bef87ad2adb419fb43af5dfa64ef3c
