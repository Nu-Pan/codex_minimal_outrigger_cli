# `acp`

## Summary
- realization 側に残る ACP 関連の互換 import 面を扱う領域。正本側実装を複製せず、既存参照を壊さないための入口や再公開・委譲境界を置く。
- agent call parameter builder 群について、apply fork、review oracle、session、TUI、indexing などの既存公開参照を正本側 canonical 実装へ接続するための上位入口になる。

## Read this when
- realization 側または利用者向け公開面に残る ACP 関連 import を、正本側実装へどう接続しているか確認したいとき。
- agent call parameter builder の公開 import path、再公開層、委譲層、一時的な互換補正の所在を上位から切り分けたいとき。
- apply fork、review oracle、session join、TUI 起動・resolve、indexing 関連の builder 系入口のどれへ進むべきか判断したいとき。
- 正本側 package 構造に合わせて realization 側に互換 package や薄い入口が残っている理由、削除条件、移行判断を確認したいとき。

## Do not read this when
- ACP builder の prompt、出力条件、structured output schema、正本仕様そのものを確認したいとき。正本側の対応する本文へ進む。
- agent call parameter の型定義、file access mode、model class、repo root 解決などの共通構造を確認したいとき。共通定義を扱う領域へ進む。
- apply fork の CLI 制御、fork 適用処理、git 操作、作業レポート生成フローを調べたいとき。ここは parameter 構築入口と互換境界に限られる。
- TUI の画面表示、イベント処理、入力操作など UI 本体の実装を調べたいとき。TUI 本体の領域へ進む。
- indexing の生成処理、探索処理、データ構造、入出力仕様を調べたいとき。互換入口ではなく実体を持つ正本側実装へ進む。

## hash
- f72451816d2b4445ac0ddeb63a3798ac36431744d0e9ae472eba627960a138c4

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
- cmoc の realization implementation のうち、複数サブコマンドや上位 workflow から共有される runtime helper 群をまとめる領域。Codex CLI 呼び出し、設定、path、git、ログ、状態、結果型、エラー表示、内容 hash、CLI 実行ライフサイクル、INDEX.md 更新 preflight など、横断的な実行時基盤への入口になる。
- 単一の機能実装だけでなく、下位の責務別 helper と、それらをまとめて再公開する facade を含むため、共通 runtime API の依存関係や境界を確認する起点として使う。

## Read this when
- サブコマンドや workflow から共通利用される runtime helper の責務分担、公開 import 面、または横断的な実行時処理の入口を探したいとき。
- Codex CLI の exec/TUI 起動、profile・sandbox・CODEX_HOME・Structured Output・quota/capacity retry・call log など、Codex 呼び出し境界の実装を追いたいとき。
- 設定ファイル、runtime path、状態ファイル、ログ、外部コマンド結果、利用者向けエラー表示、git 操作、内容 hash 保存など、複数機能から共有される基盤処理を確認または変更したいとき。
- INDEX.md 更新の preflight、対象列挙、鮮度判定、既存エントリー再利用、生成結果検証、Markdown 化、更新 commit など、目次同期処理の実装を追いたいとき。
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外表示、サブコマンド logger の設定や解除など、個別コマンドの外側にある共通ライフサイクルを調べたいとき。

## Do not read this when
- 個別サブコマンド固有の引数定義、業務処理、画面出力、状態更新フローだけを調べたいときは、そのサブコマンド実装へ直接進む。
- 正本仕様、設計意図、path model の概念定義、INDEX.md エントリー文面の基準や prompt 文言そのものを確認したいときは、対応する oracle 側の本文を読む。
- テスト期待値や fixture の確認だけが目的のときは、対応する realization test を読む。
- 共有 helper の利用先でどの値を渡すか、どのタイミングで呼ぶかという上位 workflow 固有の判断だけを知りたいときは、呼び出し側の実装を読む。
- 単に package 境界だけを確認したい場合を除き、個別 helper の具体的な挙動はこの階層の責務別本文へ進んで確認する。

## hash
- b7765ef7355812d2ca2542009ee72a4db28e8820344d72e12a8df46d287aa503

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
- cmoc の各サブコマンド実行本体を収める realization implementation 領域で、CLI runtime から呼ばれる init、indexing、tui、session、apply、review oracle の処理入口と、その近接補助処理へ進むための階層である。
- この階層では、サブコマンドごとの preflight、worktree・branch・state 操作、Codex exec/TUI 呼び出し、report 生成、利用者向け Markdown 出力の制御を扱う。
- session・apply・review は下位 package や補助モジュールに分かれており、ライフサイクル操作、apply run、review oracle loop、INDEX.md 差分取り込みなどの個別責務へ読み進める入口になる。

## Read this when
- cmoc の特定サブコマンドがどの実装ファイルまたは下位 package にあるかを探したいとき。
- init、indexing、tui、session fork/join/abandon、apply fork/join/abandon、review oracle の実行条件、状態遷移、branch/worktree 操作、Codex 呼び出し、出力や report の流れを調べ始めるとき。
- CLI runtime から個別サブコマンド本体へ渡される command 名、argv、preflight、work root runtime 指定、Codex exec callback の接続箇所を確認したいとき。
- session、apply、review oracle のように複数ファイルへ分かれたサブコマンド群で、まず大分類を選び、対象列挙・merge・cleanup・report・process tracking などの詳細処理へ進みたいとき。

## Do not read this when
- Typer app へのサブコマンド登録、トップレベル CLI 構成、共通 runtime、path model、git wrapper、設定 load、state file のデータ構造や永続化形式だけを調べたいとき。
- サブコマンドの正本仕様や利用者向け仕様そのものを確認したいときは、oracle doc 側を読む方が適切なとき。
- Codex prompt builder、Structured Output parameter、prompt profile、file access prompt の詳細だけを確認したいときは、ACP builder 側を読む方が適切なとき。
- INDEX.md の文章生成・更新アルゴリズム、lock、commit 処理など indexing 共通処理の詳細を調べたいときは、共通 indexing 実装へ直接進む方が適切なとき。
- 個別サブコマンドや補助処理が既に特定できており、そのファイルだけを読めば足りるとき。

## hash
- b68bd3cf2a28b80f78a8e7be5d8f9128d0624b1fdb66d934a7b686e926bb060c
