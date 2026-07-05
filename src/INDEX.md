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
- cmoc の共有 runtime helper 群をまとめる領域。Codex 起動、profile、config、content hash、CLI 実行ライフサイクル、doctor 前処理、error、git、logging、path、result、state、indexing preflight、apply process 管理など、複数サブコマンドから使われる実行時支援を扱う。
- 共通 API の集約入口と、責務別 runtime 実装が同階層に並ぶため、サブコマンド固有処理ではなく実行基盤側の依存元・公開面・横断的な補助処理を探す入口になる。

## Read this when
- 複数のサブコマンドや runtime helper から共有される実行時 API、結果型、例外、path、git、logging、config、state などの実装を確認または変更したいとき。
- Codex exec/TUI の起動、profile・CODEX_HOME・schema・quota/capacity retry・call log・Structured Output 検証・preflight 連携など、Codex 呼び出し基盤を調べたいとき。
- INDEX.md の自動更新 preflight、entry 再生成、hash による再利用、indexing commit、対象除外条件、git ignore や binary 判定などの実装を扱うとき。
- apply abandon に関わる process 特定・pid file・subprocess 追跡・signal 送信・linked worktree 解決など、apply 実行時の低レベル管理を確認したいとき。
- CLI サブコマンドを共通実行ライフサイクルへ接続する処理、doctor 前処理、サブコマンドログ、終了コード化、例外表示、完了サマリー出力を確認したいとき。
- cmoc 管理領域の path、config JSON、session state file、git worktree/branch、ignore 設定、共通エラーレポート、実行結果モデルなど、runtime 層の共有境界を調べたいとき。

## Do not read this when
- 個別サブコマンドの利用者向け仕様、CLI 引数、業務ロジック、画面出力、session/apply/run の high-level な制御フローだけを確認したいときは、該当する command 実装へ進む。
- oracle file に書かれた正本仕様、path placeholder の定義、INDEX.md entry の文章基準、config 型の正本定義、session state の仕様意図を確認したいだけなら、oracle 側の該当文書や定義へ進む。
- 生成済み INDEX.md の個別 entry 内容や、特定 directory のルーティング判断を確認したいだけなら、その directory のルーティング文書または対象本文を読む。
- 特定の helper 関数や具体的な処理がどの責務別 runtime 実装にあるか既に分かっている場合は、この階層全体ではなく直接その実装本文へ進む。
- ログファイル、config、state、call log などの生成済み実行履歴や保存済みデータを調査するだけで、runtime 実装自体を変更しないとき。

## hash
- 338b055a273cb20d65056ab53a0dcdd494ffeb1b3dc01209ce9f9e0bb4dbe2be

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
- cmoc のサブコマンド実装を集める階層。apply、session、review、indexing、doctor/init、tui など、CLI runtime から呼び出される各操作単位の入口と上位制御へ進むためのルーティング対象である。
- 個別サブコマンドの lifecycle、preflight、state/branch/worktree/process の扱い、Codex 呼び出し、merge/cleanup/report/output などを確認するときに、該当する下位対象を選ぶ入口となる。

## Read this when
- cmoc のサブコマンド実装の所在を探し、apply、session、review、indexing、doctor/init、tui のどこへ進むべきか判断したいとき。
- CLI runtime に接続されたサブコマンド単位の実行順序、事前条件、状態更新、git 操作、利用者向け出力を確認したいとき。
- apply run、session join、review oracle、INDEX.md maintenance、doctor preprocess、TUI 起動など、複数の下位実装候補から対象を絞り込みたいとき。
- サブコマンド固有の report 生成入口、Codex 呼び出し入口、merge/conflict/cleanup 制御、対象列挙や状態遷移の接続点を探したいとき。

## Do not read this when
- CLI runtime 共通の実行ラッパー、repo root 解決、git wrapper、state 永続化、worktree 操作など、サブコマンドに依存しない基盤だけを調べたいとき。
- Codex に渡す prompt、Structured Output schema、parameter builder、config 定義など、サブコマンド入口ではなく builder や oracle 側の詳細だけを確認したいとき。
- INDEX.md の生成内容、oracle file・realization file の定義、ルーティング規則など、サブコマンド実装ではない仕様概念を確認したいとき。
- 対象サブコマンドや責務が既に決まっており、下位の個別実装へ直接進めるとき。

## hash
- ed464b308dd8b05949982a8c4e09344f395595b0693f7992a19289c0b199d3e9
