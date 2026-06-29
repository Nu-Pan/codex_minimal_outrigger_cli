# `acp`

## Summary
- ACP builder 関連の realization implementation を束ねる入口。oracle src 側の正本実装を複製せず既存の `acp.*` / `acp.builder.*` import を維持する互換公開面が中心で、下位の個別 builder 領域へ進むための分岐点になる。
- 通常の builder 実体は別領域に委ねる一方、quota availability probe 用の最小 AgentCallParameter builder だけはこの配下で扱い、Codex CLI に渡す probe prompt の組み立てに責務を限定する。

## Read this when
- ACP builder まわりの旧 import 経路や互換 package が、oracle 側の正本実装や実体 module へどう接続されているかを確認したいとき。
- `acp.*` または `acp.builder.*` 参照を移行・削除する作業で、互換入口を残す理由、公開面との関係、削除条件を確認したいとき。
- apply、indexing、review、session、TUI など、どの ACP builder 下位領域へ進むべきかを最初に見分けたいとき。
- quota 枯渇後の availability probe で使う最小 AgentCallParameter builder の入口を探しているとき。

## Do not read this when
- AgentCallParameter の基本型、model、reasoning、file access mode、structured output schema などの共通定義を調べたいとき。
- apply fork、review oracle、session join、TUI 起動などの具体的な builder ロジックや正本の prompt・出力条件を直接確認したいときは、該当する下位領域または oracle 側の正本実装へ進む。
- Codex exec の quota error 検出、polling loop、resume token、ログ保存、profile や cwd 構築など runtime 側の制御を調べたいとき。
- 新しい ACP 機能や API 仕様を追加する場所を探しているとき。この領域は主に互換維持と probe prompt 組み立ての入口であり、仕様追加の正本ではない。

## hash
- 019351fc7abed6d4fdfa427d4b9b4e7ba2b2fe31646193a530fa79a164393daf

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
- cmoc の実行時共通機能を集めた実装領域。Codex 呼び出し、CLI サブコマンド実行ライフサイクル、設定、content hash、git 操作、logging、path 解決、実行結果、session state、INDEX.md 自動更新など、複数の上位機能から使われる runtime helper 群への入口になる。
- 単一の業務サブコマンドではなく、実行環境、外部コマンド境界、永続状態、ログ、エラー表示、INDEX 更新 preflight といった横断的な支援責務を扱う。

## Read this when
- Codex CLI の exec/TUI 呼び出し、profile、sandbox、CODEX_HOME、Structured Output、quota/capacity retry、call log などの共通実行境界を調べたいとき。
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外表示、サブコマンドログ、current logger、step timing、quota 待機集計を確認または変更したいとき。
- cmoc の実行時設定、runtime path、content hash、binary 判定、git repository/worktree 操作、git ignore 判定、外部コマンド結果、session state file などの共有 helper を探すとき。
- Codex 実行前の INDEX.md 自動更新 preflight、対象走査、既存エントリー再利用、hash 鮮度判定、エントリー生成依頼、Structured Output 検証、Markdown 描画を追いたいとき。
- 複数の runtime helper 群を横断して公開 import 経路や責務分担を確認し、どの個別実装へ進むべきか判断したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、CLI への command 登録、利用者向け業務フロー、またはサブコマンド固有の状態更新だけを調べたいとき。
- oracle file の正本仕様、prompt 文面、path model の抽象定義、INDEX.md 仕様意図など、人間が所有する仕様断片を確認したいとき。
- テストコード、fixture、利用者向け README、補助スクリプトなど、実行時共通 helper 以外の realization file を探しているとき。
- 特定の上位機能が共有 helper から取得した値をどう使うかだけを知りたいとき。その場合は、その上位機能の実装を直接読む。

## hash
- 1ec781477374b5fa84a947646cb61d28876e854694f89006685c1f46cd11067f

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
- cmoc の CLI サブコマンド実装を集める領域で、初期化、indexing、TUI、apply、review、session などの利用者向け操作を runtime・git 操作・状態管理・出力生成へ接続する入口になる。
- 各対象はサブコマンドごとに分かれ、単体ファイルは薄い orchestration、下位 package は lifecycle や loop、report、対象列挙、merge などの段階別実装を担う。
- CLI 登録後に実際のコマンド挙動、事前条件、worktree/branch 操作、Codex 呼び出し、利用者向け結果出力のどこを読むべきかを選ぶための分岐点として使う。

## Read this when
- cmoc のサブコマンド実行本体がどこにあり、対象操作に応じて init、indexing、tui、apply、review、session のどれへ進むべきかを切り分けたいとき。
- サブコマンドが CLI runtime を通じて preflight、work root runtime、git 操作、Codex 実行関数、状態更新、標準出力や report 生成へどう接続しているかを追いたいとき。
- apply run、review oracle、session lifecycle など、branch/worktree を伴うサブコマンドの大きな制御順序や下位 helper への入口を探したいとき。
- 初期化、INDEX.md maintenance、TUI 起動など、個別サブコマンドの実行条件、副作用、利用者向け出力を実装側から確認・変更したいとき。

## Do not read this when
- Typer app へのトップレベル登録、CLI 全体の共通 runtime、設定読み込み、path model、git wrapper、state schema など、サブコマンド本体ではなく共有基盤だけを調べたいとき。
- oracle doc にある外部仕様や正本仕様断片を確認したいとき。実装挙動ではなく仕様根拠が必要なら oracle 側を読む。
- INDEX.md の生成アルゴリズム、review finding の prompt、apply report の本文構造、process tracking など、より直接の下位モジュールや builder が既に特定できているとき。
- テスト、fixture、実行ログ、生成済み report の内容を確認したいだけで、サブコマンド実装の制御フローを読む必要がないとき。

## hash
- 7e67ca84b4947b391ea69bfced2ff17706b9946a9ae24d8de03e377043a1aff1
