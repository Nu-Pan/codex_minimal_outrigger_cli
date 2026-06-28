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
- ACP builder 配下の realization 側パッケージを束ねる領域。正本側 builder 実装への互換 import 境界を中心に、apply、indexing、review、session、TUI などの下位 builder 領域へ進むための入口として機能する。
- この階層自体は builder の主要な生成ロジック本体ではなく、src 側の公開経路から oracle 側実装や下位領域へ到達できるようにするための薄い接続層を扱う。

## Read this when
- ACP builder 全体の src 側入口が、正本側 builder package とどう対応しているかを確認したいとき。
- apply、indexing、review、session、TUI など、どの下位 builder 領域へ進むべきかを切り分けたいとき。
- realization implementation 側で、builder 関連の import 互換 package や再公開境界の有無を確認したいとき。
- builder の実処理本体ではなく、src 側から oracle 側実装へ接続する公開入口の構成を把握したいとき。

## Do not read this when
- builder の具体的な生成処理、データ構造、バリデーション、prompt 構成、制御フローを調べたいとき。その場合は対応する下位領域または正本側実装を読む。
- fork 適用、review finding、session join、TUI 起動など個別機能の挙動を直接確認したいとき。その場合は該当する下位領域へ進む。
- agent call parameter の共通定義、モデル種別、reasoning、ファイルアクセスモードそのものを調べたいとき。共通 ACP 定義や基本定義を読む。
- 正本仕様断片としての要求を確認したいとき。この領域は realization 側の互換入口であり、正本仕様本文ではない。

## hash
- 8cb34547ccd64e02d650c3533c16f9b9c874dd23139a0dc6d18e87bf6f73354a
