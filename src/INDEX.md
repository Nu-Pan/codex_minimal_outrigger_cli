# `acp`

## Summary
- ACP builder 系の realization 側互換入口をまとめる領域。oracle 側の正本実装を複製せず、既存の公開 import 経路を維持しながら実体 module や oracle 側 package へ委譲する役割を持つ。
- 直下の互換入口は、既存の ACP 参照を残すための公開面維持に限定される。下位の builder 領域は、apply、review、session、TUI、indexing、quota probe などの agent call parameter builder 名前空間ごとに、互換再公開、委譲、局所補正、parameter 変換境界を扱う。

## Read this when
- ACP builder に関する古い公開 import 経路が、oracle 側の canonical 実装や realization 側の実体 module へどう接続されているか確認したいとき。
- 既存利用者や realization 側に残る ACP 系 import を維持する理由、移行状況、削除条件を判断したいとき。
- agent call parameter 生成について、realization 側で互換層、委譲層、局所的な prompt 表記補正、parameter 変換境界のどれとして扱われているか切り分けたいとき。
- apply fork、review、session join、TUI 起動や resolve parameter、indexing、quota availability probe などの builder 入口から、目的に合う下位領域を選びたいとき。

## Do not read this when
- ACP builder の canonical な仕様、人間意図、prompt 正本、正本側の組み立て仕様を確認したいときは、対応する oracle 側の仕様断片または実装へ進む。
- AgentCallParameter 型、FileAccessMode、path model、git helper などの共通型や共通処理そのものを調べたいときは、それぞれの基本実装へ進む。
- apply fork 全体の制御フロー、branch 操作、CLI 引数処理、diff 生成、quota 待機、resume token、call log などの runtime 挙動を追いたいときは、呼び出し元の実装へ進む。
- TUI の画面表示、イベント処理、入力操作、UI 構成など、parameter builder ではない UI 本体を調べたいとき。
- indexing や review finding の生成、探索、判定、検証ロジックそのものを変更したいときは、互換再公開層ではなく実処理を持つ正本側または対象実装を読む。

## hash
- b67262da8930e294bbb1e4403f7e6442154ea4817149fe4807cc6aed6ec3c85a

# `basic`

## Summary
- 正本側にある ACP 型、path model、構造化文書 API を realization 側の既存公開面へ再公開する互換領域。
- 正本実装や型を複製せず、既存の `basic.*` 参照を保つための薄い入口として位置づけられる。
- 削除条件は、realization 側と利用者向け公開面から対応する `basic.*` 参照がなくなり、正本側または実体 module への移行が済んでいること。

## Read this when
- realization 側で維持されている `basic.*` import 経路や再公開対象を確認したいとき。
- ACP 型、path model、構造化文書 API を正本側から再公開している互換境界を確認したいとき。
- `basic.*` 互換参照を残す理由、移行方針、または削除条件を判断したいとき。

## Do not read this when
- ACP 型、path placeholder、path 解決、構造化文書、Markdown 描画などの実体定義や処理内容を確認したいとき。その場合は再公開先の正本側実装を読む。
- 新しい基本型、path 変換仕様、構造化文書の挙動を追加・変更する場所を探しているとき。この領域は互換再公開を担い、正本側の仕様追加場所ではない。
- CLI 挙動、生成ロジック、変換処理、テスト観点など、`basic.*` 互換 import の維持と無関係な実装責務を調べたいとき。

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
- cmoc の realization implementation における共通 runtime helper 群をまとめる領域。Codex CLI 呼び出し、CLI サブコマンド共通処理、設定、内容 hash、エラー表示、git 操作、実行ログ、path 解決、結果型、session state、INDEX.md 更新 preflight など、複数の上位機能から再利用される実行時支援を扱う。
- 個別 module は、公開 import の集約入口、Codex exec/TUI 実行境界、profile/sandbox/CODEX_HOME/schema 管理、quota/capacity retry、サブコマンド lifecycle、設定 JSON、内容ベース保存、Markdown エラーレポート、git worktree/branch 操作、JSON Lines log、`.cmoc` 配下の保存先 path、実行結果モデル、session state 永続化、目次同期処理などの責務に分かれている。
- 上位の CLI command や workflow が共通の実行時機能へ接続する入口であり、実装詳細を追う場合は対象責務に対応する下位 runtime 実装へ進むためのルーティング起点になる。

## Read this when
- 複数の CLI サブコマンドや workflow から共有される runtime 支援の所在を探したいとき。
- Codex CLI の exec/TUI 起動、Structured Output 検証、quota/capacity retry、profile/sandbox/CODEX_HOME/schema 配置、call log や subprocess 境界の処理を確認・変更したいとき。
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外表示、current logger、サブコマンド実行 log、step timing、quota 待機時間集計を追いたいとき。
- 設定ファイルの読み書き、内容 hash による保存、binary 判定、共通エラーレポート、外部コマンド結果や Codex 実行結果の受け渡しモデルを扱うとき。
- repository/worktree/cmoc root の解決、`.cmoc` 配下の sessions/reports/logs/worktrees/schema/config などの保存先 path、timestamp や duration 表示、memo 配下判定を確認したいとき。
- git command の共通実行境界、branch/HEAD/worktree 状態検査、cmoc 管理 branch や linked worktree、`.cmoc` の ignore 管理を扱うとき。
- session/apply state file の JSON 構造、branch 名からの session_id 抽出、state 読み書き・検証・探索の実装を調べたいとき。
- Codex 実行前の INDEX.md 更新 preflight、目次対象列挙、hash による鮮度判定、既存エントリー再利用、Structured Output から Markdown への変換、更新 commit 条件を確認・変更したいとき。

## Do not read this when
- 個別 CLI サブコマンドの引数定義、command 登録、利用者向け workflow、固有の状態更新や出力 schema だけを調べたいときは、該当する上位実装へ直接進む。
- 正本仕様断片、prompt 文言、path model、設定モデル、FileAccessMode などの仕様意図を確認したいときは、対応する oracle または basic 側の本文を読む。
- INDEX.md エントリー文面の人間向け判断基準やルーティング文書そのものの仕様だけを確認したいときは、対象本文とエントリー基準を読む。
- 生成済み log の解析、サブコマンドログファイルの利用側、または git・path・state から取得した値の上位利用方法だけを追いたいときは、その読み取り側や呼び出し元へ進む。
- 共通 helper の公開面ではなく、特定の helper 関数やデータ構造の詳細だけが必要な場合は、この領域全体ではなく責務に対応する個別 runtime 実装を読む。

## hash
- fb0e0536caffad142d00aca07b83db897c2f7e8462b0ff0623b3d43e31485bed

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
