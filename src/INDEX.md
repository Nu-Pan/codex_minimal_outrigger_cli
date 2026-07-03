# `acp`

## Summary
- oracle src 側の acp builder を正本に保ちながら、realization 側に残る acp 系 import 互換面を受け持つ領域。実装本体の複製ではなく、旧公開 import 経路、再 export、module alias、package path 接続、公開型への最小変換を通じて既存参照を成立させる。
- acp builder 群の互換入口を確認するための入口であり、builder の正本仕様や各機能の実行フローではなく、oracle 側 canonical 実装と realization 側公開面の接続境界を扱う。

## Read this when
- acp 系 import 互換性、互換入口を残す理由、削除条件、oracle 側 canonical 実装への委譲経路を確認したいとき。
- oracle 側 builder 出力を realization 側の公開型へどう適合させているかを確認・変更したいとき。
- apply fork、quota probe、review、session、TUI、indexing、common recovery などの agent call parameter builder 入口を探したいとき。
- oracle src 由来の acp builder 実装を複製せず、realization 側 package path や既存公開 import 面だけを維持する構成を調べたいとき。

## Do not read this when
- agent prompt、parameter 生成内容、review 判定、TUI 起動パラメータなどの正本仕様や人間意図を確認したいだけなら、対応する oracle 側 builder または oracle doc を読む。
- apply、review、session、TUI など各機能そのものの実行フロー、CLI 引数処理、画面描画、branch 操作、エラー処理を調べたいときは、それぞれの機能実装や呼び出し元へ進む。
- AgentCallParameter の基礎構造、model、reasoning effort、file access mode、path model、汎用 git helper などの共通定義を確認したいだけなら、該当する共通実装を直接読む。
- 新しい acp 機能や API 仕様を追加する場所を探しているとき。この領域は互換維持と接続境界の確認用であり、機能追加の入口ではない。

## hash
- 9d6f9c63eb006c197e15f61c04dab2d19b5fd99140f3004ab307f76c2fb899a1

# `basic`

## Summary
- oracle 側にある basic 関連の正本実装を realization 側で重複実装せず、既存の `basic.*` import 経路として再公開する互換層を収めるディレクトリ。
- ACP 基本型、path model、構造化文書 API などについて、正本側実装への参照を保ちながら、realization 側および利用者向け公開面の既存参照を維持する入口として位置づけられる。
- この互換層の削除可否は、realization 側と利用者向け公開面から該当する `basic.*` 参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- `basic.*` 経由の既存 import 経路、再公開範囲、互換維持の理由を確認したいとき。
- oracle 側の ACP 基本型、path model、構造化文書 API を realization 側へ複製せず参照する方針を確認したいとき。
- `basic.*` 互換層を残す条件、移行条件、削除できる条件を調べたいとき。

## Do not read this when
- ACP 関連型、path placeholder、path 解決処理、構造化文書処理の定義内容や実処理を確認したいとき。その場合は再公開先の正本側実装を読む。
- CLI 挙動、実行制御、ファイルアクセス制御、テスト挙動など、basic API を利用する処理本体を調べたいとき。
- 既存の `basic.*` 互換参照や公開名に関係しない新仕様・新機能を検討しているとき。

## hash
- 2b1864cfa5bf55fe66730ae8be859de20f405a82e121a9512102f6001b42e250

# `cmoc_runtime.py`

## Summary
- 公開モジュール名を既存の実体モジュールへ差し替えるだけの互換レイヤー。実装本体は別モジュールに委譲し、この入口から import する利用者にも同じ実体を見せるために、実行時のモジュール登録を置き換える。
- 既存の呼び出し元や配布設定が古い import path を参照している期間だけ残す移行用コードであり、責務別の実行時モジュールまたは実体モジュールへ参照元が移った後は削除対象になる。

## Read this when
- 公開されている古い import path と実体モジュールの対応関係を確認したいとき。
- 互換 import path を残す理由、削除条件、または移行状況を調べるとき。
- この入口を import した場合に、どのモジュール実体が利用されるかを確認したいとき。

## Do not read this when
- 実行時処理そのもののロジック、設定解釈、状態操作、CLI 挙動を調べたいとき。この対象は実装本体ではなく委譲だけを行う。
- 新しい実行時機能を追加・修正したいとき。互換入口ではなく、実体側または責務別の実行時モジュールを読む方が直接的である。
- 互換 import path の削除可否と無関係な一般的なモジュール探索やパス定義を調べたいとき。

## hash
- a36ad0b5d09cbe7d2be546fdafcd27ff3ddaf803744331274a69fb25f15cd7ee

# `commons`

## Summary
- cmoc の共通 runtime 支援を集約する領域。Codex 呼び出し、INDEX 更新、CLI 共通ライフサイクル、設定、内容 hash、エラー表示、git 操作、logging、path、結果モデル、session state、apply process 管理など、複数サブコマンドから参照される実行時 helper を扱う。
- 多くの対象は実処理本体と互換 import・公開入口に分かれており、横断的な runtime API の入口確認と、責務別 helper の挙動確認の両方の起点になる。

## Read this when
- 複数サブコマンドで共有される runtime helper、共通データ型、共通例外、共通 logging、共通 path 解決、git 境界、config/state 永続化を確認または変更したいとき。
- Codex exec/TUI 呼び出し、profile 生成、quota/capacity retry、Structured Output、call log、file access post-check、INDEX 更新 preflight など、agent call 周辺の共通実行制御を追いたいとき。
- CLI サブコマンドの共通実行ライフサイクル、終了コード化、エラー表示、完了サマリー、subcommand log event など、個別 command に入る前後の共通処理を扱うとき。
- apply abandon の process 停止、pid file、managed worktree 復元、session state file、cmoc 管理 branch/worktree など、runtime state と外部プロセス・git 状態の接続を調べるとき。
- INDEX.md の自動更新、対象走査、hash 鮮度判定、既存エントリー再利用、entry 生成依頼、Markdown 描画など、routing 文書生成の実行経路を確認したいとき。

## Do not read this when
- 個別サブコマンドの利用者向け仕様、引数定義、業務処理、出力 schema だけを確認したいとき。その場合は command 層や対応するテストへ直接進む。
- path placeholder、config 型、file access rule、INDEX.md 仕様意図、session state の正本要求など、oracle 上の仕様断片そのものを確認したいとき。
- 特定 helper の内部挙動だけを調べたい場合に、集約入口だけで判断できるとき。責務が分かっているなら対応する下位実装を直接読む。
- 生成済みログや実行履歴の内容確認が目的で、runtime logging や call log の実装を変更しないとき。

## hash
- 279fa3986c218c67902425843f8200e1201224038f788549199eb493d2a4335e

# `config`

## Summary
- oracle 側の設定実装・設定定義を正本に保ったまま、realization 側や公開面に残る旧来の設定参照を受けるための互換入口をまとめる領域。
- 設定ロジック本体や正本仕様を持つ場所ではなく、既存 import 経路を維持するための再公開・橋渡しだけを担う。

## Read this when
- realization 側で旧来の設定参照がどこで受け止められているかを確認したいとき。
- 設定定義を複製せずに oracle 側の正本へ寄せたまま、既存参照名を維持している境界を調べたいとき。
- 旧来の設定 import や再公開を削除・置換する作業で、互換入口を残す理由や削除できる条件を確認したいとき。

## Do not read this when
- 設定項目の内容、型、読み込み、検証など、設定挙動の本体を確認したいとき。
- oracle 側の正本仕様断片または正本となる設定実装そのものを確認・変更したいとき。
- 新しい設定項目や公開面を追加する設計判断をしたいだけで、旧来参照との互換維持が論点ではないとき。

## hash
- 17a599971aa7a7a73a6a5499580e2f5660f4a85618ca80119352eb9cd8185b91

# `main.py`

## Summary
- cmoc の最上位 CLI を構成し、Typer アプリケーション、`session`・`apply`・`review` のサブコマンドグループ、各 CLI コマンドから実装関数への委譲を定義する実装入口。
- 通常の CLI 引数解析エラーを cmoc 形式のエラーレポートへ変換する Typer group を定義し、補完実行時だけ通常の Click/Typer 処理へ逃がす。
- console script から `cmoc` としてアプリケーションを起動するためのトップレベル関数を持つ。

## Read this when
- cmoc の公開 CLI コマンド構成、サブコマンド名、option 名、デフォルト値、各コマンドがどの実装関数へ委譲されるかを確認または変更したいとき。
- CLI 引数解析エラーを cmoc の `CmocError` と `render_error` で表示する挙動、または shell completion 時の例外処理分岐を確認または変更したいとき。
- `cmoc` console script 起動時に Typer app がどの `prog_name` で呼ばれるか、またはトップレベル app とサブ Typer app の接続を確認したいとき。

## Do not read this when
- 個別サブコマンドの本体処理、永続状態操作、git 操作、worktree 操作、レビュー処理、INDEX.md 更新処理の詳細を知りたいだけのときは、各サブコマンド実装を直接読む。
- CLI から呼ばれる実装関数の内部エラー生成、ドメインロジック、入出力ファイルの内容を調べたいだけのときは、この入口ではなく委譲先を読む。
- Typer や Click の一般的な使い方、または cmoc 外のパッケージ設定だけを調べたいときは、この対象を読む優先度は低い。

## hash
- 8e9205551785f5e63cb72c666b12049b600ee51d0e204d4198c7d568ba55a7a3

# `oracle.py`

## Summary
- 通常起動時に `src` だけが import path にある場合でも、正本側 `oracle/src/oracle` package を `oracle.*` として解決するための互換 shim。
- realization 側に残る `oracle.*` 再公開入口を個別に複製せず、正本側 package への submodule search path だけを提供する。

## Read this when
- `PYTHONPATH=src` や `bin/cmoc` からの起動直後に、`oracle.other` や `oracle.acp_builder` の import がどう成立するか確認したいとき。
- `src/config`、`src/basic`、`src/acp/builder` の薄い再公開 module が正本側実装へ到達する import 境界を確認・変更するとき。
- oracle src を realization 側へ複製せずに、既存互換 import path を成立させる理由を確認したいとき。

## Do not read this when
- 個別の正本仕様断片、prompt builder、設定定義、path model、ACP builder の本文を確認したいとき。その場合は `oracle/src/oracle` 配下の該当本文を読む。
- CLI サブコマンドや runtime helper の実処理を調べたいとき。この対象は import 境界だけを扱う。
- apply fork の個別 prompt 構築や AgentCallParameter の値を確認したいときは、該当 builder を直接読む。

## hash
- b6f4097cc1550a057bef77dda6b9e5434b394da2d2831fb96ccbf3d319c4222d

# `sub_commands`

## Summary
- CLI サブコマンドの実行本体を集める実装領域。初期化、index maintenance、TUI 起動、session lifecycle、apply lifecycle、review oracle など、利用者向け操作から各ドメインの制御へ進む入口になる。
- 各領域はサブコマンド単位またはサブコマンド群単位で分かれており、CLI runtime から呼ばれる orchestration、事前条件検査、git 状態操作、worktree・branch・state の更新、report 出力への接続を確認する起点になる。

## Read this when
- 利用者向けサブコマンドの実行フロー、事前条件、状態遷移、git 操作、stdout や report 出力への接続を確認または変更したいとき。
- session、apply、review など lifecycle を持つ操作について、開始・合流・破棄・後始末のどの実装へ進むべきかを判断したいとき。
- index maintenance、初期化、TUI 起動など、共通 runtime や下位 helper をサブコマンドとして呼び出す薄い orchestration 層を探したいとき。
- 個別サブコマンドから、対象列挙、review loop、report rendering、conflict 解決、prompt parameter builder、git helper などの下位処理へどこから入るかをたどりたいとき。

## Do not read this when
- CLI parser、Typer app への登録、トップレベル command routing、共通 runtime wrapper だけを確認したいとき。
- git command wrapper、path model、state model、config、ignore 判定、lock、commit 処理など、複数サブコマンドから使われる低レベル helper の詳細だけを調べたいとき。
- Codex に渡す prompt や parameter builder の本文、Structured Output schema、TUI launch parameter の詳細だけを変更したいとき。
- oracle file の正本仕様、INDEX.md 生成規則、oracle file と realization file の一般定義を確認したいとき。

## hash
- 5fc6ec2d5263c0f24fea5bf6e836619f35e041c1722fc1296c81dacef64f8ae5
