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
- `cmoc apply fork` の作業レポート向けに、適用ブランチ上の生の差分を人間向け変更要約へ変換する AI 呼び出しパラメータを組み立てる正本実装。
- 差分本文を補助入力として complete prompt に埋め込み、読み取り専用のファイルアクセス、効率重視モデル、対応する Structured Output schema を指定して返す責務を持つ。

## Read this when
- `cmoc apply fork` の作業レポートで、git diff 由来の変更内容をどのような role、summary、goal、補助入力で要約エージェントへ渡すか確認したいとき。
- 変更要約生成用の AgentCallParameter のモデル種別、reasoning effort、ファイルアクセスモード、schema 参照先を確認または変更したいとき。
- apply fork 系の処理で、差分テキストを解析・整形せずに prompt へ渡す境界を確認したいとき。

## Do not read this when
- `cmoc apply fork` の実際の git 操作、ブランチ作成、差分取得、適用処理の流れを確認したいだけのとき。
- 変更要約の Structured Output schema そのものの項目や制約を確認したいとき。
- complete prompt の共通構築規則、path placeholder の解決規則、StructDoc の markdown 描画仕様を調べたいとき。

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
- `cmoc apply fork` で、指定された oracle file または realization file を起点に realization file の要修正点をファイル単位で列挙する AI エージェント呼び出しパラメータを構築する正本。
- 起点パスを `<target-path>` として complete prompt に埋め込み、oracle standard、realization standard、apply review standard を含む read-only 調査用 prompt を生成する。
- ファイル数分呼び出される重い処理だが、下流工程への影響が大きいため MAINSTREAM モデルと MEDIUM reasoning を選ぶ、という判断根拠を持つ。

## Read this when
- `cmoc apply fork` の中で、特定ファイルを起点に所見リストアップ用の agent call parameter をどう作るか確認したいとき。
- apply fork の所見列挙 prompt に含める role、summary、goal、placeholder、standard 群、file access mode の構成を確認したいとき。
- 所見リストアップ処理で oracle file と realization file を read-only に調査させる意図や、`<target-path>` の解決方法を確認したいとき。
- ファイル単位の所見列挙が下流工程に与える影響を理由に、モデルクラスや reasoning effort をどう選んでいるか確認したいとき。

## Do not read this when
- `cmoc apply fork` の実際の所見統合、修正適用、レビュー結果の解釈など、ファイル単位の列挙 prompt 構築より後段の処理を調べたいとき。
- oracle file と realization file の基本定義、path keyword、各 standard の本文そのものを確認したいとき。
- agent call parameter の汎用データ構造、model class、reasoning effort、file access mode の定義を確認したいとき。
- complete prompt の組み立て規則や markdown rendering の詳細を確認したいとき。

## hash
- 9b0f19cf132f0da09b6530de64be558f71605d380949239b6c3c98014b8ad910

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出された所見に対応する修正作業を、AI エージェントへ依頼するための呼び出しパラメータを組み立てる正本実装。
- 所見リストを JSON コードブロックとして prompt に埋め込み、realization file の修正、realization standard への準拠、git add/commit 禁止を含む作業指示を生成する。
- モデル種別、reasoning effort、ファイルアクセス権限、完全 prompt の markdown レンダリング結果をまとめたエージェント呼び出し入口を担う。

## Read this when
- `cmoc apply fork` の所見対応フェーズで、AI に渡す prompt の役割・内容・制約を確認したいとき。
- 所見本文をどの形式で prompt に含めるか、複数所見をどう列挙するかを確認したいとき。
- 所見対応作業における file access mode、モデルクラス、reasoning effort の指定根拠を確認したいとき。
- realization file 修正依頼に realization standard や oracle/realization basic を含めるかどうかを確認したいとき。

## Do not read this when
- `cmoc apply fork` の通常修正処理そのものや、realization file の具体的な編集アルゴリズムを調べたいとき。
- 所見の生成、分類、検出、レビュー処理を調べたいとき。
- 共通の prompt 構築 API、構造化 markdown レンダリング、パス解決、エージェント呼び出しパラメータ型そのものの仕様を調べたいとき。
- `cmoc apply fork` 以外のサブコマンド用 prompt や、所見対応ではない apply 系 prompt を調べたいとき。

## hash
- f9f304dfe1dda61a95ab9a19e78c9f09560cf0e018b07acd09e4b4a336332db5
