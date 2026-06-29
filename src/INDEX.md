# `acp`

## Summary
- ACP builder 互換層の realization 側入口を束ねる領域。既存の `acp.*` import 経路を維持しつつ、実体は正本側または下位 builder 実装へ委譲する。
- この階層自体は機能本体ではなく、公開 import path、再公開、互換維持、削除条件を判断するための案内役である。

## Read this when
- `acp.*` または ACP builder 系の既存 import 経路が、realization 側でどの互換入口により維持されているかを確認したいとき。
- 正本側の ACP builder 実装と realization 側の公開面との対応、委譲、再公開の境界を把握したいとき。
- apply、indexing、review、session、TUI 関連の builder 領域へ進む前に、この階層が担う互換境界と下位領域の切り分けを確認したいとき。
- 移行期間中の `acp.*` 参照を残す理由や、互換入口を削除してよい条件を判断したいとき。

## Do not read this when
- ACP builder の具体的な parameter 構築処理、プロンプト本文、出力 schema、判定意味論を調べたいとき。正本側本文または該当 builder の実装へ進む。
- apply fork、review、session join、TUI など個別機能の詳細な制御フロー、入出力変換、git 操作、画面挙動を調べたいとき。より直接の機能実装を読む。
- AgentCallParameter 型、model class、reasoning effort、file access mode、repo root 解決などの共通定義を調べたいとき。定義元の共通領域へ進む。
- 新しい ACP 機能や builder 本体を追加する場所を探しているとき。この階層は互換公開面と委譲入口が中心であり、処理本体の追加先ではない。

## hash
- d768228843ed7cb876334710caa3c7dd4f5dad921e7e052ad540d069783b1e41

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
- cmoc の realization implementation のうち、複数の上位機能から使われる共通 runtime helper 群を収める領域。Codex CLI 呼び出し、CLI サブコマンド共通ライフサイクル、設定、git、path、ログ、エラー、状態、結果型、内容 hash、INDEX.md 更新などの横断的な実行支援を扱う。
- 上位コードが個別サブコマンド固有処理ではなく、実行環境・外部コマンド・永続状態・利用者向け共通表示・Codex 呼び出し境界を共有するための入口として位置づく。

## Read this when
- runtime helper の公開入口や、複数領域をまとめて import できる共通 API の所在を確認したいとき。
- Codex exec/TUI 呼び出し、profile 生成、quota/capacity retry、Structured Output 検証、call log、resume token、preflight の実行制御を調べたいとき。
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外表示、サブコマンドログ作成、current logger の扱いを確認または変更したいとき。
- 設定ファイルの読み書き、既定値復元、不正 JSON や不正値の利用者向けエラー化を扱うとき。
- git subprocess 境界、branch/worktree 状態確認、cmoc 管理 branch や linked worktree 操作、.cmoc の ignore 管理を調べたいとき。
- 実行時の root/path 解決、標準保存先、timestamp、memo 判定、一時的な作業ディレクトリ変更を使う処理の参照先を探すとき。
- session/apply state の永続化、state file の JSON 検証、branch 名からの session_id 抽出、active session 探索を扱うとき。
- INDEX.md 更新 preflight、目次対象列挙、hash による再生成判定、既存エントリー再利用、Structured Output 検証、Markdown 生成、更新 commit の流れを確認したいとき。
- 共通のエラー報告、外部コマンド結果、Codex exec 結果、内容 hash 保存、binary 判定など、複数機能にまたがる小さな runtime 支援の責務境界を確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、コマンド登録、業務処理、利用者向け出力 schema だけを調べたいときは、該当する上位コマンド実装へ進む。
- cmoc の正本仕様断片、path model の概念定義、INDEX.md エントリー文面の要求、CLI 出力互換性など人間意図を確認したいときは、oracle 側の本文を読む。
- 個別 helper の利用先だけを追いたいときは、呼び出し側の実装から読む方が直接的である。
- テスト期待値、fixture、外部挙動の検証観点を確認したいだけなら、対応する realization test を読む。
- 実行ログや状態ファイルなど生成済み runtime artifact の内容を調査したいだけのときは、この実装領域ではなく対象 artifact または読み取り側へ進む。

## hash
- d15829569dad53c4993e392f6153c093e5142cdcf630d2167bd7991673684267

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
