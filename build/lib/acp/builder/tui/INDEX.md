# `__init__.py`

## Summary
- oracle.acp_builder.tui と互換性を持つ package の入口であることだけを示す。具体的な TUI 実装や挙動はこの対象内では定義していない。

## Read this when
- oracle.acp_builder.tui 互換の package 境界が存在するかを確認したいとき。
- この package 自体に公開された説明や初期化時の意図があるかを確認したいとき。

## Do not read this when
- TUI の具体的なコマンド、画面、イベント処理、状態管理を調べたいとき。
- oracle 側の正本仕様や互換元の詳細を確認したいとき。

## hash
- 0a593accdb428d084c035fe120f2a06b5788abb28e112e72252680ca369fb14d

# `launch_tui.py`

## Summary
- TUI 起動パラメータの正本実装を oracle 側に保ったまま、既存の公開 import path から参照できるようにする互換接続モジュール。

## Read this when
- `acp.builder.tui.launch_tui` から TUI 起動パラメータ生成を import する経路の維持・削除条件を確認したいとき。
- TUI 起動パラメータの正本が oracle 側にある前提で、realization 側の参照接続だけを確認したいとき。

## Do not read this when
- TUI 起動パラメータの生成内容そのものを確認したいときは、oracle 側の正本実装を読む。
- 新しい TUI 起動仕様や利用者向け挙動を判断したいだけで、既存 import path の互換接続に関心がないとき。

## hash
- 23d4d93c40bb8191cb1d3b58b15845e17afca479d63366ca50c92836df1b6091

# `resolve_parameter.py`

## Summary
- TUI の resolve-parameter builder について、既存の import 経路を一時的に維持する互換レイヤーを扱う。正本の builder を再公開し、既存 TUI 側の import surface 向けに `NO_RULE` を除いた file access mode 群を提供する。
- 恒久的な実装本体ではなく、呼び出し側が正本側の経路へ移行するまで残すべき互換モジュールとして位置づけられている。

## Read this when
- TUI の resolve-parameter builder を既存の互換 import 経路から利用している箇所を調査・変更するとき。
- TUI 向けに公開される file access mode の候補から `NO_RULE` が除外される理由や公開面を確認するとき。
- この互換モジュールを削除できる条件、または正本側 import 経路への移行状況を確認するとき。

## Do not read this when
- resolve-parameter builder の実体や生成内容を変更したいとき。この対象は正本 builder を再公開するだけなので、正本側の builder を直接読む。
- file access mode 自体の定義や列挙値を変更したいとき。この対象は既存 TUI 向けに候補を絞るだけで、定義元ではない。
- 新しい TUI 機能や永続的な builder 実装を追加したいとき。この対象は移行完了後に削除される互換 import 経路である。

## hash
- cb619844023de6245704fce405a8473073988a8795d275f54d87a487d5750b70
