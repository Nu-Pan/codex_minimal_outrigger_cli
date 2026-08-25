# `edit`

## Summary
- oracle 編集用の agent call 起動定義を扱うディレクトリです。現時点では `launch_exec.py` が、`cmoc oracle edit` の本命処理および仕様削減処理に使う `codex exec` の prompt、アクセスモード、モデル・推論設定、作業ディレクトリ、indexing 実行有無を定めています。

## Read this when
- `cmoc oracle edit` の本命 agent call または仕様削減 agent call の起動条件・パラメータを確認または変更するとき。
- oracle 編集用 prompt の構築や、仕様削減時の参照境界を確認するとき。

## Do not read this when
- oracle file の編集内容や仕様そのものを確認したいとき。
- agent call の一般的なパラメータ定義だけを確認したいとき。

## hash
- fe0644b6cf6c750287f22e4e609cec477640c3ac296f58ed85d61afb88a455e2

# `investigation`

## Summary
- `cmoc oracle investigation` 用の TUI 起動パラメータを構築する関数を定義する。ユーザー指示を完全プロンプトへ組み込み、oracle 調査向けの読み取り専用範囲、リポジトリルート起点、固定モデル、最大推論強度、インデックス事前処理などを設定する。

## Read this when
- `cmoc oracle investigation` の TUI 起動パラメータや、oracle 調査エージェントへユーザー指示を渡す経路を確認・変更するとき。

## Do not read this when
- oracle 調査プロンプトの一般仕様を確認するときは、完全プロンプトを構築する定義元を直接読む。
- TUI 起動以外の prompt builder、パス解決、構造化文書レンダリングの仕様を確認するときは、それぞれの定義元を直接読む。

## hash
- d993e860d3bfabef8ec188919fce28012f89dd458e85f1714606d4bdb8160b59

# `review`

## Summary
- oracle review 用の所見列挙・採否判定・整理・擁護理由調査・反証理由調査に関する Structured Output スキーマと、各 agent call の prompt／起動パラメータ定義を収録するディレクトリ。各 JSON スキーマは対応するレビュー処理の出力契約を示し、各 Python ファイルは入力所見や既知理由を agent call へ渡す構築入口となる。

## Read this when
- oracle review の所見列挙、採否判定、重複・矛盾整理、擁護理由追加、反証理由追加に関する出力契約を確認するとき。
- これらの agent call の prompt、oracle 専用アクセス制約、モデル・推論設定、Structured Output 指定、インデックス事前処理を確認・変更するとき。

## Do not read this when
- oracle review の具体的な判定基準、所見内容、レビュー方針を確認したいときは、各 agent call が参照するレビュー規則や oracle file を直接読むべきです。
- このディレクトリ以外の agent call の出力契約や、レビュー実行そのものの処理を確認するときは、対応する別のスキーマまたは実装へ直接進むべきです。

## hash
- d9e40f99fd619dd4806274ea689fde499121ce1726e2c7bf7b99523062510a8c
