# `acp`

## Summary
- realization 側に残る ACP builder 互換 import 面の入口。正本側 builder 実装を複製せず、既存の `acp.*` / `acp.builder.*` 参照を成立させるための package と薄い adapter 群を置く。
- apply fork、review oracle、indexing、session join、TUI 起動・parameter 解決などの AgentCallParameter 生成経路を正本側実装へ接続し、必要な範囲で repo root 解決、oracle src import 経路補正、生成 prompt の局所補正、TUI 用 file access mode 公開を担う。
- quota availability probe は、現行の正本側に専用 builder がないため、runtime 側へ prompt literal を置かないための暫定 adapter として扱われる。

## Read this when
- 既存の `acp.*` または `acp.builder.*` import 経路が、正本側の ACP builder 実装へどう接続されているか確認したいとき。
- apply fork、review oracle、indexing、session join、TUI 関連、quota availability probe の AgentCallParameter 生成入口や互換公開面を探しているとき。
- 正本側 builder へ委譲する前後で、repo root 解決、oracle src import 経路補正、parameter 型の適合、prompt 内 placeholder や typo の最小補正、TUI 用 mode tuple 公開があるか確認したいとき。
- 互換入口や暫定 adapter を残す理由、または削除できる条件を判断したいとき。

## Do not read this when
- ACP builder の prompt 仕様、出力 schema、判定基準、所見処理などの正本内容を確認したいときは、委譲先の正本側実装または正本仕様断片を読む。
- apply fork、review、session join、TUI、indexing の処理本体や制御フローを変更したいときは、この互換層ではなく実体を持つ実装側を読む。
- Codex exec の quota 待機状態機械、resume token、call log、subcommand event など runtime 側の制御を調べたいときは、runtime 実装を読む。
- TUI の画面表示、イベント処理、入力操作など UI 本体を調べたいときは、TUI 実装側を読む。
- AgentCallParameter、FileAccessMode、path placeholder などの共通型や基礎概念そのものを確認したいときは、基本モジュールや path model を読む。

## hash
- d281bafb7ff8cd0b1cc17c8914d0aa99c2888950e1113ce92b9715b4855c8dda

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
- cmoc の共有 runtime helper 群をまとめる実装領域。Codex 呼び出し、indexing preflight、CLI サブコマンド共通処理、設定、内容 hash、エラー表示、git 操作、実行ログ、path 解決、結果型、session state など、複数の上位機能から使われる共通境界を扱う。
- 個別 helper の本体だけでなく、既存 import path を維持する facade や、実行前フック、外部コマンド結果、永続状態、利用者向けエラー化といった横断的な runtime 契約への入口になる。

## Read this when
- Codex CLI の exec/TUI 起動、profile・sandbox・CODEX_HOME・Structured Output・quota/capacity retry・call log など、Codex 実行境界の挙動を確認または変更したいとき。
- CLI サブコマンド共通の実行ライフサイクル、標準出力、終了コード、例外表示、サブコマンドログ、current logger の扱いを追いたいとき。
- INDEX.md 更新 preflight、対象列挙、既存エントリー検証、ハッシュによる鮮度判定、Structured Output から Markdown への描画、更新 commit の流れを調べたいとき。
- 設定ファイルの JSON 永続化、内容 hash 保存、binary 判定、共通エラー表示、git repository/worktree 操作、runtime path 解決、実行結果モデル、session state 永続化など、複数機能で共有される runtime 基盤を扱うとき。
- 上位コードが共通 runtime helper をどの集約入口から import できるか、または互換 import path がどの責務別実装へ接続されるか確認したいとき。

## Do not read this when
- 個別 CLI サブコマンドの引数定義、command 登録、業務フロー、利用者向けオプションだけを調べたいときは、CLI 層や該当サブコマンドの実装へ進む。
- cmoc の正本仕様断片、path model、Codex 実行ルール、INDEX.md 仕様、session state 仕様意図そのものを確認したいときは、oracle 側の文書や実装を読む。
- prompt 文面、エントリー生成 prompt、個別の出力 schema、レビューや apply/session など上位 workflow 固有の判断を変更したいだけのときは、その呼び出し側を読む。
- ログや状態に保存された値の利用先、個別コマンドでの設定値の使い方、生成済みログの解析処理など、共通 runtime 境界より上位の利用文脈を知りたいときは、該当する上位 module を読む。
- 単にパッケージ境界を確認するだけなら入口の短い初期化本文で足り、個別 helper の挙動を調べる場合はこの領域内の責務別実装へ直接進む。

## hash
- cf0a1b1949b87b0d790bd35b19759d526966d310a258486348ec4e0ada034e13

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
- `src/sub_commands` は cmoc の CLI サブコマンド実装を集めた領域で、初期化、indexing、TUI、session、apply、review oracle など、利用者操作から runtime・git・Codex 実行へ接続する入口を扱う。
- 単独ファイルのサブコマンド実装と、session/apply/review 系の下位 package・補助モジュールが同居し、各コマンドの事前条件確認、状態遷移、branch/worktree 操作、report 出力、INDEX.md 反映などの読む先を選ぶための階層である。
- CLI 全体の登録や共通 runtime ではなく、個別サブコマンドの実行順序と、その実行中に呼ばれる下位処理へ進むためのルーティング対象として位置づけられる。

## Read this when
- cmoc の個別サブコマンドについて、実行入口、preflight、runtime への渡し方、利用者向け出力、git 操作や Codex 実行の呼び出し位置を探したいとき。
- 初期化、indexing、TUI、session、apply、review oracle のどの実装領域へ進むべきかを、サブコマンド単位で切り分けたいとき。
- session branch、apply branch/worktree、review worktree、INDEX.md 更新 commit、report 生成など、サブコマンド実行に伴う状態・branch・worktree 操作の入口を確認したいとき。
- CLI から呼ばれる処理と、共通 runtime、config、path model、git wrapper、Codex parameter builder などの下位・周辺実装との接続点を追いたいとき。

## Do not read this when
- Typer app へのコマンド登録、トップレベル CLI 構成、共通 runtime の一般規約だけを確認したいときは、CLI entrypoint や runtime 側を読む。
- path token、state schema、config model、git wrapper、ignore 判定、Codex parameter builder、INDEX.md 生成ロジックそのものなど、サブコマンド固有でない共通処理の詳細を調べたいとき。
- oracle 上の公開仕様や設計意図を確認したいときは、実装領域ではなく対応する oracle doc を読む。
- テストや fixture の期待挙動を確認したいときは、実装入口ではなく対応する test 領域を読む。
- 特定の下位責務がすでに分かっており、apply、session、review loop、review target 列挙、review report、review INDEX 反映などの個別モジュールへ直接進めるとき。

## hash
- e24a19b5b3c3351c89551e389f66c2621def00dd229eec357ddd48b0c82623ff
