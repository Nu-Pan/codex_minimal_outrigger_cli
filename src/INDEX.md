# `acp`

## Summary
- ACP builder 領域の入口。oracle 側 builder を正本として扱い、旧来の公開 import 経路を維持する互換入口と、realization 側で必要な AgentCallParameter 構築境界への案内を担う。
- canonical oracle 実装への委譲・再公開、旧 import 互換を残す理由と削除条件、oracle builder 戻り値を公開型や runtime 要件へ最小限適合させる境界を確認するための対象。

## Read this when
- ACP builder 全体で、oracle 側正本実装と realization 側互換入口の接続方針を確認したいとき。
- 旧来の acp.builder 系 import path や acp.* 参照を canonical 実装へ移行する作業で、互換入口を残す理由や削除条件を調べたいとき。
- apply fork、quota probe、review、session、TUI、indexing など builder 領域のうち、どの下位対象へ進むべきかを判断したいとき。
- oracle builder の生成結果を realization 側 AgentCallParameter、公開型、runtime 保存、既知表記補正へ適合させる境界を探しているとき。
- realization 側または利用者向け公開面に残る acp.* import の扱いを判断したいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容の正本仕様や人間意図を確認したいだけなら、対応する oracle 側 builder を読む。
- apply、review、session、TUI など各機能そのものの実行フロー、CLI 引数処理、状態操作、UI 挙動を調べたいなら、それぞれの機能実装へ進む。
- ACP parameter の公開型、汎用 git helper、path model、file access mode、Structured Output schema など builder 互換層と無関係な基礎実装を確認したいなら、該当する共通実装を直接読む。
- acp builder の実装内容や生成処理そのものを調べたいときは、互換入口ではなく実装本体へ進む。
- 新しい acp 機能、公開 API、新規 import 経路を設計したいだけなら、既存互換層ではなく正本仕様と利用者向け公開面の方針を確認する。
- acp.* 参照がすでに全公開面と realization 側から消えていることだけを確認済みで、互換入口の詳細を読む必要がないとき。

## hash
- 7ff535e97cca846cdae9fcf0ea18bdec0b63e76823ae84744aa0f3ac318c49be

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
- cmoc の共有 runtime helper 群を扱う領域。Codex CLI 起動、preflight、config、content hash、doctor、error、git、logging、path、result、state、apply process 管理など、複数の command 実装から使われる共通実行時処理を集約する。
- runtime 系 API の再公開入口と、責務別 runtime 実装の両方を含むため、共通 helper の公開面を確認する入口にも、具体的な runtime 挙動へ進む入口にもなる。

## Read this when
- CLI サブコマンドから共通実行ライフサイクル、ログ、エラー、終了コード、doctor 前処理、runtime state などへ接続する実装を探すとき。
- Codex exec/TUI 呼び出し、profile、schema、quota/capacity retry、Structured Output 検証、call log、preflight indexing などの共通 runtime 制御を確認または変更したいとき。
- git 操作、worktree・branch 管理、ignore 判定、oracle file 判定、path 解決、config 永続化、session state 読み書きなど、複数機能で共有される実行時基盤を扱うとき。
- apply abandon の process 特定・停止、pid file、Codex subprocess tracking など、apply 実行を支える低レベル runtime 補助を調べるとき。
- INDEX.md の自動再生成 preflight、entry 生成依頼、hash による再利用、indexing commit、対象除外条件を実装側で確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの CLI 引数、利用者向け出力、業務ロジック、上位制御フローだけを確認したいときは、該当する command 実装へ進む。
- oracle file に書かれた正本仕様、path placeholder の概念定義、INDEX.md entry の文章基準、CLI 出力 schema の仕様を確認したいだけなら、対応する oracle 側を読む。
- 生成済み INDEX.md の個別内容、実行済みログ、特定 session の状態ファイルなど、成果物や状態そのものを調査したいだけなら、対象の生成物または状態ファイルを直接確認する。
- runtime helper の公開入口だけを確認したい場合は集約入口へ進み、特定の処理内容を確認したい場合は該当する責務別 runtime 実装へ直接進む。

## hash
- 7fd22b9ddb5955d3abdd89999c78e069c8745b4bcca69aacf3f71540b5bce024

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
- CLI サブコマンド実装の集約階層で、apply、session、review、indexing、doctor/init、TUI などの実行入口へ進むためのルーティング地点。
- 各対象は、CLI runtime との接続、実行前検査、branch・worktree・state・report などの orchestration、または特定サブコマンド固有の制御ロジックを担う。
- 個別の低レベル helper や正本仕様ではなく、利用者向けサブコマンドの実行フローから読む対象を選ぶための入口になる。

## Read this when
- CLI サブコマンドの実装入口を探し、どの下位対象へ進むべきかを選びたいとき。
- apply run、session 操作、review oracle、INDEX maintenance、doctor/init、TUI 起動など、サブコマンド単位の実行順序や orchestration を確認・変更したいとき。
- サブコマンドが CLI runtime、preflight、git/worktree/state/report、Codex 実行処理へどう接続しているかを上位から追いたいとき。
- 特定サブコマンドの失敗時処理、cleanup、branch 操作、出力や report 生成など、公開コマンドに近い制御境界を調べたいとき。

## Do not read this when
- CLI parser やトップレベルのサブコマンド登録だけを確認したいときは、CLI entrypoint 側を読む。
- git wrapper、worktree 操作、path model、state schema、config、runtime 共通処理などの低レベル helper 自体を変更したいときは、それぞれの共通基盤側を読む。
- Codex prompt parameter、Structured Output schema、INDEX.md 生成規則、oracle file や realization file の概念定義などの正本仕様を確認したいときは、oracle 側の該当文書を読む。
- サブコマンド実装ではなく、個別の report 描画、対象列挙、review loop、INDEX 統合処理などに読む対象が絞れているときは、その責務を担う下位対象へ直接進む。

## hash
- 679e9056b28d8c3d53fa38b071494e936913adaff6a6061b5e77f341fe13b98a
