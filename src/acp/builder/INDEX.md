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
- apply 系の agent call parameter builder への入口となる領域。package 初期化要素と、fork 適用で使う builder 群への下位入口を含み、実処理は主に下位の個別 builder 領域に委ねる。
- realization 側から oracle 側 builder を利用するための互換 package として位置づけられ、apply 系の処理準備を調べる際に、まず package 構造と下位領域の分担を見分けるための階層である。

## Read this when
- apply 系の agent call parameter builder がどの下位領域に分かれているかを確認したいとき。
- apply builder 領域が oracle 側の package 構造に対応する互換 packageとして置かれているか確認したいとき。
- fork 適用に関する agent 呼び出し準備、oracle builder への委譲、realization 側 parameter 型への適合を調べる入口を探しているとき。
- 変更要約、ファイル単位所見列挙、所見適用など、apply fork の個別 agent 呼び出し準備へ進む前に上位の配置を確認したいとき。

## Do not read this when
- apply fork の具体的な builder 実装や repo root 解決、oracle import 経路補正、parameter 型変換を直接調べたいときは、下位の fork 用 builder 領域へ進む。
- apply fork コマンド全体の制御フロー、fork 作成、branch 操作、diff 生成、CLI 引数処理を調べたいときは、コマンド実装や上位の apply fork 実装へ進む。
- agent prompt、出力条件、変更要約や所見処理の正本仕様を確認したいときは、委譲先の oracle 側 builder または正本仕様断片を読む。
- package 初期化の互換性メモだけで十分な場合を除き、この階層自体には公開 API や具体的な適用ロジックの定義を期待しない。

## hash
- 701ec977b0f06fbfb6f6a79d4e93b731b69f1160c2dc4895c4de00ac87f32c96

# `common`

## Summary
- ファイルアクセス規則違反からの復旧に関する builder common 領域。oracle 側の互換 builder package の入口、リカバリー用 agent call parameter の realization 適応、復旧結果データを任意の JSON object として受け渡すための schema を扱う。

## Read this when
- ファイルアクセス規則違反時に起動するリカバリー agent call の parameter 構築経路や realization 側型への適応処理を確認・変更したいとき。
- oracle 側 builder との互換 package の入口や import 経路、package 初期化の扱いを確認したいとき。
- 復旧結果または復旧方針を厳密な項目定義ではなく任意の JSON object として許容している根拠を確認したいとき。
- 参照される structured output schema が存在しない場合の fallback 挙動を確認したいとき。

## Do not read this when
- ファイルアクセス規則そのものの定義、読み書き禁止範囲、違反判定ロジックを調べたいとき。
- 復旧処理そのものの手順、判定条件、エラーメッセージを確認したいとき。
- oracle 側の正本仕様断片やリカバリー parameter builder 本体を確認したいとき。
- 一般的な agent call parameter の型定義や file access mode の意味を調べたいとき。

## hash
- ad69be6da9a3e69738a7d29197e05f74dba9bf39a6c6ccb61ee8f8745822f514

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
- Codex quota availability probe のために、既存の AgentCallParameter から最小限の動作確認用 AgentCallParameter を生成する builder です。
- base parameter の model class、reasoning effort、file access mode を引き継ぎ、意味のある作業を依頼しない固定 prompt を持つ probe parameter を返します。

## Read this when
- Codex quota availability probe で使う AgentCallParameter の組み立て内容を確認・変更したいとき。
- quota probe が通常の agent call と同じ model class、reasoning effort、file access mode を使う理由や、probe prompt の意図を確認したいとき。
- Codex CLI 呼び出し前の quota availability 確認処理から、実際に渡される parameter の生成元を追うとき。

## Do not read this when
- AgentCallParameter 型そのものの定義やフィールド仕様を確認したいときは、その型を定義する basic.acp 側を読む。
- Codex CLI の実行規則や quota availability probe の正本仕様を確認したいときは、対応する oracle doc を読む。
- probe parameter の生成後に Codex CLI を起動する runtime 側の処理を確認したいときは、この builder ではなく実行側の module を読む。

## hash
- 4a4a7eebc4ed7184af908b6f5e4a7e4a93d853c29603dd8e2c73d85ce792dcac

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
