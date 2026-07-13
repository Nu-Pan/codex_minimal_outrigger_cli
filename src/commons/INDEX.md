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
- `cmoc` 全体で共通に使う実行・設定・状態・git・パス・ログまわりの基盤をまとめて再公開する集約点。個別の実装ではなく、この層で何が共通入口として扱われるかを確認したいときに読む。

## Read this when
- 共通 runtime の入口がどこにあるかを把握したいとき。
- コマンド実行、preflight、設定の読み書き、状態の保存、git/worktree 管理、ログ/レポート/セッション/スキーマ保存先の扱いをまたぐ変更をするとき。
- 複数の下位モジュールに分散している基盤処理を、どの共通 API として使うべきか判断したいとき。

## Do not read this when
- 特定の helper の内部アルゴリズムや例外処理だけを見たいときは、まずその helper の実装側を読む。
- 個別サブコマンドの振る舞い、CLI 画面、ドメイン固有の処理を確認したいときは、対応する上位モジュールを読む。
- 単にパス生成、git 判定、設定変換、状態永続化の細部だけが必要なときは、この集約点ではなく該当する下位実装を直接読む。

## hash
- 6e149683c5808b3b814137b4009f79ee5520a0442ef2b9f8c50f88a6f9025f9e

# `indexing.py`

## Summary
- Codex 呼び出し前の indexing preflight を登録・実行し、排他制御下で各階層の INDEX.md を再生成して必要な更新 commit を作る実装を扱う。
- indexable な directory・child の列挙、既存 entry の hash 検証と再利用、Codex による不足 entry 生成、Structured Output からの entry Markdown 描画までを担う。

## Read this when
- INDEX.md の自動更新、鮮度判定、hash 形式、entry の再生成条件、または indexing commit の作成挙動を変更したいとき。
- indexing 対象から除外する file・directory、binary・symlink・memo・git ignored の扱い、または directory traversal の条件を確認したいとき。
- Codex に INDEX.md entry 生成を依頼する入力内容、実行時の root・cwd・config・purpose、または生成結果の検証エラーを調べたいとき。
- 既存 INDEX.md entry の parse、必須 section 構造、bullet-only 制約、hash 抽出条件に関する不具合を調査するとき。

## Do not read this when
- INDEX.md entry の自然言語生成プロンプトや Structured Output schema の正本側定義だけを確認したいときは、oracle 側の prompt builder や indexing 仕様を直接読む。
- 通常の CLI コマンド引数、設定ファイル全体、または Codex 実行基盤そのものを調べたいだけなら、それぞれの担当 module を読む。
- 個別の INDEX.md 文面を人間がどう書くべきかの方針を確認したいだけなら、この実装ではなく indexing 標準や entry standard の正本仕様を読む。

## hash
- dacc5d7428ac22757c3c87ba8deac1328124e8779fa43df5a9b81834e19665a1

# `runtime_apply.py`

## Summary
- apply 実行に対応する worktree と apply process 追跡状態を扱う runtime 補助コード。session branch から linked worktree を探す処理、apply branch 名から managed worktree path を復元する処理、apply process の pid file 読み書き、Codex subprocess group を含む停止処理をまとめる。

## Read this when
- apply 実行中 process の記録、追跡、削除、停止、または abandon 時の停止安全性を確認・変更したいとき。
- session branch や apply branch から worktree path を特定する runtime 処理を確認・変更したいとき。
- pid 再利用、pidfd、process start time、process group、zombie child を考慮した process 停止ロジックを確認したいとき。

## Do not read this when
- apply の CLI 引数、出力文言、状態遷移そのものを確認したいだけなら、subcommand 側または対応する app spec を先に読む。
- 汎用的な git 実行、worktree 置き場、process start time 取得、pid file lock の実装を確認したい場合は、それらを定義する runtime 基盤へ進む。
- apply と無関係な session 管理、prompt 構築、通常のファイル操作を調べる場合は読まなくてよい。

## hash
- d140e6a14473bec52d65e02ccd6c504f7a14b08e0b263dd943a21dcdf9b007b8

# `runtime_cli.py`

## Summary
- CLI サブコマンド共通の実行ライフサイクルをまとめる。work root 検査、doctor preprocess の呼び出し、サブコマンドログの初期化、step 通知、完了サマリー、例外時の終了コード化と stderr/stdout の振り分けを一箇所で扱う。
- 個別サブコマンドの業務処理ではなく、サブコマンド共通の実行順序や失敗時の見せ方を変えるときに読む。

## Read this when
- 新しいサブコマンドをこの共通実行経路に載せるとき。
- work root での実行制約や、runtime state を repo root に置くか work root に置くかの判断を変えるとき。
- doctor preprocess を挟む位置、step 開始通知、完了サマリー、returncode の扱いを調整するとき。
- 例外を標準出力と標準エラーのどちらに出すか、または `CliRunResult` の stdout 契約を変えるとき。

## Do not read this when
- 各サブコマンド固有のビジネスロジックだけを変更するとき。
- サブコマンドログの保存形式や詳細イベント仕様だけを変えたいときは、ログ実装側を読む。
- doctor preprocess の修復内容そのものを変えたいときは、doctor preprocess 側を読む。
- エラー文言の生成ルールだけを変えたいときは、エラー整形側を読む。

## hash
- b09cd25b8c1c7599ad0d0e6df775f89211c03a86f79447f78391cf884d7a2b88

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
- Codex exec の単一試行ループを扱う実行制御モジュール。Structured Output 検証、capacity retry、quota 待機と代表 probe、resume 継続、実行ログ記録を一体で管理する。
- TUI 起動や別サブコマンドの分岐はここに置かず、`codex exec` の呼び出し条件、再試行条件、出力検証、イベント記録の境界を読むときに進む。
- worktree 変更 path の収集も含むが、責務の中心は実行制御であり、一般的な path 操作や他のサブコマンド制御だけなら別モジュールを優先する。

## Read this when
- `codex exec` の再試行条件、Structured Output の扱い、quota/capacity エラー時の振る舞い、resume token の扱いを確認したいとき。
- 実行時にどのログが残り、call log や subcommand event に何を記録するかを確認したいとき。
- quota 待機中の代表 probe の開始・継続・失敗・復帰の境界を確認したいとき。

## Do not read this when
- TUI の起動や画面制御を追いたいとき。
- 一般的な設定読み込み、git 状態収集、runtime path 群の実装だけを確認したいとき。
- `codex exec` 以外のサブコマンド分岐や、個別の prompt 生成ロジックだけを確認したいとき。

## hash
- 479cff8f427fb7710703d0a9c3f3c60b4eaf4e124468fe5facf92784782d97cc

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しに関する console 出力と、起動失敗時の error 文面を共通化する補助をまとめた対象。呼び出し通知の表示形式を確認したいときや、失敗理由の整形を他の出力経路と揃えたいときの入口になる。
- console に出す時刻・経過時間・終了コードの組み立てを見たい場合と、`CmocError` を含む例外を利用者向けの短い error text に直したい場合に読む。

## Read this when
- Codex CLI 呼び出しの通知を console に出す処理を追加・修正したい。
- 起動失敗や例外の文面を、console 出力と event で同じ表現に揃えたい。
- 経過時間や時刻表示を含む呼び出しログの見え方を確認したい。

## Do not read this when
- 呼び出しの記録先そのものや永続化の責務を変えたいときは、保存・記録側の対象を先に読む。
- Codex 以外の CLI 表示や一般的な runtime エラー処理を変えたいだけなら、より上位の入出力処理を読む。
- `console_timestamp` や `format_duration` の表示仕様だけを追いたいときは、それらを定義している対象を直接読む。

## hash
- 3aa2c9b4388542920c4557bddf5901e75f441a15c053f019c7c9b9f20c90267d

# `runtime_codex_preflight.py`

## Summary
- Codex exec/TUI 実行の直前に登録済みの INDEX 更新 preflight を挟むための薄い委譲層。preflight の登録・解除、実行起点 root の決定、再入抑止と直列化を扱い、実際の Codex 実行は runtime 側へ渡す。

## Read this when
- Codex exec/TUI 呼び出し前に indexing preflight が実行される条件や順序を確認したいとき。
- run_indexing_preflight、cwd、root、parameter.cwd から preflight の起点 root がどう決まるかを調べたいとき。
- indexing preflight の登録解除、再入防止、ロックによる直列実行の挙動を変更したいとき。

## Do not read this when
- Codex exec/TUI の実行本体、サブプロセス実行、戻り値の組み立てを調べたいときは runtime 実行側を読む。
- repo root や work root の判定規則そのものを調べたいときは path 解決を担う runtime path 側を読む。
- AgentCallParameter の項目定義や run_indexing_preflight の意味を確認したいときは basic 側の parameter 定義を読む。

## hash
- 21640496726fe5b154993e3215648edd155e6984b8fcb368ada7a22845c04670

# `runtime_codex_profile.py`

## Summary
- Codex CLI へ渡す実行環境と、その返り値の解釈をまとめる境界層。`FileAccessMode` から sandbox/permission profile/書き込み許可/読み取り許可を組み立てる処理、`CODEX_HOME` の解決と検証、Codex subprocess の起動と child process 追跡、schema 配置、JSONL エラー判定を扱う。
- Codex 起動前後の制約が交差する変更ではここを読む。特に、argv と環境変数の組み立て、read/write 境界、runtime state と realization file の分離、quota/capacity/error の判定、tracked subprocess の扱いを変える作業はこのファイルが入口になる。
- 単純な上位コマンドの流れや個別サブコマンドの UI 仕様だけを追う作業ではここは不要で、より直接のサブコマンド実装や app spec を読む方が適切。

## Read this when
- Codex subprocess に渡す `argv`、`--sandbox`、permission profile、`CODEX_HOME`、または追加 read/write path の許可条件を変える。
- Codex 実行結果の JSONL から error / capacity / quota / resume token をどう判定するかを確認したい。
- apply 実行中の child process tracking、pid file のロック、tracked subprocess の記録・削除の挙動を変える。
- Structured Output schema の配置先や、schema 用の hashed file 生成に関わる処理を追う。

## Do not read this when
- 個別サブコマンドの利用者向け文言や操作手順だけを変更したい。
- Codex 以外の一般的な path 操作、git 判定、runtime path 解決だけを確認したい。
- この境界層を経由しない内部 helper の細部だけを修正したい場合は、該当 helper を直接読む方が速い。

## hash
- f96f5fdf207522952813d2061b2f03b1e5333b1fcd33d29f8b5fb07c2028abcb

# `runtime_codex_tui.py`

## Summary
- Codex TUI を起動する共通処理で、`AgentCallParameter` から呼び出し argv・`CODEX_HOME`・call log・サブコマンドログをまとめて準備し、実行結果を `CommandResult` か例外で返す。
- Codex の起動前後で記録内容や失敗時の扱いを揃えたいときに読む。特に、起動先の cwd 決定、`CODEX_HOME` の解決と検証、呼び出しログ出力、失敗イベント記録の責務を確認するときの入口になる。

## Read this when
- Codex TUI の起動方法や、起動時に残す call log とサブコマンドログの内容を変えたい。
- `CODEX_HOME` の解決・検証や、Codex 呼び出し前の argv 組み立てを見直したい。
- Codex 実行失敗時の例外変換や、起動失敗をイベントとして記録する経路を確認したい。

## Do not read this when
- Codex 以外の実行経路や、別サブコマンドの引数組み立てだけを見たい。
- 単に `CommandResult` の定義や一般的な設定読み込み処理だけを確認したい。
- call log の保存先だけを知りたい場合は、直接 `runtime_paths` 側を読む方が近い。

## hash
- 56354704e19d5e51bc279f550754fc1a964cd8fe3e3a1d66fa012c93f2a9af97

# `runtime_config.py`

## Summary
- cmoc の設定を正本 config 型と永続化 JSON の間で変換し、設定ファイルの読み込み、検証、既定値補完、書き戻しを担う。
- 利用者が編集する config JSON の型不正や構文不正を、利用者向けの CmocError 境界へ変換する。

## Read this when
- 設定ファイルの保存形式、既定値補完、読み込み時の検証、または sync 時の生成・正規化挙動を確認・変更したいとき。
- config の enum key map、Codex model spec、int 値、optional section の JSON 復元ルールを調べたいとき。
- 設定ファイル不在、JSON 構文不正、top-level 不正、値型不正に対する利用者向けエラーを確認したいとき。

## Do not read this when
- config 型そのものの項目定義や既定値を確認したいだけなら、config 定義側を読む。
- Codex model 名や reasoning effort 名の正本定義を確認したいだけなら、oracle 側の model config 定義を読む。
- 設定ファイルのパス解決だけを確認したいなら、runtime path 側を読む。

## hash
- 1120d55ea7a5a55ce14b73f76f472319f67fe3da04ee9717c70ebf73e14deeda

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
- `src/commons/runtime_doctor.py` は、`doctor preprocess` の共通修復処理をまとめる入口。`<work-root>` と main worktree の両方に対して、`.cmoc/local` の追跡除外、`.agents` の追跡固定、cmoc managed ollama の可用性確認を行い、修復差分を commit して元の index を復元する責務を持つ。
- この対象では、Git common directory 単位の排他ロック、HEAD 起点の一時 index を使った修復 commit、現在 index の退避と復元、`.gitignore` と `.agents/.gitkeep` の修復合成までを扱う。

## Read this when
- `doctor preprocess` の実行順、排他条件、修復対象、commit までの流れを確認・変更したいとき。
- `.cmoc/local` を追跡対象外に保つ条件と、既存 tracked file の扱いを確認したいとき。
- `.agents` を追跡対象として固定する条件、placeholder の追加条件、失敗時の扱いを確認したいとき。
- linked worktree で main worktree 側も含めて修復する理由や、共有 index を壊さないための復元方法を確認したいとき。
- doctor 用の process lock や、修復だけを別 index で commit する実装境界を確認したいとき。

## Do not read this when
- `doctor preprocess` の個別仕様そのものではなく、特定サブコマンド固有の前提条件を知りたいときは、そのサブコマンド側を読む。
- Git の一般的な操作方法や、共通 runtime の他の責務だけを確認したいとき。
- cmoc managed ollama の取得・配置・起動の詳細だけを確認したいときは、そちらの正本仕様断片を読む。

## hash
- f052fc72e4e25abf1737ef356b05346752771460d6e0d6532c6bec01be54e2cc

# `runtime_errors.py`

## Summary
- cmoc の実行時例外と、任意の例外を利用者向け Markdown エラーレポートへ変換する共通処理を定義する。エラー概要、復旧案、詳細、呼び出しスタックを一貫した形式で出力するための入口となる。

## Read this when
- 利用者に表示する cmoc 共通エラーレポートの構成や文面を確認・変更したいとき。
- 実装内で発生させる利用者向け例外に、概要・復旧案・詳細を持たせる方法を確認したいとき。
- 例外ごとの復旧案が少ない場合に既定の Next actions がどう補われるかを確認したいとき。

## Do not read this when
- 個別コマンド固有のエラー判定条件や入力検証ロジックを調べたいとき。
- エラーレポートを出力する CLI エントリーポイント側の制御を調べたいとき。
- Markdown エラーレポート以外の通常出力や成功時出力の形式を調べたいとき。

## hash
- 51eb58dfc241cb76b6debfce4a06a3169cb6a2a29d0a6f123f7c5b6c0bd03e95

# `runtime_git.py`

## Summary
- Git まわりの共通境界をまとめた実行時ヘルパー群です。branch 判定、worktree の作成・削除、状態取得、`.cmoc/local` の ignore 制御、oracle file 判定を扱います。
- `git` 呼び出しの失敗を利用者向けエラーへ揃える境界や、cmoc 管理領域の worktree・ignore 判定を確認したいときに読む対象です。

## Read this when
- `git` subprocess の失敗処理や、branch / HEAD / status の取得方法を確認したい。
- cmoc が管理する worktree の作成・削除条件や、管理外 worktree を拒否する制約を確認したい。
- `.cmoc/local` を tracked にしないための ignore 追加・検査・修復ロジックを確認したい。
- oracle file かどうかの判定基準を確認したい。

## Do not read this when
- session / apply / review のコマンド全体の制御フローを追いたいときは、各 `sub_commands` 側を読む。
- git 以外の入出力変換やレポート生成を追いたいときは、このファイルではなく該当機能の実装を読む。
- 既に `git` 呼び出し境界や ignore 判定の詳細を知っていて、上位コマンドの振る舞いだけを追いたいときは、より上位のモジュールを先に読む。

## hash
- ec4a87a8ad077112339331808411cd7608e7aea9599f594b7dbcdcc39132f493

# `runtime_logging.py`

## Summary
- サブコマンドごとの JSON Lines ログと経過時間をまとめる共有 logger を定義する。`ContextVar` で現在の logger を深い runtime helper から参照できるようにし、step timing と quota 待機時間も保持する。
- コンソール出力やファイル出力の連携で、イベント記録の単位、step 開始・終了の扱い、現在 logger の受け渡し方法を変えるときの入口になる。

## Read this when
- サブコマンド実行中に残すイベント記録の追加・変更をするとき。
- step の開始時刻、経過時間、quota 待機時間など、サブコマンド全体の実測値の集計方法を変えるとき。
- 深い runtime helper から現在のサブコマンド logger を参照・差し替え・復元する流れを確認したいとき。

## Do not read this when
- 個別サブコマンドの実処理や引数処理だけを変えるときで、共有 logger の記録方式に触れない場合。
- Codex CLI 呼び出しの詳細な記録形式だけを扱いたい場合は、`runtime_codex_logging.py` を先に読む。
- タイムスタンプ付き path の予約やログ保存先の決定だけを確認したい場合は、`runtime_paths.py` を先に読む。

## hash
- f4eb36e9d2b4bb2881b61820de8725a8b750ddb8c0118b57ba999d1bf7d9e241

# `runtime_ollama.py`

## Summary
- cmoc が管理する Ollama の導入、systemd user service の同期、`127.0.0.1:11434` での提供確認、モデルの取得・load・GPU 推論確認を一連で担う単一 preflight の入口。
- config から cmoc provider の model 名を集め、重複排除したうえで必要な model だけを対象にする。
- 実処理は install/service/procfs/HTTP/model 検証に分かれるが、外部からは `ensure_ollama_serves_local_slm` を起点に読むべき対象。

## Read this when
- cmoc provider の local SLM を Ollama で serve 可能にする流れを追いたいとき。
- Ollama の archive install、user service 設定、`/proc` による listener と MainPID の突合、`/api/generate` による load、`/api/ps` による GPU 使用確認の境界を確認したいとき。
- どの model を対象にするかの決定と、失敗時にどの段階で止まるかを知りたいとき。

## Do not read this when
- Ollama の provider 選択や model 仕様そのものを確認したいときは、config 側や app_spec 側を先に読む。
- systemd や procfs、HTTP クライアントの一般的な使い方だけを知りたいときは、この対象よりも各責務の実装や標準ライブラリ側を読む。
- 単独の helper 再利用先を探しているだけなら、まずはこのファイルの外で同責務の入口がないかを確認する。

## hash
- 7a29c53f3a4a68e3b958bdfda14d9390cf26f6c1e9dee953e868d8c88ecc32eb

# `runtime_paths.py`

## Summary
- 実行時に `<repo-root>` / `<work-root>` を解決し、失敗時は `CmocError` に変換する root 解決ユーティリティをまとめる。cwd 指定時の解決補助、`pushd` を使った一時的な cwd 切替、`cmoc-root` 解決もここで扱う。
- 時刻文字列の生成と、セッション・レポート・ログ・worktree・schema・config の保存先パス決定を扱う。`memo` 配下判定のような、保存先やルート判定に関わる周辺ロジックも含む。

## Read this when
- root placeholder から実パスを解決する処理や、その失敗をユーザー向けエラーに変換する挙動を変えるとき。
- 実行時刻表記、ファイル名向けの timestamp、または `.cmoc/local` 配下の各種保存先ルールを変えるとき。
- cwd を一時的に切り替えて外部 API の前提に合わせる必要がある処理を確認するとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや、セッション・ログ・レポートの中身を扱う実装を追うとき。
- `INDEX.md` のルーティングや他モジュールの責務境界だけを確認したいとき。
- path 解決や保存先決定と無関係な CLI 解析、出力整形、状態遷移を見たいとき。

## hash
- 44eb6c915159efffe5354bd1bfa12c771b7f1e9dc6d838f6860733fd18564cee

# `runtime_preprocess_command.py`

## Summary
- `cmoc` の前処理コマンド群をまとめて読むための入口。実行開始時のラッパーと、前処理本体の順序、設定同期後に差分をコミットする流れを追いたいときに読む。

## Read this when
- `cmoc` の前処理コマンドの実行順や、前処理・設定同期・設定コミットのつながりを確認したい。
- 設定を人間編集対象として扱いつつ、前処理で現在形へ戻す扱いを確認したい。
- 設定ファイルの差分を明示的に追跡対象へ戻して commit する判断を確認したい。

## Do not read this when
- 各前処理ステップの具体的な処理内容や失敗時の細部を追いたいときは、各ステップの実装へ直接進む。
- `cmoc` 以外のサブコマンドの手順を知りたいときは、そちらのコマンド実装を読む。
- 設定データの中身そのものを知りたいときは、設定定義側を読む。

## hash
- 96b19ba19c1d2faade9ee3c7903b53a6a8ff5e8883f65ffd6f7e342ef240c434

# `runtime_results.py`

## Summary
- 外部コマンド実行結果と Codex exec 実行結果を保持する不変 dataclass を定義する。
- コマンド終了コード、標準出力・標準エラー、生成物パス、Codex home、schema、実行時間、quota 待機情報など、runtime 実行後に他処理へ渡す結果コンテナを扱う。

## Read this when
- 外部コマンドや Codex exec の実行結果を受け渡す型のフィールドを確認・変更したいとき。
- call log、prompt log、stdout/stderr log、output、schema などの実行成果物パスを保持する結果オブジェクトを扱うコードを読むとき。
- quota 待機時間や poll 回数など、Codex exec 実行結果に付随する計測値の保持場所を確認したいとき。

## Do not read this when
- 実際に外部コマンドや Codex exec を起動する処理、ログファイルを書き出す処理、quota 待機制御の実装を探しているとき。
- CLI 引数、設定読み込み、argv 上書き生成、schema 生成など、実行結果コンテナへ渡される値の作成元を調べたいとき。
- runtime 結果型ではなく、ユーザー向け出力形式やテスト期待値の仕様を確認したいとき。

## hash
- c9bf5b582e21beadd3ab372c424bc794a332ddbfd657f47369776b0109590f13

# `runtime_state.py`

## Summary
- session state file の永続化モデルと読み書き処理を扱う。session/apply の state 断片、branch 名からの session_id 抽出、現在 branch に対応する state 読み込み、canonical JSON 書き戻し、home branch に紐づく active session 探索の入口になる。

## Read this when
- session state file の schema、必須 field、許容 state、null/string 制約を確認または変更したいとき。
- cmoc/session、cmoc/apply の branch 名から session_id を特定する処理や、その失敗時エラーを確認または変更したいとき。
- session state file の保存先、読み込み、書き戻し、home branch から active session を探す処理を確認または変更したいとき。

## Do not read this when
- session state file のディレクトリ配置だけを確認したいときは、runtime path を扱う対象を直接読む。
- 個別サブコマンドの操作手順や状態遷移の業務仕様を確認したいときは、対応する app spec やコマンド実装を読む。
- CmocError の表示形式や共通エラー処理だけを確認したいときは、runtime error を扱う対象を読む。

## hash
- 5453ce64ca708e9c80e6e3aa4a0416dbc93461ecafdc6a30864d7db0274f46bf
