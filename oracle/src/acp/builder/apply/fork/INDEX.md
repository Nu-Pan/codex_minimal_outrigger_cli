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
- `cmoc apply fork` の作業レポート向けに、適用用ブランチ上の差分テキストから人間向け変更要約を生成する AI 呼び出しパラメータを組み立てる正本仕様断片。
- 未整形の `git diff` 出力を読み取り専用コンテキストとして prompt に埋め込み、変更内容を指定 schema で返す要約担当エージェントを呼ぶためのモデル種別、推論量、アクセスモード、出力 schema 参照を定める。

## Read this when
- `cmoc apply fork` の作業レポートに載せる変更要約の生成 prompt や AI 呼び出し条件を確認・変更したいとき。
- 適用用ブランチ上の差分をどのような入力として要約エージェントへ渡すかを確認したいとき。
- 変更要約生成で使う読み取り専用制約、モデルクラス、推論量、出力 schema の接続を確認したいとき。

## Do not read this when
- `cmoc apply fork` の実際の差分取得、ブランチ操作、適用処理そのものを調べたいとき。
- 変更要約の JSON schema 本体だけを確認したいとき。
- 汎用 prompt 構築処理や共通 prompt 部品の実装詳細を調べたいとき。
- `cmoc apply fork` 以外のサブコマンドのレポート生成や要約 prompt を調べたいとき。

## hash
- e958bca0852f6b124010f16314781a5093835941077ed2faef44217ce9587626

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` で、指定された oracle file または realization file を起点に realization file の所見をファイル単位で列挙する AI 呼び出しパラメータを構築する正本実装。
- 読み取り専用で oracle standard、realization standard、apply review standard を含む complete prompt を組み立て、所見リスト用の Structured Output schema を指定して MAINSTREAM モデルへ渡す役割を持つ。

## Read this when
- `cmoc apply fork` のファイル単位レビューや所見リストアップの prompt 内容、AI の役割、調査対象、達成条件を確認したいとき。
- 所見列挙用エージェント呼び出しで参照する standard 群、ファイルアクセスモード、モデルクラス、推論強度、出力 schema の選択を確認したいとき。
- 対象パスとリポジトリルートを prompt にどう埋め込み、oracle file と realization file をどの範囲で読む前提にしているかを確認したいとき。

## Do not read this when
- `cmoc apply fork` のファイル単位ではない処理、全体統合、実際の fork 適用、またはレビュー結果の集約ロジックを確認したいとき。
- 所見リストの JSON schema 自体の項目や検証条件を確認したいとき。
- path keyword や repo root 解決の一般仕様、complete prompt の共通構築処理、standard 本文そのものを確認したいとき。

## hash
- 828e4f9dfd774dd768a2937f394254c2d7c1f5cc9145338503b6a3f8207b7700

# `finding_application.py`

## Summary
- `cmoc apply fork` が所見本文をもとに realization file 修正用の AI 呼び出しパラメータを組み立てる正本実装。
- 修正担当エージェント向けに、所見はヒントであり絶対指示ではないこと、git add と git commit を禁止すること、realization standard に従うことを含む完全 prompt を生成する。
- モデル種別、reasoning effort、realization write のファイルアクセス権限、生成済み markdown prompt を `AgentCallParameter` として返す。

## Read this when
- `cmoc apply fork` の所見対応作業で、AI エージェントにどの role、goal、注意事項、所見本文、標準文書を渡すかを確認したいとき。
- 所見修正用の prompt に含める制約、特に所見本文の扱い、git 操作禁止、realization file の修正権限を確認したいとき。
- 所見対応作業のエージェント呼び出しで使う model class、reasoning effort、file access mode の正本値を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の CLI 解析、fork 作成、差分適用、レビュー実行など、所見対応 prompt 生成以外の処理を調べたいとき。
- oracle file と realization file の基本定義や標準そのものを読みたいとき。
- 生成された prompt を受け取った後に realization file をどう修正するかという、個別の実装修正手順を調べたいとき。

## hash
- 5ccbcdfb0b6df05c24d272cc714f85e83eda521118be32160ce9294c947e0064

# `finding_list.json`

## Summary
- 実装調査で見つかった問題を、人間が修正要否を判断し実装担当へ渡せる所見リストとして表す JSON schema。正本仕様・実装の根拠位置、要求、観測された実装、問題理由、修正方針をそろえて記録するための構造を定義する。

## Read this when
- 実装が oracle file や standard に明確に違反している箇所をレビュー結果として記録する出力構造を確認したいとき。
- 所見に含める根拠位置、仕様要求、観測内容、問題理由、修正方針の粒度を確認したいとき。
- 実装レビューや fork/apply 系の処理で、検出された findings を機械処理できる JSON として扱う箇所を実装・テストするとき。

## Do not read this when
- 実装差分の判定ロジックや、どのファイルを調査対象にするかの探索手順を知りたいとき。
- oracle file と realization file の基本定義やレビュー基準そのものを確認したいとき。
- 所見リストを利用者へ表示する文面や CLI 出力全体の振る舞いを確認したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `refine_finding.py`

## Summary
- `cmoc apply fork` で realization file に対する所見リストを改善する AI エージェント呼び出しパラメータを組み立てる正本実装。入力されたファイル別所見の連結結果を prompt に埋め込み、重複・矛盾・明らかな False-Positive の除去、新規所見の追加、先頭から順に消化可能な所見リストへの整理を依頼する。
- 読み取り専用のファイルアクセス、oracle・realization・apply review の各標準を含む完全 prompt、 flagship model と高い reasoning effort、所見リスト用 schema を返す呼び出し設定を定義する。

## Read this when
- `cmoc apply fork` のレビュー結果や所見リストを、実装変更前に整理・精査するための agent 呼び出し内容を確認したいとき。
- 所見リスト改善 prompt に含める役割、目標、入力所見、参照標準、ファイルアクセス制約を変更・検証したいとき。
- apply fork 系の処理で、所見リスト用 Structured Output schema がどの agent 呼び出しに紐づくかを確認したいとき。

## Do not read this when
- `cmoc apply fork` の実際の実装適用、fork 作成、ファイル編集、git 操作の処理を調べたいとき。
- 所見リストの JSON schema 自体、または改善後 JSON の項目定義を確認したいとき。
- oracle file や realization file の一般定義、path keyword、共通 prompt 組み立て処理そのものを調べたいとき。

## hash
- dbcd18cc3d27d4bf74eb05d955961889209e4d95d238beac43350f7867314d6a
