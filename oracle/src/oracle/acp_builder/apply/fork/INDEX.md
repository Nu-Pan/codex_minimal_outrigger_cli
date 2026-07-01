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
- `cmoc apply fork` の作業レポート用に、git diff そのままの差分テキストから変更要約生成エージェント呼び出しパラメータを組み立てる oracle src。
- 要約担当 AI の role、summary、goal、readonly のファイルアクセス、差分コードブロック、`<repo-root>` プレースホルダ、Structured Output schema の参照先を定義する。

## Read this when
- `cmoc apply fork` で作業レポート向けの変更要約を生成する prompt や agent call parameter の正本仕様を確認したいとき。
- `raw_git_diff` をどのように prompt へ渡すか、差分要約生成時の file access mode、model class、reasoning effort、出力 schema の指定を確認したいとき。
- `cmoc apply fork` の変更要約が参照する `<repo-root>` プレースホルダや oracle/realization 基本説明の組み込み方を確認したいとき。

## Do not read this when
- `cmoc apply fork` の実際の git 操作、branch 操作、作業レポート保存処理を確認したいとき。
- 差分要約の Structured Output schema そのものの項目や型を確認したいとき。
- apply 系以外のサブコマンドの prompt や agent call parameter を確認したいとき。

## hash
- 6e989f5c5236652fcaa587074dd0aa04df726ac6c636631cdbfdea6e27f4af94

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
- `cmoc apply fork` で、1 つの対象ファイルを起点に realization file の要修正点を列挙するための AI エージェント呼び出しパラメータを組み立てる oracle src。
- 読み取り専用のファイルアクセス、oracle/realization/apply review 各 standard を含む complete prompt、対象パスと repo root の placeholder、MAINSTREAM モデルと MEDIUM reasoning effort の選択を正本として定める。

## Read this when
- `cmoc apply fork` のファイル単位所見リストアップ呼び出しで、AI に渡す role、summary、goal、標準文書、placeholder、Structured Output schema の指定を確認したいとき。
- 対象ファイルを起点に、必要な oracle file と realization file を読ませて realization file の要修正点を列挙させる prompt 正本を確認したいとき。
- ファイル数分呼び出される処理で MAINSTREAM モデルを使う理由や、トークン消費と下流影響の判断根拠を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の制御フロー、所見の統合、修正適用、実行結果処理を調べたいとき。
- apply review standard の内容そのもの、または所見リストが満たすべき判定基準の詳細を調べたいとき。
- AgentCallParameter、complete prompt builder、path placeholder 解決、markdown rendering などの共通部品の実装詳細を調べたいとき。

## hash
- 9b0f19cf132f0da09b6530de64be558f71605d380949239b6c3c98014b8ad910

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出された所見に対応するための AI エージェント呼び出しパラメータを構築する oracle src。所見一覧を JSON コードブロックとして作業 prompt に埋め込み、realization file の修正担当に渡す正本 prompt の内容を定める。

## Read this when
- `cmoc apply fork` の所見対応作業で、エージェントに渡す role、summary、goal、注意事項、所見本文の組み立てを確認したいとき。
- 所見対応エージェントの file access mode、model class、reasoning effort、または prompt に含める oracle/realization standard の指定を確認したいとき。
- `cmoc apply fork` が生成する所見対応用 AgentCallParameter の構成を変更・検証したいとき。

## Do not read this when
- `cmoc apply fork` 以外のサブコマンド用 prompt や agent call parameter を確認したいとき。
- 所見の検出ロジック、fork の作成処理、または git 操作そのものを調べたいとき。
- realization file の修正内容そのものや、所見対応エージェントが実行した結果を確認したいとき。

## hash
- f9f304dfe1dda61a95ab9a19e78c9f09560cf0e018b07acd09e4b4a336332db5
