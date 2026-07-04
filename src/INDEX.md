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
- cmoc の共有 runtime 補助実装をまとめる領域。Codex CLI 呼び出し、preflight、profile、設定、git、path、logging、state、error、content hash、CLI 共通ライフサイクルなど、複数サブコマンドから使われる実行時基盤を扱う。
- この階層には、runtime 系 API の集約入口と責務別 runtime 実装が配置され、個別サブコマンド固有の業務処理ではなく共通実行時支援への入口になる。

## Read this when
- 複数サブコマンドや複数 runtime 領域にまたがる共通 helper、runtime API の公開入口、または runtime_* 実装の所在を探したいとき。
- Codex exec/TUI 起動、profile、CODEX_HOME、Structured Output、quota/capacity retry、indexing preflight、call log など Codex 呼び出し基盤を確認または変更したいとき。
- work root 検査、CLI 共通終了処理、runtime config、git 操作、path 解決、ログ、state file、共通エラー表示、content hash 保存などの共有 runtime 挙動を調べたいとき。
- apply 実行時の linked worktree 復元、pid file、process tracking、abandon 時の停止処理など、apply の低レベル runtime 補助を扱うとき。

## Do not read this when
- 個別サブコマンドの引数定義、利用者向け業務フロー、出力 schema、prompt 本文、または command 固有の制御を調べたいときは、対象サブコマンドや prompt builder 側へ進む。
- path placeholder、config 型、oracle/realization 定義、INDEX.md entry 基準などの正本仕様断片そのものを確認したいときは、oracle 側の該当本文を読む。
- 生成済みログ、生成済み INDEX.md、個別 directory のルーティング判断、または実行履歴の内容確認だけが目的で、runtime 実装を変更しないとき。

## hash
- 698d77809f2f559ee3b312c606f0eddf8da07be90e959865c684f4dd8eb78c26

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
- cmoc の利用者向けサブコマンド実装を集める領域。apply、doctor、indexing、review、session、TUI などの実行入口と、各サブコマンド固有の事前条件、状態遷移、出力、失敗時処理を扱う。
- 低レベル helper や正本仕様ではなく、CLI runtime や共通処理を利用してサブコマンド単位の外部挙動へ接続する orchestration 層を探すための入口。

## Read this when
- 特定の cmoc サブコマンドの実行本体、CLI runtime への接続、command 名や argv の扱い、利用者向け出力を確認または変更したいとき。
- apply や session の branch/worktree/state 操作、review oracle の対象列挙から report 出力までの上位制御、indexing 実行、doctor preprocess 呼び出し、TUI 起動制御のどこへ進むべきか判断したいとき。
- サブコマンド固有の preflight、clean worktree 要件、merge conflict、想定外差分、cleanup、失敗時 report やエラー処理を追いたいとき。
- 利用者向けコマンド単位の外部挙動を変更するため、該当する実行本体や report 生成処理を選びたいとき。

## Do not read this when
- git 実行、branch/worktree 操作、state file、process id、path model、CLI runtime、設定 schema などの共通 helper の詳細だけを確認したいとき。
- INDEX.md の生成内容、ルーティング文書規則、oracle file や realization file の定義など、サブコマンド実行制御から独立した仕様を確認したいとき。
- サブコマンドの正本仕様そのものを確認したいときは、対応する oracle doc を読む。
- 具体的に読むべきサブコマンド実装または report 生成対象が既に分かっており、その対象へ直接進めるとき。

## hash
- 2a8eb17b7337b4ce780319b71fe1a8fed4ce4e24dc5c04fcbc46deb0e192af52
