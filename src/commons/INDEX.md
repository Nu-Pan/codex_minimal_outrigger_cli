# `__init__.py`

## Summary
- cmoc の実行時に複数箇所から共有される補助機能をまとめる領域の入口。
- 対象そのものは共有 runtime helper 群のパッケージ境界を示すだけで、個別 helper の責務は下位要素の本文で確認する。

## Read this when
- cmoc の実行時処理で、複数モジュールから使う共通 helper の配置場所や入口を確認したいとき。
- 共有 helper 群の下位要素へ進む前に、この領域が runtime helper 用のまとまりであることを確認したいとき。

## Do not read this when
- 特定の helper の実装、入出力、失敗時挙動を確認したいとき。この対象ではなく、該当する下位要素の本文を読む。
- CLI コマンド固有の処理やテスト固有の処理を調べたいとき。共有 runtime helper ではなく、より直接その責務を持つ対象へ進む。

## hash
- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary
- `commons.cmoc_runtime` が提供する公開名の集合を確認したいときに読む。複数の責務別 runtime module を束ね直した互換境界で、個別の実装ではなく「この名前が外へ公開されるか」を判断する入口である。
- このファイル自体は実装の中心ではないため、各関数やデータ型の挙動を追う目的では読まない。挙動の根拠は、そこから再公開されている各 `runtime_*` module を直接読む。

## Read this when
- `commons.cmoc_runtime` から import される名前や、後方互換の公開面を確認したい。
- 型検査や lint で、このモジュールがどのシンボルを外部契約として出しているかを見たい。

## Do not read this when
- 個別機能の実装や失敗時挙動を知りたい。そういう場合は対応する `runtime_cli`、`runtime_git`、`runtime_config`、`runtime_content`、`runtime_state`、`runtime_paths`、`runtime_logging`、`runtime_errors`、`runtime_doctor`、`runtime_codex_*` を直接読む。
- `cmoc_runtime` そのものの処理ロジックを探している。ここには再公開の配線しかない。

## hash
- d734a8cfaacbf2fd725ca4a6861ebd5283bd74f3f90a1a972f97b80a178dc7f7

# `indexing.py`

## Summary
- `cmoc` の indexing preflight と `INDEX.md` 更新の中核です。Codex 呼び出し前の登録、repository ロック、更新対象 directory の列挙、既存 entry の再利用、欠損 entry の生成、差分 commit までをまとめて扱います。
- `INDEX.md` の文字列形式や hash 検証、対象ファイルの採否ルール、Codex で 1 件分の entry を生成して整形する経路もここにあります。

## Read this when
- `cmoc indexing` の前処理や `INDEX.md` 自動更新の流れを変えたいとき。
- directory の列挙対象、symlink・`.gitignore`・memo 除外、既存 entry 再利用条件、hash 更新判定を確認したいとき。
- entry の Markdown 形式、Structured Output の検証、Codex への生成依頼方法を追いたいとき。
- indexing 更新をどの lock で直列化し、どの条件で commit するかを確認したいとき。

## Do not read this when
- `cmoc indexing` の CLI 引数や起動導線だけを見たいときは `sub_commands/indexing.py` 側を読む。
- `INDEX.md` 形式そのものの正本仕様だけを確認したいときは oracle 側を読む。
- Codex 実行基盤や一般的な preflight 全体の制御だけを追いたいときは `runtime_codex_preflight.py` 側を読む。

## hash
- d87f22d4c72132947055e6da5a7343184e15b951a6cfdbcec52f9362ce5300b3

# `runtime_apply.py`

## Summary
- apply 実行中の process と child process group を、pid file・start time・process group ID を使って同一性確認しながら停止、追跡解除、清掃する共通基盤。apply の破棄や停止で実行中 process を直接扱う必要があるときに読む。
- apply run の lock、pid file の保存・読取・削除、Codex subprocess 追跡の有効化と復元、stale な process 情報の判定をまとめて扱う。branch や worktree の選択、session state の更新だけを見たい場合は別の層を読む。

## Read this when
- `cmoc apply abandon` などで、実行中の apply process を安全に止める経路を変えたいとき。
- pid file と実 process の同一性確認、start time の扱い、Codex child group の停止条件を確認したいとき。
- apply 実行中だけ有効にする追跡情報の公開・復元・削除の順序を確認したいとき。
- stale な apply process 情報を無視する条件や、cleanup 競合を避けるための直列化を確認したいとき。

## Do not read this when
- apply の引数、状態遷移、report 文言、branch や worktree の削除条件だけを見たいとき。この対象ではなく apply サブコマンド本体を読む。
- session state の保存形式や branch 解決だけを追いたいとき。process 停止よりも状態管理側の責務を持つ対象を先に読む。
- 一般的な process 制御や git worktree 一覧取得だけが目的のとき。この対象は apply 停止と追跡に責務が限られる。

## hash
- 47e70c8b3b1671ada93553b3231bbae38f8f14329c3ac9a2eccaf65431dd509a

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行をまとめる。work root 前提の検査、事前処理、step 通知、完了サマリー、戻り値の終了コード化、例外時のエラー表示を一つの経路で扱う。
- サブコマンド単位の stdout 契約を持つ結果型と、実行中の step 数を共有する補助を置く。

## Read this when
- CLI サブコマンドの起動・終了・失敗時の扱いを変えたいとき。
- step 開始通知や完了サマリーの出し方を変えたいとき。
- work root 前提の検査や、runtime state を repo root と work root のどちらに置くかを判断したいとき。
- サブコマンドの戻り値を終了コードや標準出力にどう反映するかを確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジックだけを変更するとき。
- サブコマンド logger の保存形式やエラー整形の詳細だけを確認したいときは、より下位の logging / errors / paths 側を読む。
- doctor preprocess 自体の中身だけを追いたいときは、実行側ではなく doctor 側の文書や実装を読む。

## hash
- 256fd6112f362a6036e13f5ee7d0c78927df7bd1b13d3cb04924fa612ac6d8e4

# `runtime_codex.py`

## Summary
- Codex 実行系の公開入口をまとめる薄い再エクスポートモジュール。exec 実行と TUI 実行の起動関数を同じ import 元から参照できるようにする。

## Read this when
- Codex 実行ランタイムの利用側で、exec 実行または TUI 実行の起動関数をどこから import するか確認したいとき。
- 実行方式ごとの実装詳細ではなく、runtime_codex 系の公開 API 境界だけを確認したいとき。

## Do not read this when
- exec 実行の具体的な処理、引数処理、プロセス制御を確認したいときは、exec 実行側の実装を直接読む。
- TUI 実行の具体的な処理、端末制御、対話実行の挙動を確認したいときは、TUI 実行側の実装を直接読む。
- 新しい実行ロジックや分岐を追加する場所を探しているときは、この再エクスポートではなく各実行方式の実装へ進む。

## hash
- bce418fcd1f6bffaed81f3724333817408657aed46183fa20819ffc1b40a7993

# `runtime_codex_exec.py`

## Summary
- Codex exec の単発実行制御を担う中核。Structured Output 検証、capacity / quota の再試行、resume 継続、実行ログとイベント記録を一体で扱うため、exec の失敗処理や待機制御を読むときに起点にする。
- TUI 起動や subcommand 全体の配線ではなく、`codex exec` の呼び出し・再試行・結果収集の挙動を確認したいときに読む。ログ命名、quota 待機の代表 probe、schema 付き出力の扱いまで含めて追う必要がある場合もここから入る。

## Read this when
- `codex exec` の呼び出し条件、引数構築、stdin prompt の保存、出力 JSON の検証、再試行条件を確認したいとき。
- capacity エラーや quota 枯渇時の待機・probe・resume の流れを追いたいとき。
- call log / stdout / stderr / output の保存先や、subcommand event に何が記録されるかを確認したいとき。
- 実行中の Codex 呼び出しが失敗したときの例外変換や診断情報の出し方を確認したいとき。

## Do not read this when
- TUI の起動や表示を直したいときは、TUI 側の module を読む。
- git 差分の収集や worktree 変更 path の取得だけを確認したいときは、git / path 取得系の module を読む。
- `codex exec` の内部状態機械ではなく、CLI 全体の入口やコマンド配線を追いたいだけのときは、より上位の subcommand 実装を読む。

## hash
- e728c903ba7f0f64b9037557551b5967967935a01b3aef77893f29b4b7c3f3d4

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出し時の console 通知と、その失敗理由を console/event で共通化する error text 変換を扱う。

## Read this when
- Codex 呼び出しの開始通知、経過時間、終了コード、起動失敗メッセージの表示を変えたいときに読む。
- Codex 固有の失敗情報を、人間向け console 表示とイベント記録で同じ文面に揃えたいときに読む。

## Do not read this when
- 一般的なログ出力の整形や保存先を変えたいだけなら、汎用の runtime logging 側を読む。
- `codex exec` の引数構成、プロンプト生成、実行制御を変えたいだけなら、呼び出し本体の実装を読む。

## hash
- 6ca8648503df249ad1c39cf3d01e3c95496fd6762ca7d903a9caaa7b39b6f9d6

# `runtime_codex_preflight.py`

## Summary
- Codex 実行・TUI 実行の直前に indexing preflight を差し込むための実行ラッパーと、その登録・無効化・再入防止を扱う。既存の Codex 呼び出し経路に preflight を挟みたいときに読む。
- preflight をどの root で走らせるかの決定規則も含む。`cwd` / `root` / `parameter.cwd` のどれを起点にするか、work tree 内外の扱いを変えたいときに読む。

## Read this when
- Codex exec/TUI の前処理として indexing を実行したい、またはその有効・無効を切り替えたいとき。
- preflight の登録先を確認したい、あるいはテストや限定実行で preflight を外したいとき。
- preflight の起点 root の選択や、再入を抑えた直列実行の挙動を変えたいとき。

## Do not read this when
- indexing preflight の中身そのものを変更したいときは、`commons.indexing` 側を読む。
- AgentCallParameter の項目定義や `run_indexing_preflight` の意味だけを確認したいときは、`basic.acp` 側の定義を読む。
- Codex 実行本体や TUI 本体の詳細を知りたいときは、`commons.runtime_codex` を読む。

## hash
- 5bcc7833c65502e04727671312ba51a98009381970887b11934a0a20f9af3713

# `runtime_codex_profile.py`

## Summary
- Codex CLI 起動前後の実行環境、権限上書き、`CODEX_HOME`、子プロセス追跡、schema 配置、JSONL エラー判定をまとめて扱う。Codex の呼び出し条件や失敗時解釈を決めるときに読む。

## Read this when
- Codex subprocess に渡す argv・sandbox/permission profile・read/write 制約の組み立てを変更したいとき。
- `CODEX_HOME` の解決や検証、Codex CLI 不在時の扱いを確認したいとき。
- apply/abandon 系の child process tracking、process group 停止、resume token、capacity/quota/error 判定を変更したいとき。
- Structured Output schema の配置や Codex 出力 JSON の読解方法を変更したいとき。

## Do not read this when
- Codex 呼び出し以外の一般的な runtime path / git 判定 / file access rule だけを変えたいときは、より直接の実装を読む。
- 単なる CLI 引数パースやサブコマンド定義の入口を探しているだけなら、この境界ではなくコマンド層を読む。
- oracle 側の正本仕様そのものを確認したいときは、この実装ではなく `{{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py` を読む。

## hash
- 5a40a31ebd4779c1ec28344612afc9c63b5f91776ebf7334c2aad5596acbade4

# `runtime_codex_tui.py`

## Summary
- `cmoc tui` から Codex CLI/TUI を起動する入口。実行用 `cwd` と work root の解決、`CODEX_HOME` の検証、設定上書き argv の組み立て、呼び出し情報の保存、成功・失敗時の console/logger への通知を扱う。
- Codex の起動方法そのものを変えたいとき、または TUI 起動で保存される call log とエラー処理の境界を確認したいときに読む。

## Read this when
- Codex TUI の起動コマンド、`--cd` や prompt の渡し方、call log の内容、起動失敗時の例外変換を確認・変更したい。
- `CODEX_HOME` の解決と preflight、設定上書き argv、`codex_call` イベント出力の関係を追いたい。

## Do not read this when
- Codex exec の一般的な subprocess 境界や JSONL 出力仕様を見たいだけなら、起動形式の違う Codex 実行側のファイルを読む。
- コンソール表示の書式だけを直したいなら、起動ロジックではなくログ出力専用のファイルを先に読む。

## hash
- dfa24892ebf53b0a2d100c4b79349206d121207078ef1dc5752669a4a5a9a7a2

# `runtime_config.py`

## Summary
- `cmoc` の設定 JSON を `CmocConfig` と相互変換し、既定値補完・検証・保存・同期まで扱う入口。設定ファイルの読み書き、欠損項目の復元、形式不正時の利用者向け例外を確認したいときに読む。

## Read this when
- `config.json` の読み込み、書き戻し、初回生成、同期のいずれかを変えたいとき。
- 設定値の JSON 表現と runtime の型表現の対応、既定値補完、入力検証の境界を確認したいとき。
- 設定不正時に `CmocError` へ変換される条件や、利用者へ出すメッセージを調整したいとき。

## Do not read this when
- `config.json` の保存先そのものだけを知りたいときは `runtime_paths` を直接読む。
- 設定型の定義や項目そのものを変えたいときは `config.cmoc_config` 側を読む。
- 設定を使う各サブコマンドの振る舞いを追いたいときは、`tui`、`apply/fork`、`review/oracle`、`runtime_doctor` などの呼び出し元を読む。

## hash
- 14db36478944f71011c1654ad666f4e63610b6219e41f56788070e17b826d13b

# `runtime_content.py`

## Summary
- ファイル内容または文字列内容から SHA-256 digest を計算し、digest をファイル名に含めた内容アドレス型ファイルを書き出す小さな runtime content helper 群。
- 出力先 directory の作成有無が異なる 2 種類の書き出し関数と、先頭 chunk の NUL byte と読み取り可否による簡易 binary 判定を扱う。

## Read this when
- 内容 hash を使った成果物ファイル名の生成、重複書き込み回避、または内容アドレス型の一時・補助ファイル保存を確認・変更するとき。
- ファイル内容や文字列内容の SHA-256 digest 計算処理を使う箇所を探すとき。
- テキスト対象と binary 対象を粗く分けるための簡易判定ロジックを確認・変更するとき。

## Do not read this when
- path model、run/work/root の意味、またはパス表記そのものの仕様を確認したいとき。
- CLI 引数、サブコマンド、標準出力、終了コードなど利用者向けの公開面を確認したいとき。
- hash 値を使わない通常のファイル読み書き、設定読み込み、永続状態管理の実装を探しているとき。

## hash
- d121b59cd941f68e101d0bf9b1eb0f0fdd2fe8c928d89dd6447b3079581fb905

# `runtime_doctor.py`

## Summary
- doctor preprocess の共通修復本体を担う。current worktree と main worktree をまとめてロックし、`.gitignore`・`.agents/.gitkeep`・worktree config の修復を一時 index で合成して commit し、元の index を復元する処理を実装している。
- Git common directory 単位の doctor lock、HEAD 起点の一時 index、現在 index の退避と復元、`git` 実行ラッパ、blob/mode を保った stage など、doctor preprocess 固有の Git 操作がまとまっている。
- `.cmoc/gu` の追跡解除、`.agents` の追跡保証、同期済み config の追跡保証、managed ollama の可用性確認を一つの流れとして扱うための入口である。

## Read this when
- doctor preprocess の実行順、修復対象、commit される差分の範囲を変えたいとき。
- doctor 実行時の並行制御、worktree 間での修復合成、index 復元、エラー時の Git 挙動を確認したいとき。
- `.agents` や worktree config の追跡保証、`.cmoc/gu` の ignore 追加と追跡解除の扱いを調べたいとき。

## Do not read this when
- 個別の Git 共通操作や path 解決だけを見たいときは、`runtime_git` や `runtime_paths` を先に読む。
- config 同期の詳細だけを見たいときは `runtime_config` を読む。
- managed ollama の起動・可用性確認だけを見たいときは `runtime_ollama` を読む。

## hash
- 260121e3ae5d397c799008a9aa9d44e8af6c186600f407c17321eebe7825c4e0

# `runtime_errors.py`

## Summary
- cmoc の実行時例外を利用者向け Markdown エラーレポートへ整形する責務を持つ。例外種別ごとの表示差と、既定の復旧案補完をまとめて確認したいときに読む。

## Read this when
- 利用者向けのエラーレポートの見出し、Summary、Next actions、Detail、Call stack の出し方を変えるとき。
- cmoc 固有の例外に、復旧案や詳細情報をどう保持させるかを確認したいとき。
- 例外から出力文字列を作る共通処理を他の実行経路から使いたい、またはその出力内容を変更したいとき。

## Do not read this when
- 例外の発生箇所そのものや、個別機能の失敗原因を探したいだけのときは、呼び出し元や各機能の実装を先に読む。
- Markdown 以外の出力形式や、通常の成功出力の整形を変えたいだけのときは読まない。

## hash
- 152fcb4b8030f5fb2be82569787d2862effba44076d46afbc39bdb088b736e9a

# `runtime_git.py`

## Summary
- Git の実行境界、branch/worktree の作成・削除、`.cmoc/gu` の ignore 制御、`git status` の path 分類、oracle file 判定をまとめて扱う。sub-command や runtime 実装から Git まわりの共通処理を追うときに読む。

## Read this when
- Git subprocess の失敗を利用者向けエラーへ変換する共通処理を確認したいとき。
- managed branch や linked worktree の作成・削除・存在確認、または clean worktree 前提の判定を追いたいとき。
- `.cmoc/gu` を追跡対象外にする処理や、その ignore 状態の検査を追いたいとき。
- `git status` の結果から path を分類する処理、または tracked / ignored を踏まえた oracle file 判定を確認したいとき。

## Do not read this when
- 単なる repository root や worktree root の解決だけを追いたいときは、path 変換側を先に読む。
- session state や run state の保存・読出しだけを追いたいときは、Git 共通処理ではなく state 側を読む。
- CLI の引数解釈や sub-command の入出力の流れだけを追いたいときは、各 sub-command の実装を直接読む。

## hash
- a0090ae952b5554b67e283d37a7d7c9bd84108a66d479c419f8a998b580abb2c

# `runtime_logging.py`

## Summary
- サブコマンド実行中の JSON Lines ログ記録、step timing の計測、quota 待機時間の集計、現在の logger を深い呼び出し先へ受け渡す処理を扱う。実行時イベントの記録形式や完了サマリーに出る計測値を変えるときに読む。

## Read this when
- サブコマンドごとの log file を新しく作る・追記する・イベント種別を増やす・step 開始/終了の計測を変える・待機時間の集計方法を確認する必要がある。
- contextvar で現在の logger を参照する経路や、深い runtime helper から logger を使えるようにする責務を確認したい。

## Do not read this when
- path 予約や logs ディレクトリの一般的な扱いだけを確認したいなら、`runtime_paths` 側を読む。
- ログ内容そのものではなく、上位コマンドの制御フローや引数解釈だけを見たいなら、この対象ではなくコマンド層を読む。

## hash
- 01fababfe41483ba8194c1aec614beda27fe55ad5010a54e0b61e8a190f71a09

# `runtime_ollama.py`

## Summary
- `cmoc managed Ollama` の起動・修復・検証を 1 本の preflight として扱う実装の入口。archive の取得と展開、user systemd の同期、`127.0.0.1:11434` の所有者確認、モデル pull/load、GPU 推論確認までを順序つきでまとめているため、この一連の流れを追うときに読む。

## Read this when
- `ensure_ollama_serves_local_slm` の全体フロー、失敗時の停止条件、または `cmoc provider` のモデル利用可能性保証の挙動を確認したいとき。
- ollama の配置先、service file、lock、procfs ベースの検証、`/api/generate` と `/api/ps` を使う判定のつながりを知りたいとき。
- 管理対象 model の選定と、service 起動後にどの順で model を取得・load・GPU 確認するかを把握したいとき。

## Do not read this when
- `cmoc` の設定読み込みや model spec の解釈だけを見たいときは、`runtime_config` 側を先に読む。
- 個別のエラー型や runtime path の定義だけを見たいときは、この file ではなく各補助 module を直接読む。
- Ollama の利用方針や 11434 固定の必要性だけを確認したいときは、実装よりも `{{work-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md` を先に読む。

## hash
- f864fab7e62dce81fe9ba2bfb1710ef42be556c4a5b9d9390f14f51953f5dd6f

# `runtime_paths.py`

## Summary
- cmoc 実行時の root 解決と関連する runtime path 生成をまとめた基盤。repository root / worktree root / cmoc root の解決、cwd を一時切替して外部解決 API を使うための保護、timestamp や duration の表示整形、`.cmoc` 配下の各種 runtime directory の組み立てを扱う。

## Read this when
- root 解決の失敗を runtime error に変換する流れを確認したいとき
- `.cmoc` 配下の session / report / log / schema / config の保存先を決める処理を追いたいとき
- cwd 前提の外部 API を process-wide に直列化して使う必要があるとき
- timestamp 表示や duration 表示の共通ルールを確認したいとき

## Do not read this when
- 個別の path placeholder の実体変換だけを追うなら `basic.path_model` 側を直接読む
- cmoc の各機能ごとの保存内容や利用タイミングを知りたいなら、各サブシステムの実装を読む
- エラーメッセージ文言の全体像や CLI の振る舞いを知りたいだけなら、呼び出し元のコマンド処理を読む

## hash
- c238d9bab51ff7e5482f5521f8e16824df565c5437077d44667b12e34ddec88f

# `runtime_preprocess_command.py`

## Summary
- `cmoc` の preprocess 系サブコマンド実行をまとめる薄いラッパー。コマンド開始時の共通処理と、事前診断(preprocess)の呼び出し、最後の最小出力をつなぐ役割が中心で、個別サブコマンド本体よりも起動経路の整理を読むときに参照する。

## Read this when
- `cmoc` の各サブコマンドを実行前に共通の前処理へ通す流れを確認したいとき。
- コマンド実行時に work root や repo root をどう取得し、どのタイミングで診断処理を走らせるかを見たいとき。
- サブコマンド開始ステップの表示と、その後の最小限のヘッダ出力の責務を確認したいとき。

## Do not read this when
- 事前診断(preprocess)そのものの内容や判定基準を知りたいときは、直接その診断実装側を読む。
- CLI の引数定義やサブコマンド列挙を追いたいときは、個別コマンド定義側を読む。
- 共通のパス解決や CLI 実行基盤の詳細を知りたいときは、runtime_paths や runtime_cli 側を読む。

## hash
- c9a2178b1f21f1239059f2b05992c5ba13756483053e288203185c99e9d55320

# `runtime_results.py`

## Summary
- `Codex` 呼び出し結果や外部コマンド結果を、型付きの最小インターフェースとして扱いたいときに読む。実行結果の構造を共通化するだけで、実行処理や保存処理の流れはここでは扱わない。

## Read this when
- `CodexExecResult` や `CommandResult` のような結果オブジェクトの形を確認したいとき。
- テストや注入先から参照する、コマンド実行結果の共通プロトコルを確認したいとき。
- 実行後に残るログや出力パスをどの属性で受け渡すかを知りたいとき。

## Do not read this when
- コマンド実行そのもの、ログの書き込み、CLI 制御の流れを追いたいときは、実行や永続化を担当する別の実装を読む。
- 出力 JSON の生成規則やスキーマ定義を知りたいときは、結果コンテナではなく生成側の実装を読む。
- 単なる subprocess 呼び出しや `dataclass` の一般的な使い方を確認したいだけなら、この対象は不要。

## hash
- 6946c4bfa9df5459a6e648ea3d37fa1b1ad8def2316ecb699d8196db762d81bb

# `runtime_state.py`

## Summary
- cmoc の session/apply state file を読み書きし、branch 名から session_id を取り出す共通基盤。state の JSON 検証、保存形式、fork 時の排他 lock、home branch に紐づく active session の探索を扱う。

## Read this when
- session state file の保存形式や検証条件を変えるとき
- session/apply branch から session_id を解決する挙動を確認したいとき
- session fork の排他制御や active session 探索の責務を確認したいとき
- state file の読み込み・書き戻し・エラー文言の共通化先を探しているとき

## Do not read this when
- 個別サブコマンドの実行手順や stdout 形式だけを変えるときは、各 sub_command の本文を先に読む
- session state の永続化を伴わない一時的な UI 変更だけならここは読まない
- git 操作や branch 作成の詳細実装だけを追いたいなら、branch/state 連携を扱う別の実装を読む

## hash
- 0dd8e9d30a216467abff8714452d83ecc78ceb9824fe48186bb818f0e5089aaa
