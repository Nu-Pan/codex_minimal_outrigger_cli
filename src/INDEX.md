# `acp`

## Summary
- 対象は realization 側に残る ACP builder 互換公開面の入口であり、正本側の builder 実装を複製せずに既存の `acp.*` / `acp.builder.*` import path を成立させるための薄い再公開・委譲・adapter をまとめる。
- 下位には apply fork、review oracle、indexing、session join、TUI 起動・resolve、quota availability probe などの agent call parameter 構築経路への入口があり、多くは正本側実装への接続、既存参照維持、削除条件を示す境界として機能する。
- 正本側に同用途の builder がない quota probe など一部の暫定境界も含むが、主目的は ACP builder の本体仕様や処理本体を置くことではなく、realization 側から正本側または暫定実装へ進むための互換層を保つことにある。

## Read this when
- realization 側に残る `acp.*` / `acp.builder.*` import path が、正本側 ACP builder または暫定 adapter へどのようにつながっているか確認したいとき。
- agent call parameter builder のうち、apply fork、review oracle、indexing、session join、TUI、quota availability probe のどの下位領域へ進むべきか切り分けたいとき。
- 既存参照を壊さないために残された再公開・委譲・互換入口の理由や、削除できる条件を確認したいとき。
- oracle package を通常 import できない配置への fallback、正本側戻り値の realization 側型への適合、runtime 側から prompt literal を外すための暫定 adapter など、互換境界に関わる処理の所在を探したいとき。

## Do not read this when
- ACP builder の正本仕様、prompt 内容、structured output schema、AgentCallParameter の本来の組み立て規則を確認したいとき。正本側の対応する builder 実装や仕様文書へ進む。
- 個別の生成処理、探索処理、状態管理、UI 表示、CLI 制御、git 操作、fork 適用処理など、agent call parameter 構築入口を越えた実処理を調べたいとき。
- AgentCallParameter、FileAccessMode、model class、reasoning effort、repo root 解決などの共通型や基本仕様を確認したいとき。定義元の基本モジュールまたは正本側本文へ進む。
- 新しい ACP builder の正本ロジックや仕様を追加・変更したいとき。互換層ではなく、実体を持つ正本側または該当する処理本体へ進む。

## hash
- 93a383057d7d6b1b273257a72c20e62e04db78c11a3d6d2f85dd66efe7c212bc

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
- cmoc の realization implementation のうち、複数の CLI サブコマンドや上位処理から共有される runtime helper 群を収める領域。Codex 呼び出し、設定、内容 hash 保存、共通エラー、git 操作、実行ログ、path、結果型、永続 state、目次更新 preflight などの横断的な実行時支援を扱う。
- この階層は、共通 runtime API の集約入口と、責務別に分かれた下位 helper 実装への入口である。上位コマンド固有の処理ではなく、実行境界、永続化、外部プロセス、ログ、状態、目次同期などを複数機能から再利用するための実装を探すときの起点になる。

## Read this when
- CLI サブコマンド間で共有される runtime helper の責務分担や、どの下位実装へ進むべきかを判断したいとき。
- Codex exec/TUI 呼び出し、profile・sandbox・CODEX_HOME・Structured Output schema・quota/capacity retry・resume・call log など、Codex CLI との実行境界を確認または変更したいとき。
- 設定ファイルの読み書き、内容 hash による保存、binary 判定、共通エラーレポート、git repository 操作、subcommand event log、runtime path、実行結果型、session state のいずれかの共通 runtime 実装を探しているとき。
- INDEX.md 更新の preflight、目次生成対象の列挙、hash による鮮度判定、既存エントリー再利用、Structured Output 検証、Markdown 生成、更新 commit までの実装経路を追いたいとき。
- 上位コードが複数の runtime 領域を横断して利用しており、公開 import 面や共通 helper の依存先を整理したいとき。

## Do not read this when
- 正本仕様断片、用語定義、path model、CLI の利用者向け仕様、設定モデル自体の定義を確認したいだけのときは、oracle や basic/config 側の本文へ進む。
- 個別サブコマンドの引数定義、command 登録、業務処理、UI 出力、状態遷移フローを調べたいときは、該当する上位コマンド実装へ進む。
- 共通 helper の利用先で渡される具体的な値、個別 workflow の呼び出し順、テスト期待値だけを確認したいときは、その呼び出し元または対応する test を読む。
- 生成される INDEX.md の文面基準や prompt の正本意図だけを確認したいときは、この runtime 実装ではなく、対応する oracle または prompt builder 側を読む。
- 外部コマンド、git、path、logging、state などのうち単一の低レベル責務だけを調べたい場合は、この階層全体ではなく該当する責務別 runtime 実装へ直接進む。

## hash
- 6bbb999430197ae8ec2d4c2f370769a4ad2ab8d61b79c643f30226a5371ee4fd

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
- cmoc の各 CLI サブコマンドの実行本体を収める実装領域であり、CLI runtime から呼ばれる command body、preflight、利用者向け出力、git 操作、state 更新、report 生成への接続点を扱う。
- 初期化、INDEX maintenance、TUI 起動、session ライフサイクル、apply ライフサイクル、review oracle 実行に関する処理がまとまっており、単独サブコマンドの薄い orchestration と、複数モジュールに分かれたサブコマンド群への入口が混在する。
- 共通 runtime、ACP builder、設定モデル、path model、git wrapper そのものではなく、それらをサブコマンドとして組み合わせて実行条件確認、branch/worktree 操作、Codex 呼び出し、commit、cleanup、Markdown 出力へ進める層として読む。

## Read this when
- 特定の cmoc サブコマンドが CLI runtime からどの関数・事前条件・command 名・argv で起動されるかを確認したいとき。
- 初期化、indexing、TUI、session、apply、review oracle のどの実装領域へ進むべきかを、サブコマンド単位で切り分けたいとき。
- サブコマンド実行時の clean worktree 要求、cmoc ignore 保証、active session 判定、scope 検証、state 遷移、branch/worktree 作成・merge・削除、report 出力の流れを追い始めるとき。
- Codex exec または Codex TUI をサブコマンドからどの目的・cwd・config・追加権限で呼び出しているかを確認したいとき。
- session branch と apply branch/worktree、review worktree、INDEX.md 変更 commit、merge conflict 処理など、複数の下位 helper にまたがるサブコマンド上位制御を調査するとき。

## Do not read this when
- Typer app へのトップレベルなサブコマンド登録や CLI 全体のエントリーポイントだけを確認したいとき。
- repo root/work root 解決、共通 error 型、git 実行 wrapper、state schema、config load、timestamp、report directory など、サブコマンド固有でない runtime helper の詳細を調べたいとき。
- Codex に渡す prompt や Structured Output parameter の本文、file access prompt、ACP builder の中身だけを確認したいとき。
- oracle 上の公開仕様、設計意図、サブコマンド利用者向け要求を確認したいとき。実装ではなく oracle doc を読むべき。
- 対象が初期化、indexing、TUI、session、apply、review oracle のどれかに既に特定できており、その下位モジュールまたは個別処理へ直接進めるとき。

## hash
- 03251406cf8d9bbba9f8fcf811f54d85be017339b47acca7a7be20f2e844e352
