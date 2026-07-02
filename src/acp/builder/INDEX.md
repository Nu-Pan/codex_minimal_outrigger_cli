# `__init__.py`

## Summary
- oracle.acp_builder を既存の acp.builder 参照から利用できるようにするための互換入口。正本実装を oracle 側に置いたまま、公開済み参照経路を維持する役割を持つ。
- 互換維持のためだけに残される薄い入口であり、削除条件は realization 側と利用者向け公開面の双方から acp.builder.* 参照がなくなること。

## Read this when
- acp.builder.* 参照が残っている理由や、oracle.acp_builder との互換関係を確認したいとき。
- acp.builder 系の公開入口を削除・移動・置換してよいか判断したいとき。
- realization 側の互換コードについて、残す理由と削除条件を確認したいとき。

## Do not read this when
- oracle.acp_builder の具体的な実装内容や builder の本体仕様を調べたいとき。
- acp.builder.* 以外の ACP 関連モジュールの責務や挙動を調べたいとき。
- 互換入口ではなく、新規機能の実装場所やテスト対象を探しているとき。

## hash
- bce540ff289ae7f7f8c83e9796e27376d4c6313646e45756110fa755ab94158c

# `apply`

## Summary
- apply builder 領域のうち、apply fork 向け ACP builder 群と oracle 側 apply builder package に対応する互換 package 初期化要素を含む階層。主な責務は、oracle 側 builder を利用できるようにし、生成された parameter を realization 側の公開型へ適合させることである。

## Read this when
- apply fork の agent call parameter 構築経路を確認・変更したいとき。
- apply fork 用 builder が oracle 側 builder に委譲し、戻り値を realization 側の公開型へ変換する流れを確認したいとき。
- packaged layout と開発 tree layout の両方で oracle builder を import 可能にする処理を確認したいとき。
- apply builder 領域が oracle 側 package 構造と対応する互換入口を持つか確認したいとき。

## Do not read this when
- apply fork コマンド全体の実行フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理を調べたいときは、上位の apply fork 実装を読む。
- agent prompt、出力条件、parameter 生成内容、人間意図などの正本仕様を確認したいときは、対応する oracle 側 builder を読む。
- ACP parameter のデータ構造や公開型そのものを確認したいときは、基本型定義を読む。
- apply fork 以外の ACP builder、汎用 git 操作 helper、path model を調べたいだけのときは、それぞれの共通実装を読む。

## hash
- ba29c791f282b6618bfae5135c91417964bbf4550ab0f84b885c5e7e71ef03ca

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
- review builder 領域の realization package と review oracle 系 builder 実装への入口。package 初期化は oracle 側同名 package との互換名前空間だけを示し、下位階層では review oracle 周辺の agent call parameter 生成、正本側 builder への委譲、prompt placeholder の暫定補正、旧来 import 経路の互換 wrapper を扱う。

## Read this when
- review builder 領域で、realization 側 package の存在確認から review oracle 系 agent call parameter 生成処理までの読む先を選びたいとき。
- 正本側 builder の出力を realization 側でどう補正しているか、特に oracle root placeholder 表記の暫定補正を追いたいとき。
- レビュー指摘の列挙・判定・検証に関する旧来 import 経路、委譲先、互換層の残置理由や削除条件を確認したいとき。
- 同名機能が realization 側にあるように見える場合に、実体が canonical oracle 側か薄い wrapper かを切り分けたいとき。

## Do not read this when
- review builder の正本仕様断片、prompt の正本文面、判定仕様、検出ロジックそのものを確認したいときは、対応する oracle file または canonical 実装を読む。
- agent call parameter の共通データ構造、model、reasoning effort、file access mode などの基礎定義を調べたいときは、基礎定義側を読む。
- 互換 import 経路や review oracle builder と無関係な CLI 表示、テスト方針、review 機能全般を調べたいときは、より直接その責務を持つ対象へ進む。

## hash
- b5982b09e4ce2166f96a96ee67c2e95418af42cdfc1006f94bbe53b9ce6eef84

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
