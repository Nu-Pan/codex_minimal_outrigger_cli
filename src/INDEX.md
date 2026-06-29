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
- cmoc の realization implementation のうち、Codex CLI 呼び出し、CLI サブコマンド共通処理、設定、git、path、logging、content hash、状態永続化、エラー表示、実行結果モデル、INDEX.md 自動更新などを支える共有 runtime helper 群を収める領域。
- 個別サブコマンド固有の業務処理ではなく、複数の上位処理から使われる実行時境界・永続状態・外部コマンド境界・利用者向け共通表示・indexing preflight を調べるための入口になる。
- 一部には互換 import や集約 import だけを担う薄い入口も含まれるため、具体的な挙動を追う場合は、責務別の runtime helper 本文へ進むための階層として扱う。

## Read this when
- Codex exec や TUI 起動に関する profile 準備、sandbox/file access mode、CODEX_HOME、subprocess 実行、Structured Output、retry、quota/capacity 待機、call log、resume 継続の共通制御を確認または変更したいとき。
- CLI サブコマンド共通の実行ライフサイクル、work root 検査、開始・完了表示、終了コード化、例外時エラー表示、サブコマンド logger の設定と解除を調べたいとき。
- INDEX.md の自動更新 preflight、対象走査、除外判定、既存エントリー再利用、hash 鮮度判定、Codex へのエントリー生成依頼、Structured Output 検証、Markdown 描画、排他制御、差分 commit 条件を追いたいとき。
- 設定 JSON の読み書き、既定値補完、不正設定の利用者向けエラー化、または設定項目追加に伴う runtime 変換を扱うとき。
- git command 実行境界、repository 状態検査、cmoc 管理 branch/worktree の作成・削除、git ignore/exclude 判定、追跡済み管理領域の除外処理を確認したいとき。
- runtime path、repository/worktree/cmoc root 解決、実行状態やログ・schema・config の保存先、timestamp/duration 表示、memo 配下判定、cwd 一時切替の共通挙動を確認したいとき。
- サブコマンド event log、step timing、quota 待機時間集計、current logger の context 管理、Codex 呼び出し完了時の console 通知を調べたいとき。
- content hash、内容ベースの保存、binary 判定、外部コマンド結果や Codex exec 結果の共有データ構造、session state file の読み書きと検証、共通エラーレポート形式を確認したいとき。
- 複数の runtime helper を横断して、どの共有 API が集約入口から公開されているか、または互換 import 経路がどの実装へ接続されるかを確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、command 登録、利用者向け操作フロー、サブコマンド固有の状態更新や業務処理だけを調べたいとき。その場合は該当する CLI command 実装側へ進む。
- oracle file の正本仕様、path model の抽象定義、INDEX.md や session state などの仕様意図そのものを確認したいとき。その場合は対応する oracle doc または oracle src を読む。
- テスト期待値、fixture、実行シナリオの検証観点を調べたいだけのとき。その場合は realization test 側を読む。
- 公開 import 経路や集約入口を変える必要がなく、特定 helper の具体的な引数・失敗時処理・副作用だけを調べたいときは、この階層全体ではなく責務が一致する個別本文へ直接進む。
- Codex や git など外部コマンドを実際に起動する上位ワークフローではなく、利用者が見る CLI 出力 schema や report の最終形だけを確認したいときは、その出力を組み立てる呼び出し元を読む。
- README、AGENTS、補助スクリプト、プロジェクト設定、包装用ファイルなど、共有 runtime helper ではない ancillary 領域の責務を調べたいとき。

## hash
- a3c1ff07ee7ca18708e14e206db9c3fc65f61f27ad32de8416b92f4a06cf09f9

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
- cmoc の主要サブコマンド実装を集約する領域で、初期化、indexing、TUI、apply、session、review oracle などの CLI 実行入口へ進むための判断起点になる。
- 各実装は CLI runtime への接続、事前条件確認、git・worktree・state 操作、Codex 呼び出し、利用者向け出力や report 生成など、サブコマンドごとの大きな orchestration を担う。
- apply、session、review のように下位 package へ分割された操作と、単一 module にまとまった init・indexing・tui の入口を切り分けて案内する階層である。

## Read this when
- どのサブコマンド実装へ進むべきかを、初期化、indexing、TUI、apply、session、review oracle などの利用者操作単位から選びたいとき。
- CLI runtime 経由の起動、preflight、clean worktree 要求、cmoc ignore 保証、work root runtime の使い方など、サブコマンド入口側の制御を確認したいとき。
- git branch・worktree・merge・cleanup・state 更新・report 出力など、複数サブコマンドにまたがる操作領域の入口を探したいとき。
- Codex exec や Codex TUI の呼び出しが、各サブコマンドからどの処理に渡されるかをたどりたいとき。
- apply、session、review の下位実装へ進む前に、開始・統合・破棄・対象列挙・loop・INDEX 反映・report 生成の責務境界を把握したいとき。

## Do not read this when
- CLI 全体の Typer app 登録、トップレベル entrypoint、共通 runtime、path 解決、git wrapper、config load、state 永続化の低レベル実装だけを調べたいとき。
- 各サブコマンドの正本仕様や利用者向け要求そのものを確認したいときは、実装入口ではなく対応する oracle 側を読む。
- INDEX.md の本文生成、差分検出、更新対象探索、lock、commit など indexing 共通処理の詳細だけを調べたいとき。
- Codex exec の汎用起動機構、LLM prompt builder、Structured Output parameter、path token 解決など、サブコマンド固有ではない基盤だけを確認したいとき。
- テスト、fixture、生成済み report、または実行ログを調べたいだけで、サブコマンド本体の制御を読む必要がないとき。

## hash
- c8e2c382df6ff1efe9104b0511fb735d284131d55505b1658d0e39aac35ba371
