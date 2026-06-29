# `acp`

## Summary
- realization 側に残る `acp.*` import 互換入口をまとめる領域。正本側の ACP builder 実装を複製せず、既存参照経路を成立させるために oracle 側実装への委譲、再公開、薄い適合を扱う。
- この領域自体は ACP builder の正本仕様や主要ロジックを所有しない。下位には builder 系の互換入口があり、apply、indexing、review、session、TUI などの既存参照経路や、TUI 起動向けの最小差分 adapter へ進む入口になる。

## Read this when
- realization 側または利用者向け公開面に残る `acp.*` import をどう扱うか判断したいとき。
- 既存の `acp.*` / `acp.builder.*` 参照が oracle 側 ACP builder 実装へどのように接続されているか確認したいとき。
- 互換入口を残す理由、削除条件、正本側実装へ移行済みかどうかの確認観点を知りたいとき。
- apply、indexing、review、session、TUI などの builder 系互換入口のうち、どの下位領域へ進むべきか切り分けたいとき。
- TUI 起動パラメータのように、正本側 builder へ委譲しつつ realization 側で最小限の差分を加える adapter を探しているとき。

## Do not read this when
- ACP builder の正本仕様、prompt 本文、model class、file access mode、Structured Output schema、AgentCallParameter 型そのものを確認したいとき。oracle 側の仕様断片または実装へ進む。
- apply、indexing、review、session、TUI の具体的な処理ロジックや入出力仕様を調べたいとき。該当する下位領域または oracle 側実装を直接読む。
- CLI 制御、git 操作、fork 適用、作業レポート生成、画面描画やキー操作など、builder 互換 import 経路ではない実行フローを調べているとき。
- 新しい ACP 機能や API 仕様を追加する場所を探しているとき。この領域は互換維持の入口であり、機能追加の正本ではない。
- realization 側と利用者向け公開面から `acp.*` 参照が消えていることだけを確認済みで、互換入口の詳細を読む必要がないとき。

## hash
- c867deb1854c480760ef11d94b5ae2719706dfb8e8153fcc2bf12213612750dc

# `basic`

## Summary
- 正本側の ACP 型、path model、構造化文書実装を realization 側の既存公開面へ再公開する互換層をまとめる領域。
- 正本実装や正本型を複製せず、既存の `basic.*` import 経路を維持するための薄い入口群として位置づけられる。
- 配下の各対象は、互換維持する import 経路ごとに、再公開対象と削除条件を確認する入口になる。

## Read this when
- realization 側または利用者向け公開面に残る `basic.*` 参照の互換維持、移行、削除条件を調べたいとき。
- ACP 型、path model、構造化文書 API が realization 側で独自実装ではなく正本側から再公開されている境界を確認したいとき。
- 既存 import 経路を正本側または実体 module へ移行する作業で、どの互換入口が残っているかを確認したいとき。

## Do not read this when
- ACP 型、path 解決、構造化文書処理の定義や実処理そのものを変更・確認したいとき。その場合は正本側の実装を直接読む。
- CLI 挙動、生成ロジック、変換処理、テスト観点、または利用元の業務ロジックを調べたいとき。この領域は再公開だけを担う。
- `basic.*` 互換 import 経路の維持や削除条件に関係しない一般的な実装変更を行うとき。

## hash
- 1fe9354fa76d62e962b7276d2ec111fa04694aefc76f8d7a00cab7b69a1f7d83

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
- cmoc の realization implementation のうち、複数のサブコマンドや上位処理から共有される実行時 helper 群を収める領域。Codex CLI 呼び出し、preflight indexing、設定、内容 hash、CLI 共通実行、エラー表示、git 操作、ログ、path、結果型、session state など、runtime 横断の共通境界を扱う。
- 個別機能の業務ロジック本体ではなく、外部コマンド・永続状態・利用者向けエラー・実行ログ・共通 import 面をそろえるための基盤実装への入口として位置づく。

## Read this when
- CLI サブコマンドや上位 workflow から使う共通 runtime API、結果型、例外、ログ、path、git、設定、状態永続化の責務境界を探したいとき。
- Codex CLI の exec または TUI 起動に関する profile 準備、sandbox/read-write root、call log、Structured Output 検証、quota/capacity retry、resume token、preflight 実行制御を確認または変更したいとき。
- Codex 実行前の indexing preflight、索引 entry の鮮度判定、対象抽出、生成依頼、Markdown entry 描画、lock や git commit を含む索引更新の実装を追いたいとき。
- 設定ファイルの JSON 変換、内容 hash 保存、binary 判定、利用者向けエラーレポート、外部 command 結果、session state file など、複数領域で再利用される runtime 境界の挙動を確認したいとき。
- 共通 helper の公開 import 面を整理し、上位コードがどの runtime 名へ依存しているか、または互換 import がどの実装へ接続されるかを確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、command 登録、業務処理、利用者向け workflow だけを調べたいときは、呼び出し側のサブコマンド実装へ直接進む。
- path model、oracle file、realization file、INDEX.md の意味仕様など、正本仕様断片そのものを確認したいときは oracle 側の本文を読む。
- 特定の公開出力 schema、prompt 本文、設定モデルのフィールド定義、基本パス概念、CLI 利用者仕様だけを確認したいときは、それぞれの定義元や仕様本文へ進む。
- 生成済みログや状態ファイルを解析する読み取り側、個別機能での保存先利用、または各 feature 固有の制御フローを調べたいだけのときは、その利用元実装を読む。
- 同階層にある個別 helper の詳細挙動ではなく、単にこの領域が共有 runtime helper 群かどうかだけを確認したい場合は、パッケージ入口以上の本文を読む必要は薄い。

## hash
- e47c3297ad940de43d16e63e4ae14a4d842cadec4d378dc365701a7b23d88ce9

# `config`

## Summary
- oracle 側の設定実装・設定定義を正本に保ったまま、realization 側や公開面に残る旧来の設定参照を受けるための互換入口をまとめる領域。
- 設定ロジック本体や正本仕様を持つ場所ではなく、既存 import 経路を維持するための再公開・橋渡しだけを担う。

## Read this when
- realization 側で旧来の設定参照がどこで受け止められているかを確認したいとき。
- 設定定義を複製せずに oracle 側の正本へ寄せたまま、既存参照名を維持している境界を調べたいとき。
- 旧来の設定 import や再公開を削除・置換する作業で、互換入口を残す理由や削除できる条件を確認したいとき。

## Do not read this when
- 設定項目の内容、型、読み込み、検証など、設定挙動の本体を確認したいとき。
- oracle 側の正本仕様断片または正本となる設定実装そのものを確認・変更したいとき。
- 新しい設定項目や公開面を追加する設計判断をしたいだけで、旧来参照との互換維持が論点ではないとき。

## hash
- 17a599971aa7a7a73a6a5499580e2f5660f4a85618ca80119352eb9cd8185b91

# `main.py`

## Summary
- cmoc の最上位 CLI を構成し、Typer アプリケーション、`session`・`apply`・`review` のサブコマンドグループ、各 CLI コマンドから実装関数への委譲を定義する実装入口。
- 通常の CLI 引数解析エラーを cmoc 形式のエラーレポートへ変換する Typer group を定義し、補完実行時だけ通常の Click/Typer 処理へ逃がす。
- console script から `cmoc` としてアプリケーションを起動するためのトップレベル関数を持つ。

## Read this when
- cmoc の公開 CLI コマンド構成、サブコマンド名、option 名、デフォルト値、各コマンドがどの実装関数へ委譲されるかを確認または変更したいとき。
- CLI 引数解析エラーを cmoc の `CmocError` と `render_error` で表示する挙動、または shell completion 時の例外処理分岐を確認または変更したいとき。
- `cmoc` console script 起動時に Typer app がどの `prog_name` で呼ばれるか、またはトップレベル app とサブ Typer app の接続を確認したいとき。

## Do not read this when
- 個別サブコマンドの本体処理、永続状態操作、git 操作、worktree 操作、レビュー処理、INDEX.md 更新処理の詳細を知りたいだけのときは、各サブコマンド実装を直接読む。
- CLI から呼ばれる実装関数の内部エラー生成、ドメインロジック、入出力ファイルの内容を調べたいだけのときは、この入口ではなく委譲先を読む。
- Typer や Click の一般的な使い方、または cmoc 外のパッケージ設定だけを調べたいときは、この対象を読む優先度は低い。

## hash
- 8e9205551785f5e63cb72c666b12049b600ee51d0e204d4198c7d568ba55a7a3

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
- cmoc の各 CLI sub command の realization implementation を集約する領域で、操作別の実行入口と orchestration を扱う。
- session lifecycle、apply lifecycle、review oracle、INDEX maintenance 起動、初期化処理、TUI 起動など、CLI runtime から呼ばれる処理を個別実装へ振り分ける入口になる。
- サブコマンド横断の共通基盤そのものではなく、各操作固有の preflight、branch/worktree 操作、state 更新、Codex 実行、report/CLI 出力、cleanup へ進むためのルーティング起点として読む。

## Read this when
- cmoc のサブコマンド実行フローを調べ始め、どの操作別実装へ進むべきかを選びたいとき。
- CLI runtime から各サブコマンド固有処理へ渡す command 名、argv、preflight、runtime root、Codex 実行 callback、利用者向け出力の入口を探したいとき。
- branch/worktree 操作、state file 更新、clean worktree 要求、cmoc ignore 保証、report 生成、cleanup などが、どのサブコマンド実装に属するかを切り分けたいとき。
- 個別操作の詳細に入る前に、session lifecycle、apply lifecycle、review oracle orchestration、INDEX maintenance 起動、初期化処理、TUI 起動の実装上の境界を確認したいとき。

## Do not read this when
- CLI アプリ全体の登録、top-level entrypoint、共通 runtime、git wrapper、path model、設定 load、state model の詳細だけを調べたいときは、それぞれの共通実装を読む。
- サブコマンドの正本仕様や利用者向け要求そのものを確認したいときは、実装ではなく対応する oracle doc を読む。
- 対象のサブコマンドや操作が既に特定できており、実行入口ではなく fork、join、abandon、review loop、report、target 列挙、INDEX merge などの詳細だけを調べたいときは、該当する下位実装を直接読む。
- INDEX.md の文章生成、差分検出、lock、commit など indexing 共通処理の内部ロジックや、Codex prompt builder の具体的な文面・schema だけを調べたいときは、この階層ではなく各専用実装を読む。

## hash
- bbc200198445b2051ddadbc421a873bcb24ba37991fb50e3c208657f56946d86
