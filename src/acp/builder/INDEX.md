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
- apply 系の agent call parameter builder を扱う realization 側領域。package 初期化要素と、apply fork 向けに oracle 側 builder へ委譲する薄い builder 群への入口になっている。
- この領域の実装は prompt や parameter の正本内容を自前で定義するのではなく、oracle 側実装を呼び出し、realization 側の型境界へ適合させる責務を持つ。

## Read this when
- apply 系 builder の realization 側 package 構造と、oracle 側 package との対応を確認したいとき。
- apply fork の変更要約、ファイル単位所見列挙、所見適用に使う agent call parameter が、realization 側のどの入口から構築されるかを調べたいとき。
- apply fork 向け builder が共有する repo root 解決、oracle 側 import 経路補正、oracle parameter から realization 側 ACP 型への適合処理を確認したいとき。

## Do not read this when
- agent call parameter の prompt 内容、出力条件、正本仕様そのものを確認したいとき。この領域は oracle 側 builder への委譲層なので、対応する oracle 側本文を読む。
- apply fork コマンド全体の CLI 制御、fork 適用処理、git 操作、作業レポート生成フローを調べたいとき。この領域は agent call parameter 構築入口に限られる。
- apply fork 以外の ACP builder、CLI 挙動、path model、ACP 型定義そのものを調べたいとき。より直接の実装または正本仕様へ進む。

## hash
- 701ec977b0f06fbfb6f6a79d4e93b731b69f1160c2dc4895c4de00ac87f32c96

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
- quota availability probe 用 AgentCallParameter を構築する realization 側の暫定 adapter。Codex exec runtime に prompt literal を置かず、probe 呼び出しも parameter の prompt を保存して stdin に渡す境界へ揃える。
- 現行 oracle src に quota probe 専用 builder がない制約を明示し、同用途の oracle builder が追加された時点で置換・削除する対象である。

## Read this when
- Codex exec の quota 待機中に実行される代表 probe の prompt、schema 無し指定、または元呼び出し parameter から引き継ぐ model/reasoning/file access の境界を確認・変更したいとき。
- runtime 側で probe prompt を直接作らないための暫定 adapter が残っている理由と削除条件を確認したいとき。

## Do not read this when
- quota 待機の状態機械、代表 probe の共有、resume token、call log、subcommand event の制御を調べたいときは Codex exec runtime を読む。
- oracle 側に quota probe 専用 builder が存在するか、または正本仕様としてどう定義すべきか確認したいときは oracle 側の acp_builder と app_spec を読む。

## hash
- d2967195fb145e02d6f2ee795d9cc966b20a4502a6a14fc96b58793db181f68a

# `review`

## Summary
- review builder 領域の realization 側入口であり、正本側 review builder と対応する package 名前空間、および review oracle builder 周辺の互換 import path と薄い補正 wrapper を束ねる領域。
- 具体的な review 処理本体を持つ領域ではなく、古い実装側 import 経路を正本側へつなぐ再公開と、正本側 builder が生成した AgentCallParameter の prompt 内 oracle root placeholder 表記を局所補正する経路を確認するための入口。
- review finding の列挙・判定・challenger 検証は正本側の実装を再公開し、finding 統合と advocate 検証は正本側 builder への委譲結果に既知の prompt 表記補正だけを加える、互換層中心のまとまり。

## Read this when
- review builder 領域で、正本側 package と対応する realization 側 package が存在するか、import 経路が成立するかを確認したいとき。
- review oracle builder 周辺で、古い realization 側 import 経路が残っている理由、削除条件、正本側実装への委譲関係を切り分けたいとき。
- finding 統合や advocate 検証の AgentCallParameter 生成について、正本側 builder の結果を保ったまま prompt 内の oracle root placeholder 表記だけを補正する wrapper の有無を確認したいとき。
- 同名機能の実装本体がこの領域にあるのか、正本側へ再公開しているだけなのか、または局所的な prompt 補正だけを担っているのかを判断したいとき。

## Do not read this when
- review finding の列挙・判定・検証ロジックそのもの、または prompt の正本仕様を確認したいとき。正本側の対応する実装や仕様断片へ進む。
- review builder の具体的な処理本体、関数、クラス、出力、制御フローを調べたいとき。互換 package 初期化や薄い wrapper ではなく、実処理を担う対象を読む。
- review oracle 以外の builder、CLI 表示、テスト方針、AgentCallParameter 型の共通仕様を調べたいとき。より直接その責務を持つ領域へ進む。
- 新しい判定ロジックや検証処理を追加・変更したいとき。この領域は互換再公開と正本側 builder への追従用補正が中心であり、実装本体の変更先ではない。
- 生成済み parameter の利用側挙動だけを追う作業で、古い import 経路や prompt 表記補正の有無が関係しないとき。

## hash
- ade3b379627f9f40fe5e7aee91f3a8511998dffd1817884418224c2f9c7c4c44

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
- ACP builder の TUI 関連公開 import path を、正本側の実装へ中継する互換層をまとめる階層。TUI 起動パラメータ生成と resolve-parameter builder の既存参照を維持し、TUI 向け file access mode tuple も公開する。
- ここにある実装は TUI の画面処理や builder の正本ロジック本体ではなく、realization 側または利用者向け公開面に残る既存 import 経路を成立させるための再公開・委譲を担う。

## Read this when
- ACP builder の TUI 関連 API を既存の公開 import path から使えるように保っている互換層を確認したいとき。
- TUI 起動パラメータ生成や resolve-parameter builder が、realization 側から oracle 側の canonical 実装へどう接続されているかを確認したいとき。
- TUI 向け import surface で公開される file access mode の選択肢や、builder 関数の再公開範囲を確認したいとき。
- 正本側 import path への移行に伴い、この互換層を削除できる条件を調べたいとき。

## Do not read this when
- TUI 起動パラメータや resolve-parameter builder の実際の組み立て仕様を確認したいとき。ここではなく oracle 側の canonical 実装を読む。
- TUI の表示、イベント処理、画面構成、入力操作などの UI 本体実装を調べたいとき。
- AgentCallParameter や FileAccessMode の型定義・意味を確認したいとき。ここでは型や列挙値を利用・公開するだけで、定義本体は別の基本モジュールが担う。
- TUI 以外の ACP builder 経路、または UI 非依存の parameter 構築全般を調べたいとき。

## hash
- 3d3ccc7c3599265b864d6f03f95716c3677e3806db42b4c7e7371a7a4440e6f2
