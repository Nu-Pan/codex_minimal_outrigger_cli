# `edit`

## Summary
- `cmoc oracle edit` における本命編集 agent call と、成功後の仕様削減 agent call の起動設定を組み立てる入口。
- 空の `fork` ディレクトリは、現時点で確認できる本文ファイルを持たない。

## Read this when
- `cmoc oracle edit` の agent call 起動条件、完全 prompt、oracle 専用アクセスモード、作業ディレクトリ、indexing preflight、または仕様削減処理の設定を確認・変更するとき。
- `fork` にファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- oracle file の具体的な編集内容や仕様削減の判断基準を確認したい場合は、実際の編集対象 oracle file を読む。
- 一般的な agent call パラメータや共通 prompt 構築を確認したい場合は、対応する共通 builder や型定義を読む。
- `fork` 配下の具体的なファイルを直接確認できる場合は、空ディレクトリの入口情報を読む必要はない。

## hash
- 3c35c0cf5d8ccca6d044d3ff0e99cdcfdfb946397c7bcb043120ac050141fd19

# `investigation`

## Summary
- `cmoc oracle investigation` の TUI 起動パラメータを構築し、ユーザー指示を調査用完全プロンプトへ組み込む入口。oracle ツリーの読み取り専用調査、作業ディレクトリ、ポリシー設定、起動前インデックス処理を定義する。

## Read this when
- oracle 調査の TUI 起動時に、ユーザー指示の組み込み方、アクセス範囲、作業コンテキスト、各種ポリシー、構造化出力設定、起動前処理を確認するとき。

## Do not read this when
- oracle 調査プロンプトの共通構造や oracle・ルーティング規則そのものを確認したいとき。完全プロンプト生成や各ポリシーの定義元を直接読む方が適切。

## hash
- 4d40b4cdc8c4a0526ac30a8305525fd141a8684915360232fbd8ec6b1e30748f

# `review`

## Summary
- oracle review 配下で、所見の列挙・採否判定・重複整理・賛否理由の追加調査に関する Structured Output スキーマと agent call 構築定義を扱う。
- 各スキーマは所見や理由の調査結果、採否、編集操作など、対応するレビュー段階のエージェント間データ契約を定義する。

## Read this when
- oracle review の所見列挙、採否判定、重複・矛盾整理、擁護理由または反証理由の追加調査について、出力契約や agent call の入力・起動設定を確認または変更するとき。
- 所見本文や既知の賛否理由をレビュー用プロンプトへ渡す経路、oracle の読み取り専用条件、ルーティング条件、Structured Output 設定を追跡するとき。

## Do not read this when
- oracle review の具体的な判定基準、所見内容、oracle file 本文、またはレビュー実行本体を確認したいときは、対応するレビュー規則・oracle file・実装を直接読む。
- oracle review 以外の agent call の出力形式や、一般的な Structured Output の定義だけを確認したいとき。

## hash
- cdd56a530866f6552beea83e1f8e9a644807ac6d979f1704fbbac3014fbe1f70
