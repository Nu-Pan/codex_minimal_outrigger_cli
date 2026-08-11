# `fork`

## Summary
- 対象ディレクトリ内の本文を確認し、`cmoc realization apply fork` の起動設定と prompt 構築を担う実装への入口を示します。

## Read this when
- `cmoc realization apply fork` の実行時に、追従対象の差分、作業範囲、完了条件、作業ディレクトリ、モデルやアクセス設定を組み立てる処理を変更・確認するとき。

## Do not read this when
- 他の realization コマンドの prompt や起動設定を確認するとき。
- 実際の差分適用ロジック、個別の oracle・realization ファイル、または一般的な AgentCallParameter の仕様を直接確認するとき。

## hash
- 8c2e798c9027bf24c0f57dc456eab7d062940c41d9b455d01c48af5ec053a10f
