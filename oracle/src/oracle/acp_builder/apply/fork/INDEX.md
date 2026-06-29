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
- `cmoc apply fork` の作業レポート向けに、git diff そのものを入力として変更要約生成用の agent call parameter を組み立てる oracle src。
- ファイルアクセスプロファイル、complete prompt、Structured Output schema の参照先、モデル種別と推論強度を結び、差分要約担当 agent の呼び出し条件を定義する。

## Read this when
- `cmoc apply fork` が作業レポート用の変更要約を生成する際の prompt、入力差分の扱い、agent call parameter の構成を確認したいとき。
- 変更要約 agent に渡す role、summary、goal、補助プロンプト、プレースホルダ、ファイルアクセス権限の正本仕様断片を確認したいとき。
- `cmoc apply fork` の変更要約出力 schema と prompt 構築処理の対応関係を調べたいとき。

## Do not read this when
- `cmoc apply fork` の実際の git 操作、branch 操作、差分取得処理を確認したいとき。
- 変更要約の Structured Output schema の項目そのものを確認したいとき。
- 汎用的な prompt 構築、ファイルアクセスプロファイル、パスプレースホルダ解決の共通実装を確認したいとき。

## hash
- 39f8e03312feee3f3e19f1a92821cbaecf0570ef2a0d12c3d0d035f230c0ac22

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
- `cmoc apply fork` で特定ファイルを起点に realization file の要修正点を列挙するための、AI エージェント呼び出しパラメータを構築する prompt 正本。file access profile、complete prompt の役割・目的・標準適用、モデルクラス、reasoning effort、出力 schema 対応ファイルを定める。

## Read this when
- `cmoc apply fork` のファイル単位の所見リストアップ agent call の入力 prompt や呼び出しパラメータを確認・変更したいとき。
- 所見列挙で読むべき対象、Structured Output schema への要求、apply review standard の適用有無を確認したいとき。
- ファイル数分呼び出される apply fork 系処理で、モデルクラスや reasoning effort の選択理由を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の処理フローや集約処理を確認したいだけの場合。
- 所見リストの Structured Output schema そのものを確認したい場合。
- file access profile、path 解決、complete prompt の汎用的な組み立て仕様を確認したい場合。

## hash
- 65814c968bbfec2eb7cf744fafd35e758135bf71e4fc3298351e78724031fe0c

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出された所見に対応するための agent call parameter を構築する正本実装。所見リストをプロンプト本文へ埋め込み、realization file の修正担当 AI に渡す role、goal、file access profile、標準規則、placeholder を組み立てる。

## Read this when
- `cmoc apply fork` の所見対応作業で AI に渡すプロンプト、モデル種別、reasoning effort、file access profile を確認・変更したいとき。
- 所見本文の扱い、git 操作禁止、realization standard の適用など、所見対応 agent call の作業条件を確認したいとき。
- 所見リストがどのような markdown 構造や JSON code block としてプロンプトへ渡されるかを確認したいとき。

## Do not read this when
- `cmoc apply fork` 以外のサブコマンドや、所見対応ではない通常の agent call parameter を確認したいとき。
- oracle file や realization file の一般定義、path placeholder の意味、file access profile の詳細仕様を確認したいとき。
- 所見を生成する側の処理や、実際に realization file を修正する実装本体を探しているとき。

## hash
- b49e1a25fa969d2dcc4888309a1d2af679a40908dfdfaf0e72bd64d95a387f5a
