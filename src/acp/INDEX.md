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
- ACP builder 領域の realization 側入口で、正本側 builder 実装への互換 import 境界と、変更適用系 fork、indexing、review、session、TUI などの下位 builder 領域へ進むための分岐点をまとめる。
- この階層では、実処理を持つ実装本体よりも、src 側から正本側実装や下位領域へ到達する公開経路、互換 package、呼び出し parameter builder、出力契約入口の位置づけを扱う。

## Read this when
- ACP builder 配下で、どの下位領域が変更適用、indexing、review、session、TUI、互換公開入口のどれを担うかを切り分けたいとき。
- src 側の ACP builder package が、正本側の builder package 構造や実装へどのように対応しているかを確認したいとき。
- agent 呼び出し parameter の builder 群や出力契約の入口を探しており、まず変更適用系 fork など対象領域を選びたいとき。
- 実処理本体を読む前に、この階層が主に互換 import 境界なのか、下位に具体的な builder 実装入口を持つのかを判断したいとき。

## Do not read this when
- 個別の builder 関数、class、prompt 構成、データ構造、制御フローの詳細を直接調べたいとき。その場合は該当する下位領域または正本側実装を読む。
- fork 作成、git 操作、作業ディレクトリ管理、CLI 表示、レポート保存など、builder ではない実行制御や表示処理を追いたいとき。
- oracle standard、apply review standard、realization standard など、判断基準や正本仕様本文そのものを確認したいとき。
- 正本側の仕様断片や prompt builder 本体を編集・確認したいとき。この階層は realization 側の入口や互換境界を扱う。

## hash
- 27b38c69c6df43297ac780fae8faed3e2b07b50aae5a758899b8d81f530cfbc9
