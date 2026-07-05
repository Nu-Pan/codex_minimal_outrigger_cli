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
- cmoc の共有 runtime helper 群を収める implementation directory。Codex 起動、設定、git、path、state、logging、error、content hash、INDEX 更新 preflight、CLI 共通ライフサイクルなど、複数 command から使う実行時支援を責務別 module と集約 import で扱う。

## Read this when
- CLI command 実装から使う共通 runtime API の定義元や公開入口を探すとき。
- Codex exec/TUI 起動、profile、preflight、call log、Structured Output 検証、quota/capacity retry、apply process tracking など Codex 実行境界を確認または変更したいとき。
- config 読み書き、git/worktree 操作、root/path 解決、session state 永続化、subcommand logging、共通 error 表示など runtime 横断の helper を確認または変更したいとき。
- INDEX.md 自動更新 preflight、entry 再生成、hash による再利用、indexing commit 作成に関する実装を調べたいとき。

## Do not read this when
- 個別 CLI subcommand の利用者向け引数、出力、業務ロジックだけを調べたいときは、その command 実装へ進む。
- path placeholder、config 型、INDEX entry 文章基準、session state の仕様意図など正本仕様断片を確認したいときは、対応する oracle file を読む。
- 生成済み INDEX.md や log、state、config の個別内容を確認したいだけで、runtime 実装を変更しないとき。
- 特定 helper の具体処理だけを読む対象が既に分かっているときは、この directory 全体ではなく該当 runtime module を直接読む。

## hash
- 35f568c4c6bdc08df09d0e7a03d34aebaca79e7a98548518f10616e702d13f6e

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
- CLI サブコマンド実装を集約する階層。apply、session、review、doctor、indexing、tui などの利用者向け command を runtime や共通処理へ接続する入口になる。
- 各サブコマンドの事前条件確認、状態遷移、git/worktree 操作、Codex 実行連携、出力や report 生成への上位 orchestration を扱う。

## Read this when
- 利用者向けサブコマンドの実装場所を探し、どの個別 command または下位 package へ進むべきか判断したいとき。
- サブコマンドが CLI runtime、state、branch、worktree、git 操作、Codex 実行、report 出力へどう接続しているかを確認または変更したいとき。
- apply、session、review のような run 単位の開始、破棄、取り込み、merge、cleanup、失敗時処理などの外部挙動を追いたいとき。
- doctor、indexing、tui のような単発 command の実行入口、preflight、parameter 解決、利用者向け出力を調べたいとき。

## Do not read this when
- CLI runtime の共通実行制御、repo root 解決、設定読み込み、git wrapper、state 型などの低レベル共通処理だけを調べたいとき。
- Codex に渡す prompt、parameter builder、Structured Output schema の内容だけを確認したいとき。
- INDEX.md の生成ロジック、oracle file や realization file の一般定義、ルーティング規則そのものを調べたいとき。
- サブコマンドの正本仕様だけを確認したいときは、実装ではなく対応する oracle 側の文書を読む。

## hash
- ac96527a1f1cbf4982a7665b29c1ed10a62d65ffa24ce0c9c1860a4f56ecb3f9
