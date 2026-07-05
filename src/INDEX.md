# `acp`

## Summary
- ACP builder 関連の realization 側入口。oracle 側 builder を正本に保ちながら、旧 `acp.*` import 経路を維持する互換層と runtime 用の一部 builder への入口を持つ。
- apply、review、session、TUI、indexing、quota availability probe など、用途別 builder の互換維持、canonical oracle 実装への中継、realization 側公開型や runtime path への適合境界を扱う。

## Read this when
- ACP builder の旧 import 経路が oracle 側 canonical 実装や互換入口へどう接続されるかを調べるとき。
- apply fork、review、session、TUI、indexing など、用途別 agent call parameter builder の読む先を選びたいとき。
- oracle 側 builder の戻り値を realization 側の公開型や runtime path に適合させる境界を確認または変更するとき。
- 既存 caller を canonical import path へ移行する作業で、互換入口を残す理由、公開面維持、削除条件を確認したいとき。
- quota waiting が使う Codex 呼び出し用の最小 AgentCallParameter 構成を調べたいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したい場合は、対応する oracle 側 builder や oracle file を読む。
- apply、review、session、TUI など各機能の実行フロー、UI、branch 操作、finding 処理など builder 以外の本体挙動を調べたい場合は、それぞれの実装領域へ進む。
- AgentCallParameter の公開型、path model、git helper、file access mode など共通基盤だけを調べたい場合は、それぞれの定義元を読む。
- 新しい公開 API や新規 import 経路を設計したいだけの場合は、互換維持層ではなく canonical な公開面や設計対象を読む。

## hash
- 66f9a9d31506fc1d7b60168dc0b487092d426facd75e7ec7f6915cb48c6553e6

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
- cmoc の共有 runtime 実装をまとめる領域。Codex CLI 起動、profile、config、content hash、CLI 実行境界、doctor 前処理、error、git、logging、path、result、state、indexing preflight、apply process 管理など、複数 command から使われる共通実行時支援を扱う。
- runtime 系 API の集約 import 入口と、責務別 runtime_* 実装の入口になる。

## Read this when
- CLI command や agent 実行系から呼ばれる共通 runtime helper の定義元を探したいとき。
- Codex exec/TUI の起動、profile、Structured Output、quota/capacity retry、call log、preflight、subprocess 追跡の実装箇所を絞り込みたいとき。
- config 読み書き、git 操作、path 解決、state 永続化、共通 error/report、subcommand logging など、複数機能で共有される実行時処理を確認または変更したいとき。
- INDEX.md の自動更新や indexing preflight、または apply abandon の process 停止・worktree 解決の実装を探したいとき。
- runtime helper の公開入口から責務別 module への接続関係を確認したいとき。

## Do not read this when
- 個別サブコマンドの CLI 引数、利用者向け制御フロー、業務ロジックだけを調べたいときは、command 実装側を読む。
- oracle file にある正本仕様、prompt 本文、INDEX.md entry の文章基準、path keyword の概念定義だけを確認したいときは、oracle 側の該当文書を読む。
- 生成済み INDEX.md の個別 entry 内容、実行済み log、特定 session の状態内容を確認したいだけで、共通 runtime 実装を変更しないとき。
- 特定 helper の低レベル挙動が分かっており、その責務別 runtime_* module を直接読めるときは、この階層全体ではなく対象 module へ進む。

## hash
- f48670b6d20fab9d3f36e2523ecf8b2547053ffb9208029acf48e8277ce8c876

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
- CLI サブコマンド実装をまとめる階層で、apply、session、review、init/doctor、indexing、tui などの利用者向けコマンドから各実行ロジックへ進む入口になる。
- 各コマンドの薄い orchestration、runtime への接続、branch/worktree/state/report/cleanup などの高水準な制御フローを扱い、詳細な生成・判定・低レベル helper は下位対象または共通基盤へ分担している。

## Read this when
- 特定の CLI サブコマンドの実装入口や、どの下位対象へ進むべきかを選びたいとき。
- apply run、session 操作、review oracle、init/doctor、indexing、tui の実行順序、事前条件、state・branch・worktree・report との接続を概観したいとき。
- サブコマンドが共通 runtime、Codex 実行、git 操作、INDEX maintenance、config 同期などへどう接続しているかを追い始めたいとき。

## Do not read this when
- CLI parser 全体の登録や dispatch、共通 runtime、git/worktree/state/path model などの低レベル helper そのものを調べたいとき。
- Codex prompt parameter、Structured Output schema、oracle file や realization file の正本仕様を確認したいとき。
- INDEX.md の本文生成、review finding の prompt、report 描画、対象列挙など、すでに責務が明確な個別ロジックだけを変更したいときは、その下位対象を直接読む。

## hash
- 34ea204c48784c5aa96985c21ad6ed2c7a74e1ed8dd3646979598224e8bca1dc
