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
- ACP の agent call parameter 構築領域を束ねる realization implementation 階層。正本側実装への互換 import 境界を中心に、変更適用、索引生成、レビュー、セッション結合、TUI 起動・パラメータ解決に関する builder 入口へ進むための起点になる。
- 多くの下位要素は正本側 package や prompt builder を src 側の公開経路から再利用する薄い境界であり、一部の変更適用系 builder は model、reasoning effort、file access mode、prompt、structured output schema を用途別に組み立てる。

## Read this when
- ACP builder 領域で、realization 側 package が正本側 package と互換の import 経路を提供しているか確認したいとき。
- 変更適用、索引生成、レビュー、セッション結合、TUI のどの builder 入口または下位領域へ進むべきかを切り分けたいとき。
- agent call parameter 構築で、repo root や oracle src の解決、正本側 prompt builder の利用、model・reasoning effort・file access mode・structured output schema の指定がどこで行われるか確認したいとき。
- 実処理本体ではなく、src 側から正本側実装へ到達する公開境界、再エクスポート、互換 package の有無を確認したいとき。

## Do not read this when
- ACP builder ではなく、fork 作成、git 操作、作業ディレクトリ管理、レポート保存、CLI サブコマンドルーティングなどの実行制御を調べたいとき。
- 正本側の prompt、review standard、realization standard、path model、各種 schema や列挙値の定義そのものを確認したいとき。
- 変更要約、所見、レビュー結果など、builder が生成または利用する成果物の内容だけを読みたいとき。
- 各処理の具体的なアルゴリズム、画面構成、入力フロー、状態管理、判定基準を理解したいとき。その場合は対応する正本側実装またはより直接の下位領域を読む。

## hash
- 82ff32eb86a39d72ff22b63a1f3716f539e8a8ed1f88c59ed488de9e56cfca5d
