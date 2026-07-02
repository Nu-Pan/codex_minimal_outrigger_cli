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
- TUI 起動パラメータ生成関数の実体を oracle 側に置いたまま、既存の公開 import path から同じ関数を参照できるようにする互換用モジュール。
- realization 側や利用者向け公開面に残っている既存参照を維持するための薄い再 export であり、TUI 起動パラメータの仕様や組み立てロジック自体は持たない。

## Read this when
- TUI 起動パラメータ生成関数の import 経路、公開面との互換性、または oracle 側実装への接続を確認したいとき。
- 既存の公開 import path を削除・移動・置換してよいか判断するために、互換コードを残す理由と削除条件を確認したいとき。
- TUI builder 周辺で、realization 側から oracle 側の TUI 起動パラメータ正本へどのように委譲しているかを確認したいとき。

## Do not read this when
- TUI 起動パラメータの具体的な構造、値、生成ロジックの正本を確認したいとき。この対象は再 export だけを担うため、oracle 側の実体を読む。
- TUI 画面の描画、イベント処理、ユーザー操作、または端末 UI の挙動を調べたいとき。
- 互換 import path ではなく、新しい起動仕様や利用者向け CLI 挙動そのものを設計・確認したいとき。

## hash
- 23d4d93c40bb8191cb1d3b58b15845e17afca479d63366ca50c92836df1b6091

# `resolve_parameter.py`

## Summary
- TUI 用 resolve parameter builder の旧 import surface を維持する互換モジュール。正本側 builder を再公開し、既存 TUI 呼び出し向けに NO_RULE を除いた file access mode 群を提供する。

## Read this when
- `acp.builder.tui.resolve_parameter` からの import 互換性、公開名、削除条件を確認する。
- TUI resolve parameter builder の呼び出し元を正本側 import path へ移行する作業を行う。
- 既存 TUI import surface が参照する file access mode の選択肢を確認する。

## Do not read this when
- 正本仕様としての TUI resolve parameter builder の内容を確認したい場合は、oracle 側の canonical builder を読む。
- TUI 以外の builder や file access mode 全体の定義を確認したい場合は、それぞれの定義元を読む。
- 互換 import path の維持や移行に関係しない resolve parameter 処理を調べる。

## hash
- cb619844023de6245704fce405a8473073988a8795d275f54d87a487d5750b70
