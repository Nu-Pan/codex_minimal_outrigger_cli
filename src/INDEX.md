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
- cmoc の共有 runtime helper 群を収める実装領域。CLI 共通実行ライフサイクル、Codex 呼び出し、INDEX 更新 preflight、apply process 管理、config、content hash、doctor 前処理、error、git、logging、path、result、state など、複数の command から使われる実行時支援を扱う。
- 個別 helper の実装だけでなく、runtime 系 API をまとめて再公開する入口や、Codex exec/TUI の互換 import 境界も含む。

## Read this when
- CLI サブコマンドから共通利用される runtime helper の所在を探したいとき。
- Codex exec/TUI 呼び出し、profile、sandbox、CODEX_HOME、Structured Output、retry、quota/capacity、call log、preflight の実装を確認または変更したいとき。
- INDEX.md の自動更新、entry 再生成、hash による再利用、indexing commit、indexing preflight 連携を確認または変更したいとき。
- apply abandon に伴う apply process や Codex subprocess group の特定・停止、pid file、worktree 解決、process tracking を調べたいとき。
- config JSON の読み書き、content hash 保存、doctor 前処理、CmocError 表示、git wrapper、runtime logging、path 解決、実行結果モデル、session state 永続化などの共通 runtime 実装を扱うとき。
- 複数の runtime helper をまとめて import している呼び出し元の依存先や、runtime API の公開入口を確認したいとき。

## Do not read this when
- 個別 CLI サブコマンドの利用者向け仕様、引数、業務ロジック、上位制御フローだけを調べたいとき。その場合は command 実装側を読む。
- oracle file、realization file、path keyword、INDEX.md entry の文章基準など、正本仕様断片そのものを確認したいとき。その場合は oracle 側の文書や実装を読む。
- 生成済み INDEX.md の個別 entry 内容や、特定 directory のルーティング判断だけを確認したいとき。その場合は対象 directory の INDEX.md または対象本文を読む。
- subcommand log、runtime path、config 型、error 型などの利用箇所ではなく仕様意図や正本定義を確認したいだけのとき。
- 公開 runtime API に加える必要が決まっていない、単一 command 内だけの小さな処理を実装したいとき。

## hash
- 3dfc804e8caf6978512fb57ceffd2a982b479d23a1d39bd966474a070188722f

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
- cmoc のサブコマンド実装を集約する領域。apply、session、review、indexing、doctor/init、tui などの CLI 実行入口から、各 workflow の制御層へ進むための入口になる。
- 各サブコマンド固有の実行条件、状態遷移、branch/worktree 操作、Codex 呼び出し、report 出力、利用者向け表示を確認する起点になる。
- 共通 runtime や低レベル helper そのものではなく、サブコマンドとして既存の共通処理や下位 module をどう接続するかを扱う階層である。

## Read this when
- cmoc のサブコマンド実装場所を選び、どの workflow の実行入口へ進むべきか判断したいとき。
- apply、session、review、indexing、doctor/init、tui の CLI 実行フロー、引数受け渡し、実行前検査、状態更新、出力の接続関係を確認または変更したいとき。
- サブコマンドが branch/worktree 操作、state、report、Codex 実行、INDEX maintenance などの下位処理をどの module へ委譲しているかを追いたいとき。
- 特定サブコマンドの高レベルな lifecycle 操作から、より詳細な対象列挙、loop、merge、cleanup、report 生成処理へ読み進める入口を探しているとき。

## Do not read this when
- CLI runtime の共通実行制御、repo root 解決、設定読み込み、git wrapper、state 型、path model などの汎用 helper 自体を調べたいとき。
- Codex に渡す prompt、Structured Output schema、parameter builder の詳細だけを確認または変更したいとき。
- oracle file や realization file の一般定義、ファイルアクセス規則、仕様文書上の分類など、サブコマンド実装ではない正本仕様を確認したいとき。
- INDEX.md の内容生成、差分検出、lock、commit などの共通 indexing ロジックそのものを調べたいとき。
- 対象が既に特定のサブコマンド下位処理に絞れている場合は、その責務を持つ下位 module を直接読む。

## hash
- 0794fcfba1601fdca483414a70be1da44e82f21d7af7fc1fbfc2fca86905303a
