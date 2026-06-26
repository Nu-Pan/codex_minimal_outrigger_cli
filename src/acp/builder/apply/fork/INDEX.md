# `change_summary.json`

## Summary
- 差分要約を意味カテゴリごとに整理するための JSON Schema。変更カテゴリごとの人間向け要約と、根拠となる主要な変更パスの集合を表す構造を定義する。

## Read this when
- フォーク適用や変更処理の結果として、変更内容をカテゴリ別の要約として出力・検証する schema を確認したいとき。
- 差分要約に含める情報の粒度、カテゴリ単位のまとまり、主要な変更パスの扱いを確認したいとき。

## Do not read this when
- 実際の差分生成アルゴリズム、フォーク作成手順、ファイル適用処理の制御フローを調べたいとき。
- 個別カテゴリ名の網羅的な一覧や、変更パス抽出の具体的な実装規則を探しているとき。

## hash
- 4148f8f7efb949b4872076b64dcb4bd2792df6d888011903c10501ce6f519987

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向けに、変更要約生成用の AI エージェント呼び出しパラメータを組み立てる実装。
- 未整形の git 差分を読み取り専用コンテキストとして prompt に埋め込み、効率重視モデル・中程度推論・対応する Structured Output schema を指定して返す。

## Read this when
- `cmoc apply fork` 実行後の変更要約レポートを生成する prompt やエージェント呼び出し条件を確認・変更したいとき。
- 作業ブランチ上の git diff をどのように AI 要約担当へ渡しているかを追いたいとき。
- 変更要約生成で使うモデル種別、推論強度、ファイルアクセスモード、出力 schema の対応付けを確認したいとき。

## Do not read this when
- 差分そのものの取得方法、fork 適用処理、ブランチ操作、または git コマンド実行処理を調べたいだけのとき。
- 生成される変更要約 JSON の項目定義や schema 内容を確認したいだけのとき。
- 汎用 prompt 部品の構築規則や markdown レンダリング処理を調べたいとき。

## hash
- f7139a4d9752c26d62ddb939269bfbde48caa56ed647ad461b99e24cc8ad869b

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
- `cmoc apply fork` で、指定された oracle file または realization file を起点に、work tree 内の realization file の要修正点をファイル単位で列挙するための AI 呼び出しパラメータを構築する実装。
- 所見リストアップ担当としての役割、読み取り専用のファイルアクセス、oracle/realization/apply review 各 standard を含む complete prompt を組み立て、MAINSTREAM モデル・MEDIUM reasoning の呼び出し設定として返す。

## Read this when
- `cmoc apply fork` の中で、対象ファイル単位に要修正点を調査するエージェント呼び出しの prompt やモデル設定を確認・変更したいとき。
- apply fork の所見列挙フェーズで、target path と work root がどのように prompt に埋め込まれ、どの standard が有効化されるかを確認したいとき。
- ファイル単位の所見リストアップ結果に対応する Structured Output schema ファイルの選ばれ方を確認したいとき。

## Do not read this when
- apply fork 全体の制御フロー、複数ファイルへの呼び出し順、列挙結果の集約・適用・表示を調べたいだけのとき。
- complete prompt の共通構築処理、path 解決処理、AgentCallParameter や ModelClass そのものの定義を調べたいとき。
- oracle file や realization file の定義、apply review standard の内容そのものを確認したいとき。

## hash
- cb7b0d664859e5e14b4544befaed393c3d3d520aa898fbed026cf429c177cfba

# `finding_application.py`

## Summary
- 所見リストを受け取り、`cmoc apply fork` の所見対応作業を AI エージェントへ依頼するための呼び出しパラメータを組み立てる実装。所見本文を JSON コードブロックとしてプロンプトに埋め込み、realization file 修正用の役割・目標・注意点・標準参照を含む完全な prompt を生成する。

## Read this when
- `cmoc apply fork` で検出済み所見を修正担当エージェントへ渡す prompt や AgentCallParameter の内容を確認・変更したいとき。
- 所見本文の列挙形式、JSON 表現、作業上の注意点、realization file 書き込み権限、利用する model class や reasoning effort の指定を調整したいとき。
- 所見対応作業で oracle/realization の基本説明や realization standard を prompt に含めるかどうかを確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の fork 作成、ブランチ操作、差分適用、実行制御を調べたいだけのとき。
- 所見を生成・検出する処理そのものを調べたいとき。
- complete prompt の共通構築処理、StructDoc の markdown rendering、repo root 解決、AgentCallParameter 型定義の詳細を調べたいとき。

## hash
- a18a7c5c2a2c1c37f21238d6fa69437dd805ae1dfea7adb82b9f437e27b8bd64
