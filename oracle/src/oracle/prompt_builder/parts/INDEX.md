# `apply_review_standard.py`

## Summary
- oracle file と realization file の不整合を見つけて所見化するための規範を構築する。ここでは、実装差の指摘に使う判断基準と、その根拠の取り方を定めている。
- oracle file に明記されていない隙間を、所見の根拠として使ってよいかを判断するための規範を扱う。仕様断片だけで断定せず、正本仕様と実装の両方から自然に言える範囲に限定する。
- realization file だけを見て明らかな致命的問題を所見に含めてよいかを判断するための規範を扱う。品質改善の提案ではなく、実行不能や明白なバグのような重大問題を対象にする。

## Read this when
- oracle file と realization file の差分をレビューし、所見の根拠を整理したいとき。
- 仕様断片の未定義部分を、所見として扱うべきか迷うとき。
- 実装単体で見て明らかな致命的問題を、所見として挙げるか確認したいとき。

## Do not read this when
- 所見の列挙ではなく、実装そのものやテストを直したいとき。
- oracle file にない細部まで含めた網羅的な仕様確認をしたいとき。
- 単なる可読性改善や命名改善だけを確認したいとき。

## hash
- 4fd4833b9568a36c8a24181f5f9811732a0ed2b8e831d309ff00b05156a03974

# `file_access_rule.py`

## Summary
- AI エージェント向けのファイル読み書き規則を組み立てる正本側の部品。`FileAccessMode` ごとに、どの範囲を読み書き禁止にするかの文面と `StructDoc` を返すため、このルーティングはアクセス制御文面やモード追加・変更の確認時に読む。

## Read this when
- ファイルアクセス規則の文面を追加・変更したいとき。
- `FileAccessMode` ごとの禁止範囲や例外の扱いを確認したいとき。
- `repo-root` と `work-root` の関係で、どの範囲を規則に含めるかを見直したいとき。

## Do not read this when
- 実際のファイルアクセス判定ロジックそのものを追いたいときは、呼び出し側や関連する実行時コードを見る。
- `StructDoc` の内部表現や `PlaceholderMap` の一般的な定義だけを知りたいときは、ここではなくそれぞれの定義元を読む。
- この部品の文面を使って生成された実装側の挙動確認だけが目的なら、生成先の realization 側を読む。

## hash
- f60612bd39bb52368a6a96a1c286335e1f0ce317b6d0b3ad3f9d46f04390bcd0

# `index_entry_standard.py`

## Summary
- `INDEX.md` エントリーの書き方を規範化するための標準。対象を読むべき条件、対象の責務、読むべきでない境界をどう書くかを決める。
- 対象本文を読まなくても進む先を選べるようにすることが主眼で、詳細説明や機械的な識別情報は入れない。

## Read this when
- `INDEX.md` に載せる案内文の粒度や書き方を決めたいとき。
- 同じ階層の対象の中から、どれを読むべきかを判断できる入口文を整えたいとき。
- 対象の責務と、読む条件と、読まなくてよい境界を短く整理したいとき。

## Do not read this when
- 個別の実装や詳細仕様を確認したいときは、各対象の本文を直接読む。
- 単なるファイル名や出力形式の確認だけが目的なら、この標準ではなく周辺のルーティング規則側を見る。
- 対象外の責務や将来用途まで含めた包括的な目次を作りたいときは、この断片ではなく別の規範を読む。

## hash
- 942b23384c6e0468b807b626d94ad638b8898badc3a7dd37cd5cb0a8f771ddce

# `oracle_and_realization_basic.py`

## Summary
- `oracle` と `realization` の基本定義を、`{{work-root}}` を基準に短く参照できるようにする説明部品。上位の prompt/文書生成で、両者の境界や下位概念の呼び分けが必要なときに読む。

## Read this when
- `oracle file` と `realization file` の定義境界を確認したいとき。
- `oracle doc`、`oracle src`、`oracle test`、`realization implementation`、`realization test`、`realization ancillary` の呼び分けを揃えたいとき。
- このリポジトリで使う `{{work-root}}` 基準の用語整理が必要なとき。

## Do not read this when
- 個別の oracle 仕様断片や実装方針を知りたいときは、対応する下位の oracle 文書や実装本文を直接読む。
- `INDEX.md` の具体的なルーティング先だけを探しているときは、より下位階層の案内文書を読む。
- ファイル一覧や実装の詳細を確認したいだけなら、この基本定義ではなく該当モジュール本文を読む。

## hash
- af9deebb609c1a8d26f18656aa74fe8d085ae7b14aea7c9888b3b44482c4d3f5

# `oracle_review_standard.py`

## Summary
- `cmoc review oracle` で oracle file の所見分類ルールを組み立てる本文。fatal / minor / 所見にしないものの境界を確認したいときに読む。

## Read this when
- `cmoc review oracle` のレビュー結果として、どの差分を fatal 所見や minor 所見にするか判断したいとき。
- oracle file だけから問題と言い切れる範囲と、仕様の隙間として扱う範囲の境界を確認したいとき。
- 用語の不統一、typo、日本語の誤りをレビュー所見に含める基準を確認したいとき。

## Do not read this when
- oracle と realization の基本区分や、oracle file の一般原則を確認したいときは、基礎説明の本文を読む。
- `cmoc review oracle` の CLI 入出力や実行フローだけを確認したいときは、この規範ではなく実行側を読む。
- oracle file に適用するレビュー基準ではなく、realization file の実装品質や整理方針を確認したいときは別の標準を読む。

## hash
- e75eefaf48b7cdec017e185b15562c1b698944df71465d545b684de3f9eb300e

# `oracle_standard.py`

## Summary
- `oracle standard` の規範文書を組み立てる入口。標準群の並び、各標準の背景・要求・例の内容、そして `StructDoc` へ渡す構造を確認したいときに読む。
- この定義を変えるべきなのは、oracle file 全体に適用する基準文の内容や構成を調整するときで、個別の oracle file や他の prompt builder の内容を直したいだけなら別の対象を見る。

## Read this when
- oracle file に共通する規範文の内容や粒度を見直したいとき
- 標準の追加・削除・再分類が必要か判断したいとき
- `oracle standard` という文書の構造と、各標準の責務の境界を確認したいとき

## Do not read this when
- 個別の oracle file や実装の振る舞いを直したいだけのとき
- `StructDoc` や共通の標準変換処理の一般的な実装だけを確認したいとき
- この文書の下流で使われる別の prompt builder の内容を見たいとき

## hash
- 44a731f03bef07e78578477f06d0911569244875809ae1c0d17c7dc9f57b6df2

# `realization_standard.py`

## Summary
- realization file に対する規範文書を組み立てる。実装・テスト・補助ファイルの増やし方や、既存実装の整理方針を変えるときに読む。

## Read this when
- realization file の追加・分割・統合・削除の方針を決めたい。
- realization code や realization test の重複整理、旧仕様の除去、抽象化の追加可否を判断したい。
- コメントや docstring に残すべき意図・根拠・削除条件の書き方を確認したい。

## Do not read this when
- 個別の実装ファイルやテストの挙動だけを確認したいなら、その対象の本文を直接読む。
- oracle 側の別の仕様断片を探しているだけなら、この定義文書ではなく該当分野の oracle 本文を読む。

## hash
- 6daf5d447392ace3472e1530bfcee535755fba0919937f99edb52f6de4f58a90

# `routing_rule.py`

## Summary
- `INDEX.md` を起点に、作業対象へ進むための案内だけをまとめる。本文そのものではなく、必要な文脈を絞り込むためのルーティング基準として使う。
- 同階層や下位階層に進むべきか、候補本文を直接読むべきかの判断を助ける。

## Read this when
- 対象領域をまだ絞れておらず、まず読むべき本文候補を選びたいとき。
- 下位ディレクトリへ進む前に、その階層の案内が必要なとき。
- `INDEX.md` だけでは判断できず、候補本文を読んで根拠を確認したいとき。

## Do not read this when
- すでに読むべき本文が分かっていて、直接その本文を確認したほうが早いとき。
- 総当たりで関連ファイルを探すのではなく、他の案内やより直接の本文に進むべきとき。
- `INDEX.md` と本文の差異そのものを確認しているときは、案内ではなく本文を根拠に扱うべきとき。

## hash
- 0264980cdd927da5be0d9580428c1d9fb3a129f66b254b0d462d7be9cbd1af5b
