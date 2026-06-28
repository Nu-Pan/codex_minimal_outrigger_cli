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
- ACP builder realization implementation の上位入口で、正本側 builder 実装への互換 import 境界と、apply、indexing、review、session、TUI など下位 builder 領域へのルーティングを束ねる。
- この階層の多くは実処理本体ではなく、正本側 package 構造に対応する src 側の公開経路や shim を提供するが、apply 領域には agent call parameter、prompt、JSON schema、共通 helper など実際の構築処理へ進む入口も含まれる。

## Read this when
- ACP builder 全体で、src 側の package 構成が正本側 builder package とどう対応しているかを確認したいとき。
- apply fork、indexing、review、session join、TUI など、builder のどの下位領域へ進むべきかを切り分けたいとき。
- 正本側実装を src 側 import 経路から再公開している互換境界や、処理実体を持つ下位領域の入口を確認したいとき。
- agent に渡す parameter builder、prompt 組み立て、出力 schema、TUI パラメータ解決入口など、ACP builder 配下の公開入口を探し始めるとき。

## Do not read this when
- 個別 builder の具体的な関数、クラス、生成ロジック、バリデーション、制御フローを直接調べたいときは、該当する下位領域または正本側実装を読む。
- apply fork 全体の作成、git 操作、commit、作業ディレクトリ管理、レポート保存など builder 外の実行制御を追いたいとき。
- 正本 prompt、レビュー基準、path model、index entry 定義など oracle 側の仕様断片そのものを確認したいとき。
- CLI 表示整形、git 操作一般、実際の realization file 編集内容、または builder 以外の ACP 処理を調べたいとき。

## hash
- 024b61aec0f67974cd0c29bd73fc4bfe439e3f59253dc61bebea262718c285dc
