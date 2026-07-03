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
- サブコマンド実装を機能単位で分けて収める領域。apply、session、review、init、indexing、tui など、各 CLI 操作の実行入口と上位 orchestration へ進むための分岐点になる。
- 各サブコマンドの事前条件、状態遷移、git/worktree/state/Codex 呼び出し、report や stdout 生成などを確認する際に、どの下位領域または実装ファイルを読むべきか判断する入口になる。

## Read this when
- どのサブコマンド実装へ進むべきかを、機能名や扱う状態から切り分けたいとき。
- apply run、session 操作、review oracle、init、indexing、tui の実行フローや上位制御を確認・変更する入口を探しているとき。
- サブコマンドごとの branch、worktree、state、report、INDEX.md、Codex 実行、git 操作の責務境界を把握したいとき。
- CLI runtime や共通 helper ではなく、利用者が実行する個別サブコマンド側の orchestration を追いたいとき。

## Do not read this when
- git command wrapper、state 読み書き、root 解決、Codex runtime、設定モデル、path model など、複数サブコマンドで使う共通処理そのものを調べたいとき。
- oracle file、realization file、INDEX.md エントリー生成規則など、サブコマンド固有ではない仕様概念を確認したいとき。
- Typer app への登録やトップレベル CLI 配線だけを確認したいときは、CLI entrypoint やサブコマンド登録側を読む。
- 個別サブコマンドの正本仕様そのものを確認したいときは、対応する oracle doc を読む。

## hash
- 339f32e0ad94c1272a1ab4f648b23463fdae1a2294aa0d0089a0c6fc1d22164a
