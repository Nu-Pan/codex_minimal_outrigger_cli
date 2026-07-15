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
- `commons` 配下の runtime 群を束ねる統合入口。Codex 実行・TUI 起動、設定と状態の読み書き、Git/作業ツリー操作、ログ・パス・出力処理をまたいで扱うときにここを起点に読む。
- 各低レベル helper の詳細ではなく、`cmoc` 全体の実行フローやサブコマンド横断の共通処理を追いたい場合に使う。個別の設定変換、Git 操作、状態管理だけを知りたいなら、それぞれの専用モジュールを直接読む。

## Read this when
- Codex 実行や TUI 起動の前後で、設定・状態・Git・ログをどう連携させるかを確認したいとき。
- 作業ディレクトリや worktree、branch、session、schema store などの共通パスや永続状態の扱いを横断的に把握したいとき。
- サブコマンド実行の周辺で、エラー整形や subprocess 実行、ハッシュ付き出力、実行結果の共通表現をまとめて追いたいとき。

## Do not read this when
- 特定の責務だけを調べたいときは、設定なら `runtime_config`、Git なら `runtime_git`、状態なら `runtime_state`、パスなら `runtime_paths` を直接読む。
- サブコマンド固有の振る舞いだけを確認したいときは、ここではなく各サブコマンド実装を読む。
- 個々の low-level helper の実装差だけを追う目的では、まずこの統合入口を読む必要はない。

## hash
- 612c735076091aea4798f3103ca3c336d1c4eb55da60bd7e3e0627a360ec7021

# `indexing.py`

## Summary
- - `INDEX.md` の自動更新処理、更新対象の列挙、既存 entry の再利用判定、欠落 entry の生成、更新分の git commit をまとめて扱う。
- - Codex 呼び出し前の indexing preflight 登録と、対象 1 件分の entry 生成・整形・検証も含む。

## Read this when
- - `INDEX.md` を自動生成・再生成する流れ、対象の深い順処理、差分の commit まで含めて追いたい。
- - 既存 `INDEX.md` から entry を読み戻して再利用する条件、hash による鮮度判定、壊れた entry の扱いを確認したい。
- - entry 生成結果の schema 検証や、対象が binary・ignore・memo・symlink のときの除外条件を確認したい。
- - Codex 実行前の preflight 登録や、indexing 用のロック・並列生成の制御を確認したい。

## Do not read this when
- - `INDEX.md` の各 entry に書くべき文面の正本仕様だけを知りたいなら、entry standard 側を読む。
- - indexing 以外の git 操作、一般的な runtime ヘルパー、別サブコマンドの実行制御を確認したいだけなら、このファイルは読まなくてよい。
- - 個別ファイルの実装内容や他の `commons` モジュールの責務を知りたいだけなら、直接その対象を読む。

## hash
- e59ac9b889406e0fc52dbf6370edeed2f825b2df091bf8d21dfd9065170441a2

# `runtime_apply.py`

## Summary
- apply 実行中の process とその child group を、安全に特定して停止・追跡解除・pid file 清掃するための共通基盤。`cmoc apply abandon` の cleanup と競合しない lock、親 process の生存確認、Codex subprocess の tracking、stale な pid 情報の判定を扱う。
- この層に進むのは、apply の破棄・停止・後始末で process identity や pid file を直接扱う必要があるときだけでよい。branch/worktree の選択や session state の更新だけを見たいなら、より上位の apply サブコマンド側を読む。

## Read this when
- `cmoc apply abandon` で実行中の apply を止める経路や、pid file と実 process の同一性確認を変えたい。
- Codex child の追跡範囲、process group の停止条件、stale tracking の扱いを確認したい。
- apply run の lock と追跡情報を、どのタイミングで公開・解除するかを知りたい。

## Do not read this when
- apply の引数、状態遷移、report 文言、branch/worktree の削除条件だけを見たい。この場合は apply サブコマンドの仕様側を先に読む。
- session state の保存形式や branch 解決だけを追いたい。このファイルは process 停止と追跡に責務が限られるため、より直接の状態管理側を読むべきである。
- 一般的な process 制御や git worktree の一覧取得だけが目的なら、ここではなくそれぞれの責務に近い実装を読む。

## hash
- 851e25362f8c6524f1b26d22561d352aae061f4f5e9a01ea0a6af6384c610fe4

# `runtime_cli.py`

## Summary
- `src/sub_commands` 配下の各サブコマンドに共通する起動・終了の流れを扱う入口。work root の前提確認、doctor preprocess の挿入、サブコマンドログと step 通知、完了サマリー、例外時のエラー表示をまとめて調整したいときに読む。`CliRunResult` のように、サブコマンド本体が標準サマリーとは別の stdout 契約を返す場合もここを確認する。

## Read this when
- 複数の CLI サブコマンドに共通する実行ライフサイクルを変更したいとき。
- work root での実行前提や、doctor preprocess をいつ挟むかを見直したいとき。
- サブコマンドログ、step 開始通知、完了サマリー、エラー出力の共通動作を揃えたいとき。
- サブコマンド本体から終了コードや追加 stdout を返す契約を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務手順や入出力の仕様だけを知りたいときは、各サブコマンド本体を読む。
- サブコマンドログの保存先や表示文面だけを確認したいときは、ログ仕様の文書を読む。
- doctor preprocess の共通修復内容そのものを確認したいときは、前処理仕様を直接読む。
- エラーレポートの文面や既定の stdout / stderr 方針だけを知りたいときは、エラーハンドリング仕様を読む。

## hash
- 42726719c4ed10c48a15094cd9186f39340a153ae0210585fb183ecefaeaf678

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
- Codex exec の実行制御をまとめて扱う入口。単発試行の呼び出し、Structured Output 検証、capacity retry、quota 待機と代表 probe、resume 継続、call log と subcommand event の記録を同じ状態機械として管理する。
- 変更対象が exec の失敗時挙動、再試行条件、ログ出力、resume token の扱い、または worktree の変更 path 取得であればここを読む。TUI 起動や別サブコマンドの制御は対象外で、そちらの入口を先に読む。

## Read this when
- Codex 実行の再試行条件や失敗時の分岐を変えるとき。
- Structured Output の検証条件、出力 JSON の読み取り、schema 不一致時の扱いを変えるとき。
- quota 待機、代表 probe、resume token の再開条件、capacity retry の相互作用を確認したいとき。
- call log、stdout/stderr/output の保存、subcommand event の記録内容を変更するとき。
- worktree 上の変更 path を収集する挙動を確認したいとき。

## Do not read this when
- TUI の起動や表示を変えたいだけのとき。
- exec 以外のサブコマンド実装や汎用設定読み込みだけを見たいとき。
- git 状態取得の一般的な実装を探しているだけで、この関数群の返却形式に関心がないとき。

## hash
- 73bbe18fbf61cab01b1f17a8afc6502b4fc568b31020d63133c8cee5c4dbf70c

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
- Codex subprocess 起動前後の実行環境を組み立てる入口。`argv`、`CODEX_HOME`、sandbox/permisson profile、追加 read/write 許可、schema 配置、JSONL error 判定を扱う変更で読む。

## Read this when
- Codex CLI を呼ぶ前に、どの `cwd`・`CODEX_HOME`・sandbox/permission profile を渡すかを決める必要がある。
- 追加 read/write path の許可境界や、worktree / oracle / memo / reserved root の扱いを変える。
- Codex subprocess の出力から schema 配置、resume token、capacity/quota/error 判定を解釈する処理を変える。

## Do not read this when
- 単純な CLI 引数パースや設定値の定義だけを追いたい場合は、より上位の呼び出し側を読む。
- process tracking の保存形式や abandon/stop の操作だけを変える場合は、該当する sub_command 側の文書や実装を読む。
- このモジュールの境界外にある一般的な runtime helpers や git 判定だけを見たい場合は、個別 helper 側を直接読む。

## hash
- 19158f19d48230f7f33d60c5e245c7b7b06f1d22517888b46fdb67b61b8d37bf

# `runtime_codex_tui.py`

## Summary
- `cmoc tui` で Codex CLI/TUI を起動する実行経路を扱う。ユーザー入力プロンプトの受け渡し、`CODEX_HOME` の解決と事前検証、設定上書き argv の組み立て、call log と実行結果の記録までをまとめて確認したいときに読む。

## Read this when
- Codex TUI 起動時の引数生成や実行前検証を直したい。
- プロンプト保存位置、call log の記録内容、実行結果イベントの出し方を確認したい。
- Codex 起動時に使う `CODEX_HOME`、cwd、読み取り専用パスの扱いを追いたい。

## Do not read this when
- `cmoc exec` など別の Codex 呼び出し経路だけを調べたい。
- agent call のパラメータ解決そのものを直したい。
- サブコマンド共通のログ形式だけを見たい場合は、より上位の実行・ログ関連の対象を読む。

## hash
- e0ea8aff71c383f305655b65963834fd866b04bb74b3aa1d717aa717ac937c6b

# `runtime_config.py`

## Summary
- `cmoc` の設定 JSON を実際に読み書きし、既定値補完・型検証・エラー境界・同期保存のふるまいを確認したいときに読む。人間が手編集する設定ファイルの受け口なので、復元失敗時の扱いと保存時の表現が主題になる。

## Read this when
- `{{work-root}}/.cmoc/gt/ar/config.json` の読み込み・保存・自動生成・再同期の仕様を変更するとき
- 人間編集された設定 JSON の検証条件や、壊れた設定を利用者向けエラーに変換する境界を確認したいとき
- 設定値のデフォルト補完や、設定オブジェクトと JSON 表現の対応を追いたいとき

## Do not read this when
- `CmocConfig` の項目定義そのものだけを確認したいときは `{{work-root}}/oracle/src/oracle/other/cmoc_config.py` を先に読む
- 設定ファイルの保存先そのものだけを確認したいときは `{{work-root}}/src/commons/runtime_paths.py` を先に読む
- サブコマンド側の利用箇所だけを追いたいときは各 `load_config` / `sync_config` 呼び出し側を読む

## hash
- 256df40ecb0e7c046e232522994ec435efa34b47941a663e3f584d42a1c85fde

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
- doctor preprocess の排他制御、current/main worktree の共通修復、修復差分の commit、元の index 復元、`.agents` / `.cmoc/gu` / config の扱いをまとめて見る入口。個別の git 補助関数を探すより、doctor 全体の流れや worktree 間の整合性を確認したいときに読む。

## Read this when
- doctor 実行前の共通修復手順や、linked worktree を含む処理の流れを追いたいとき。
- doctor の lock、index 復元、repair commit の作り方、`.agents` の追跡化、`config.json` の追跡保証の関係を確認したいとき。
- doctor preprocess が失敗したときの git 側の修復・例外処理の責務を見たいとき。

## Do not read this when
- 単一の CLI コマンドやサブコマンド引数の入口だけを追いたいときは、各 runtime CLI / command モジュールを先に読む。
- cmoc config の同期仕様だけを見たいときは `runtime_config` 側を読む。
- ollama の起動可否だけを見たいときは `runtime_ollama` 側を読む。
- 汎用の git ヘルパーや path ヘルパーを探しているだけなら、このファイルではなく `runtime_git` や `runtime_paths` を読む。

## hash
- 6c5f7c53fb3dcac88c772f91f86fba7d5bfcac3b881434e470d29b21be119530

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
- Git 呼び出しの共通化、branch と worktree の命名・存在判定、managed worktree の作成/削除、`.cmoc/gu` の ignore 保証、oracle file 判定をまとめる基盤。
- cmoc の session/apply/run 系機能から、このファイルを介して Git と repository 状態を扱うときに読む。

## Read this when
- git subprocess の失敗を cmoc 利用者向けのエラーにそろえたい
- current branch や HEAD commit、clean worktree 条件を確認したい
- cmoc 管理 branch や managed worktree の作成・削除・存在判定を扱いたい
- `.cmoc/gu` を追跡対象外にする処理や、その状態確認を扱いたい
- oracle file / realization file の判定を使って差分分類やアクセス制御を実装したい

## Do not read this when
- Git 以外の path 操作や state 管理だけを見たい場合は、より直接の path / branch / config 系モジュールを読む
- cmoc のコマンド組み立てやユーザー向け振る舞いの詳細だけを見たい場合は、各 sub command 側を読む
- worktree の保存形式や branch model の正本仕様を知りたい場合は、対応する oracle 側を読む

## hash
- 4c87304d459ac920cce68d5e41b1300717248f0942cc904b490ec175e5315e0a

# `runtime_logging.py`

## Summary
- サブコマンド実行中の JSON Lines ログと待機時間の集約、ならびに深い処理から現在の logger を参照・一時差し替えする仕組みを扱う。コンソールの完了サマリーとファイルログのイベント単位を揃えたいときに読む。

## Read this when
- サブコマンドの開始・ステップ開始・終了・イベント追記・待機時間集計の振る舞いを確認したいとき。
- 処理階層の深い場所から、現在実行中のサブコマンド logger を取得したり、一時的に差し替えたりする必要があるとき。
- コンソール表示とファイルログで同じ step 実測値を共有する責務を確認したいとき。

## Do not read this when
- ログファイルの保存先ルールや必須イベントの定義だけを知りたいときは、対応する oracle 文書を直接読む。
- 個別の CLI サブコマンド実装やログ出力の文言を調整したいだけなら、まず各サブコマンド本体や出力整形側を読む。
- 単に path 解決や timestamp 生成の仕様を見たいだけなら、このモジュールではなくそれらを扱う共通基盤を読む。

## hash
- 48aac399b7d34b3a6ce8c0150d8c8cbc0ae6cea2bd2af0b509bb2c1ef42b54f3

# `runtime_ollama.py`

## Summary
- cmoc 管理下の Ollama を単一の事前確認処理として扱う実装。インストール、systemd user service の整備、プロセス所有者と listener の対応確認、model の取得・load、GPU 利用確認を同じ流れでまとめているため、この責務を変えるときの入口になる。

## Read this when
- cmoc の local SLM を managed Ollama で供給する可否や起動完了条件を変えたいとき。
- Ollama の取得先、service 起動条件、model の pull/load 条件、GPU 確認条件のいずれかを変えるとき。
- procfs や systemd user service を使った所有者・listener 確認の方法を見直すとき。

## Do not read this when
- Ollama 以外の model provider の分岐や、別の preflight 全体の制御だけを追いたいとき。
- config の読み込み方や path 定義だけを変えたいときは、先にそれらの責務を持つ対象を読むべきで、この entry は後回しでよい。
- Ollama の UI や API の一般的な使い方だけを知りたいとき。

## hash
- 0c2727a9959ee1bf799d98398f3d0bd8b6b5bfda3a96878605c9c30169412571

# `runtime_paths.py`

## Summary
- `repo_root`/`work_root` で実行時の root 解決を扱う。`cwd` 起点の解決、`pushd` による cwd 切替の直列化、`CmocError` への変換を確認したいときに読む。
- `.cmoc` 配下の runtime / config / log / report / schema / session / worktree の保存先を決める関数がまとまっている。保存場所やディレクトリ構成を変える可能性があるときに読む。
- timestamp 生成と duration 表示の共通形式を定めている。ファイル名の時刻表記や console・ログの時間表示を揃えたいときに読む。
- `memo` 配下判定と、agent が読み取れる `.cmoc/g*/ar` directory 群の扱いを確認したいときに読む。

## Read this when
- 実行時に repo root または worktree root を解決する処理を変更したい。
- `.cmoc` 配下の保存先や runtime directory の配置を変更したい。
- timestamp 付き path 予約や duration の表示形式を揃えたい。
- `memo` 判定や cwd 切替の直列化が必要な処理を確認したい。

## Do not read this when
- 静的な設定値や CLI 引数の定義だけを見たいときは、この file ではなく設定側を読む。
- Codex 呼び出し規約や file access policy の本体を確認したいときは、別の正本を読む。
- session / report / log の保存内容そのものを見たいときは、保存先を返すこの file ではなく各保存処理を読む。

## hash
- 743829f503ac960ac71da71a82eb3ce4211d543a4a2f84b360776f7d9000b238

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
- session/apply の永続状態を 1 か所で扱う基盤。state 断片の型、JSON 読み書き、ブランチ名と session-id の対応、session fork の排他 lock をまとめている。
- `cmoc session` / `cmoc apply` 系の実装で、状態ファイルの保存先決定・読み込み・検証・書き戻しが必要なときの入口。
- 状態の詳細な遷移ロジックそのものではなく、共通の state 取扱いだけを担うため、上位コマンドの実行順や merge / abandon の手順確認には進まない。

## Read this when
- session state の JSON スキーマ、欠落や型不正の扱い、保存形式を確認したいとき。
- 現在の branch から対応する session state file を引く処理や、active session の探索、session fork の直列化が必要なとき。
- session / apply の各サブコマンド実装で、状態アクセスを共通化したいとき。

## Do not read this when
- `cmoc session fork` / `join` / `abandon` / `apply` の操作手順やエラー条件を知りたいだけなら、各 sub command 実装と仕様文書を直接読む。
- Git 操作や worktree 操作の詳細を追いたいだけなら、state ではなく `runtime_git` 側を読む。
- 保存先ディレクトリの一般ルールだけを確認したいなら、state 操作ではなくパス解決の責務を持つ別モジュールを読む。

## hash
- 3bee74f81cb432604178bd25a70bbac64c12818f382cd00e0332ddc1ae3ef064
