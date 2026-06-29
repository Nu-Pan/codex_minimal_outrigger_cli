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
- ACP builder の realization 側入口であり、oracle 側 builder 実装を `acp.builder` 配下の import 経路から参照できるようにする互換 package 群を束ねる。
- apply、indexing、review、session、tui などの builder 領域へ進む分岐点で、主な実体は oracle 側に置かれ、この階層では公開経路、薄い adapter、実行側契約に合わせた小さな補正を扱う。
- 具体的な AgentCallParameter 生成、Structured Output schema 連携、review finding 系の検証、session join、TUI パラメータ解決などは下位領域へ進んで確認する。

## Read this when
- realization implementation 側で ACP builder の各領域がどの package 境界から公開されているかを把握したいとき。
- oracle 側 builder 実装と `acp.builder` 配下の互換 import 経路の対応関係を確認したいとき。
- apply、indexing、review、session、tui のどの builder 領域へ進むべきかを、この階層を入口に切り分けたいとき。
- builder 本体ではなく、realization 側で oracle 側定義を再公開する窓口や、実行時契約に合わせた薄い補正箇所を探しているとき。

## Do not read this when
- ACP builder の正本仕様、prompt 本文、Structured Output schema の詳細、model 設定などを確認したいとき。その場合は oracle 側の対応箇所を読む。
- AgentCallParameter、path model、enum などの基礎定義そのものを調べたいとき。その場合は基本定義の領域を読む。
- fork 作成、git 操作、差分適用、CLI 入出力、TUI 画面描画など、builder 呼び出し後または周辺 workflow の制御を調べたいとき。
- 各 builder 領域の具体的な生成ロジック、判定基準、入出力変換を直接確認したいとき。その場合は該当する下位領域または委譲先の oracle 側実装を読む。

## hash
- 22fd3d5f0a6676777f1fffa33d6fb2164a39cd35890923b4d97ece2c15b43c8c
