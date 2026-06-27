# `apply`

## Summary
- apply 系サブコマンドの実装をまとめる領域。apply run の開始、実行ループ、結果 report、join、abandon、実行中 process と pid file の管理まで、apply 状態遷移に関わる CLI 制御と低レベル runtime helper への入口になる。
- session branch と apply branch、isolated worktree、apply state、report、cleanup、merge、process 停止など、apply run のライフサイクル全体を調べるときに、目的別の実装へ進むための分岐点として使う。

## Read this when
- apply fork、join、abandon のいずれかの CLI 実行条件、状態遷移、worktree・branch・process id・report の扱いを調査または変更したいとき。
- apply branch と session branch の関係、apply worktree の探索や削除、apply process の停止、pid file の読み書きなど、apply 実行時状態に関わる処理の読む先を選びたいとき。
- apply fork の scope 列挙、finding 適用、commit 作成、禁止対象差分のロールバック、収束判定、失敗時 report 生成までの流れを追いたいとき。
- 未 join の apply run を破棄する処理、または apply branch の成果を session branch へ取り込む処理のどちらを読むべきか判断したいとき。
- apply の利用者向け出力、warning、report 内容、cleanup 対象、merge conflict 処理のうち、どの責務の実装が入口になるかを切り分けたいとき。

## Do not read this when
- apply 以外のサブコマンドの実行フロー、引数定義、出力、状態遷移を調べたいとき。
- git 実行、state file 読み書き、config 読み込み、timestamp、reports directory などの共通 runtime 基盤そのものを変更したいとき。
- Codex に渡す prompt、AgentCallParameter、structured output parameter の詳細だけを調べたいとき。
- oracle file や INDEX.md の正本仕様、realization 品質基準、ルーティング文書生成規則を確認したいだけのとき。
- apply の具体的な開始・破棄・取り込み・report・process 管理に関係しない一般的な CLI パッケージ構成だけを確認したいとき。

## hash
- 6c7e22ea17777452e513ac55d1f70c1cfb69e5a998dbe71b85d2cfc464d78903

# `indexing.py`

## Summary
- INDEX.md の自動保守を行う CLI サブコマンドと preflight 処理を実装している。
- 対象ツリーを走査して indexable な子要素を選別し、既存エントリーの hash 再利用、Codex による不足エントリー生成、Markdown への描画、更新差分の commit までを一連の処理として扱う。
- 排他 lock、worktree 事前条件、既存エントリー形式検証、対象内容抽出、鮮度判定用 hash 計算など、INDEX.md 更新処理の制御ロジックの入口になる。

## Read this when
- INDEX.md を自動生成・更新するサブコマンドの実行順序、preflight 登録、commit 作成条件を確認したいとき。
- indexable な directory や child の選別条件、memo・git ignored・binary・隠しファイルの除外挙動を変更または調査したいとき。
- 既存 INDEX.md エントリーの再利用条件、必須 section と hash の検証、対象 hash の計算方法を確認したいとき。
- Codex CLI に渡す index entry 生成入力、Structured Output の検証、生成結果の Markdown 描画に関わる処理を追いたいとき。

## Do not read this when
- 個別サブコマンドの business logic を調べたいだけで、INDEX.md の保守処理や preflight に関係しないとき。
- Codex 実行そのものの低レベル実装、Git コマンド wrapper、設定読み込み、path model の詳細を確認したいときは、それぞれの runtime や utility 実装を読む方が直接的。
- INDEX.md エントリー生成 prompt の具体的な構築内容だけを確認したいときは、entry parameter builder 側を読む方が直接的。
- 生成済み INDEX.md の内容を読むべき対象の選別に使うだけなら、この実装ではなく該当階層のルーティング文書を読む。

## hash
- 7dfa3b920d6f4555f8702e5300c1a60e29c76bd3a09bdfd88c9338f9fc64aec0

# `init.py`

## Summary
- `cmoc init` サブコマンドの実行本体を扱う。CLI runtime 経由で初期化処理を起動し、work root の `.cmoc` ignore 保証、設定同期、初期化コミット作成、利用者が事前に持っていた staged 差分と `.gitignore` 状態の復元をまとめて担う。
- 初期化成功時に stdout へ出す Markdown 形式の結果文もここで組み立てる。

## Read this when
- `cmoc init` の実行順序、初期化コミット、設定同期、または `.cmoc` を `.gitignore` に含める処理を確認・変更したいとき。
- 初期化前から存在する `.gitignore` の worktree/index/HEAD 状態や、利用者が事前に staged していた差分を `cmoc init` 後にどう戻すかを調べるとき。
- `cmoc init` のログ作成前に行う ignore 保証と、その副作用を後続の復元処理から区別する仕組みを確認したいとき。
- `cmoc init` 成功時の利用者向け Markdown 出力を変更・検証したいとき。

## Do not read this when
- 個別の git コマンド実行 wrapper、runtime 共通処理、repo/work root 解決、設定同期、または ignore パターン生成そのものの実装を調べたいだけのときは、それらを定義する共通 runtime 側を読む。
- 他のサブコマンドの CLI 挙動、出力、状態復元を調べたいときは、対象サブコマンドの実装へ進む。
- `cmoc init` の外部挙動をテスト観点から確認したいだけのときは、対応するテストを読む。

## hash
- a7f12d58923b83b9f3941a0e829e20e9ed445db35c3a5fc9c20b6112c3620faf

# `review.py`

## Summary
- review oracle サブコマンドの実行入口と実行全体の制御を担う実装。indexing preflight を通したうえで CLI 共通実行枠に処理を渡し、active session branch・clean worktree などの前提確認、isolated review worktree と一時 review branch の作成、oracle 対象列挙、レビュー実行、INDEX 変更の commit/merge、レポート出力、失敗時レポート出力と後片付けをまとめて orchestration する。
- レビュー対象の列挙、review loop、INDEX 変更の commit/merge、レポート描画・書き込みなどの具体処理は下位モジュールへ委譲し、この対象はそれらを現在の session state と worktree 操作に接続する入口として位置づく。

## Read this when
- review oracle サブコマンドがどの前提条件で実行を拒否するか、どの順序で一時 worktree・branch・review loop・merge・report 生成を進めるかを確認したいとき。
- review oracle の scope 指定、active session branch 判定、clean worktree 要求、cmoc ignore 確保、失敗時にも report path を出力して例外を再送出する制御を変更したいとき。
- review oracle の処理全体に新しい段階を差し込む、または既存の対象列挙・review loop・INDEX 変更 commit/merge・レポート生成 helper の接続関係を追いたいとき。

## Do not read this when
- oracle file の列挙条件そのものを調べる場合は、対象列挙を担当する下位モジュールを直接読む。
- review loop 内で Codex 実行結果から finding を作る処理や finding merge operation の適用内容を調べる場合は、loop を担当する下位モジュールを直接読む。
- review report の表示形式、finding section の描画、report file の内容や path 表示を調べる場合は、report を担当する下位モジュールを直接読む。
- review branch の merge conflict 解決、INDEX 変更 commit、worktree status path の扱いを単独で調べる場合は、index 変更処理を担当する下位モジュールを直接読む。

## hash
- 2ef95be3d2d0fe22ecac96e4882f71d98eb321210eb481f04634db39f969a994

# `review_index.py`

## Summary
- review 用 worktree で生成されたルーティング文書の差分を検査し、許可された変更だけを commit する処理を担う。
- review branch を session branch へ merge し、競合がルーティング文書だけに限定される場合は現在側を採用または削除して自動解決する。
- git の status、diff、merge、checkout、rm、commit などを呼び出す制御と、想定外差分や merge 失敗時の cmoc 向けエラー化をまとめている。

## Read this when
- review oracle が作成したルーティング文書差分だけを commit する条件や、ルーティング文書以外の差分を拒否する挙動を確認したいとき。
- review branch の merge 後 HEAD 取得、merge 失敗時の扱い、未解決競合の自動解決条件を確認したいとき。
- git status の porcelain 出力から変更パスを抽出する処理、rename/copy の扱い、unmerged stage の確認方法を調べたいとき。

## Do not read this when
- 通常のサブコマンド引数定義、CLI 出力形式、ユーザー入力の parsing を調べたいだけのとき。
- ルーティング文書の内容生成、要約文作成、Structured Output の schema 定義を調べたいとき。
- oracle file と realization file の概念やルーティング文書そのものの仕様を確認したいとき。

## hash
- fd46086c773e71294be6c9b8ed3da758d0729bfa1dc795d5f35336f661efd447

# `review_loop.py`

## Summary
- review oracle による finding の列挙、統合、検証、判定を一連のループとして実行する制御ロジックを扱う。
- oracle path と finding の対応付け、finding_id や検証理由・判定結果の初期値付与、merge operation の適用と妥当性検証を担う。
- Codex 実行関数に渡す review oracle 用パラメータを組み立て、設定値で定められた反復回数に従って finding list を更新する入口になる。

## Read this when
- review oracle の finding enumerate/merge/validate/judge の実行順序、反復条件、停止条件を確認または変更したいとき。
- finding の `oracle_path` を実パスへ解決し、既存 finding を対象 oracle file ごとに絞り込む挙動を確認したいとき。
- merge finding の `delete`、`replace`、`merge` operation が既存 finding list にどう適用されるか、また不正な target や重複利用をどう拒否するかを確認したいとき。
- finding に `finding_id`、`advocate_reasons`、`challenger_reasons`、`verdict`、`judge_reason` の初期値が付与される箇所を追いたいとき。
- review oracle の各段階で Codex 実行関数へ渡す目的文字列、作業ディレクトリ、ログルート、設定の受け渡しを確認したいとき。

## Do not read this when
- review oracle 用プロンプトや Structured Output parameter の具体的な構築内容を確認したいだけなら、builder 側の対象を読む。
- 設定ファイル上の review oracle 反復回数や設定 schema の定義を確認したいだけなら、設定モデル側の対象を読む。
- path keyword の定義や `<...>` 形式の path 解決規則そのものを確認したいだけなら、path model 側の対象を読む。
- CLI サブコマンドの引数定義、コマンド登録、利用者向け入出力を確認したいだけなら、サブコマンド入口や CLI 定義側の対象を読む。
- review finding の品質基準や oracle file と realization file の仕様上の関係を確認したいだけなら、正本仕様断片側の対象を読む。

## hash
- 86cde0b2e0151ed2d36309831353b40d7525abae13ac516f2e8f44bbd517cffb

# `review_report.py`

## Summary
- review oracle の実行結果を、YAML frontmatter 付き Markdown レポートとして生成・保存する処理を担う。
- 評価対象 oracle、採択・棄却された finding、実行中エラー、ブランチ・コミット情報を集計し、レポート全体の result と本文セクションへ整形する。
- oracle パスをレポート上で読みやすい表示に変換する補助処理と、finding 一覧・frontmatter 項目の描画処理を含む。

## Read this when
- review oracle のレポート保存先、生成タイミング、Markdown 構成、frontmatter に出す値を確認・変更したいとき。
- accepted/rejected finding の分類、fatal/minor 件数、error/no_targets/fatal/minor/ok の result 判定条件を確認・変更したいとき。
- レポート内で oracle ファイルパスをどのように相対表示するか、または oracle ツリー外のパス表示をどう扱うかを確認・変更したいとき。

## Do not read this when
- review oracle がどの oracle を収集・評価するか、finding をどう生成するかを知りたいだけのとき。
- CLI 引数の定義、サブコマンド登録、セッション状態の生成・更新、git ブランチ操作の詳細を調べたいとき。
- 生成済みレポートの内容を読むだけで、レポート描画ロジックや判定条件を変更しないとき。

## hash
- 2fbc344b8b86ae4b1da1c963eabef9d6a2ef658e6fdeda3ff15196af1f021166

# `review_targets.py`

## Summary
- review oracle が検査対象にする oracle file を列挙する処理を担う。scope が full の場合は全対象を返し、それ以外では session_start_commit から HEAD までに oracle 配下で変更された対象だけを返す。
- oracle file 候補の列挙では oracle ツリーを再帰走査し、通常ファイルのうち INDEX.md、root memo、git ignore 対象を除外して並び順を安定させる。

## Read this when
- review oracle の対象ファイル集合が scope によってどう変わるかを確認・変更したいとき。
- session_start_commit を基準にした差分対象の判定や、git diff の対象範囲を確認・変更したいとき。
- oracle file 候補から INDEX.md、root memo、git ignore 対象を除外する条件を確認・変更したいとき。
- review oracle が参照する oracle file の列挙順やフィルタ条件に関する不具合を調査するとき。

## Do not read this when
- review oracle の結果表示、診断内容、プロンプト、出力形式を確認したいだけのとき。
- oracle file や realization file の概念定義そのものを確認したいとき。
- oracle 以外の realization file や test file の列挙条件を確認したいとき。
- root memo 判定、git ignore 判定、git コマンド実行 helper の詳細を確認したいとき。

## hash
- 8757d7467f9e0f50ab5b0c8b0f40fda477f0e603870376d607db08c28669e79e

# `session`

## Summary
- active session の作成、home branch への join、merge せず破棄する操作など、session 系サブコマンドの実行本体をまとめる実装領域。
- 各サブコマンドは CLI runtime 経由で実行され、branch 条件、clean worktree、session state の読み書き、git 操作、利用者向け出力などを扱う。
- session パッケージ自体は最小限の入口であり、具体的な挙動は個別サブコマンド実装へ進んで確認する。

## Read this when
- session 系サブコマンドのどの実装へ進むべきかを切り分けたいとき。
- session の開始、join、破棄に関する事前条件、状態遷移、branch 操作、成功時出力、失敗時の扱いを調査・変更したいとき。
- active session、home branch、session branch、session state と CLI 実行処理の接続を確認したいとき。
- merge conflict 解消、cleanup 失敗時 rollback、`.cmoc` の git ignore 準備など、session 操作に付随する個別制御の読む先を選びたいとき。

## Do not read this when
- session state の schema、永続化形式、path 解決、git wrapper、runtime wrapper などの共通 helper 自体を調べたいとき。
- CLI 全体のサブコマンド登録、session 以外のサブコマンド、または oracle 上の正本仕様を確認したいとき。
- Codex CLI に渡す conflict resolution prompt や parameter の内容そのものを調べたいとき。
- 個別の session 操作が既に分かっており、その実装だけを直接読めば足りるとき。

## hash
- 7a208fb387ccca5bbc6dd80daabf1c32ac77edd8203c109ad8c9f34f42c26f0d

# `tui.py`

## Summary
- `cmoc tui` の実行フローを実装するサブコマンド本体。利用者が編集する依頼文の作成、エディタ起動、依頼文の読み取り、TUI 用パラメータ解決、完全 prompt の保存、Codex TUI 起動までを扱う。
- TUI 起動時の AgentCallParameter 構築、TUI で許容する file access mode の検証、Markdown 依頼文の見出し構造化、解決済み JSON からの値取り出しを担う。

## Read this when
- `cmoc tui` の起動手順、依頼文編集から Codex TUI 実行までの制御フローを確認・変更したいとき。
- TUI 実行時に作成される元 prompt と完全 prompt の保存場所・命名・読み取り処理を確認したいとき。
- TUI で利用するエディタ選択、エディタ異常終了時のエラー、利用可能な editor command の優先順を確認・変更したいとき。
- TUI 用の file access mode 制限、解決済みパラメータから AgentCallParameter を作る処理、complete prompt に含める標準指示フラグの扱いを確認したいとき。
- Markdown の見出しと fenced code block を考慮して、利用者 prompt を StructDoc 階層へ変換する挙動を確認・変更したいとき。

## Do not read this when
- TUI 以外のサブコマンドの CLI 制御や実行フローを調べたいだけのとき。
- Codex CLI/TUI の実際の外部プロセス実行、config 読み込み、repository root や work root の解決など、runtime 共通処理を調べたいとき。
- TUI パラメータ解決用の prompt/schema そのものや、許容される file access mode の定義元を調べたいとき。
- complete prompt 全体の組み立て規則や StructDoc の markdown 描画規則を調べたいとき。
- indexing preflight の詳細な条件や、INDEX 生成・更新の実装を調べたいとき。

## hash
- 10df8d618f0de7d5b9f8e1b914e10a117d9388932d95cedb196ef89fd330681b
