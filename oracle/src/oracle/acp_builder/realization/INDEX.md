# `apply`

## Summary
- `cmoc realization apply fork` の AgentCallParameter と完全 prompt を構築する実装への入口です。oracle file の差分、関連する realization file の調査範囲、完了条件、作業ディレクトリ、モデル、推論強度、アクセスモード、事前インデックス処理を定義します。

## Read this when
- `cmoc realization apply fork` の起動時に、oracle file の差分を realization file へ反映する prompt や作業範囲を変更・確認するとき。
- 同コマンドの作業ディレクトリ、ファイルアクセス権、モデル、推論設定、実行前インデックス処理を変更・確認するとき。

## Do not read this when
- 他の realization コマンドの prompt や起動パラメータを確認するとき。
- 差分そのものを適用する処理、個別の oracle・realization file の内容、または `AgentCallParameter` 共通仕様を直接確認するとき。

## hash
- 9814d875c68410e452442dd64374bf0091ea4c5596b83a5929b95108a8fa8c66

# `refactor`

## Summary
- refactor fork に対する agent call の構築定義と、その出力契約を扱う領域。変更差分の要約処理と、ファイル単位のレビュー・修正処理への入口。

## Read this when
- refactor fork の変更差分を要約する agent call の prompt、実行設定、作業ディレクトリ、出力契約を確認するとき
- refactor fork のファイル単位レビュー・修正 agent call の対象範囲、アクセス権、検証要求、出力契約を確認するとき
- 変更要約またはレビュー・修正結果の構造化出力スキーマを確認するとき

## Do not read this when
- refactor fork 自体の実装処理や差分生成処理を調べるとき
- 一般的な prompt 構築規則や refactor と無関係な agent call を調べるとき
- レビュー対象となる個別ファイルの実装内容や所見を確認するとき

## hash
- b1e6eee34948abffb90f017dfa08865ae4924ae481d7153b529f92f7982b37d6
