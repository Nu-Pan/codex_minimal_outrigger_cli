# `acp`

## Summary
- ACP 互換層の入口で、oracle 側 builder を正本に保ちながら既存の acp 系 import 経路を維持する領域。
- 公開 import 面の移行期間中に残す互換入口と、個別 builder 領域へ進むためのルーティングを担う。
- 実際の builder 実装、prompt、parameter 構築、finding 処理、TUI 挙動は下位領域または対応する実体 module へ委ねる。

## Read this when
- 既存の acp 系 import 参照を oracle 側 canonical 実装や realization 側 wrapper へどう接続しているかを確認したいとき。
- apply、review、session、tui、quota probe、indexing などの builder 互換入口のうち、読むべき下位領域を判断したいとき。
- acp 系互換 package や再公開 module を削除または移行する作業で、残す理由や削除条件を調べ始めるとき。
- oracle src 由来の acp builder 互換 import が realization 側または利用者向け公開面でどう維持されているかを確認したいとき。

## Do not read this when
- oracle 側 builder の正本仕様、prompt 本文、parameter 生成内容を確認したいだけなら、対応する oracle 側 builder を直接読む。
- apply、review、session、TUI など各機能の実行フローや本体挙動を調べたい場合は、それぞれの実装領域へ進む。
- AgentCallParameter 型、path model、git helper、file access mode など ACP builder 以外の共通基盤を確認したい場合は、その定義元を読む。
- 特定の変換処理、wrapper の詳細挙動、既知 typo 補正、runtime path 接続などを変更する場合は、該当する個別 module または下位 package を読む。

## hash
- ff451940106c25e6c85f5144a6578f39e1068598cdb6f7f35c39b9914c9db615

# `basic`

## Summary
- oracle 側にある基本型・path model・構造化文書などの正本実装を複製せず、realization 側の既存公開 import 経路として再公開する互換層。
- 既存参照を維持するための入口であり、削除可否は realization 側と利用者向け公開面から対応する互換参照がなくなったかで判断する。

## Read this when
- realization 側で基本型、path model、構造化文書 API の既存 import 経路や再公開内容を確認したいとき。
- oracle 側の正本定義・実装を複製せず参照する互換方針を確認したいとき。
- 既存公開参照を整理し、この互換層を残す理由や削除条件を判断したいとき。

## Do not read this when
- 基本型、path model、構造化文書そのものの仕様や実処理を確認したいとき。その場合は oracle 側の正本定義・実装を読む。
- 互換用の再公開経路ではなく、個別の利用元、CLI 挙動、テスト挙動、一般的な path 変換仕様を調べたいとき。
- 新しい公開面や正本仕様断片を追加する実装場所を探しているとき。

## hash
- ad0cfb03fb2c682437a55ec2ac464197bd2fc5eb3bb3da22e79f7473d62523e7

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
- cmoc の共通 runtime 支援を集めた領域。Codex CLI 起動、実行前処理、設定、git、path、state、logging、error、content hash、CLI 共通ライフサイクル、INDEX 更新 preflight など、複数サブコマンドから使われる実行時基盤を扱う。
- 個別責務の実装に加え、複数の runtime API をまとめて再公開する入口や、互換 import path を維持する薄い境界も含む。

## Read this when
- CLI サブコマンドから共通利用される runtime helper の所在を探したいとき。
- Codex exec/TUI 呼び出し、profile、sandbox、CODEX_HOME、Structured Output、quota/capacity retry、call log、preflight の実装を確認または変更したいとき。
- INDEX.md 自動更新、entry 再生成、indexing commit、対象除外、directory hash、Codex への entry 生成依頼の処理を扱うとき。
- work root 検査、doctor 前処理、サブコマンドログ、進捗表示、終了コード化、例外表示、完了サマリーなど CLI 共通実行形式を確認または変更したいとき。
- git command wrapper、branch/worktree 管理、ignore 判定、oracle file 判定、status 解析など git 状態に依存する共通処理を扱うとき。
- runtime config の読み書き、content hash 保存、path 解決、時刻・duration 表示、session state 永続化、CmocError 表示形式など共通基盤の挙動を調べたいとき。
- apply abandon に伴う apply process や Codex subprocess の追跡・停止、pid file、process group、pid reuse 対策を確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI 引数、利用者向け出力、上位制御フローだけを確認したいときは、該当する command 実装へ進む。
- 正本仕様、prompt 文面、INDEX entry の文章基準、path keyword の定義、config 型の正本定義、session state の仕様意図を確認したいだけなら、oracle 側の該当文書や正本実装を読む。
- 生成済み INDEX.md の個別 entry 内容や、特定 directory のルーティング判断を確認したいだけなら、その directory の INDEX.md または対象本文を読む。
- ログ、設定、state、schema、call log、report など生成済みファイルの内容調査が目的で、runtime 実装自体を変更しないとき。
- 構造化された結果モデル、例外表示、path 計算、git wrapper などのデータ定義や低レベル helper だけが必要な場合は、この領域内のより直接の責務を持つ対象へ進む。

## hash
- 4436c9b3bc99f32cfa28dd50b6830310b3976b75f43287b4517fef181082b5b4

# `config`

## Summary
- oracle src 側の設定実装を正本に保ったまま、realization 側に残る旧来の設定 import 経路を受ける互換入口をまとめるディレクトリ。
- 設定定義や設定ロジック本体を保持せず、正本側の型や実装を再公開して既存の公開参照を維持する境界を扱う。

## Read this when
- `config.*` や設定定義の公開 import 経路が realization 側でどこに残っているか確認したいとき。
- oracle src 側の設定実装を複製せず、realization 側から互換参照として再公開する方針を確認・変更するとき。
- 旧来の設定参照を削除・置換する作業で、この互換入口や再公開経路を削除できる条件を判断したいとき。

## Do not read this when
- 設定値の定義、意味、読み込み、検証などの本体挙動を確認したいとき。
- oracle src 側の正本となる設定実装そのものを確認したいとき。
- 新しい設定項目や設定公開面を追加する作業で、既存の互換 import 経路の残存理由が論点ではないとき。

## hash
- 97eb1bfd8f73945ab835c22962809b5a59009f2d7e1581a56e7058b6c8c786a4

# `main.py`

## Summary
- Typer による cmoc の最上位 CLI 入口を定義し、主要サブコマンドを対応する実装関数へ接続する。
- Click/Typer の通常の引数解析エラーを cmoc 形式のエラーレポートへ変換し、補完実行時だけ通常の Typer 挙動を維持する。
- apply fork と review oracle の scope option 値を CLI 公開値として定義し、各実装へ文字列値を渡す。

## Read this when
- cmoc の CLI コマンド構成、サブコマンド名、option の公開面を確認または変更したいとき。
- CLI 入口から各 sub_commands 実装へどの関数が呼ばれるかを追いたいとき。
- Typer/Click の引数解析エラーが cmoc のエラー表示へ変換される経路を確認したいとき。
- console script 実行時に Typer app がどの prog_name で起動されるかを確認したいとき。

## Do not read this when
- 各サブコマンドの実処理、git 操作、worktree 操作、状態更新の詳細を知りたいだけなら、対応する sub_commands 側を読む。
- cmoc のエラーレポート形式そのものや CmocError の構造を確認したいだけなら、runtime 側を読む。
- INDEX.md 更新処理、oracle review 処理、apply/session 処理など個別機能の内部仕様を確認したいだけなら、この CLI 接続層ではなく各実装を読む。

## hash
- cb7ee361b9445d7c2a928441e07765ae4eaed3d2e06d35acd79015f249e66dde

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
- CLI の各サブコマンド実装を集約する階層。session、apply、review、indexing、doctor/init、TUI などの実行入口と、各 workflow の上位 orchestration へ進むための入口になる。
- サブコマンド単位の lifecycle 制御、runtime への接続、branch/worktree/state/report の扱い、対象列挙や merge/cleanup などの処理の所在を選ぶためのルーティング対象である。

## Read this when
- どのサブコマンド実装へ進むべきかを選びたいとき。
- session や apply の fork/join/abandon、review oracle、indexing、doctor/init、TUI の実行フローをサブコマンド単位で確認したいとき。
- CLI runtime から各 workflow の共通処理へどう接続しているか、または command 実行時の preflight、状態遷移、branch/worktree 操作、report 出力の入口を探したいとき。
- review oracle の対象列挙、finding loop、INDEX.md 変更反映、report 描画など、review 系処理の担当箇所を選びたいとき。
- apply run や session lifecycle の cleanup、merge、conflict handling、process/state 管理に関わる実装場所を探したいとき。

## Do not read this when
- CLI 共通 runtime、git wrapper、state 読み書き、worktree 操作、path model、config 定義など、サブコマンド固有ではない基盤だけを調べたいとき。
- Codex に渡す prompt、Structured Output schema、parameter builder の本文や schema 詳細だけを確認したいとき。
- INDEX.md の生成規則、oracle file・realization file などの仕様概念、または各サブコマンドの正本仕様だけを確認したいとき。
- 対象サブコマンドと担当ファイルがすでに決まっており、その下位 module の詳細ロジックへ直接進めるとき。
- トップレベル CLI のサブコマンド登録や dispatch だけを確認したいとき。

## hash
- c7921dd779601c063519d77620ba8c5d7aa4de8ff27f98c94b9809681568cf47
