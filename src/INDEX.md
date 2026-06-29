# `acp`

## Summary
- realization 側で ACP builder 互換名前空間を維持する入口領域。既存の acp 系 import path を残しつつ、実体は正本側または別 module 側の builder 実装へ委譲するための境界を担う。
- 下位には、acp 直下の互換入口と、apply・review・session・TUI・indexing などの builder 領域へ進むための入口がある。ここ自体は ACP builder の正本仕様や処理本体を所有せず、公開参照経路の維持と下位対象選択のための案内に位置づけられる。

## Read this when
- realization 側に残る acp 系 import path が、正本側 builder 実装や実体 module とどう接続されているか確認したいとき。
- 旧来の acp 系参照を互換入口として残す理由、公開 import 面での扱い、削除条件を判断したいとき。
- ACP builder 関連で、apply・review・session・TUI・indexing などのどの下位領域へ進むべきかを大まかに切り分けたいとき。
- builder の処理本体ではなく、realization 側から正本側実装へ委譲する名前空間や package 境界を確認したいとき。

## Do not read this when
- ACP builder の prompt 本文、structured output schema、モデル選択、file access mode、判定基準などの正本仕様を確認したいとき。対応する oracle 側の本文を読む。
- apply・review・session join・TUI・indexing などの具体的な処理内容や入出力仕様をすでに調べる対象として特定しているとき。該当する下位領域または正本側実装へ直接進む。
- 新しい ACP 機能や API 仕様を追加する場所を探しているとき。この領域は互換維持と委譲入口のための領域であり、機能追加の正本入口ではない。
- CLI 全体の制御フロー、fork 作成、git 操作、ユーザー向け挙動、TUI 画面やイベント処理を調べたいとき。ACP builder 互換入口ではなく、それらを実装する対象を読む。

## hash
- d912acf53b755082ecee4db0a27842369e3da4df2c22c3c748c5f25b30df0c56

# `basic`

## Summary
- realization implementation の basic 領域で、既存の basic 系 import 経路を保つための互換・再公開層をまとめる場所。ACP 関連型、path model、構造化ドキュメント関連の公開名を正本側の実体へ接続し、この層自体には独自の定義・変換・検証ロジックをほぼ持たない。
- 正本側の基本概念を複製せず、realization 側や利用者向け公開面に残る既存参照を維持する入口として位置づけられる。互換層を残す理由や削除条件は、既存参照が残っているか、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- realization implementation から正本側の basic 系公開要素へどの import 経路で接続しているかを確認したいとき。
- ACP 関連型、path model、構造化ドキュメント関連の公開名について、独自実装ではなく正本側の再公開になっている互換境界を確認したいとき。
- 既存の basic 系参照を維持する必要があるか、または互換入口を削除できるかを判断したいとき。
- 正本側の基本型や基本概念を realization 側で複製せずに公開している理由を確認したいとき。

## Do not read this when
- ACP 関連型、path model、構造化ドキュメントの具体的な定義、列挙値、変換規則、検証ロジック、挙動を調べたいとき。その場合は再公開元の正本側実装を読む。
- CLI 挙動、生成処理、テスト観点、または basic 領域以外の realization implementation の責務を調べたいとき。
- 正本仕様断片そのもの、oracle file と realization file の基本概念、またはルーティング文書の生成規則を確認したいとき。
- 新しい基本型や新しい挙動を追加する場所を探しているとき。この対象は互換用の公開入口であり、正本側の定義追加場所ではない。

## hash
- ef20b14eaabf3dde66ce344012d9e8b0114678a8dded41acd4e70edb4a06622d

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
- cmoc の realization implementation における共通 runtime helper 群をまとめるディレクトリ。Codex CLI 呼び出し、preflight indexing、CLI 共通ライフサイクル、設定、内容 hash、エラー表示、git 操作、ログ、パス、実行結果、session state など、複数サブコマンドから共有される実行時支援がここに集約されている。
- 上位コードが利用する共通 API の集約入口と、責務別 runtime module への分岐点を兼ねる。個別 module は薄い互換 facade、外部プロセス境界、永続状態、利用者向けエラー、ログ・保存先・path 解決などの横断的な境界処理を扱う。
- INDEX.md 生成 preflight と entry 生成処理も含むため、cmoc 自身が各階層のルーティング文書を更新する流れを実装側から追う入口にもなる。

## Read this when
- 複数の CLI サブコマンドから共有される runtime helper、結果型、エラー型、ログ、設定、git、path、state、Codex 呼び出し境界の実装を探すとき。
- Codex exec/TUI の起動準備、profile・sandbox・CODEX_HOME・schema 配置、call log、quota/capacity retry、resume token、Structured Output 検証の実装を確認または変更したいとき。
- Codex 実行前に INDEX.md 更新などの indexing preflight がどう登録・実行・skip されるか、また索引 entry の鮮度判定・生成・保存・commit がどう行われるかを調べるとき。
- CLI サブコマンド共通の開始終了ログ、進捗表示、完了サマリー、戻り値から終了コードへの変換、例外時の利用者向けエラー表示を確認または変更したいとき。
- 設定ファイルの読み書き、内容 hash 保存、binary 判定、git worktree/branch 操作、.cmoc ignore 保証、runtime path 解決、session state 永続化などの共通実装を探すとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、利用者向け入出力、状態遷移の上位 workflow を調べたいだけのとき。その場合は該当するコマンド実装へ進む。
- 正本仕様断片、path keyword の概念定義、INDEX.md entry に書くべき意味情報、session state の仕様意図などを確認したいとき。その場合は oracle 側の本文を読む。
- 特定 runtime helper の詳細だけを調べたいときは、この階層全体ではなく責務に対応する個別 module を直接読む。
- 生成済みログ、出力 JSON、設定値、state file などの実データ内容を確認したいだけのとき。この階層はそれらを扱う実装であり、個別生成物の本文ではない。
- テスト期待値や fixture を変更したいときは、まず対応する test 側の本文へ進み、必要になった場合だけこの階層の実装を参照する。

## hash
- 5c7fc8374b4a312ce095235e8bd81bc445bd544d07eefcf071d3157a2c8e63d0

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
