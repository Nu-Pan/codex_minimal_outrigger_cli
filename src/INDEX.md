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
- cmoc の共有 runtime 実装をまとめる領域。Codex 起動、INDEX 更新 preflight、CLI 共通実行、config、content hash、doctor 前処理、error、git、logging、path、result、session state、apply process 管理など、複数サブコマンドから使われる共通実行時 helper と公開 import 入口を扱う。

## Read this when
- CLI サブコマンドや上位 workflow から使う共通 runtime API、結果型、error、path、git、logging、state、config、Codex 呼び出し境界の依存先を探したいとき。
- Codex exec/TUI 実行、INDEX.md indexing preflight、doctor preprocess、apply abandon の process 停止など、サブコマンド横断の実行制御を確認または変更したいとき。
- 共有 runtime helper の公開入口や責務別 module の配置を確認し、個別 runtime_* 実装へ読む先を絞りたいとき。

## Do not read this when
- 個別 CLI サブコマンドの利用者向け仕様、引数、出力 schema、業務ロジックだけを確認したいときは、その command 実装や対応する oracle doc を読む。
- path placeholder、config 型、INDEX entry 文面基準など、正本仕様断片そのものを確認したいときは oracle 側の該当対象を読む。
- 生成済み INDEX.md、ログ、state、report の個別内容を調べたいだけで、runtime 実装や共通 helper を変更しないとき。

## hash
- 9135e5c66ad404b18c3915828ce8ea2baa436d4c52c613218fa7cf26322bc98b

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
- CLI サブコマンドの実行本体を集める階層。apply、review、session、doctor、indexing、TUI など、利用者向けコマンドを runtime、state、git 操作、Codex 実行、レポート出力へ接続する入口になる。
- 各サブコマンド固有の事前条件確認、状態遷移、branch/worktree 操作、利用者向け出力、失敗時処理を追うための上位ルーティング地点であり、詳細な共通 helper や prompt/schema 定義へ進む前に読む対象を選ぶ場所である。

## Read this when
- CLI サブコマンドの挙動を確認または変更するために、どの実装領域へ進むべきかを選びたいとき。
- apply、review、session のように branch、worktree、state、process id、report、cleanup を伴うコマンドの上位制御フローを追いたいとき。
- doctor、indexing、TUI など、runtime 経由で共通処理を呼び出すサブコマンド固有の接続点や出力を確認したいとき。
- review oracle の対象列挙、finding 処理、INDEX 変更反映、report 生成など、review 系処理のどの下位責務へ進むべきかを判断したいとき。

## Do not read this when
- CLI runtime、設定読み込み、git wrapper、state 型、path model などの共通基盤そのものを調べたいとき。
- Codex に渡す prompt、parameter builder、Structured Output schema の詳細だけを確認したいとき。
- oracle file や realization file の一般定義、INDEX.md 生成規則、ルーティング規則そのものを確認したいとき。
- 特定サブコマンドの正本仕様を確認したいだけのときは、実装ではなく対応する oracle doc を読む。

## hash
- 6dfe4e4873c986a77f6deca66f21adc4460d97a8764d6db60d1f9cdaf00a9280
