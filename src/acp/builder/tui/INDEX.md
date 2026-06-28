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
- ACP builder TUI 起動入口の src 側 shim であり、oracle 側の実装を同名モジュールとして再エクスポートする。
- このファイル自体は挙動を定義せず、src 配下から oracle 側 TUI 起動実装へ到達するための薄い公開口として位置づけられる。

## Read this when
- src 側の ACP builder TUI 起動入口が、どの oracle 側実装に委譲されているか確認したいとき。
- src 配下の import 経路や公開モジュール境界を確認し、実処理ではなく再エクスポートの有無だけを見たいとき。

## Do not read this when
- ACP builder TUI の起動処理、画面構成、引数処理、終了処理などの実装詳細を調べたいときは、再エクスポート元の oracle 側実装を直接読む。
- 新しい TUI 挙動や仕様判断の根拠を探しているときは、この shim ではなく対応する oracle file や実処理を持つモジュールを読む。

## hash
- 970311b93d0cd6ca26c05ba352efc06cc4da54608d29746e22cad14887aead2a

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
