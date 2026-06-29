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
- apply 系の ACP builder 領域への入口となる package。apply builder 全体の実体は下位要素に分かれており、package 初期化の互換要素と、apply fork 用の AgentCallParameter 生成・structured output schema 連携を扱う下位ディレクトリを束ねる。
- oracle 側の apply builder 構造に対応する realization 側 adapter 群を探すための分岐点であり、具体的な apply fork の builder 実装や出力契約へ進む入口になる。

## Read this when
- apply 系 ACP builder の中で、package 初期化だけを見るべきか、apply fork 系の builder・schema へ進むべきかを判断したいとき。
- oracle 側 apply builder と realization 側 AgentCallParameter 生成の対応関係を、apply 領域の入口から辿りたいとき。
- `cmoc apply fork` の変更要約、ファイル単位の所見列挙、所見適用などに関わる builder や structured output schema の所在を探したいとき。

## Do not read this when
- fork 作成、git 操作、差分適用、実行制御など apply fork コマンド全体の制御フローを調べたいとき。
- prompt 本文や正本仕様断片としての builder 挙動を確認したいとき。この領域は oracle 側 builder へ橋渡しする realization 側要素が中心である。
- repo root 解決、path model、AgentCallParameter、enum 型そのものの定義を調べたいとき。この領域ではそれらを利用するが、基礎定義は別領域にある。

## hash
- f3bb50f5ae4050a0f30926694c2f0db98c2c8b33a240bf8fd27c0ccbc04848bf

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
- review builder 領域の realization 側互換境界。上位 package と、その配下の review oracle builder 向け公開経路を用意し、finding の列挙・判定・結合・advocate/challenger 検証を正本側実装へ委譲する。多くは正本側 API の再公開で、advocate 検証パラメータ生成だけは正本側結果を包み直し、prompt 内の oracle root placeholder 表記を realization 側で補正する。

## Read this when
- review builder 領域で、realization 側 package が正本側 package と互換の import 経路を提供しているか確認したいとき。
- finding の列挙・判定・結合・advocate/challenger 検証が、realization 側からどの境界を通じて正本側実装へ到達するか確認したいとき。
- review oracle builder 関連の実装が独自アルゴリズムを持つのか、正本側実装の再公開を主責務とするのかを切り分けたいとき。
- advocate 検証パラメータ生成で、prompt 内の oracle root placeholder 表記だけが realization 側で補正される理由と位置を確認したいとき。

## Do not read this when
- finding 列挙・判定・結合・検証の具体的なアルゴリズム、prompt 構成、判定基準、入出力仕様を理解したいとき。その場合は委譲先の正本側実装や仕様断片を読む。
- review workflow 全体、CLI 入出力、builder 全体の責務分担、または finding 以外の review 処理を調べたいとき。より上位または該当責務の対象へ進む。
- model class、reasoning effort、file access mode、Structured Output schema などの共通定義を調べたいとき。それらを定義する正本側または共通定義を読む。
- package 初期化や互換 import 境界ではなく、実処理本体を変更したいとき。この領域の大半は再公開であり、処理本体の変更先ではない。

## hash
- 08833098dee372aaeb3a86fbf77c4a289a4f16a325b3c1594eb40eb3198e498d

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
- ACP builder の TUI 関連呼び出しパラメータを、正本側の定義から realization implementation 側へ接続する薄い package。
- TUI 起動用パラメータでは正本側の構築結果を再利用しつつ、起動時に消費しない Structured Output schema path を実行時契約に合わせて無効化する。
- TUI のパラメータ解決入口と、TUI で提示するファイルアクセスモード候補を基本定義の列挙値から参照できるようにする。

## Read this when
- TUI 起動または TUI パラメータ解決に使う AgentCallParameter が realization implementation 側でどう公開されているか確認したいとき。
- TUI 起動処理が存在しない Structured Output schema path を公開しないようにしている互換調整を確認・変更したいとき。
- TUI で扱うファイルアクセスモード候補が基本定義の列挙値と同期しているか確認したいとき。
- 正本側の ACP builder TUI 実装を、実行側 package から import できる形に接続する箇所を探しているとき。

## Do not read this when
- TUI の画面描画、入力処理、イベントループなど、起動後の TUI 本体の挙動を調べたいとき。
- パラメータ構築や解決の正本仕様断片そのものを確認したいとき。
- Structured Output を実際に消費する agent call や JSON schema の内容を調べたいとき。
- ファイルアクセスモード自体の意味や基本定義を確認したいとき。

## hash
- 01df73688f2bfcdab47931ac7ccc89582b5f9b15e5a365a1351fe5e278d86ad6
