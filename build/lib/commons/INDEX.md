# `__init__.py`

## Summary
- cmoc の共有実行時ヘルパー群のパッケージ入口である。
- このファイル自体は共有ヘルパー用パッケージであることだけを示し、個別 helper の責務や利用条件は下位モジュール側で確認する。

## Read this when
- cmoc 実行時に複数箇所から使われる共有 helper 群のパッケージ境界を確認したいとき。
- 共有 runtime helper 配下の個別モジュールへ進む前に、この階層が共有補助処理の置き場であることを確認したいとき。

## Do not read this when
- 特定の helper 関数・クラス・副作用・失敗時挙動を確認したいとき。その場合は該当する下位モジュールを読む。
- CLI コマンド、設定、永続状態、テストなど、共有 runtime helper 以外の責務を調べたいとき。

## hash
- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary
- 実行時共通機能を外部からまとめて参照するための集約入口。Codex 実行、profile、config、content hash、CLI 実行、error、git、logging、path、result、state に関する既存 runtime module の公開要素を一箇所から import できるようにしている。
- 独自ロジックや仕様判断は持たず、下位 runtime module 群への薄い facade として位置づけられる。

## Read this when
- 複数の runtime 共通機能を利用する呼び出し側で、どの公開要素が集約入口から参照できるか確認したいとき。
- runtime module 群の import 経路を整理する変更や、公開される共通 helper・型・定数の追加削除を検討するとき。
- Codex 実行、git 操作、状態管理、設定、path、logging などを横断的に使うコードの依存入口を確認したいとき。

## Do not read this when
- 個別 helper の挙動、引数、例外、永続状態の更新条件を知りたいときは、それを定義している下位 runtime module を直接読む。
- CLI サブコマンドの制御フローやユーザー向け挙動を確認したいときは、コマンド実装側を読む。
- hash 計算、git 操作、Codex profile 構築など、単一責務の実装を変更するだけなら、この集約入口ではなく該当する定義元を読む。

## hash
- 1f4b3c37a1e680ec77e3065cb3cd68676b0d79551bbc1f65b89c78719cfabf24

# `indexing.py`

## Summary
- Codex 呼び出し前に各階層の INDEX.md を更新し、変更があれば indexing commit として保存する処理を担う。
- indexing 用の排他 lock、対象ディレクトリと子要素の列挙、既存 entry の再利用判定、対象 hash 計算、Codex への entry 生成依頼、Structured Output の検証と Markdown への描画を扱う。
- INDEX.md entry の必須セクションや hash 形式を検証し、対象内容の変化に応じて深い階層から順に再生成するための入口になる。

## Read this when
- Codex 実行前 preflight として INDEX.md 更新を登録・実行する流れを確認または変更したいとき。
- INDEX.md の生成対象、除外対象、対象 hash、既存 entry の再利用条件、更新順序、並列生成の挙動を調べたいとき。
- INDEX.md entry 生成結果の schema 検証、Markdown 出力形式、hash セクションの検証でエラーになる原因を追うとき。
- INDEX.md 更新差分だけを git add して commit する処理や、indexing 用 lock file の場所と排他制御を確認したいとき。

## Do not read this when
- 各 entry に書かせる文章の方針や prompt 部品そのものを変更したいだけなら、entry 生成パラメータや oracle 側 prompt 定義を直接読む。
- 通常の CLI コマンド定義、Codex 実行基盤、設定読み込み、git 実行 helper の詳細を調べたいだけなら、それぞれの実装へ進む。
- 個別ディレクトリや個別ファイルの INDEX.md 文面を人間向けに検討したいだけなら、その対象本文を読む。

## hash
- 6ba17c4c80501d669fa28fcf2b4202f71ff6a7c45240909755758c3e971c5982

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを扱う実行基盤。work root 検査、pre-log 処理、サブコマンドログの作成、開始・実行・完了表示、終了コード処理、例外表示、標準完了サマリーを一箇所で管理する。
- 標準サマリーとは別の stdout 契約を持つサブコマンド向けの結果型と、work root で実行されていることを検査する処理も含む。

## Read this when
- CLI サブコマンド実装の呼び出し方、共通ログ出力、開始・完了メッセージ、終了コードの扱いを確認または変更したいとき。
- サブコマンド例外時のエラー表示先、例外に付随する stdout、標準完了サマリーの出力順や内容を確認したいとき。
- init など、ログ作成前の検査や runtime state の配置先が通常のサブコマンドと異なる処理を追いたいとき。
- cmoc が work root 以外で実行された場合の検査とエラーメッセージを確認したいとき。

## Do not read this when
- 個別サブコマンドの業務処理そのものを確認したいだけなら、そのサブコマンド実装を直接読む。
- サブコマンドログの永続化形式や step timing の内部構造を確認したい場合は、ログ管理側の実装を読む。
- path model や root 検出の定義そのものを確認したい場合は、runtime path 側または対応する oracle を読む。

## hash
- add81e2cda35041a82bd78cd995edbaca0e6561e6da1438a9ee203063373515c

# `runtime_codex.py`

## Summary
- Codex 実行系の公開入口として、exec 実行と TUI 実行のランタイム関数をまとめて再公開する薄い集約モジュール。実体の処理は下位モジュールにあり、この対象自体は import 経路の整理だけを担う。

## Read this when
- Codex ランタイム機能を外部から import する公開入口を確認したいとき。
- exec 実行と TUI 実行のランタイム関数が、どの公開モジュールからまとめて参照されるかを確認したいとき。
- 公開 export の追加・削除により、呼び出し側の import 経路へ影響が出る変更を扱うとき。

## Do not read this when
- exec 実行または TUI 実行の具体的な処理内容、引数処理、外部コマンド実行の挙動を調べたいときは、それぞれの実装本体を読む。
- Codex ランタイム以外の共通処理、設定、パス解決、テスト支援を調べたいとき。
- 再公開される関数の内部仕様ではなく、呼び出し元の利用箇所だけを調べたいとき。

## hash
- bce418fcd1f6bffaed81f3724333817408657aed46183fa20819ffc1b40a7993

# `runtime_codex_exec.py`

## Summary
- Codex exec の単一試行ループと、その周辺の実行制御を扱う。Structured Output 検証、capacity retry、quota 代表 probe、resume 継続、call log/subcommand event 記録、実行後の file access rule 違反検出と修復を同じ状態機械としてまとめている。
- Codex CLI の argv・profile・CODEX_HOME・schema・log path を準備し、`codex exec` の subprocess 実行結果を `CodexExecResult` として返す責務を持つ。
- 作業差分から file access rule 違反 path を抽出する補助処理も含み、Codex 実行後に残った不許可変更を recovery agent call で修復する入口になる。

## Read this when
- Codex exec 呼び出しの再試行、quota 待機、resume token、Structured Output 検証、Codex call log の生成や記録内容を変更する。
- Codex 実行後の file access rule 違反検出、違反修復 agent call、`FileAccessMode` ごとの書き込み許可判定を確認または変更する。
- `CodexExecResult` に入る実行ログ path、schema/output 読み取り、subcommand log の `codex_call` event、quota wait 集計の発生箇所を追う。

## Do not read this when
- TUI 起動や Codex exec 以外の Codex CLI サブコマンド分岐だけを調べる場合は、より直接の実行入口や TUI 側の module を読む。
- Codex profile、schema 配置、CODEX_HOME 解決、quota/capacity エラー判定などの低レベル helper 自体を変更する場合は、それらを定義する runtime Codex profile/helper 側を読む。
- agent call parameter の prompt 構築や quota probe 用 prompt の内容を変更する場合は、ACP builder 側を読む。

## hash
- 8fa8c7813ae276082201d234f1529eab24d1fdcfde91449adaa513f55162c356

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出し完了時に、目的、呼び出しログ、経過時間、終了コードを利用者向け console へ出力する通知処理を提供する。
- console 表示用の時刻と経過時間整形は共通の runtime path 系 helper に委ね、oracle doc の console/log 仕様に対応する出力形式だけを組み立てる。

## Read this when
- Codex CLI 呼び出し後に利用者へ表示される console 通知の文面、項目、整形、flush 挙動を確認または変更したいとき。
- Codex CLI 呼び出しログへの path、経過時間、終了コードが console にどう表示されるかを追いたいとき。
- oracle doc の console/log 仕様に対応する realization 側の出力箇所を探しているとき。

## Do not read this when
- console 表示に使う時刻文字列や経過時間文字列そのものの整形規則を確認したいだけのときは、それらの helper 定義を読む。
- Codex CLI 呼び出しログファイルの生成、保存、内容記録の処理を調べたいときは、呼び出しログを作成する側の実装を読む。
- 実行時 path モデルや `<work-root>` などのパス概念の仕様を確認したいときは、対応する oracle 側の path 仕様を読む。

## hash
- f958a19df4363d9585a17c45b2fee6d85d6cd968c79555d33f83707bdfbf8aca

# `runtime_codex_preflight.py`

## Summary
- Codex 実行または TUI 起動の直前に、設定済みの indexing preflight を一度だけ差し込むためのラッパー実装。
- preflight の登録・解除、実行中の再入防止、スレッド間排他、実行 root の決定、特定 purpose の preflight skip 判定を扱う。
- 実際の Codex 実行処理は runtime 側へ委譲し、この対象はその前段で indexing を起動する制御境界として位置づく。

## Read this when
- Codex 実行前に indexing を自動実行する制御を確認・変更したいとき。
- preflight の再入防止、排他制御、登録解除の挙動を調べたいとき。
- Codex 呼び出し時の cwd または root から preflight 対象 root がどう決まるかを確認したいとき。
- index entry 生成や conflict resolution で preflight を skip する条件を変更したいとき。

## Do not read this when
- Codex 実行コマンド自体の起動方法、標準入出力、終了結果の扱いを調べたいだけのときは、runtime 実行本体を読む。
- パス語彙や work root 判定の詳細を調べたいだけのときは、runtime path 系の定義を読む。
- AgentCallParameter や実行結果型の構造を調べたいだけのときは、それぞれの型定義を読む。

## hash
- 3878cafea4f3209a564a38a3ebe0f67ca85915e34f09112258511701c00f4c48

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界で必要な profile 生成、sandbox/cwd/write root 判定、CODEX_HOME 検証、apply child process tracking、Structured Output schema 配置、Codex JSONL の error/retry/resume 判定をまとめる実装。
- FileAccessMode を Codex CLI が理解する実行環境へ変換し、cmoc 側の読み書き禁止領域を profile と実行前検査で保つための入口。

## Read this when
- Codex CLI 起動前の profile 本文、sandbox mode、writable_roots、作業 cwd、追加 read/write path の許可判定を確認・変更したいとき。
- CODEX_HOME の解決・検証、profile ファイルの生成・再利用、Codex subprocess に渡す環境変数の扱いを確認したいとき。
- apply abandon と連動する Codex child process の pid 記録、lock、削除、pid 再利用検出の挙動を確認・変更したいとき。
- Structured Output schema の配置、Codex output JSON 読み取り、JSONL stdout/stderr からの error detail・resume token・capacity/quota retry 判定を扱うとき。

## Do not read this when
- prompt 本文に表示する file access rule の文言や oracle 側の仕様断片を確認したいだけなら、対応する oracle 側の prompt builder 部品を読む。
- Codex CLI を呼び出す上位サブコマンドの業務フロー、ユーザー向けコマンド仕様、apply/session/tui の全体制御を確認したいだけなら、そのサブコマンド実装を読む。
- runtime path の保存先規則や hash file 書き込み処理そのものを変更したい場合は、path 管理や runtime content の実装を読む。

## hash
- 4745798d2e690fe89108f37d19bc16c19b9072f5cff5d3c57aaeade0fb9f2379

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出しを実行するために、実行 root、cwd、設定、call log、Codex profile、CODEX_HOME 検証、subprocess 起動、実行結果の console/log 記録、失敗時の CmocError 変換をまとめる実行入口。
- AgentCallParameter と CmocConfig を受け取り、file access mode に応じた Codex cwd と profile を準備してから Codex CLI/TUI を起動する責務を持つ。

## Read this when
- Codex TUI 起動時の argv、profile 名、CODEX_HOME、cwd、file access mode の扱いを確認または変更したいとき。
- Codex TUI 呼び出しの call log JSON に記録される内容、保存場所、timestamp、purpose、model_class、reasoning_effort を確認したいとき。
- Codex TUI subprocess の失敗を CmocError として扱う流れや、returncode、elapsed_sec、console 出力、subcommand logger への codex_call event を追いたいとき。
- extra_read_paths や linked worktree を含む TUI 用 profile 準備と writable root の関係を確認したいとき。

## Do not read this when
- Codex exec や TUI 以外の Codex 呼び出し経路を確認したいだけのとき。
- Codex profile 生成、CODEX_HOME 解決、file access mode から cwd を決める個別ロジックそのものを変更したいとき。
- runtime 設定の読み込み、path 算出、logger 実装、CommandResult 型の詳細を確認したいだけのとき。

## hash
- 282709994a710f28c42883f934e94c9c2d1ae4a36a91fefc1f755598a316f5e9

# `runtime_config.py`

## Summary
- cmoc の設定データを JSON へ保存可能な dict に変換し、JSON から設定オブジェクトへ復元する処理を担う。
- 設定ファイルの読み込み、存在しない場合や不正な JSON・不正な値に対する CmocError、既定値での同期書き込みを扱う。
- 設定ファイルの物理パスは runtime_paths 側に委ね、この対象は設定内容のシリアライズ、デシリアライズ、読み書きの制御に集中する。

## Read this when
- cmoc config の JSON 構造、既定値の補完、enum key の復元、数値設定の型変換を確認したいとき。
- 設定ファイルが存在しない、JSON として読めない、top-level が object ではない、不正な値を含む場合のエラー文言や再実行案内を変更したいとき。
- 初期化や同期処理で設定ファイルを生成・更新する流れ、または設定オブジェクトから JSON を書き出す流れを追いたいとき。

## Do not read this when
- 設定クラスそのものの項目定義や既定値を確認したいだけなら、設定モデル定義を直接読む。
- 設定ファイルの配置場所や root からのパス解決だけを確認したいなら、runtime_paths 側を読む。
- 個別コマンドが設定値をどう利用するかを調べたい場合は、そのコマンド実装や設定値の利用箇所を読む。

## hash
- 9bc797d6ae683de03d7f73ecba67078ac5048aba263a064e4a99e34b0b5aead5

# `runtime_content.py`

## Summary
- 実行時に扱うファイル内容の補助処理をまとめるモジュール。ファイルや文字列の SHA-256 digest 計算、内容 hash を名前に含むファイル保存、簡易的な binary file 判定を扱う。

## Read this when
- 内容 hash に基づくファイル名生成や保存処理の挙動を確認・変更したいとき。
- ファイル内容または文字列内容から SHA-256 digest を計算する処理を探しているとき。
- テキストとして扱えるファイルかどうかを、先頭 chunk と読み取り可否で粗く判定する処理を確認したいとき。

## Do not read this when
- CLI command の入出力や利用者向け挙動を確認したいだけのとき。
- hash 対象となる内容の生成元や、保存されたファイルの利用側を調べたいとき。
- 厳密な MIME 判定や文字コード判定の仕様を探しているとき。

## hash
- 327f8182b1ab2047a3f5f70e49d2feb4fba2029da38769d649f9ed82f4175106

# `runtime_errors.py`

## Summary
- cmoc の実行時例外と、例外を利用者向け Markdown エラーレポートへ変換する共通処理を扱う。
- エラー概要、復旧・調査手順、詳細、Call stack を含む共通出力形式を組み立てる入口になる。

## Read this when
- 利用者向けエラー表示の文面、項目構成、復旧案の補完挙動を確認したいとき。
- cmoc 内で発生した例外を共通の Markdown エラーレポートへ変換する処理を調べたいとき。
- 独自の実行時例外に保持させる情報や、通常例外を受けた場合の既定表示を確認したいとき。

## Do not read this when
- 個別コマンド固有の入力検証やエラー発生条件を調べたいとき。
- ログ保存、永続状態、プロセス終了コードなど、エラーレポート文字列の生成以外を調べたいとき。
- Call stack の生成元である Python 標準ライブラリの挙動そのものを調べたいとき。

## hash
- 51eb58dfc241cb76b6debfce4a06a3169cb6a2a29d0a6f123f7c5b6c0bd03e95

# `runtime_git.py`

## Summary
- git subprocess 呼び出しを cmoc の CommandResult と利用者向け CmocError に変換し、branch・HEAD・clean worktree など git repository 状態の取得と検査を担う。
- cmoc 管理 branch と linked worktree の作成・削除・branch 削除を扱い、管理外 worktree を削除しないための path 検証も含む。
- .cmoc を git 追跡対象外にするための ignore/exclude 更新、初期化済み repository の ignore 状態検査、任意 path の git ignore 判定を提供する。

## Read this when
- git コマンド実行失敗を cmoc のエラー形式へそろえる境界処理を確認・変更したいとき。
- 現在 branch、HEAD commit、未コミット差分の有無など、git 状態を前提条件として扱う処理を追うとき。
- cmoc が作成する branch namespace、run/apply 用 linked worktree の作成・削除、管理外 worktree 削除防止の挙動を確認するとき。
- .cmoc の ignore 設定、git index からの除外、clean worktree を保つための exclude 利用、oracle/realization file 判定に使う git ignore 判定を確認するとき。

## Do not read this when
- CLI 引数解析、subcommand の入出力、利用者向け JSON schema を確認したいだけのとき。
- cmoc の domain state file の読み書きや session/apply/run の状態遷移そのものを確認したいとき。
- oracle file と realization file の定義や path model の正本仕様を確認したいときは、対応する oracle 側を読む。
- git 以外の外部コマンド実行、LLM 呼び出し、prompt 組み立ての処理を確認したいとき。

## hash
- 15cb165e66243e3f32378864165e42984718c8920ba2978b0ff521353cf57366

# `runtime_logging.py`

## Summary
- サブコマンド実行中のイベントログと実測時間を集約する runtime logging 実装。JSON Lines 形式のログファイルをサブコマンド単位で確保し、イベント、step 開始、step 経過時間、quota 待機時間を記録・参照できるようにする。
- contextvars を使って現在の制御文脈に紐づく logger を差し替え・復元・取得する入口を提供し、深い runtime helper から任意にサブコマンド logger を利用できるようにする。

## Read this when
- サブコマンド単位の JSON Lines ログ生成、ログファイル名の一意確保、イベント record の内容、flush の扱いを確認または変更したいとき。
- step の開始・完了サマリー向け実測時間・サブコマンド全体の経過時間・Codex quota 待機時間の集計方法を確認または変更したいとき。
- runtime helper から現在のサブコマンド logger を参照する仕組み、または contextvars による logger の一時差し替えと復元を扱うとき。

## Do not read this when
- ログ保存先や timestamp の具体的な path 解決規則だけを確認したいときは、runtime path を扱う実装を直接読む。
- console 表示の文言や完了サマリーの表示形式だけを変更したいときは、表示を組み立てる側の実装を読む。
- oracle 上のログ仕様そのものを確認したいときは、対応する app spec の正本仕様断片を読む。

## hash
- 6c9b4a4c583c28c18afd061c8230290bf642e6b5004f5889d6039988207fbd45

# `runtime_paths.py`

## Summary
- 実行時に使うルート解決、時刻文字列、実行状態用ディレクトリ、設定パス、memo 配下判定、作業ディレクトリ一時変更をまとめる補助モジュール。oracle 側の path model を直接公開せず、runtime 用の例外表現に変換して利用する入口になる。

## Read this when
- 実行中の現在位置から `<repo-root>`、`<work-root>`、`<cmoc-root>` を特定する処理を確認・変更したいとき。
- `.cmoc` 配下の sessions、reports、log、worktrees、state、config などの実行時パス生成規則を確認・変更したいとき。
- 実行ログや表示用の timestamp、経過時間表示、または一時的な作業ディレクトリ変更の共通処理を扱うとき。
- `<work-root>/memo` 自体または配下を判定する境界を確認・変更したいとき。

## Do not read this when
- パスプレースホルダの正本定義や root 解決アルゴリズムそのものを確認したいとき。oracle 側の path model を読む方が直接的。
- 個別コマンドが生成した report、session、log の内容や schema を確認したいだけのとき。各生成・利用側の処理を読む方が直接的。
- 一般的な runtime error の定義や表示形式を確認したいとき。エラー型を定義している共通エラー処理を読む方が直接的。

## hash
- 7415276735049b6804964a29f6671212540142e6dec612218466b2617747e2fc

# `runtime_results.py`

## Summary
- 外部コマンド実行と Codex exec 呼び出し結果を保持する小さなデータ構造を定義する。終了コード、標準出力・標準エラー、生成物、ログやプロファイル関連のパス、実行時間や quota 待機情報を受け渡すための型をまとめている。

## Read this when
- 外部コマンドや Codex exec の実行結果を関数間で受け渡すデータ構造を確認したいとき。
- Codex exec の出力本文、JSON 出力、ログファイルパス、codex home、profile、schema、経過時間、quota 待機情報の保持先を確認したいとき。
- 実行結果を表す戻り値型にフィールドを追加・削除する変更を検討するとき。

## Do not read this when
- 外部コマンドや Codex exec を実際に起動する処理を探しているとき。
- ログファイルや出力ファイルの作成・保存・削除条件を確認したいとき。
- CLI 引数、設定読み込み、プロファイル生成、schema 内容そのものを確認したいとき。

## hash
- 149af60f60abfd4347d39a62b9b27d873af9cb1148cba531f191e860be3a9e8b

# `runtime_state.py`

## Summary
- session state file の永続化構造、読み書き、検証、cmoc 管理 branch 名から session_id を解決する処理を担う。
- session と apply の状態断片を dataclass で表し、欠落 field や不正 state を CmocError として扱う入口になる。
- home branch に対応する active session の探索や、canonical JSON 形式での state 保存が必要な処理から参照される。

## Read this when
- session state file の schema、読み込み、保存、検証エラーの挙動を確認・変更したいとき。
- cmoc session branch または cmoc apply branch から session_id を取り出す処理を確認・変更したいとき。
- 現在 branch に対応する session state file をロードする制御や、home branch に紐づく active session 検出を扱うとき。
- session/apply の許可 state、必須 field、破損 state file のエラー文脈を変更したいとき。

## Do not read this when
- session state file の保存先ディレクトリ規則だけを確認したい場合は、runtime path を扱う対象を読む。
- CmocError の表示形式や例外クラス自体を変更したい場合は、runtime error を扱う対象を読む。
- session state を利用する個別 CLI command の業務フローだけを追いたい場合は、その command 実装を直接読む。
- oracle 側の session state 正本仕様を確認したい場合は、対応する oracle doc を読む。

## hash
- 639a3107fd6c4d1ad5208798d2042e7bdaa8b70ba12f3984bd72b4432b5dab30
