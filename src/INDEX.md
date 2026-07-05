# `acp`

## Summary
- oracle src 側の agent call parameter builder を正本に保ちながら、realization 側で旧 `acp.*` import 経路を維持する互換領域。canonical oracle 実装への中継、再公開、公開型変換、runtime path 接続など、既存参照を壊さないための最小適応層を扱う。

## Read this when
- agent call parameter builder 周辺で、旧 `acp.*` import がどの canonical 実装や互換入口へつながるかを確認したいとき。
- oracle 側 builder を複製せず正本として使いながら、realization 側で package path、module alias、公開型変換、runtime path 接続をどう補っているかを調べたいとき。
- apply fork、quota probe、review、session、TUI などの agent call parameter 構築入口や互換層の残存理由・削除条件を確認したいとき。
- 既存 caller や利用者向け公開面に残る `acp.*` import を canonical path へ移行する作業で、影響範囲を絞りたいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいとき。対応する oracle 側 builder や oracle file を読む。
- agent call parameter の基本型、enum、構造化出力 schema、汎用 git helper、path model などの共通定義を調べたいとき。それぞれの定義元へ進む。
- apply、review、session、TUI など各機能の実行フロー、UI、branch 操作、結果判定、外部コマンド実行を調べたいとき。機能本体の実装を読む。
- 新しい acp 機能や API 仕様を追加する場所を探しているとき。この対象は互換維持と最小適応層の入口であり、新機能設計の入口ではない。

## hash
- 871c1d3698bf7219f005efd72f17aaff6274f7ddbdb99325bb64f21b9f306cc6

# `basic`

## Summary
- oracle 側の基本型・path model・構造化文書実装を realization 側で複製せず、既存の `basic.*` 公開参照として再公開する互換層をまとめるディレクトリ。
- ACP、path model、struct doc などの既存 import 経路を正本側実装へ委譲し、後方互換性と公開名を維持する入口として位置づけられる。
- 削除可否は、realization 側と利用者向け公開面から該当する `basic.*` 参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- `basic.*` 経由の既存公開参照、互換維持、移行、削除条件を確認したいとき。
- oracle 側の基本型・path model・構造化文書実装を realization 側へ複製せず再公開している import 経路を調べたいとき。
- ACP 型の既定 preflight 付与、path model API、構造化文書 API など、basic 互換層が提供する公開面や `__all__` を調整したいとき。

## Do not read this when
- ACP 型、path placeholder、構造化文書処理などの正本定義や実装詳細そのものを確認したいとき。その場合は再公開先の oracle 側実装を読む。
- preflight 処理、indexing、CLI 挙動、テスト挙動など、`basic.*` 互換参照の維持や削除条件に関係しない処理を調べたいとき。
- 既存の basic 公開参照ではなく、新規 API 設計や利用元固有の挙動だけを確認したいとき。

## hash
- ddd5f3fcf95fe84d0a51ba34e5edc5ce6f7e273f44a044efc2c4d81d41d0394c

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
- cmoc の共通 runtime helper 群を収める実装ディレクトリ。Codex 起動、profile、設定、content hash、CLI 実行、doctor 前処理、error、git、logging、path、result、state、apply 補助、INDEX.md indexing preflight など、複数サブコマンドから利用される実行時支援を責務別モジュールで扱う。
- 複数の runtime_* 実装をまとめて再公開する集約入口と、互換 import path を維持する薄い橋渡しも含む。

## Read this when
- CLI サブコマンド共通の実行ライフサイクル、Codex exec/TUI 呼び出し、preflight、profile、config、git、path、logging、state、error など、複数機能にまたがる runtime 共通処理を確認または変更したいとき。
- 新しいサブコマンドや上位処理から、既存の共通 runtime API を import して使うべきか、または公開入口へ追加すべきか判断したいとき。
- INDEX.md 自動更新、Codex call log、quota/capacity retry、doctor preprocess、apply process tracking、session state file など、cmoc の実行基盤側の挙動を追いたいとき。

## Do not read this when
- 個別 CLI サブコマンドの利用者向け仕様、引数、出力 schema、業務フローだけを確認したいときは、対象サブコマンドの実装または対応する oracle doc を読む。
- path placeholder、config 型、INDEX.md entry 文面基準、session state の仕様意図など、正本仕様断片そのものを確認したいときは oracle 側の該当本文を読む。
- 生成済み INDEX.md の個別 entry 内容、実行済みログ、特定 session/report の状態調査だけが目的で、runtime 実装自体を変更しないとき。

## hash
- f9adba60b6d3343ea10c5d91bd5176694b307d621976849e0933b08434b00ab9

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
- cmoc の Typer ベース CLI 入口を定義し、トップレベル・session・apply・review 各コマンドを対応する sub_commands 実装へ接続する。
- CLI option 用の scope enum と、通常実行時の Click 引数解析エラーを cmoc 形式のエラーレポートへ変換する Typer group を含む。
- console script から起動される main 関数と、doctor、tui、indexing、session/apply/review 系サブコマンドの公開面を確認する入口になる。

## Read this when
- cmoc の CLI コマンド構成、サブコマンド名、Typer command 登録、console script 起動経路を確認・変更したいとき。
- CLI option の公開値、特に apply fork と review oracle の scope 値や既定値を確認・変更したいとき。
- Typer/Click の通常引数解析エラーを cmoc のエラー表示へ変換する処理を確認・変更したいとき。
- CLI 入口から各 sub_commands 実装へどの関数が委譲されるかを追いたいとき。

## Do not read this when
- 各サブコマンドの実処理、git 操作、worktree 操作、doctor 修復内容、indexing 更新内容の詳細を確認したいだけなら、対応する sub_commands 配下の実装を直接読む。
- cmoc のエラー表示データ構造や render_error の詳細を確認したいだけなら、runtime 側の実装を読む。
- oracle 上のコマンド仕様そのものを確認したい場合は、対応する oracle doc を読む。

## hash
- ecf37fbe5b9ceb9fb4d58e8b63d7f647c6acf8cc96693c66c79e208dcde3e352

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
- CLI サブコマンドの実行本体を集約する領域。apply、session、review、doctor、indexing、TUI などの利用者向け操作について、runtime や共通 helper へ渡す前後の上位制御を扱う。
- 各対象はサブコマンド単位またはその補助処理単位で分かれており、事前条件、状態遷移、branch/worktree/state 操作、Codex 呼び出し、report 出力、失敗時処理など、外部挙動に近い実装へ進むための入口になる。

## Read this when
- CLI サブコマンドの実行フロー、公開挙動、利用者向け出力、失敗時処理、または runtime/helper との接続点を確認・変更したいとき。
- apply、session、review、doctor、indexing、TUI のどの実行本体または補助処理へ進むべきか判断したいとき。
- branch、worktree、state、report、Codex 実行、INDEX 更新反映などを、特定サブコマンドの上位制御として追いたいとき。
- サブコマンド固有の preflight、cleanup、merge conflict、rollback、対象列挙、loop、出力生成などの担当箇所を選びたいとき。

## Do not read this when
- git 実行、path model、state file schema、process id、設定 schema、CLI runtime、Codex 呼び出し wrapper など、サブコマンド固有でない共通基盤の詳細だけを調べたいとき。
- oracle file、realization file、INDEX.md 生成規則、ルーティング文書規則など、CLI サブコマンド実行制御から独立した仕様を確認したいとき。
- INDEX.md の内容生成、差分検出、lock、commit などの共通 indexing ロジックそのものを調べたいとき。
- 具体的に読むべきサブコマンド実装や補助 module が既に分かっており、その対象へ直接進めるとき。

## hash
- f0da990bdeb9d4a8dd6a866f5212ef4f3e7974e382417a25bf9f1c3b1d3bc52f
