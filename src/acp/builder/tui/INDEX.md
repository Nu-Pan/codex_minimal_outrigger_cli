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
- oracle 側にある TUI 起動パラメータ生成関数を、既存の公開 import path から参照できるように再公開する互換用モジュール。
- TUI 起動パラメータの正本を oracle 側に置いたまま、realization 側や利用者向け公開面に残る参照を成立させるための薄い入口である。
- この互換入口は、realization 側と利用者向け公開面から該当 import path 参照がなくなった時点で削除できる。

## Read this when
- TUI 起動パラメータ生成関数の公開 import path の互換性を確認・変更したいとき。
- oracle 側の TUI 起動パラメータ生成関数を realization 側からどの名前で再公開しているかを確認したいとき。
- 互換用 import path を削除できるかどうか、削除条件を確認したいとき。

## Do not read this when
- TUI 起動パラメータの正本となる生成ロジックや仕様を確認したいときは、oracle 側の実体を読む。
- TUI の画面構成、入力処理、イベント処理などの実装を調べたいときは、TUI 本体の実装へ進む。
- 互換 import path ではなく、新しい公開 API や CLI の利用方法を調べたいときは、公開面を定義している対象を読む。

## hash
- a88611127f710dfc4faa014cf5a1420685ccb329009914d37c15cfa1ceb0cc28

# `resolve_parameter.py`

## Summary
- TUI 向けのパラメータ解決機能を正本側実装から公開し、TUI で扱うファイルアクセスモードの選択肢を基本定義の列挙値から組み立てる薄い realization 実装。
- 独自の解決ロジックを持つ入口ではなく、正本側の TUI パラメータ解決と基本定義の列挙値を、実装側から参照できる形に接続する役割を持つ。

## Read this when
- TUI のパラメータ解決を realization implementation 側でどこから import しているか確認したいとき。
- TUI で提示・利用するファイルアクセスモードの候補が、基本定義の列挙値と同期しているか確認したいとき。
- 正本側の TUI パラメータ解決実装を realization 側へ露出する接続部分を変更・確認したいとき。

## Do not read this when
- パラメータ解決の具体的な仕様や処理内容を確認したいときは、正本側の TUI パラメータ解決実装を読む。
- ファイルアクセスモード自体の定義や意味を確認したいときは、基本定義側の列挙値を読む。
- TUI 全体の画面構成、入力フロー、表示処理を調べたいだけなら、より直接それらを実装する対象を読む。

## hash
- c5a764ce2693eef8273489b9de5d8f063ec7dcd7e72609d239251b54dc4554bd
