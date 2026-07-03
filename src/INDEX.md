# `acp`

## Summary
- oracle src 側の ACP builder を正本として扱いながら、realization 側に残る ACP 系 import 経路の互換入口をまとめる領域。実体実装の複製ではなく、canonical 実装への委譲、旧公開名の維持、用途別 builder へのルーティングを担う。
- apply、review、session、indexing、TUI、quota probe などの builder 関連領域へ進む入口であり、移行期間中の公開 import 面、wrapper、戻り値変換、既知表記補正の境界を確認するために使う。

## Read this when
- realization 側または公開面に残る ACP 系 import を、canonical な oracle 側実装や realization 側 wrapper へどう接続しているか確認したいとき。
- 用途別 ACP builder の入口を選び、apply fork、review、session、indexing、TUI、quota probe などの下位領域へ進みたいとき。
- oracle src 由来の builder 実装を複製せずに互換 import を維持している理由、移行方針、削除条件を確認したいとき。
- 既存 caller を canonical import path へ移行する作業で、旧 import 経路や再公開 module の扱いを判断したいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容などの正本仕様や人間意図を確認したいときは、対応する oracle 側 builder または oracle doc を読む。
- 各機能の実行フロー、CLI 引数処理、UI 処理、branch 操作、finding 処理を調べたいときは、それぞれの機能実装へ進む。
- AgentCallParameter の公開型、path model、git helper、file access mode など builder 互換入口の外にある基礎構造を調べたいときは、該当する共通実装を読む。
- 新しい ACP 機能、公開 API、新規 import 経路を追加する場所を探しているときは、互換維持領域ではなく canonical な定義元や設計対象を読む。

## hash
- 94d36e9138301df56f090ff56e3dcbfb2cff3f797de5fb6f06e7b2ed8a1c86f7

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
- cmoc の実行時共通処理を集めた実装領域。Codex 呼び出し、INDEX 更新、CLI 共通ライフサイクル、設定、内容 hash、エラー、git、logging、path、結果モデル、session state、apply process 管理など、複数コマンドから利用される runtime helper を扱う。
- 個別コマンド固有の業務処理ではなく、サブコマンド実装から横断的に参照される薄い公開入口、互換 import 境界、低レベル runtime 補助、永続化・外部プロセス・ログ・path 解決の共通部品へ進むための入口である。

## Read this when
- CLI サブコマンド間で共有される runtime helper の所在を探したいとき。
- Codex exec/TUI 呼び出し、profile、quota/capacity retry、Structured Output 検証、call log、preflight の共通実装を確認または変更したいとき。
- INDEX.md 自動更新、entry 生成、hash 鮮度判定、git ignore・binary・symlink 除外、排他 lock、更新 commit の処理を追いたいとき。
- work root 検査、共通エラー表示、サブコマンドログ、経過時間・quota 待機時間集計、共通 completion summary など、CLI 実行ライフサイクルの横断処理を扱うとき。
- config JSON、session state、local state/log/report/schema/worktree path、git branch/worktree/ignore 判定など、永続状態や repository 状態に依存する共通処理を調べたいとき。
- apply process の pid file、linked worktree 復元、Codex subprocess group 停止、pid 再利用回避など、apply 実行時の process 管理を確認したいとき。

## Do not read this when
- 個別サブコマンドの利用者向け挙動、引数、出力 schema、業務フローだけを確認したいとき。その場合は command 実装または対応するテストへ進む。
- oracle file の正本仕様、path placeholder、file access rule、session state の仕様意図、INDEX.md の要求そのものを確認したいとき。その場合は oracle 側の該当文書または正本実装を読む。
- 特定の helper の公開入口ではなく実際の挙動が必要なときは、この階層内の責務別 runtime 実装へ直接進む。
- 生成済みログ、実行履歴、cache 的な出力ファイルの内容を調査したいだけで、runtime 実装を変更しないとき。

## hash
- 82c085f14009b0028a89080a018d0d42e1e7b55d5c0d6affe252de2e63c2bb3b

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
- cmoc の Typer ベース CLI 入口を定義し、トップレベルコマンドと session・apply・review 配下のサブコマンドを各実装関数へ接続する。
- 通常実行時の Click 引数解析エラーを cmoc 形式のエラーレポートへ変換し、shell 補完時は通常の Typer/Click 挙動を維持する。
- apply fork と review oracle の scope option 値、および apply join の force resolve option を CLI 公開面として定義する。

## Read this when
- cmoc CLI のコマンド階層、サブコマンド名、option 名、デフォルト値、実装関数への接続を確認または変更したいとき。
- CLI 引数解析エラーの表示形式や終了挙動、shell 補完時の例外処理を確認または変更したいとき。
- console script から起動される main 関数や Typer app の構成を確認したいとき。

## Do not read this when
- 個別サブコマンドの実処理、git 操作、worktree 操作、レビュー処理、INDEX 更新処理の詳細を確認したいときは、接続先の実装を直接読む。
- cmoc のエラーレポート構造や描画内容そのものを変更したいときは、runtime 側のエラー定義と描画処理を読む。
- oracle で定義されたサブコマンド仕様そのものを確認したいときは、対応する oracle doc を読む。

## hash
- 090e0a5d4cff8adb41623ebbbd34a7d1b42bac412d81a18a14b3b28da9584fe4

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
- CLI サブコマンド実装を集約する領域。session、apply、review、init、indexing、tui などの利用者向け操作について、共通 runtime や下位 helper を呼び出して実行フローへ接続する入口になる。
- 各サブコマンドの事前条件、git/worktree/state 操作、Codex 実行、report 生成、cleanup、出力処理などを、コマンド単位の orchestration として追うための階層である。
- 低レベル helper や正本仕様そのものではなく、サブコマンドとして公開される操作がどの実装領域へ分かれているかを判断するための入口になる。

## Read this when
- 利用者向けサブコマンドの実行本体や orchestration 層を探したいとき。
- session の作成・合流・破棄、apply run、review oracle、init、indexing、tui のどの実装へ進むべきかを切り分けたいとき。
- サブコマンド実行時の preflight、clean worktree 判定、branch/worktree/state 更新、commit、merge、cleanup、report や stdout 出力への接続を確認または変更したいとき。
- サブコマンドごとに、対象列挙、Codex 呼び出し、差分反映、conflict 処理、INDEX 変更反映などの制御ロジックの入口を探したいとき。

## Do not read this when
- CLI entrypoint への登録、Typer app のトップレベル配線、または共通 runtime の一般規約だけを確認したいとき。
- git 実行 wrapper、worktree 操作、state file 読み書き、root 解決、config 読み込み、Codex runtime などの低レベル共通 helper だけを変更したいとき。
- Codex に渡す prompt、Structured Output schema、parameter builder の内容だけを確認したいときは、対応する builder 側を直接読む。
- 各サブコマンドの正本仕様断片を確認したいときは、実装ではなく対応する oracle file を読む。
- oracle file、realization file、INDEX.md 生成規則、path model など、サブコマンド実行制御ではない仕様概念を調べたいとき。

## hash
- 76c0fa1693818e1497725e258246d203e06456c9809a8f3022942afe3957d401
