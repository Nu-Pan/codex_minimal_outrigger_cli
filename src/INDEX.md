# `acp`

## Summary
- realization 側に残る acp 系 import path の互換入口を扱う領域。oracle 側の acp builder 実装を複製せず、旧公開 import 経路から正本側実装へ接続する再公開・委譲の境界を示す。
- 主な対象は builder 領域の互換 package 群で、apply、indexing、review、session、tui などの builder 呼び出し入口へ進むための上位案内になる。quota probe については、正本側専用 builder が未整備な制約を補う暫定 adapter も含む。
- この領域の責務は acp builder 本体の仕様や生成処理ではなく、移行期間中に残る acp 系公開参照、旧 import 経路、oracle 側実装との対応、互換層の削除条件を見分けることにある。

## Read this when
- acp 系 import を oracle 側または実体 module 側へ移行する作業で、互換入口を残す理由や削除条件を確認したいとき。
- realization 側や利用者向け公開面に残る acp 系参照が、oracle 側 builder 実装へどう接続されているかを確認したいとき。
- apply、indexing、review、session、tui などの builder 領域について、実処理ではなく互換入口、再公開層、委譲境界を探したいとき。
- quota probe 用 AgentCallParameter の暫定 adapter が、runtime 側 prompt literal を避けるためにどの互換領域で扱われているかを確認したいとき。
- builder 領域の下位構造を見て、apply fork、review oracle、session join、TUI 起動、indexing 互換公開面のどこへ進むべきか切り分けたいとき。

## Do not read this when
- acp builder の正本仕様、prompt、出力条件、具体的な AgentCallParameter 組み立てロジックを確認したいとき。対応する oracle 側実装または正本仕様断片へ進む。
- apply fork、review、session join、TUI、indexing の実処理、制御フロー、データ構造、判定ロジックを調べたいとき。それぞれの処理本体へ進む。
- AgentCallParameter、FileAccessMode、model、reasoning、structured output schema などの共通型や基礎定義を調べたいとき。型定義を持つ基本モジュールへ進む。
- 新しい acp 機能や builder 機能の本体実装、API 仕様追加、仕様変更の根拠を探しているとき。互換入口ではなく正本側 builder または該当機能の実装領域を読む。
- CLI 表示、branch 操作、diff 生成、quota 待機状態機械、TUI 画面処理など、builder 呼び出し準備より外側のワークフローを調べたいとき。該当する runtime や command 実装へ進む。
- acp 系参照が全公開面と realization 側から消えていることを確認済みで、互換入口の詳細や削除条件を読む必要がないとき。

## hash
- bc4b15b46140f9dfb0b5476761ef9339be056b9ef33da319e948c1a704e232de

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
- CLI サブコマンドの実装入口を集める領域であり、初期化、INDEX maintenance、対話起動、session lifecycle、apply run lifecycle、review oracle 実行など、利用者操作を runtime 上の処理へ接続する責務を持つ。
- 各実装は、CLI runtime への受け渡し、事前条件確認、git branch・worktree・state 操作、Codex subprocess 連携、結果出力や report 生成への導線を扱い、詳細処理は下位モジュールや共通 helper へ委譲する。
- サブコマンド単位で読む先を選ぶための入口であり、apply・session・review のような複数ファイルに分かれる領域では lifecycle 全体のどの段階を調べるべきかを切り分ける起点になる。

## Read this when
- CLI サブコマンドとして公開される処理の実行入口、runtime への渡し方、事前条件確認、利用者向け出力の実装箇所を探したいとき。
- 初期化、INDEX maintenance、対話起動、session 操作、apply run、review oracle のどの実装領域へ進むべきかを選びたいとき。
- branch、worktree、state、clean worktree 要求、ignore 保証、merge・cleanup・rollback、report 出力などがサブコマンド実行フロー上でどこから始まるかを確認したいとき。
- サブコマンド固有の orchestration と、共通 runtime・git wrapper・設定・path 解決・report rendering・対象列挙などの下位責務との境界を切り分けたいとき。

## Do not read this when
- CLI 共通 runtime、path model、git wrapper、設定読み込み、state schema、ignore 判定など、特定サブコマンドに閉じない共通処理の詳細だけを調べたいとき。
- 正本仕様断片としてサブコマンドの公開仕様や設計意図を確認したいとき。実装入口ではなく oracle 側を読むべき。
- 対象の下位処理がすでに分かっており、apply の実行時補助、review の対象列挙・loop・report・INDEX 反映、session の個別 lifecycle 処理などへ直接進めるとき。
- テスト、fixture、プロジェクト全体の CLI 登録、または INDEX.md 本文生成ロジックそのものを調べたいとき。

## hash
- 8b79fd34b3e6d57acb1cec7a0b15cdd7466e08516b245a9840e8f71cb8a82847
