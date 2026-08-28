# `apply`

## Summary
- `cmoc realization apply fork` の差分追従用 AgentCallParameter と prompt を構築する実装の入口。
- commit 範囲と oracle file の raw git diff を prompt に埋め込み、リポジトリ全体の realization file を調査・更新・検証する処理を定義する。
- realization write モード、作業ディレクトリ、実行前インデックス処理を含む fork 固有の agent call 起動条件を扱う。

## Read this when
- fork 間の oracle file 差分を realization file へ反映する agent call の prompt や起動パラメータを確認・変更するとき。
- commit 範囲や raw oracle git diff の受け渡し、関連する realization implementation・test・ancillary の調査および検証方針を確認するとき。

## Do not read this when
- 通常の realization file の実装やテストの内容を直接確認・変更したいとき。
- 差分追従以外の realization apply 起動経路や、一般的な prompt 構築処理を調べたいとき。

## hash
- 40e1c7f13fd865b82ff001df4d754455a926dc054d96a0ea79c9f055a25c9f60

# `refactor`

## Summary
- realization refactor に関する変更要約と、ファイル単位のレビュー・修正を行う agent call の契約および構築規則を扱う下位領域です。
- 変更要約では、差分を意味論的カテゴリごとに整理し、変更内容と変更ファイルを構造化して返します。
- ファイル単位のレビュー・修正では、対象を起点に oracle と realization を調査し、所見、根拠、修正結果、検証結果、正味の変更範囲を構造化して返します。
- 各 agent call は対応する Structured Output schema、prompt、ファイルアクセスモード、作業ディレクトリ、起動前処理の構築規則を定義します。

## Read this when
- realization refactor の変更内容を人間向けに分類・要約する agent call の出力契約や起動条件を確認するとき
- realization refactor の特定ファイルを oracle と realization の規則に照らしてレビューし、必要な修正と検証を行う agent call の出力契約や構築規則を確認するとき
- 所見ごとの根拠、対応状態、修正後検証、変更 path の申告条件を確認するとき

## Do not read this when
- realization refactor の具体的な実装内容、差分そのもの、またはレビュー対象ファイルの詳細を確認したいとき
- oracle の要求や realization の設計・実装規則そのものを確認したいとき
- realization refactor 以外の agent call、変更要約、レビュー・修正契約を確認したいとき

## hash
- a6f5d695ca1ea7b22c6bdb69fad12142249b5078b9bad84ec5af579aa0731c0a
