# `acp`

## Summary
- realization 側に残る ACP builder 互換入口をまとめる領域。旧来の `acp.*` import 経路を保ちつつ、実体は oracle 側または下位 builder 実装へ委譲するための公開境界として機能する。
- この階層は ACP builder の正本仕様や具体的な組み立て処理そのものではなく、互換 package、再公開層、最小 wrapper の所在と、下位の builder 領域へ進む入口を示す。

## Read this when
- realization 側で残っている ACP 関連の公開 import path や互換入口を確認したいとき。
- 旧来の `acp.*` 参照を oracle 側や実体 module へ移行する際に、どの互換境界が残っているか判断したいとき。
- apply、indexing、review、session、TUI、quota probe などの agent call parameter builder 領域へ進む前に、上位の入口と領域分担を把握したいとき。
- ACP builder 周辺で、正本実装への委譲、再公開、prompt 表記補正、realization 側 parameter 型への適合といった互換層の所在を探したいとき。

## Do not read this when
- ACP builder の具体的な prompt、parameter 組み立て、repo root 解決、型変換、検証ロジックを確認したいときは、該当する下位 builder 領域または oracle 側の正本実装へ進む。
- apply fork、review、session、TUI などのコマンド全体の制御フロー、UI 処理、状態管理、branch 操作、diff 生成、CLI 引数処理を調べたいときは、それぞれの実処理を担う領域へ進む。
- AgentCallParameter、FileAccessMode、model、reasoning、file access、structured output schema などの共通型や基礎定義を確認したいときは、基本モジュールへ進む。
- 互換 import 経路がすでに不要かどうかではなく、新しい ACP 機能や API 仕様の追加場所を探しているときは、この互換入口ではなく正本仕様、実装本体、またはテスト対象を読む。

## hash
- 44f3cc01dbe60bbdc0dbe978dbaae33bb0fd1efc48bc610b46dd9359452dbca2

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
- cmoc の realization implementation のうち、複数のサブコマンドや実行経路から共有される runtime helper 群をまとめる領域。Codex CLI 呼び出し、TUI 起動、設定、content hash、外部コマンド結果、git 操作、ログ、path 解決、永続 state、共通エラー、CLI 実行ライフサイクル、INDEX 自動更新 preflight などを扱う。
- 個別 helper の実装だけでなく、runtime helper 群を横断して公開する集約入口や、Codex 実行前の INDEX 更新、quota/capacity retry、sandbox/profile 生成、subcommand logging など、cmoc の実行基盤に関わる処理への入口になる。

## Read this when
- サブコマンド共通の実行順序、終了コード化、標準出力、例外表示、実行ログ、現在 logger など、CLI 実行基盤の挙動を確認または変更したいとき。
- Codex CLI の exec または TUI 起動について、profile・sandbox・CODEX_HOME・cwd・call log・stdout/stderr/output 保存・retry・quota/capacity 待機・Structured Output 検証・resume 継続を追いたいとき。
- INDEX.md の自動更新 preflight、対象探索、除外判定、既存エントリー再利用、hash 鮮度判定、Codex へのエントリー生成依頼、Markdown 描画の制御を調べたいとき。
- 実行時設定の JSON 読み書き、content hash 保存、binary 判定、git repository/worktree 操作、path 解決、timestamp、memo 判定、session state 永続化などの共通 helper を探すとき。
- 外部コマンド結果や Codex 実行結果の共有データ構造、cmoc 共通例外と利用者向けエラーレポート、runtime helper 群の import 集約面を確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、CLI アプリへの command 登録、サブコマンド固有の業務処理や利用者向け workflow だけを調べたいとき。その場合は command 実装側へ進む。
- 正本仕様断片、path model の概念定義、INDEX.md や session state などの仕様意図を確認したいだけのとき。その場合は対応する oracle 側を読む。
- prompt 文面、Agent 呼び出しパラメータの構築方針、利用者向け schema の仕様、または Codex へ渡す自然言語指示そのものを変更したいときは、prompt builder や schema 定義側を先に読む。
- テスト期待値、fixture、検証観点を変更したいだけのときは、対応する realization test 側を読む。
- アプリ全体のパッケージ構成や上位ルーティングだけを把握したい段階では、より上位の実装ディレクトリ案内から読む先を絞る。

## hash
- 967d3ce4c21996847deff95b2aea4ca3b0d7020e76b2300e81a71aacfd393d81

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
- cmoc の利用者向けサブコマンド実装を集める領域で、初期化、INDEX maintenance、TUI 起動、session lifecycle、apply lifecycle、review oracle などの CLI 本体処理への入口になる。
- 各サブコマンドは CLI runtime 経由の起動、事前条件確認、git branch/worktree 操作、状態更新、Codex 実行連携、利用者向け出力や report 生成をそれぞれの責務範囲で扱う。
- サブコマンド全体のうち、どの操作領域へ進むべきかを選ぶための分岐点であり、詳細な共通処理、path model、state 永続化、git wrapper、prompt builder、oracle 仕様本文などは下位または別領域へ委譲される。

## Read this when
- cmoc の特定サブコマンドについて、CLI から実行処理へ入る位置、runtime への渡し方、preflight、利用者向け出力までの大きな流れを探したいとき。
- 初期化、INDEX maintenance、TUI 起動、session の開始・統合・破棄、apply の開始・取り込み・破棄、review oracle の実行のどの実装へ進むべきかを切り分けたいとき。
- サブコマンド固有の branch/worktree 操作、clean worktree 要求、cmoc ignore 確保、state 更新、merge conflict 対応、report 保存などの入口を探したいとき。
- Codex subprocess や Codex CLI との連携が、各サブコマンドの orchestration の中でどこから呼ばれるかを追いたいとき。
- review や apply のように複数段階の lifecycle を持つ操作について、高レベル orchestration から対象列挙、loop、merge、cleanup、report などの下位処理へ進む起点を確認したいとき。

## Do not read this when
- Typer app へのトップレベル登録、CLI 全体の構成、共通 runtime 規約だけを確認したいときは、CLI entrypoint や runtime 側を読む。
- work root、run root、repository root、path token などの基本パス概念そのものを確認したいときは、path model 側を読む。
- git コマンド実行 wrapper、clean worktree 判定、cmoc ignore 判定、設定読み込み、state 永続化 schema の詳細だけを調べたいときは、共通 helper や state 管理側を読む。
- INDEX.md の本文生成、差分検出、更新対象探索、lock、commit など indexing の詳細ロジックだけを調べたいときは、サブコマンド入口ではなく indexing 共通処理側を読む。
- oracle 上の正本仕様、prompt builder、Structured Output parameter、report 本文構造、finding の品質判断など、実装入口ではなく仕様・生成・表示の詳細を確認したいときは、それぞれの oracle doc または下位専用モジュールを読む。

## hash
- 16dba43cf8d2a4759573f05140c8d3009bb79e69a710ba9d38480b82933ab744
