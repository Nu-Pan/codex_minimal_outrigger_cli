# `acp`

## Summary
- oracle 側の canonical ACP builder を正本に保ちつつ、realization 側に残る既存の公開 import 経路を壊さず接続する互換層。
- agent call parameter builder の旧参照、再公開、module alias、package path 接続、realization 側公開型への必要最小限の適合を扱う。
- 実装本体や正本仕様ではなく、旧 import 面を維持する理由、canonical 実装への到達経路、移行期間中の削除条件を確認する入口になる。

## Read this when
- ACP builder 周辺の旧 import 経路、再 export、module alias、package path 接続が canonical 実装へどうつながるかを確認したいとき。
- 既存参照を保つための互換 package や shim を残す理由、公開面維持、削除条件、移行可否を判断したいとき。
- agent call parameter builder 入口を探し、oracle 側の生成結果を realization 側公開型や既存利用者向け公開面へ適合させる境界を追いたいとき。
- realization 側または利用者向け公開面に残る旧 import 参照の扱いを判断したいとき。

## Do not read this when
- agent prompt、structured output、parameter 生成内容、canonical builder 実装などの正本仕様断片を確認したいだけのとき。
- 各機能の実行フロー、CLI 引数処理、永続状態、git 操作、画面描画、イベント処理を調べたいとき。
- AgentCallParameter 型、共通 enum、汎用 git helper、path model、file access rule 検出、ログ収集など builder 互換層以外の共通基盤を調べたいとき。
- 旧 import 互換ではなく個別 builder の変換処理、wrapper の詳細挙動、新規公開 API の設計をしたいとき。

## hash
- c0af36a827c20f72bc478007859048ba68c9e41da8674608a553c068ba14daa1

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
- oracle src 側の設定実装を正本に保ったまま、realization 側と利用者向け公開面に残る旧来の設定参照経路を受ける互換入口群。
- 設定定義や設定ロジック本体を担わず、正本定義の複製を避けながら既存 import を成立させる境界を扱う。

## Read this when
- 旧来の設定参照経路が realization 側でどこに受け止められているか確認したいとき。
- oracle src 側の設定実装を正本に保ちつつ、互換 import を維持している理由や境界を確認したいとき。
- 設定定義の複製を避けるための再公開経路や、その削除可否を判断したいとき。

## Do not read this when
- 設定項目そのものの正本定義を確認したいとき。
- 設定値の読み込み、検証、適用などの本体挙動を調べたいとき。
- 旧来の設定参照経路や互換 import の残存理由が論点ではない作業をするとき。

## hash
- 97eb1bfd8f73945ab835c22962809b5a59009f2d7e1581a56e7058b6c8c786a4

# `main.py`

## Summary
- cmoc の最上位 Typer アプリケーションとサブコマンド階層を定義する CLI 入口。引数解析エラーを cmoc 形式へ変換する Typer group、公開サブコマンドの登録、scope option の enum、console script 用の main を扱う。
- 各サブコマンドの実処理はここでは実装せず、対応する sub_commands 配下の実装関数へ委譲する。

## Read this when
- CLI の公開コマンド構成、サブコマンド名、option 名、Typer への登録位置を確認または変更したいとき。
- 通常の Click/Typer 引数解析エラーを cmoc のエラーレポート形式へ変換する挙動を確認または変更したいとき。
- apply fork や review oracle の scope option と、実装関数へ渡される値の入口を確認したいとき。
- console script から cmoc コマンドがどの Typer app を起動するか確認したいとき。

## Do not read this when
- init、tui、session、apply、review、indexing の各サブコマンド内部処理を確認したいだけなら、対応する sub_commands 配下の実装を直接読む。
- cmoc のエラー表示本文やエラーオブジェクトの詳細を確認したいだけなら、cmoc_runtime 側を読む。
- oracle review や apply fork の仕様そのものを確認したいだけなら、対応する oracle doc を読む。
- INDEX.md 生成処理の詳細を確認したいだけなら、indexing サブコマンド実装を読む。

## hash
- ea36cb3755ae2d03964b8232e6b8fc62ed2b05381481c383fff6c2a3b0072b88

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
- cmoc のサブコマンド実装を集める領域。init、indexing、tui、apply、review、session などの実行入口と上位 orchestration を扱い、各サブコマンドの事前条件、状態遷移、git 操作、Codex 呼び出し、出力・report 生成へ進むための入口になる。
- 単一コマンドの詳細制御だけでなく、apply・review・session のように下位 module へ分かれるサブコマンド群について、どの責務の実装へ進むべきかを判断するための階層である。

## Read this when
- cmoc のサブコマンド実装を調べる起点を探しているとき。
- init、indexing、tui の実行順序、preflight、git 操作、設定・root 解決、CLI 出力など、個別サブコマンドの入口処理を確認または変更したいとき。
- apply run の開始、破棄、取り込み、finding 適用、merge・conflict 処理、report 生成など、apply 系制御の読む先を判断したいとき。
- review oracle の対象列挙、review loop、INDEX 変更反映、merge、report 出力など、review 系処理のどの module へ進むべきかを切り分けたいとき。
- session branch の作成、home branch への合流、merge せず破棄する処理など、session 系サブコマンドの実装入口を探したいとき。

## Do not read this when
- サブコマンド固有ではない git command wrapper、state 読み書き、root 解決、runtime、Codex exec runtime、report directory 生成などの共通 helper の基本挙動だけを確認したいとき。
- oracle file、realization file、path model、INDEX.md 生成規則など、CLI サブコマンド実装ではなく仕様概念を確認したいとき。
- Typer app へのトップレベル登録や CLI 全体の entrypoint だけを確認したいとき。
- INDEX.md の内容生成、差分検出、lock、commit 処理など indexing 共通処理の詳細を調べたいとき。
- Codex に渡す prompt や Structured Output parameter の具体的な組み立てだけを確認したいときは、各 builder 側を直接読む。

## hash
- b45ed8dac1be0d93673e211000d4aef68309b8634ef87b6996d76aa28b053b5e
