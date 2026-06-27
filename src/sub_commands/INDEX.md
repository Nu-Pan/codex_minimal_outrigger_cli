# `apply`

## Summary
- apply 系サブコマンドの実装をまとめるディレクトリ。apply run の開始、join、abandon、実行時 process 管理、worktree・branch 操作、report 生成までの入口になる。
- session branch と apply branch の間で変更を隔離・適用・取り込み・破棄する一連の制御を扱い、apply 固有の状態遷移、cleanup、想定外差分検出、実行結果 report の責務を下位モジュールへ分けている。

## Read this when
- apply fork、join、abandon のいずれかの CLI 実行フロー、状態遷移、worktree・branch の作成や後片付けを調べ始めるとき。
- apply 実行中 process の pid 管理、停止、stale process 判定など、apply 固有の runtime 状態操作を確認したいとき。
- apply fork の対象ファイル列挙、所見適用 loop、編集禁止対象差分の rollback、commit、report 生成を追いたいとき。
- apply 結果を session branch へ取り込む merge、想定外差分の検出や force-resolve、merge conflict report、join 後 cleanup を確認したいとき。
- 未 join の apply run を破棄して ready 状態へ戻す cleanup と利用者向け出力を確認したいとき。

## Do not read this when
- apply 以外のサブコマンド、session 作成・終了、一般的な state model、branch 名規則の共通仕様を調べたいとき。
- git command 実行 wrapper、state file 読み書き、worktree root、report root、config 読み込みなどの汎用 runtime だけを確認したいとき。
- Codex CLI に渡す prompt の詳細、INDEX.md エントリー生成、oracle/realization の一般ルールだけを調べたいとき。
- apply fork の report 表示だけ、process 停止だけ、join だけ、abandon だけのように関心対象が明確な場合は、このディレクトリ全体ではなく該当する下位実装へ直接進めるとき。

## hash
- c04d60ab8bfa7134bc1314c6a9855c6a8431568ae612a5b807f00312a1002884

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
- eval-oracle サブコマンドの実行入口として、indexing preflight、CLI runtime 経由の実行、active session branch 検証、isolated review worktree 作成、oracle target 列挙、レビュー loop 実行、INDEX 変更 commit と merge、report 出力までの全体制御を担う。
- レビュー対象列挙、レビュー loop、report rendering、review branch merge や conflict 解決などの詳細処理は別モジュールから再公開し、このモジュール自体はそれらを組み合わせる orchestration 層として位置づく。

## Read this when
- eval-oracle の起動条件、scope validation、active session branch や clean worktree の前提条件、run worktree と review branch のライフサイクルを確認したいとき。
- oracle review の一連の流れで、対象列挙、Codex 実行、INDEX 変更 commit、session branch への merge、report 書き出しがどの順序で接続されるかを追いたいとき。
- eval-oracle 実行失敗時にも report を書き出して path を表示する制御や、作成した worktree と branch の後始末を確認したいとき。
- 他の review 系 helper がサブコマンド公開面からどの名前で再公開されているかを確認したいとき。

## Do not read this when
- oracle target の列挙条件そのものを変更したい場合は、対象列挙を担当するモジュールを直接読む。
- Codex を使った review loop の prompt、反復制御、finding の merge operation を調べたい場合は、review loop を担当するモジュールを直接読む。
- review report の表示形式、section rendering、report file 書き出し内容を変更したい場合は、report 生成を担当するモジュールを直接読む。
- review branch の merge、INDEX 変更 commit、conflict 解決、worktree status path の詳細だけを調べたい場合は、review index 操作を担当するモジュールを直接読む。

## hash
- 3ef6d1bc545ad76b9bbd90750ee81f80b445e4d1ddb926c3a5e83f370594ccb0

# `review_index.py`

## Summary
- review worktree で生成された索引変更の扱いと、review branch を session branch へ取り込む際の索引競合処理を担う実装。
- 変更対象が索引文書だけであることを検査し、必要な場合だけ git add/commit を行い、merge 時に索引文書だけの競合なら ours 側または削除で自動解決する。
- git status の porcelain 出力から変更 path を抽出する補助処理と、未マージ stage に ours が存在するかを判定する補助処理も含む。

## Read this when
- eval-oracle や review worktree が生成した索引変更を、どの条件で commit するか確認・変更したいとき。
- review branch の merge 失敗時に、索引文書の競合だけを自動解決する挙動を確認・変更したいとき。
- review worktree の差分に索引文書以外が混ざった場合のエラー条件やメッセージを確認・変更したいとき。
- git status、git diff、git merge、git checkout、git rm、git commit、git ls-files を使った review indexing 周辺の制御を追いたいとき。

## Do not read this when
- 索引文書の本文生成ルールやエントリー内容の仕様を知りたいだけのとき。
- 通常のサブコマンド引数定義、CLI ルーティング、ユーザー向け出力形式を調べたいとき。
- review worktree や review branch に関係しない一般的な git helper の実装を探しているとき。
- oracle file や realization file の概念定義そのものを確認したいとき。

## hash
- 5ceecd964dac04fabef32a48030cd482c962333599d7ac5e6c395fb5ac83e7ea

# `review_loop.py`

## Summary
- review oracle の finding を、列挙、重複整理、検証、判定の順に反復処理する実行ロジックを扱う。
- oracle 由来の指摘候補を保持し、finding_id や検証理由、判定結果などの内部状態を補完しながら、Codex 実行関数へ各段階のパラメータを渡す入口である。
- finding の oracle path 解決、対象 oracle ごとの既存 finding 抽出、merge operation の検証と適用も同じ責務内に含む。

## Read this when
- review oracle の finding enumerate/merge/validate/judge の制御順序、反復回数、終了条件を確認または変更したいとき。
- finding の初期フィールド、finding_id 採番、advocate/challenger 理由、verdict、judge_reason の扱いを確認したいとき。
- merge finding の delete、replace、merge operation の入力検証、target_ids の重複・未知 ID 検出、置換後 finding の追加処理を確認したいとき。
- finding に含まれる oracle_path を実パスへ解決し、特定 oracle に関連する finding を絞り込む挙動を調べたいとき。
- review oracle 用 builder 関数と codex 実行関数のつなぎ込み、log root、worktree、config の渡し方を追いたいとき。

## Do not read this when
- 個々の review oracle プロンプトや Structured Output パラメータの文章そのものを確認したいだけなら、builder 側を直接読む。
- review oracle の反復回数など設定値の定義や読み込みを確認したいだけなら、設定モデル側を読む。
- 通常の CLI サブコマンド登録、引数解析、ユーザー向け出力の入口を確認したいだけなら、サブコマンドの上位実装を読む。
- oracle path トークン全般の定義や `<work-root>` などの解決規則そのものを確認したいだけなら、path model 側を読む。
- テストで期待される外部挙動や回帰条件を探したいだけなら、対応する realization test を読む。

## hash
- ea2d43547d6cb573c0381fe20ab8ef39eac09ed6c30d2ccf19303787816c740f

# `review_report.py`

## Summary
- eval-oracle のレビュー結果レポートを Markdown と YAML frontmatter の文字列として組み立て、review_oracle レポート保存先へ書き出す処理を担う。
- レビュー対象 oracle file、finding の severity/verdict、実行中エラー、review 用 branch/commit 情報、session 情報から、集計値・判定文・finding セクション・oracle path 表示を生成する。
- oracle path を利用者向け表示に整える補助処理と、frontmatter field、finding section、最終 verdict の描画 helper を同じ責務内に持つ。

## Read this when
- eval-oracle のレポート本文、frontmatter、見出し、判定文、finding の表示内容を変更したいとき。
- fatal/minor finding、accept/reject、エラー発生、レビュー対象 0 件などの条件がレポート結果にどう反映されるかを確認したいとき。
- review_oracle レポートの保存先作成、ファイル名生成、Markdown 書き込みの流れを確認したいとき。
- oracle file の表示パスを、repo root 相対または oracle 起点の表記へ整える処理を調べたいとき。

## Do not read this when
- CLI 引数の定義、サブコマンド登録、eval-oracle 実行フローそのものを調べたいだけのとき。
- oracle file の検出、finding の生成、LLM レビュー、accept/reject 判定ロジックを調べたいとき。
- reports directory や timestamp の共通仕様を変更したいとき。
- 生成済みレポートを読む、またはレポート内容を利用する側の処理を探しているとき。

## hash
- adbeaff12d3e31ebe81492b8ebc4dc04c0110085a5987f1a4ad86833c0d6da0a

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
- session 系サブコマンドの実装群を収める領域。通常 branch から session branch を開始する処理、active session branch を home branch へ取り込む処理、merge せず破棄する処理、およびパッケージ境界だけを担う初期化要素への入口になる。
- 各サブコマンドは CLI runtime を通じた制御フローを中心に持ち、事前条件検証、clean worktree 確認、branch 切り替え、state file 更新、session branch の削除、失敗時の扱いなど、session 操作単位の実行順序を確認するための読む先を分けている。

## Read this when
- session branch の開始、home branch への取り込み、merge しない破棄など、session 系サブコマンドごとの実行条件・状態遷移・branch 操作・利用者向け出力の読む先を選びたいとき。
- active session の重複検出、managed branch 上での禁止判定、home branch の存在確認、session/apply state の事前条件など、session 操作固有の precondition を調べる入口が必要なとき。
- session branch の cleanup、削除失敗時の warning、rollback、merge conflict 解決依頼など、session 操作中の失敗時挙動をどの実装で確認すべきか切り分けたいとき。
- session 系実装のパッケージ境界だけを確認し、具体的なサブコマンド処理へ進む前にこの領域の役割を把握したいとき。

## Do not read this when
- session state schema、apply state schema、state file の読み書き helper、path model、git 実行 wrapper、CLI runtime など、複数サブコマンドから使われる共通基盤そのものを調べたいとき。
- 共通 CLI ルーティング、サブコマンド登録全体、または session 以外のサブコマンド実装を調べたいとき。
- merge conflict 解決で Codex CLI に渡す依頼内容や indexing preflight の詳細など、session join から委譲される外部処理の中身だけを変更したいとき。
- oracle file や realization file の定義、INDEX.md の生成方針、コード品質基準など、リポジトリ全体の仕様・標準を確認したいとき。

## hash
- 3769518a6a8e814afc5886bed254fbc836767dcaf493698140751fa01d112050

# `tui.py`

## Summary
- 対話的な依頼文編集から実行条件の解決、完全なプロンプトの保存、Codex TUI 起動までをつなぐサブコマンド実装。
- TUI 用の元プロンプト作成、利用可能なエディタ選択、編集結果の読み取り、解決済みパラメータからの呼び出し条件構築を扱う。
- Markdown 見出しを構造化文書へ変換する処理や、TUI parameter JSON の入れ子形式から値を取り出す補助処理もここにまとまっている。

## Read this when
- 対話的にユーザーの依頼文を編集してから Codex TUI を起動する処理を変更したいとき。
- TUI 実行前のパラメータ解決、許可する file access mode、完全プロンプト生成、構造化出力 schema path の扱いを確認したいとき。
- 元プロンプトと完全プロンプトを TUI log 領域へ保存する条件やパス生成を調べたいとき。
- TUI 起動前に `.cmoc` ignore を保証する処理や、現在の repository/work root context から TUI 本体へ渡す値を確認したいとき。
- エディタ選択順、エディタ異常終了時のエラー、HTML comment を除去した元プロンプト読み取りの挙動を変更したいとき。
- ユーザー入力の Markdown 見出しを StructDoc 階層へ変換する fence 対応の parser 挙動を確認したいとき。

## Do not read this when
- 通常の非対話 CLI 実行、Codex exec 呼び出しの低レベル実装、runtime 共通処理そのものを調べたいだけのとき。
- TUI 用パラメータを解決する prompt builder の内容だけを変更したいときは、その builder 側を読む。
- 完全プロンプトの具体的な構成部品やレンダリング規則だけを調べたいときは、prompt/struct document 側を読む。
- 設定ファイルの読み込み、repo root/work root の定義、timestamp 生成、`.cmoc` ignore の共通仕様だけを確認したいときは runtime や basic path 関連を読む。
- サブコマンド登録や CLI 全体の dispatch を調べたいだけなら、上位の CLI entrypoint や sub command 集約側を読む。

## hash
- 326ae555cfcdc3e522e8c3c69415e18cb555817e18476f9b9fd534d9914af102
