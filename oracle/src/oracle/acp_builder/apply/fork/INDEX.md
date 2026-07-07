# `change_summary.json`

## Summary
- 差分全体を意味ごとの変更カテゴリに分け、人間向けの要約と主要な変更箇所を記録するための構造を定める。
- 変更の網羅一覧ではなく、要約の根拠として有用な主要箇所を添えて、レビューや報告で変更意図を把握しやすくするための出力契約を扱う。

## Read this when
- fork 適用後の差分を、人間が読める変更カテゴリ別サマリーとして出力・検証する処理を実装または確認するとき。
- 変更カテゴリ、変更内容の説明、主要な変更箇所の対応関係について、出力互換性を固定したいとき。
- 差分要約が空でない前提や、詳細な変更一覧ではなく主要箇所を選ぶ方針を確認したいとき。

## Do not read this when
- 個別ファイルのパッチ内容そのもの、diff 生成手順、または git 操作の仕様を確認したいとき。
- fork の作成・適用・分岐制御など、差分要約の出力契約より前後の実行フローを調べたいとき。
- ルーティング文書、テスト、実装などの変更種別ごとの具体的な判定ロジックを探しているとき。

## hash
- 51ffe6e61588c7c347494a36267c02b8d48f69f6e264fcaf396096938cdd672d

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向けに、git diff そのものを入力として人間向け変更要約を生成する agent call parameter の正本仕様断片。
- 変更要約担当 agent の role、summary、goal、readonly file access、差分埋め込み、Structured Output schema 指定、使用 model class と reasoning effort を定める。

## Read this when
- `cmoc apply fork` が作業レポート用の変更要約をどの prompt・agent call parameter で生成するかを確認する。
- 変更要約生成に渡す差分入力の扱い、特に git diff 出力を解析・整形せず prompt に含める方針を確認する。
- `cmoc apply fork` の変更要約生成で使う file access mode、model class、reasoning effort、出力 schema 参照の正本を確認する。

## Do not read this when
- `cmoc apply fork` の fork 作成、branch 操作、diff 取得、レポート保存など、変更要約 prompt 以外の処理を調べる。
- 変更要約の Structured Output schema そのものの項目や型を確認する。
- `cmoc apply fork` 以外のサブコマンドの prompt や agent call parameter を調べる。

## hash
- 621f88956b6bc0cf1539c6f2e413dd4b7caeff0e5cbe6093e70a8139c6cd5d6c

# `file_finding_enumeration.json`

## Summary
- 実装調査で見つかった問題点を、根拠位置、正本仕様上の要求、観測された実装、問題理由、修正方針として報告するための構造化出力を定義する。
- 仕様と実装の乖離をレビュー結果として人間に渡す場面で使う、所見リストの出力契約を担う。

## Read this when
- 実装レビューや適合性調査の結果として、明確に修正が必要な所見を返す出力形式を確認したいとき。
- 所見に含めるべき根拠情報、仕様要求、観測結果、理由、修正方針の粒度を確認したいとき。
- レビュー結果の生成側または検証側で、所見リストが空でない根拠位置を持つことを前提にしたいとき。

## Do not read this when
- 単に実装対象の仕様そのものを探しているとき。ここには個別機能の要求ではなく、レビュー所見の報告形式だけがある。
- INDEX.md 用エントリーや一般的なルーティング文書の書き方を確認したいとき。
- 所見を JSON 以外の文章、ログ、CLI 表示としてどう見せるかを確認したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` における、指定ファイルを起点とした所見リストアップ用の agent call parameter を構築する oracle src。読み取り専用で `<repo-root>` 内の関連 oracle file・realization file を調査し、apply review standard に従う Structured Output の所見リストを返す prompt を組み立てる。

## Read this when
- `cmoc apply fork` のファイル単位所見リストアップ agent に渡す role、summary、goal、参照標準、ファイルアクセスモードを確認したいとき。
- 所見リストアップ処理がどの placeholder、Structured Output schema、model class、reasoning effort を使って agent call parameter を作るか確認したいとき。
- ファイル単位の所見列挙が下流処理へ与える影響や、MAINSTREAM model を使う根拠を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の実行制御、所見の統合、修正適用、または CLI 引数処理を確認したいとき。
- apply review standard 自体の内容、oracle standard、realization standard の詳細を確認したいとき。
- agent call parameter の汎用データ構造、prompt builder、path 解決処理、markdown rendering の実装を確認したいとき。

## hash
- 82f129704a2d44ec6aa12ef816a9c64beb9197b89fb90a43e43de19fe8dfc0cf

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出された所見に対応する修正作業を AI agent に依頼するための prompt 正本。
- 所見本文を JSON code block として埋め込み、realization file の修正、realization standard の遵守、テスト通過を目標にした agent call parameter を構築する。
- 所見を絶対指示ではなく作業ヒントとして扱う注意、commit 禁止、realization write の file access mode など、所見対応作業の実行条件を定める。

## Read this when
- `cmoc apply fork` の所見対応 agent call で使う role、goal、注意事項、file access mode、model class、reasoning effort を確認または変更したいとき。
- 所見リストを prompt に埋め込む形式や、所見対応作業へ渡す dynamic prompt の構成を確認したいとき。
- realization file を修正する agent 呼び出しに、oracle and realization basic や realization standard を含める箇所を確認したいとき。

## Do not read this when
- `cmoc apply fork` 以外のサブコマンド用 prompt や agent call parameter を確認したいとき。
- 所見の検出ロジック、fork 処理本体、テスト実行方法、または実際の realization file 修正手順を調べたいとき。
- 共通の prompt 組み立て処理、構造化 markdown の描画、path placeholder 解決の実装を直接確認したいとき。

## hash
- 842c443ac3b9ede9dc4f5e6dfff8ec0e4561e0b63de29372c5aecb3f0f9f2eca
