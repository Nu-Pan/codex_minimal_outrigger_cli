# `acp`

## Summary
- ACP builder 関連の realization 側互換公開面をまとめる領域。正本実装を oracle 側または下位実体側に置いたまま、既存の公開 import path から builder 群へ到達できる入口を維持する。
- 主な役割は、移行期間中の互換 import 維持、正本側 package 構造との対応、薄い再公開、必要最小限の適合処理、下位 builder 領域への案内であり、builder 本体仕様や生成ロジックの正本ではない。

## Read this when
- ACP builder 関連の既存 import path を残す理由、互換境界、削除条件、移行判断を確認したいとき。
- realization 側の公開面から oracle 側実装または下位 builder 領域へどのように接続しているかを切り分けたいとき。
- apply、indexing、review、session、TUI などの個別 builder 領域へ進む前に、この階層が担う再公開と最小調整の範囲を確認したいとき。
- oracle src 由来の ACP builder 互換 import が realization 側でどこまで維持されているかを把握したいとき。

## Do not read this when
- ACP builder の正本仕様、prompt 本文、structured output schema、agent call parameter 構築ロジックを理解したいとき。
- apply fork、review oracle、indexing、session join、TUI resolve parameter など個別 builder の詳細処理や入出力仕様を直接調べたいとき。
- ACP builder 以外の CLI 制御、fork 適用、git 操作、TUI 描画、状態管理、共通型、file access mode の意味を調べたいとき。
- 新しい ACP 機能や API 仕様を追加する実装本体を探しているとき。

## hash
- b6858fa8ebb1a7fff5acf32e4db5b119ae6ecdd06473ab78e6d7468e7f632218

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
- cmoc の realization implementation のうち、複数のサブコマンドや上位処理から共有される runtime helper 群をまとめる領域。Codex CLI 呼び出し、preflight、設定、内容 hash、エラー表示、git 操作、ログ、path、実行結果、session state などの共通境界を扱う。
- 個別機能の本体というより、上位の CLI や workflow 実装が共通して依存する実行時基盤への入口であり、公開 import 面を集約する facade と、責務別の runtime 実装が同居している。

## Read this when
- サブコマンドや workflow 実装から共有 runtime helper を利用・変更するために、共通 API、結果型、エラー型、ログ、path、設定、git、state、Codex 呼び出しの依存先を探したいとき。
- Codex exec/TUI 起動、quota/capacity retry、profile・sandbox・CODEX_HOME、Structured Output 検証、call log、preflight 実行など、Codex CLI との実行境界を調査または変更したいとき。
- INDEX.md 生成 preflight、対象列挙、既存エントリー再利用、hash 判定、生成結果検証、更新 commit など、目次更新の共通実装を追いたいとき。
- cmoc の実行時設定、内容 hash 保存、binary 判定、利用者向けエラーレポート、git repository 前提条件、linked worktree、サブコマンドログ、標準保存先、session state 永続化などの共通 primitive を確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、CLI アプリへの command 登録、利用者向け workflow、またはサブコマンド固有の業務処理だけを調べたいとき。その場合は呼び出し側の command 実装へ進む。
- cmoc の正本仕様、path model、INDEX.md エントリー仕様、状態仕様、設定仕様など、人間が管理する仕様意図を確認したいとき。その場合は oracle 側の該当本文を読む。
- 共有 helper の公開面ではなく、テスト fixture や期待値、外部挙動の検証観点を調べたいとき。その場合は対応する realization test へ進む。
- git、path、設定、ログ、Codex 呼び出しなどのうち、特定の責務がすでに分かっているときは、この階層全体ではなく、その責務を持つ下位本文を直接読む。

## hash
- f6d9521b10723e1ced53a323d318ba3f264652cde5866f7964ecea9ff002ab0a

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
