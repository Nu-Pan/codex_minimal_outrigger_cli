# `__init__.py`

## Summary
- oracle.acp_builder.review と互換の package であることだけを示す、review builder 領域の package 初期化用ファイル。実装ロジックや詳細な仕様ではなく、互換名前空間としての位置づけを確認する入口になる。

## Read this when
- review builder 領域で、oracle 側の同名 package と対応する realization package が存在するかを確認したいとき。
- package としての互換性や import 経路の成立だけを確認したいとき。

## Do not read this when
- review builder の具体的な処理、関数、クラス、出力、制御フローを調べたいとき。
- 正本仕様断片としての review builder の要求を調べたいとき。
- package 初期化以外の実装変更先を探しているとき。

## hash
- adf6124f1c3a49a136159186b6a58b39f4321e0113527b60e85d8b1e3205484e

# `oracle`

## Summary
- src 側の review oracle builder から、正本側 `oracle.acp_builder.review.oracle` 配下の finding 関連処理へ到達するための薄い互換 package。finding の列挙・判定・結合・検証系モジュールを再公開する import 境界であり、この階層自体は具体的な review oracle ロジックや仕様断片を持たない。

## Read this when
- src 側の review oracle builder から、finding の列挙・判定・結合・検証系処理が正本側実装へどの import 境界で委譲されているかを確認したいとき。
- この階層が独自の review oracle ロジックを持つ場所なのか、正本側実装を公開する互換 package なのかを切り分けたいとき。
- review oracle の finding 関連モジュール群について、公開側パッケージから参照できる入口のまとまりを確認したいとき。

## Do not read this when
- finding の列挙・判定・結合・検証に関する具体的なアルゴリズム、入出力、判定基準、prompt 構成を理解したいとき。その場合は委譲先の正本側実装を読む。
- review oracle builder 全体の責務分担、CLI の入出力、または finding 以外の review 処理を調べたいとき。より上位または該当責務の本文へ進む。
- 公開 API 以外の実装詳細、テスト観点、正本仕様断片そのものを探しているとき。この階層には再公開入口以上の情報は含まれていない。

## hash
- a5963008d4dccaa5064c4de378647f2cae45e4b82ffba7844cf704f1ed1bdee7
