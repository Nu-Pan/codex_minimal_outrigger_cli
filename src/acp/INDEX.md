# `__init__.py`

## Summary
- oracle src 側の acp 実装と互換の import 経路を提供するためのパッケージ入口。
- 実処理や公開 API の定義ではなく、acp 名前空間を import 対象として成立させるための最小の入口として位置づけられる。

## Read this when
- acp パッケージ自体の import 入口が必要か、または oracle src 互換の import 経路が存在するかを確認したいとき。
- acp 配下の実装を読む前に、パッケージ入口の責務が実処理ではなく互換 import の提供に限られていることを確認したいとき。

## Do not read this when
- acp の具体的な処理内容、データ構造、関数、クラスの挙動を調べたいとき。
- oracle src の仕様断片そのもの、または acp 以外の import 互換入口を調べたいとき。

## hash
- a4fa2404d751d07495abc462d628458a8e48984730fe92845a6644bfa89ef089

# `builder`

## Summary
- ACP builder 領域の realization 側 package で、正本側実装を src 側の import 経路から参照するための互換境界をまとめる。
- この領域自体は生成・適用・レビュー・セッション・TUI などの処理本体ではなく、正本側 package への再公開入口と下位領域への接続点を束ねる位置づけである。
- 下位には、適用、indexing、review、session、TUI などの互換入口が分かれており、具体的な処理を読む前に realization 側の公開経路を確認するための案内点になる。

## Read this when
- ACP builder の src 側 package が、正本側 builder 実装とどのような import 互換境界を持つか確認したいとき。
- ACP builder 配下で、処理本体へ進む前に、適用、indexing、review、session、TUI などの下位領域の入口を選びたいとき。
- 正本側実装を src 側から再公開しているだけの薄い package か、独自処理を持つ対象かを切り分けたいとき。
- 既存の import 経路を保つための公開入口や package 初期化の有無を確認したいとき。

## Do not read this when
- ACP builder の具体的な生成処理、変換処理、適用処理、判定条件、データ構造、入出力仕様を調べたいとき。その場合は正本側の対応実装、または下位のより直接の対象を読む。
- TUI の画面構成、入力フロー、パラメータ解決の詳細など、実際の挙動を確認したいとき。正本側の TUI 実装を読む。
- review や session join などの個別アルゴリズム、検証、競合解決、finding 処理の詳細を調べたいとき。対応する下位領域または正本側本文を読む。
- oracle file としての正本仕様断片を確認したいとき。この領域は realization 側の互換 package であり、正本仕様本文ではない。

## hash
- 08eba39d7abc0aadadf3fbdb8076d7994dba10954fbad2aa6ffc25d78ac95d8a
