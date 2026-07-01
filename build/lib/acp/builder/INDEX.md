# `__init__.py`

## Summary
- oracle 側にある ACP builder 実装を、既存の acp.builder 名前空間から参照できるようにする互換入口。正本実装を oracle 側に保ったまま、旧来の acp.builder.* 参照を成立させるための薄い公開層として位置づけられる。

## Read this when
- acp.builder.* 参照の互換入口がどこで維持されているか確認したいとき。
- oracle 側の ACP builder 実装を realization 側や公開 API からどう参照しているか調べるとき。
- acp.builder.* 参照を削除または移行する作業で、この互換入口の削除条件を確認したいとき。

## Do not read this when
- ACP builder の正本実装や詳細な挙動を確認したいときは、oracle 側の実装を読む。
- 互換目的ではない新規の builder 機能追加や内部処理の変更を調べたいとき。
- acp.builder.* 参照と無関係な ACP 全般の公開面や実装を調べたいとき。

## hash
- bce540ff289ae7f7f8c83e9796e27376d4c6313646e45756110fa755ab94158c

# `apply`

## Summary
- oracle 側の apply builder と realization 側の agent call parameter を接続する互換層。apply fork 向けに、正本側 builder の import 準備、repository root 解決、runtime ACP 型への変換、変更要約・ファイル単位所見列挙・所見適用の parameter 構築へ進む入口になる。
- apply fork の実行制御そのものではなく、正本側 builder と realization 側 parameter 表現の境界を確認するためのまとまり。

## Read this when
- apply fork で変更要約、ファイル単位所見列挙、所見適用に渡す agent call parameter の構築経路を確認・変更したいとき。
- apply fork ACP builder が oracle 側 builder を import し、oracle parameter を realization 側 parameter へ変換する接続点を調べたいとき。
- apply builder 互換層の package 境界、初期化位置、builder 共通処理の責務境界を確認したいとき。

## Do not read this when
- prompt 構成、parameter 内容、所見生成規則などの正本仕様そのものを確認したいときは、対応する oracle src を読む。
- apply fork 全体の CLI 実行制御、git 操作、状態遷移を調べたいときは、apply fork の実行側へ進む。
- fork 以外の ACP builder、CLI 全体の routing、path placeholder の一般仕様、または oracle file の定義を調べたいときは、より直接の対象を読む。

## hash
- 2816fa6d48d31c0b1475f43ab553d551855a05920d64eebc7f58de9de80b116d

# `common`

## Summary
- 互換 builder common package の入口と、ファイルアクセス規則違反リカバリー用 AgentCallParameter builder wrapper およびその structured output schema を含む。
- oracle 側 builder common への互換参照、oracle 側 builder への委譲、realization 側 parameter 型への適合、schema path fallback の確認入口となる。

## Read this when
- builder common package の互換入口がどの正本側 package に対応するかを確認したいとき。
- acp.builder.common 配下を参照する既存コードの互換先を把握したいとき。
- ファイルアクセス規則違反リカバリー時に使う AgentCallParameter の構築経路を確認したいとき。
- oracle 側 builder への委譲、repo root 解決、oracle src の import 準備、realization 側 parameter への適合処理を調べるとき。
- structured output schema path が存在しない場合の fallback 挙動を変更または確認したいとき。
- 特定のキー構造を定めず、オブジェクトであれば内容を広く受け入れる schema の意味を確認したいとき。

## Do not read this when
- builder common の具体的な正本仕様や oracle 側 builder が生成する prompt 内容を確認したいとき。
- ファイルアクセス規則違反の検出条件や違反ファイル一覧の生成処理を調べたいとき。
- AgentCallParameter や FileAccessMode の基本定義そのものを確認したいとき。
- 必須プロパティ、型付きプロパティ、値制約、追加プロパティ制限を持つ JSON Schema を探しているとき。

## hash
- bc779c04447d23e14a3bb02543ba9586c1a68e07dd89334d01b20012edc7cd80

# `indexing`

## Summary
- oracle 側へ移った indexing / index entry 実装を、旧来の builder パッケージ経路から参照し続けるための薄い互換入口を収める。
- 独自ロジックではなく再公開を担い、正本実装を oracle 側に保ったまま既存公開面との互換関係を維持する領域。

## Read this when
- 旧来の builder パッケージ経路から indexing や index entry 関連 API が参照できる理由を確認したいとき。
- oracle 側の実装と realization 側に残る旧参照経路の互換関係を調べたいとき。
- 互換入口の残存理由や、旧参照を削除できる条件を確認したいとき。

## Do not read this when
- indexing や index entry の正本仕様、本体実装、生成ロジックを確認したいとき。その場合は oracle 側の対応実装を読む。
- INDEX.md エントリーの記述基準やルーティング規則を確認したいとき。その場合は対応する oracle doc を読む。
- 新しい公開 API、出力仕様、または互換入口以外の builder 領域を調べたいとき。

## hash
- c40c8417a4acc6eb1f4573bc395fdcb4515919bdd563be0910720e3e61a7e12d

# `quota_probe.py`

## Summary
- Codex quota availability probe のために、既存の AgentCallParameter から最小限の確認用パラメータを組み立てるビルダーを定義する。
- probe では元の model class、reasoning effort、file access mode を引き継ぎ、意味のある作業ではなく固定応答だけを要求する。

## Read this when
- Codex CLI の quota availability probe に使う AgentCallParameter の作り方を確認したいとき。
- 通常の agent call parameter から、動作確認用の最小プロンプトへ変換する処理を変更したいとき。
- codex_exec_rule.md に対応する probe 用パラメータ生成の実装箇所を探しているとき。

## Do not read this when
- 通常の実タスク用 AgentCallParameter の構築や入力仕様を確認したいとき。
- quota probe の起動方法、CODEX_HOME、profile、cwd の受け渡しなど runtime 側の処理を確認したいとき。
- Codex CLI 呼び出し全般の実行規則や quota 判定の正本仕様を確認したいとき。

## hash
- 4a4a7eebc4ed7184af908b6f5e4a7e4a93d853c29603dd8e2c73d85ce792dcac

# `review`

## Summary
- review builder 配下の互換用入口で、旧 import 経路を canonical 実装へつなぐ薄い再 export と、oracle 側 builder 出力の prompt placeholder 表記を限定的に補正する経路を収める。
- 実体的な review 処理ロジックではなく、互換 package としての位置づけ、削除条件、merge finding review・finding advocate review 向けの補正所在を確認する入口になる。

## Read this when
- review builder の旧 import 経路や互換 package の存在理由を確認したいとき。
- review oracle builder 由来の旧経路が canonical 実装へどう接続されているか、また互換 shim の削除条件を調べたいとき。
- oracle merge finding review や oracle finding advocate review の agent call parameter 生成で、prompt 内 placeholder 表記だけを補正する経路を確認したいとき。
- この配下が実体的な処理ではなく import 互換性や限定的な補正を担うことを確認したいとき。

## Do not read this when
- review 機能の具体的な処理内容、制御ロジック、finding の列挙・判定・validation の実装を調べたいときは、canonical 実装を直接読む。
- merge finding や finding advocate の正本 prompt、正本仕様断片、共通 agent call parameter 構造を確認したいときは、元の oracle 側定義や共通 builder を読む。
- oracle merge finding review や finding advocate review 以外の review 種別、または placeholder 補正と関係しない builder 実装を調べたいとき。

## hash
- 4c54f64e24a9f7a6d6e672db460ecca7b9a10fccdd5ac276b8a426593014a9e0

# `session`

## Summary
- oracle.acp_builder.session 互換の公開 import 経路を担う package。package 初期化部と join 配下の互換層を入口に、旧 import 経路から canonical oracle path へ橋渡しする役割を持つ。
- session 機能や conflict resolution の実装本体ではなく、互換 package としての公開面・再エクスポート・削除条件を確認するための領域。

## Read this when
- oracle.acp_builder.session 互換の import 経路や package 初期化責務を確認するとき。
- session join の conflict resolution について、旧 import 経路から canonical oracle path への再エクスポートだけを確認するとき。
- 旧 import 経路の互換維持、canonical 側への移行状況、または互換層を削除できる条件を判断するとき。

## Do not read this when
- session の具体的な実装、制御フロー、状態管理を確認したいとき。
- join session や conflict resolution の具体的な仕様・実装内容・制御ロジックを確認したいとき。
- 新しい conflict resolution の挙動を追加・変更したいとき。
- oracle 側の正本仕様断片そのものを確認したいとき。

## hash
- d6123717ef6958b1843eacf6b6c88e5dcb403422c170f2ccb42567b4af691803

# `tui`

## Summary
- TUI 関連の既存 import 経路を、正本実装を oracle 側に置いたまま維持するための互換レイヤーを扱う。package 境界の存在、TUI 起動パラメータ生成への接続、resolve-parameter builder の再公開と公開候補の絞り込みが入口になる。
- 恒久的な TUI 実装本体ではなく、呼び出し側が正本側の経路へ移行するまでの参照接続と削除条件を確認する対象である。

## Read this when
- TUI 関連の既存 import surface を維持・整理する変更を行うとき。
- TUI 起動パラメータ生成や resolve-parameter builder が、realization 側から oracle 側の正本実装へどう接続されているか確認したいとき。
- TUI 向けに公開される file access mode 候補から一部の mode が除外される公開面や理由を確認したいとき。
- 互換 import 経路を削除できる条件や、正本側 import 経路への移行状況を調べたいとき。

## Do not read this when
- TUI の具体的な画面、コマンド、イベント処理、状態管理を調べたいとき。
- TUI 起動パラメータや resolve-parameter builder の生成内容そのものを変更したいとき。この対象ではなく正本実装を読む。
- file access mode の定義や列挙値そのものを変更したいとき。
- 新しい TUI 機能や恒久的な builder 実装を追加したいだけで、既存 import 経路の互換維持に関心がないとき。

## hash
- 676fdea34390ba5c49c19c2ffd7eec7556a9c25d52f9a5bd853dd4afcfaf59dc
