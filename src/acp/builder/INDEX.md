# `__init__.py`

## Summary
- `oracle.acp_builder` を `acp.builder` として参照できるようにする互換用の公開入口。実処理を持つ実装本体ではなく、既存の import 経路を保つための薄い窓口として位置づけられる。

## Read this when
- `acp.builder` 経由の import 互換性や公開入口の有無を確認したいとき。
- `oracle.acp_builder` 側の機能を、別名のモジュール経路から公開しているかを確認したいとき。

## Do not read this when
- builder の具体的な生成処理、関数、クラス、制御ロジックを調べたいとき。その場合は実体側の実装を読む。
- 互換入口ではなく、新しい builder 機能の仕様や挙動を確認したいとき。

## hash
- 9e834d7b4a4868035265a9b1d6e846ff32541555482bed155e7bbf15576d4932

# `apply`

## Summary
- apply builder 領域の実装入口であり、oracle 側の package 構造に対応する互換 package と、fork 適用後の変更要約生成に関わる下位領域をまとめる。
- この階層自体は具体的な適用処理全体を担うのではなく、package としての入口、および fork 適用後のレポート向け agent call parameter builder や oracle 側実装への接続点へ進むための分岐点として位置づけられる。

## Read this when
- apply builder 領域が oracle 側の構造とどう対応しているかを確認したいとき。
- fork 適用後の作業レポートに含める変更要約を生成するための schema、agent 呼び出し設定、raw git diff やプロンプトの渡し方を探し始めるとき。
- realization 側の fork 適用関連 import 経路が、oracle 側の file finding enumeration や finding application 定義へどう接続するかを確認したいとき。
- この階層に実処理本体があるのか、互換入口や下位 package へのルーティングが主な役割なのかを切り分けたいとき。

## Do not read this when
- fork 作成、差分適用、git 操作、作業レポート保存など、適用処理全体の制御フローを追いたいときは、より上位の apply/fork 実装を読む。
- file finding enumeration や finding application の具体的な型、関数、挙動を確認したいときは、再エクスポート先の oracle 側本文を読む。
- agent call parameter の共通データ構造、モデル種別、reasoning、ファイルアクセスモードそのものを調べたいときは、共通 ACP 定義を読む。
- 変更要約の表示文面や CLI 出力全体の整形だけを調べたいときは、出力やレポート表示を担う領域を読む。

## hash
- 0472238c2451d79fda96e05588720ab8b0752d05b95adfce0abc611725248351

# `indexing`

## Summary
- ACP builder の indexing 領域に置かれた realization 側の互換入口で、oracle 側にある実体を src 側の import 経路から参照できるようにするための薄いパッケージである。
- この階層自体は indexing の生成処理やデータ構造の実装本体ではなく、対応する oracle 名前空間への公開経路を保つための最小構成を扱う。

## Read this when
- ACP builder indexing 関連の import 経路が realization 側から利用できるか確認したいとき。
- src 側の indexing パッケージが oracle 側の定義を独自実装せず再公開しているかを確認したいとき。
- indexing 領域で、実装本体ではなく oracle 側との互換パッケージ入口を調べたいとき。

## Do not read this when
- indexing の具体的なデータ構造、バリデーション、生成ロジック、制御フローを調べたいとき。
- oracle 側にある index_entry の正本定義や具体的な挙動を確認したいとき。
- ACP builder 全体の処理連携やテスト対象を探しており、import 互換入口の確認が不要なとき。

## hash
- b1c27037bb29a9905c86985af10e1e43d0645d58d8167683cce83634f51a3ab7

# `review`

## Summary
- review builder 領域の realization package で、主に正本側 review builder 実装への互換 import 境界を提供する。package 初期化は名前空間の存在確認に留まり、下位の oracle 領域は finding 関連処理を正本側へ委譲する入口として機能する。

## Read this when
- src 側の review builder が、正本側 review builder package とどのように対応しているかを確認したいとき。
- review builder 領域で、package としての import 経路や互換名前空間の成立を確認したいとき。
- review oracle の finding 関連処理が、src 側からどの境界を通じて正本側実装へ委譲されているかを確認したいとき。

## Do not read this when
- review builder の具体的な処理、関数、クラス、出力、制御フローを調べたいとき。
- finding の列挙・判定・結合・検証に関する具体的なアルゴリズム、入出力、判定基準、prompt 構成を理解したいとき。
- 正本仕様断片としての review builder の要求を調べたいとき。
- package 初期化や正本側実装への再公開境界ではなく、独自の実装変更先やテスト観点を探しているとき。

## hash
- f03fd21fc013712ad91476c5c477dcd1a89d86444e0a4eb22e44662e131ed6ee

# `session`

## Summary
- ACP builder の session 領域における realization 側の入口を扱う階層。正本側 package 構造との import 経路互換を成立させ、session join 領域への委譲入口を下位に持つ。
- この階層自体は session builder の具体的な処理実体を持たず、package としての成立、および join 領域へ進むための境界として位置づけられる。

## Read this when
- ACP builder の session 領域で、realization 側の package 構成が正本側とどう対応しているか確認したいとき。
- session join の競合解決機能へ進む前に、session 領域全体の入口と下位領域の位置づけを把握したいとき。
- この階層が処理実体ではなく、互換 package と下位委譲入口を束ねる場所であることを確認したいとき。

## Do not read this when
- session builder の具体的な処理、状態管理、入出力変換、判定条件を調べたいとき。より直接の実装または正本側の対応箇所を読む。
- session join の具体的な分岐、データ構造、入出力仕様を調べたいとき。下位の対応領域または正本側実装を読む。
- ACP builder 全体の設計や session 以外の領域を調べたいとき。より上位または該当領域の対象を読む。
- oracle 側の正本仕様そのものを確認したいとき。この階層は realization 側の互換境界であり、正本仕様本文ではない。

## hash
- 2c93bf1bba91509e81b2885c63b2b7c6cddd88d36fb0023de9e342fb0c09d71b

# `tui`

## Summary
- ACP builder の TUI 関連 realization implementation をまとめる薄い互換 package。実処理の多くは正本側実装へ再エクスポートされ、この階層自体は src 側から TUI 起動入口とパラメータ解決入口へ到達する公開境界を担う。
- TUI で扱うファイルアクセスモード候補を基本定義の列挙値から組み立て、正本側の TUI パラメータ解決実装と realization 側の import 経路を接続する。

## Read this when
- ACP builder TUI の src 側 package が、正本側 TUI package と互換の入口として存在しているか確認したいとき。
- TUI 起動入口や TUI パラメータ解決入口が、realization implementation 側でどの正本側実装へ委譲されているか確認したいとき。
- TUI で提示・利用するファイルアクセスモード候補が、基本定義の列挙値から作られているか確認したいとき。
- TUI 関連の実処理ではなく、src 配下の公開 import 経路、再エクスポート境界、互換 package の有無を確認したいとき。

## Do not read this when
- ACP builder TUI の起動処理、画面構成、入力フロー、終了処理などの具体的な挙動を調べたいときは、正本側の TUI 実装を読む。
- TUI パラメータ解決の仕様や処理内容そのものを確認したいときは、正本側のパラメータ解決実装を読む。
- ファイルアクセスモード自体の定義や意味を確認したいときは、基本定義側の列挙値を読む。
- 新しい TUI 挙動や仕様判断の根拠を探しているときは、この realization 側 shim ではなく対応する oracle file や実処理を持つモジュールを読む。

## hash
- a075e25b6bbaec9bd14df8a0db60b3593007a362827b15ae00658cd56609e2c9
