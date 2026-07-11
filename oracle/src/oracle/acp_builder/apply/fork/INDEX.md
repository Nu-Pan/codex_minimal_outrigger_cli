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
- `cmoc apply fork` で、起点ファイルから file 単位の所見リストを作るための AI 呼び出し条件と出力設定を確認したいときに読む。ここは prompt 正本で、呼び出し対象・制約・モデル選択の根拠を持つ。

## Read this when
- `cmoc apply fork` の file 単位所見抽出の入力条件、読むべき対象範囲、呼び出しパラメータの決め方を変えるとき。
- 所見リストアップ用 prompt の正本を修正するとき。
- この処理がどの file を前提に読むか、read-only で扱うか、どの設定で呼ぶかを確認したいとき。

## Do not read this when
- 単一の所見本文そのものや各 file の個別判断根拠を知りたいときは、ここではなく対象の oracle file または realization file 本体を読む。
- `cmoc apply fork` 以外のサブコマンドの prompt や、所見列挙以外の役割を見たいとき。
- AI 呼び出しの実行ログや生成済み結果だけを追いたいとき。

## hash
- 2c37b6c27a6232d6b95235b8b0d394b29b1eff1d0159523099da9ffa306ea59e

# `finding_application.py`

## Summary
- `cmoc apply fork` の所見本文から、所見対応用のエージェント呼び出しパラメータを組み立てる責務を持つ。`build_complete_prompt` に渡す role・summary・goal・注意事項・所見一覧のまとめ方と、返す `AgentCallParameter` の方針を確認したいときに読む。

## Read this when
- `cmoc apply fork` の所見対応作業で使うプロンプト内容や、AI 呼び出しパラメータの構成を変えたいとき。
- 所見本文の扱い、作業上の注意、モデル選択、実行モードの固定方針を確認したいとき。

## Do not read this when
- 所見対応の実際の実装やファイル修正方針を追いたいときは、所見対応先の realization 実装を読む。
- 共通の prompt 組み立て規約だけを見たいときは、個別サブコマンド用ではなく `build_complete_prompt` 側を読む。

## hash
- 17959b40cdd8d278c665de924b85da32ca858a994957a5a9b976d827921853fa
