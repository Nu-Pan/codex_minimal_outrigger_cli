# `__init__.py`

## Summary
- 正本側の ACP builder TUI パッケージとの互換性を示すだけの package 初期化地点。具体的な処理や公開オブジェクトは持たず、この階層が互換 package として存在する理由を示す。

## Read this when
- ACP builder の TUI 関連 package が、正本側の対応 package と互換の入口として用意されているかを確認したいとき。
- この package 初期化地点自体に、追加の初期化処理、公開 import、互換性説明があるかを確認したいとき。

## Do not read this when
- TUI の構築処理、画面制御、入出力処理などの実装内容を調べたいとき。
- 正本仕様断片そのもの、または互換先の詳細な挙動を確認したいとき。
- 関数、クラス、定数、CLI 動作などの具体的な公開面を探しているとき。

## hash
- 0a593accdb428d084c035fe120f2a06b5788abb28e112e72252680ca369fb14d

# `launch_tui.py`

## Summary
- TUI 起動用の AgentCallParameter 生成処理を oracle 側の正本実装へ委譲し、既存の公開 import path から同じ関数を参照できるようにする互換接続層。
- TUI 起動パラメータの定義本体は持たず、oracle 側の生成関数を呼び出して戻すことと、公開名として再エクスポートすることだけを担う。
- realization 側または利用者向け公開面に残る既存参照を維持するためのファイルであり、その参照がなくなった時点で削除可能になる。

## Read this when
- TUI 起動パラメータ生成関数の既存 import path を維持する必要があるか確認したいとき。
- oracle 側に置かれた TUI 起動パラメータ生成処理が realization 側からどう接続されているか確認したいとき。
- この互換接続層を削除できる条件、または公開面からの参照残存を調べたいとき。
- TUI 起動パラメータ生成関数の引数一覧や戻り値型が、既存参照に対してどのように中継されているか確認したいとき。

## Do not read this when
- TUI 起動パラメータの実際の組み立て内容や正本仕様を確認したいときは、委譲先の oracle 側実装を直接読む。
- TUI の表示処理、イベント処理、画面構成、入力操作を調べたいときは、この互換接続層ではなく TUI 本体側の実装を読む。
- AgentCallParameter や FileAccessMode の型定義・意味を確認したいときは、それらを定義する基本モジュールを読む。
- 既存 import path の互換性や削除条件に関係しない、新規の TUI 起動仕様を設計したいだけのときは、この接続層を入口にしない。

## hash
- 43ea47b576cd6aaee74b0810690d5e2479c1d0377243b6c03dd36005d18b42a2

# `resolve_parameter.py`

## Summary
- TUI の resolve-parameter builder について、既存の TUI 側 import surface を保つための互換モジュール。正本側の builder 関数を再公開し、TUI 利用者向けに利用可能な file access mode の tuple も公開する。
- 実体のある builder 実装ではなく、canonical な oracle 側実装へ呼び出し元を移行するまで残す互換 import path として位置づけられている。

## Read this when
- TUI 側から resolve-parameter builder を import している既存コードの互換性を確認・変更するとき。
- TUI の import surface で公開される file access mode の選択肢を確認するとき。
- canonical な oracle 側 builder への移行に伴い、この互換モジュールを削除できる条件を確認するとき。

## Do not read this when
- resolve-parameter builder の実際の組み立て処理や仕様を確認したいとき。この対象は再公開だけを担うため、canonical な builder 実装を読む方が直接的。
- FileAccessMode 自体の定義や意味を確認したいとき。この対象は列挙値を tuple として公開するだけで、mode 定義は別の基本モジュールが担う。
- TUI 以外の ACP builder import 経路や UI 非依存の parameter 構築を調べたいとき。

## hash
- 5a7fc4f43bce998fa5f6b2d56dfe1fae5bce7c9bebf69cc9b49635cca3ef12a9
