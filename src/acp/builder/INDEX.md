# `__init__.py`

## Summary
- oracle 側の acp builder 実装を正本に保ちながら、既存の acp.builder 経由の import を成立させる互換入口。
- oracle package の検索結果を確認し、oracle 側の submodule search path をこの package に追加したうえで、既存参照向けに basic module を oracle 実装へ対応付ける。
- local wrapper を oracle 側 path より優先できる順序を保ち、互換が必要な出力だけ realization 側で適応できる余地を残す。

## Read this when
- acp.builder 経由の import 互換性、特に既存の acp.builder.basic 参照が oracle 側実装へ解決される仕組みを確認したいとき。
- oracle 側の acp builder package を正本としつつ、realization 側で package path や module alias をどう接続しているかを調べるとき。
- acp.builder.* 参照を削除または移行する作業で、この互換入口を残す条件や削除条件を確認したいとき。

## Do not read this when
- oracle 側 acp builder の正本仕様や canonical module の実装内容を確認したいだけなら、oracle 側の該当実装を直接読む。
- acp.builder 以外の acp package 公開面や import 互換性を調べる場合は、より上位または該当 subpackage の入口を読む。
- builder の個別変換処理や wrapper の詳細挙動を調べる場合は、その処理を持つ個別 module を読む。

## hash
- 7af83fea8ad03595625c00432641609f104d01f963904ec5b9ef0a1d8dc05693

# `apply`

## Summary
- apply fork 向け ACP builder と、既存の apply builder import 経路を維持する互換入口を含む領域。oracle 側 builder への委譲、repo root 解決、import 準備、realization 側公開型への変換に関する実装へ進むための入口。

## Read this when
- apply fork の agent call parameter 構築経路を確認・変更したいとき。
- apply fork の builder が oracle 側 builder を呼び出し、戻り値を realization 側の公開型へ適合させる流れを確認したいとき。
- packaged layout と開発 tree layout の両方で oracle builder を import 可能にする処理を確認したいとき。
- 既存の apply builder import 経路が互換目的で残っている理由や、削除できる条件を判断したいとき。

## Do not read this when
- apply fork コマンド全体の実行フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理を調べたいときは、上位の apply fork 実装へ進む。
- agent prompt、出力条件、parameter 生成内容、人間意図などの正本仕様を確認したいときは、対応する oracle 側 builder を読む。
- ACP parameter のデータ構造や公開型そのものを確認したいときは、基本型定義へ進む。
- apply fork 以外の ACP builder、汎用 git 操作 helper、path model を調べたいだけのときは、それぞれの共通実装へ進む。
- 新しい import 経路や公開 API を追加する場所を探しているとき。

## hash
- 7069dae752a14c1ced75b10576af9f6a1cafc7be0d6686b2796aadffbb34923a

# `common`

## Summary
- acp builder common 領域で、oracle 側 builder を realization 側から利用するための互換 package。
- package 入口と、ファイルアクセス規則違反 recovery 用 builder を正本側へ委譲して AgentCallParameter へ変換する wrapper への入口を持つ。

## Read this when
- acp builder common 領域で oracle 側 builder との互換 layer の入口を確認したいとき。
- ファイルアクセス規則違反 recovery の agent call parameter 生成を、oracle 側 builder と realization 側 parameter 変換の間でどう接続しているか確認したいとき。
- 正本側 builder の import 準備、repo root 解決、oracle parameter から realization 側 parameter への変換経路を追いたいとき。

## Do not read this when
- builder common 配下の個別機能ではなく、oracle 側の正本仕様断片そのものを確認したいとき。
- agent call parameter の変換処理そのものの詳細を調べたいとき。
- ファイルアクセス規則違反の検出ロジックやログ収集処理を調べたいだけのとき。

## hash
- 1affeb1433d5fa85da8ff99df1957083f3f45d9ed6589a943e9833fd29b0b4c4

# `indexing`

## Summary
- 正本側に置かれた indexing 関連実装を、既存の公開参照から到達できるようにする互換入口をまとめる領域。実処理や仕様本体ではなく、旧来の import 経路を壊さないための薄い再公開境界を担う。
- 互換コードを残す理由、正本側実装との対応、削除できる条件を確認するための入口であり、indexing の生成処理・探索処理・データ構造そのものはこの領域の責務ではない。

## Read this when
- 旧来の公開名や import 経路が、正本側の indexing 実装へどのように接続されているか確認したいとき。
- 正本側へ実装を集約しつつ、既存利用者や残存参照を壊さないための互換公開面を確認したいとき。
- 互換入口を残す理由、削除条件、残存参照の有無に関わる変更を検討しているとき。
- 公開参照の維持または廃止に伴い、再公開先の正本側実装との対応関係を確認したいとき。

## Do not read this when
- indexing の具体的な生成処理、探索処理、データ構造、入出力仕様を確認したいとき。実体を持つ正本側実装を読む。
- インデックスエントリーの型・関数・挙動そのものを確認したいとき。再公開先の正本側実装を読む。
- 新しい indexing 機能を追加または変更したいとき。互換入口ではなく処理本体の実装側を読む。
- 互換参照の削除条件や再公開先ではなく、正本仕様全体を確認したいとき。該当する正本側の本文を読む。

## hash
- 0ab736b2c29b4ef0eadf9408768a9f99642c5d3d95caecb6c4def825217c487a

# `quota_probe.py`

## Summary
- quota availability probe 用の agent call parameter を、正本 builder から取得して realization 側の型へ適合させる互換 wrapper。
- oracle src を import 可能にしたうえで正本側の builder を呼び出し、正本 builder が存在しない場合の失敗理由を明確化する入口。

## Read this when
- quota availability probe の parameter 生成経路を確認・変更したいとき。
- oracle src の builder と realization 側の AgentCallParameter との接続方法を確認したいとき。
- 正本 builder が見つからない場合のエラー処理や import 準備の扱いを確認したいとき。

## Do not read this when
- quota probe の正本仕様や builder 本体の内容を確認したいときは、対応する oracle src を読む。
- agent call parameter の汎用的な適合処理、oracle src import 準備、repo root 解決の詳細を確認したいときは、共通 helper 側を読む。
- quota availability probe 以外の parameter builder を調べたいときは、対象となる builder へ直接進む。

## hash
- 39768e9b753b95a155819c381388166e3513a3845722084f99550cf35ee64332

# `review`

## Summary
- review builder 領域の package 入口と、review oracle builder 周辺の旧 import 経路互換層を束ねる階層。実装本体よりも、canonical oracle 側への再公開・委譲、薄い wrapper、暫定補正、移行中の互換性と削除条件を確認する入口になる。

## Read this when
- review builder 領域で、oracle 側に対応する realization package や互換名前空間があるかを確認したいとき。
- review oracle builder の旧経路 import が canonical oracle 側へどう委譲されているか確認したいとき。
- review finding enumeration、judgment、validation、merge finding などの互換 module や薄い wrapper の残存理由、移行状況、削除条件を調べたいとき。
- 正本側 builder の出力に対する realization 側の最小補正や agent call parameter 生成 wrapper の場所を探したいとき。

## Do not read this when
- review builder の具体的な処理、関数、クラス、出力、制御フローを調べたいとき。
- review finding の判定仕様、検証ロジック、prompt 正本文面など、挙動本体や正本仕様を確認したいとき。
- agent call parameter の基礎構造、共通 model 設定、file access mode などの一般仕様を確認したいとき。
- package 初期化や旧 import 互換層以外の実装変更先を探しているとき。

## hash
- 857116df4ad80bb76c8dcecf2c94b8d197cf0006fc8c4b22885010721b42dcb3

# `session`

## Summary
- ACP builder の session 領域で、oracle 側と同じ package 構造を実装側に成立させるための互換入口を扱う階層。
- この階層自体は session builder の実処理を担う場所ではなく、実体を持たない package 初期化と、session join 配下の互換境界へ進むための入口として位置づけられる。

## Read this when
- ACP builder の session 領域が oracle 側の package 構造とどう対応しているかを確認したいとき。
- session 領域が import 可能な package として存在する理由を確認したいとき。
- session join 配下へ進む前に、この領域が実処理ではなく互換 package 境界を扱う場所かどうかを見分けたいとき。

## Do not read this when
- session builder の具体的な処理、状態管理、入出力変換、関数、クラス、定数を調べたいとき。
- session join の衝突解決ロジックや判定内容など、実体を持つ処理を確認したいとき。
- oracle 側の正本仕様や互換対象そのものを確認したいとき。

## hash
- 8c4fa4ee9bc1e65c70dcc8ff005ed00bb8e4079aff3755b9674a92cfef3a0446

# `tui`

## Summary
- ACP builder の TUI 互換 package。正本側に実体を置く TUI builder 関連機能について、既存の realization 側 import path から参照できるようにする薄い互換層を収める。
- この階層自体は TUI の画面制御や起動パラメータ生成ロジックの正本ではなく、公開 import surface の維持、oracle 側実装への委譲、旧 import path から正本側 import path への移行判断の入口となる。

## Read this when
- ACP builder の TUI 関連 import path が、正本側 package や builder と互換の入口として維持されているかを確認したいとき。
- TUI 起動パラメータ生成関数や resolve parameter builder について、realization 側の既存公開 import surface が oracle 側実体へどのように接続しているかを確認したいとき。
- TUI builder 周辺の互換モジュールを残す理由、公開名、削除条件、または正本側 import path への移行方針を確認したいとき。
- 既存 TUI 呼び出し向けに公開される file access mode の選択肢を確認したいとき。

## Do not read this when
- TUI 起動パラメータや resolve parameter builder の具体的な構造、値、生成ロジックの正本を確認したいとき。
- TUI の描画、画面制御、イベント処理、ユーザー操作、端末 UI の挙動を調べたいとき。
- TUI 以外の builder、file access mode 全体の定義、CLI 動作など、互換 import path の維持や移行に関係しない公開面を調べたいとき。

## hash
- 8ac371cf10db95db117b90e515679e1087d5a1fc8233a8f029864a9f41aa17f5
