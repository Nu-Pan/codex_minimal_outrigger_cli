# `apply`

## Summary
- apply 系サブコマンドの実行処理をまとめる実装領域。apply run の開始、破棄、取り込み、実行時補助、結果レポート生成までを扱い、session branch と apply branch/worktree の間で状態・差分・後片付けを制御する入口になる。
- ユーザー操作単位の処理だけでなく、linked worktree の特定、apply process の PID 管理、実行中 process の停止、差分要約や report 保存など、apply の lifecycle を支える補助処理も含む。

## Read this when
- apply fork、apply join、apply abandon の実行条件、状態遷移、branch/worktree 操作、cleanup の流れを調べたいとき。
- apply run が session state、apply branch、apply worktree、process ID file、report をどの順序で作成・更新・削除するかを追いたいとき。
- apply fork の finding 列挙・適用 loop、編集禁止対象への差分検出、未収束時や失敗時の扱い、commit subject 生成との接続を確認したいとき。
- apply join で許容される差分、想定外差分の検出、force resolve、merge conflict report、INDEX.md だけの conflict 自動解決を確認したいとき。
- apply abandon で active run を破棄する条件、実行中 process の停止、欠落した branch/worktree を warning として扱う境界を確認したいとき。
- apply fork の成功・失敗 report の内容、差分要約、要約失敗時の fallback、保存タイミングを確認したいとき。

## Do not read this when
- apply 以外のサブコマンドや CLI 全体の dispatch、共通の引数 parser だけを調べたいとき。
- session state の schema、branch 名規則、root path 定義、git wrapper、設定読み込みなどの共通基盤だけを確認したいとき。
- Codex CLI に渡す prompt や structured parameter の内容だけを変更したいとき。
- oracle routing、INDEX.md エントリー生成、正本仕様文書そのものを確認したいだけのとき。
- apply の個別操作ではなく、全体のユーザー向け仕様や上位ドキュメントから読むべきか判断したいとき。

## hash
- 3e086db1dc85eabf28fee26b66a668d8f9677e31afc8d29c0ac765c3679b8093

# `indexing.py`

## Summary
- 作業ツリー内の各階層について、対象外の子要素を除外しながら目次対象を列挙し、既存エントリーのハッシュ再利用または Codex 呼び出しによる再生成で目次本文を更新する処理を担う。
- 目次更新を排他ロック下で実行し、更新された目次だけを git に追加して専用コミットへ保存する、サブコマンド本体と preflight 用の入口を含む。
- 目次エントリーの必須セクション検証、対象内容の抽出、対象ハッシュ計算、Structured Output から Markdown へ描画する処理まで、目次保守の制御フローをまとめて扱う。

## Read this when
- 目次保守サブコマンドの実行順序、preflight での自動更新、または更新後コミットの条件を確認・変更したいとき。
- 目次対象に含めるファイルやディレクトリの判定、除外条件、バイナリ・git ignored・作業ルート直下の memo の扱いを調べたいとき。
- 既存目次エントリーの再利用条件、ハッシュ検証、エントリー生成プロンプトへ渡す対象内容、または Structured Output からの描画処理を確認したいとき。
- 目次生成を並列化する設定値の使われ方や、Codex 実行関数が未指定の場合のエラー経路を追いたいとき。

## Do not read this when
- 個々の目次エントリーに入れる自然言語内容や Structured Output のプロンプト定義だけを調べたい場合は、エントリー生成パラメータを組み立てる側を読む。
- git コマンド実行、設定読み込み、ハッシュ計算、バイナリ判定、git ignored 判定などの低レベル runtime helper の詳細を確認したいだけなら、それぞれの runtime 実装を読む。
- 目次保守以外のサブコマンドの CLI 挙動や dispatch を調べたい場合は、そのサブコマンド実装または CLI 登録側を読む。
- 正本仕様断片としての目次ルーティング方針や oracle と realization の関係を確認したい場合は、実装ではなく該当する oracle 文書を読む。

## hash
- 5caec3c108af017e4f099f3725503817a9313d74c0bfd0de22795909a98b29d8

# `init.py`

## Summary
- 作業ツリーを cmoc が扱える初期状態へ同期するための init サブコマンド実装。実行前の利用者差分を init commit に混ぜないよう退避・復元しつつ、cmoc 用 ignore と設定同期を行い、成功時の Markdown 出力を組み立てる。
- ログ作成前に必要な ignore 保証、.gitignore の HEAD・index・worktree 状態の保存と復元、実行前 staged patch の復元など、init 固有の副作用制御を扱う入口。

## Read this when
- init サブコマンドの挙動、出力、commit 作成条件、または実行時に触れる ignore・設定同期の流れを確認・変更したいとき。
- cmoc 初期化時に利用者の staged 差分や .gitignore 状態を保護する処理を調べたいとき。
- ログ作成前に cmoc 用 ignore を保証する理由や、その事前状態を後続の復元処理へ渡す仕組みを確認したいとき。

## Do not read this when
- init 以外のサブコマンドの CLI 制御や出力を調べたいだけのとき。
- work root の判定、git コマンド実行、設定同期、cmoc ignore の具体的な共通実装そのものを調べたいとき。
- 正本仕様断片やテスト期待値を確認したいとき。

## hash
- 40c8a1439f1e36929bf9fd0e25dc79c5c54a820fe6578bff3ea04bf81445060f

# `review.py`

## Summary
- 現在の active session branch 上の oracle review コマンド実装を扱う。scope 検証、clean worktree 確認、isolated review worktree の作成、review 対象列挙、review loop 実行、INDEX 変更 commit と merge、worktree と branch の後始末、report 出力までの制御フローを束ねる入口である。
- review oracle 周辺の分割済み処理を再公開する facade としても機能し、target 列挙、loop、report、review index merge/conflict 処理などの下位モジュールへ進む前の接続点になる。

## Read this when
- review oracle サブコマンドの実行順序、前提条件、失敗時 report 出力、isolated review worktree のライフサイクルを確認したいとき。
- scope が session/full のどちらとして処理されるか、active session branch や clean worktree がどこで要求されるかを追うとき。
- review worktree 上で oracle file を列挙し、review loop を実行し、INDEX 変更を session branch へ取り込む一連の orchestration を変更するとき。
- review oracle 関連 helper の公開面や、他モジュールから import される互換的な入口を確認するとき。

## Do not read this when
- 個別の review 対象列挙規則だけを確認したい場合は、review targets を扱う下位モジュールへ直接進む。
- Codex に渡す review loop の詳細、finding の merge operation 適用、プロンプトや反復処理の中身だけを確認したい場合は、review loop を扱う下位モジュールへ直接進む。
- review report の本文生成、path 表示、finding section の render、report file 書き込み形式だけを確認したい場合は、review report を扱う下位モジュールへ直接進む。
- review index の commit、merge、conflict 解決、worktree status path の詳細だけを確認したい場合は、review index を扱う下位モジュールへ直接進む。

## hash
- 683f45afe7813f49a04b82cb6d1ba48c5faf9f4a588193292002d1d82a68fc2d

# `review_index.py`

## Summary
- review 用 worktree に作られた索引変更を検査して commit し、review branch を session branch へ merge するための git 操作を扱う実装。
- 差分対象を INDEX.md のみに制限し、非対象差分がある場合は CmocError にし、merge conflict が INDEX.md だけなら ours で解決して commit する制御を担う。

## Read this when
- review oracle が生成した索引変更だけを commit する処理を確認・変更したいとき。
- review worktree の git status から変更パスを取り出す処理、特に rename/copy を含む porcelain v1 -z の解釈を確認したいとき。
- review branch の merge 失敗時に、INDEX.md だけの conflict を自動解決する条件や手順を確認したいとき。
- review oracle が INDEX.md 以外を変更した場合のエラー化や、差分がない場合に commit しない挙動を確認したいとき。

## Do not read this when
- INDEX.md の本文生成ルールやエントリー内容の品質基準を調べたいだけのとき。
- 通常のサブコマンド引数、CLI 出力、ユーザー向けコマンド定義を確認したいとき。
- review oracle の実行プロンプト、レビュー観点、索引文書そのものの内容を確認したいとき。
- git コマンド実行 helper や CmocError の共通仕様を調べたいとき。

## hash
- 42f2f7a768474b5b07e47ec55750ce65ea6bba3439c7cd667355dc5c6ca6efa9

# `review_loop.py`

## Summary
- review oracle の finding 収集から統合、検証、判定までの反復制御を担う実装。oracle ごとの既存 finding 関連付け、finding_id や判定用フィールドの初期化、merge 操作の適用と検証、advocate/challenger/judge への Codex 実行委譲を扱う。
- review oracle 用 builder が作る各 Codex 実行パラメータと、設定された反復回数、作業ツリー基準の path 解決を組み合わせて、最終的な finding list を返す入口として位置づく。

## Read this when
- review oracle の enumerate、merge、validate、judge の実行順序や反復終了条件を確認したいとき。
- finding の `finding_id`、`advocate_reasons`、`challenger_reasons`、`verdict`、`judge_reason` がどこで初期化・更新されるかを追いたいとき。
- merge finding の delete、replace、merge 操作がどの条件で受理または拒否されるかを確認したいとき。
- finding に含まれる oracle path が絶対パス、パスキーワード付きパス、作業ツリー相対パスとしてどう解決されるかを調べたいとき。
- review oracle の Codex 呼び出しに渡す root、cwd、config、purpose の組み立てや、Structured Output からの finding/reason/verdict 取り出しを変更したいとき。

## Do not read this when
- 各 review oracle プロンプトや Structured Output schema 自体を確認したいだけなら、builder 側の oracle review parameter 定義を読む。
- 設定値の定義、既定値、読み込み方法を確認したいだけなら、設定モデル側を読む。
- path キーワードの定義や実パス解決規則そのものを確認したいだけなら、path model 側を読む。
- CLI サブコマンドの引数定義やユーザー向け入出力の入口を確認したいだけなら、サブコマンド登録・実行入口側を読む。

## hash
- d116a58b5c91dcc0446b89b792e5dd64c675efd7a66b3858cb3fbbfd92e54581

# `review_report.py`

## Summary
- レビュー対象の oracle 群に対する判定結果を Markdown レポートとして組み立て、レポート保存先へ書き出す実装。
- 評価対象数、受理・却下された fatal/minor finding 数、実行ブランチやコミット情報などを frontmatter にまとめ、本文には verdict、評価対象一覧、finding 一覧を出力する。
- レビュー処理失敗、対象なし、fatal 受理あり、minor 受理あり、問題なしの順に結果文言を決め、oracle 配下のパスは読みやすい相対表示へ整形する。

## Read this when
- oracle レビュー結果のレポート生成、保存先、frontmatter、本文構成、verdict 文言を確認または変更したいとき。
- finding の severity や verdict ごとの集計、accepted/rejected の表示順、finding セクションの出力形式を調べたいとき。
- レポート内で表示される oracle file のパス表記や、root からの相対化処理を確認したいとき。

## Do not read this when
- oracle file の探索条件、review 実行フロー、git ブランチ操作、LLM による finding 判定そのものを調べたいとき。
- CLI 引数定義、サブコマンド登録、セッション状態の作成・保存、レポート保存ディレクトリや timestamp の共通仕様を調べたいとき。
- oracle 正本仕様の内容や、review が検出すべき問題の基準を確認したいとき。

## hash
- 5a4bc1bc25bc2c3390133302a704cfab266f75d5d961859b561a4a82777866ee

# `review_targets.py`

## Summary
- review oracle が検査対象にする正本仕様断片を列挙するための実装。scope が全件対象か差分対象かを判定し、差分対象ではセッション開始 commit から現在までに変更された oracle 配下の対象だけへ絞り込む。
- 全件列挙では oracle 配下を再帰的に走査し、ルーティング文書、gitignore 対象、binary file を除外した通常 file だけを返す。

## Read this when
- review oracle の対象 file がどの条件で選ばれるかを確認したいとき。
- scope による全件 review と差分 review の分岐、またはセッション開始 commit が無い場合の挙動を確認したいとき。
- oracle 配下の file 列挙で、ルーティング文書、gitignore 対象、binary file が除外される理由や実装位置を確認したいとき。
- git diff の結果と実際に返る review 対象の対応を調べたいとき。

## Do not read this when
- review oracle の検査内容、診断基準、出力文面を確認したいとき。
- review サブコマンドの CLI 引数定義、dispatch、表示形式を確認したいとき。
- oracle file や realization file の正本上の定義そのものを確認したいとき。
- 対象列挙ではなく、git 実行 helper、binary 判定、gitignore 判定、セッション状態の保存形式を確認したいとき。

## hash
- f42029951fa3338498710cca446b7ee6dbf8f87039fc10726d2cecc385a0c05c

# `session`

## Summary
- session サブコマンド群の実行処理を集めた領域であり、session branch の作成、home branch への join、merge しない破棄といった利用者向け操作の入口になる。
- 各サブコマンド実装は、実行前条件の検証、git branch/worktree 操作、session state 更新、成功時出力、失敗時のエラー化や rollback など、コマンド固有の制御を扱う。
- session 操作のうち、作成、join、破棄のどの処理を読むべきかを選ぶための階層であり、状態ファイル schema や git helper などの低レベル共通処理へ進む前の入口になる。

## Read this when
- session branch を作成する、home branch に join する、または merge せず破棄する利用者向けサブコマンドの実行条件や副作用を調べたいとき。
- session 操作が worktree の clean 確認、managed branch 判定、active state 判定、home branch への切り替え、branch 削除、session state 更新をどの順序で行うかを追いたいとき。
- session join 中の merge conflict 解決、session abandon 中の cleanup 失敗 rollback、session fork 中の active session 重複拒否など、各サブコマンド固有の失敗処理を確認したいとき。
- session 系サブコマンドが共通 CLI 実行ラッパーや indexing preflight にどう接続されるかを確認したいとき。

## Do not read this when
- session state や apply state のデータ構造、保存形式、状態ファイル path の組み立て規則そのものを調べたいとき。
- git 実行 wrapper、branch 判定、worktree 清潔性判定、cmoc ignore 管理、timestamp 生成、共通エラー型などの低レベル helper 実装を調べたいとき。
- Typer アプリ全体のサブコマンド登録、CLI ルート構造、または session 以外のサブコマンド領域を調べたいとき。
- Codex CLI に渡す conflict resolution prompt や parameter の具体的な生成ロジックだけを調べたいとき。

## hash
- 34b44bb590ff21e4793d3db8c0806fcfc0a011f54cc056d8ce1a67f7548b722d

# `tui.py`

## Summary
- 対話的な依頼入力から Codex TUI を起動するまでのサブコマンド本体を扱う実装。利用者用プロンプトの作成とエディタ起動、AI による実行パラメータ解決、完全プロンプト保存、TUI 呼び出し用パラメータ構築を一連の流れとして接続する。
- TUI で許可されるファイルアクセスモードの検証、エディタ選択と失敗時エラー、テンプレートコメントを除いた元プロンプト読み込み、Markdown 見出しから構造化文書への簡易変換、解決済み JSON の値取り出しを含む。

## Read this when
- 対話的な依頼文編集から Codex TUI 起動までの制御フロー、引数構築、保存されるプロンプトの扱いを確認したいとき。
- TUI 用に解決された file access mode や各種標準フラグが、最終的な AgentCallParameter と完全プロンプトへどう反映されるかを確認したいとき。
- 利用可能なエディタの選択順、エディタ異常終了時のエラー、元プロンプトから HTML コメントを除去する処理を変更または調査したいとき。
- 利用者が書いた Markdown の見出しを StructDoc 階層として扱う変換ロジック、または fenced code block 内の見出しを無視する挙動を確認したいとき。
- TUI サブコマンド起動前の indexing preflight 呼び出し位置や、repository root と work root を使った実行コンテキストの渡し方を確認したいとき。

## Do not read this when
- Codex 実行や TUI 起動そのものの低レベルなプロセス実行、設定読み込み、root 判定、ログ領域作成の共通挙動を確認したいだけなら、runtime 側の実装を読む。
- TUI パラメータ解決用プロンプトの内容、解決可能な項目、許可されるファイルアクセスモードの定義を確認したいだけなら、パラメータ解決を組み立てる側の実装を読む。
- 完全プロンプトの共通フォーマットや StructDoc の Markdown レンダリング仕様を確認したいだけなら、プロンプト部品または構造化文書の実装を読む。
- indexing preflight の具体的な検査内容や索引生成の挙動を調査したいだけなら、indexing サブコマンド側の実装を読む。
- 通常の非対話的な exec 系サブコマンドや、TUI 以外のサブコマンドのコマンド処理を調べたい場合は、それぞれのサブコマンド実装を読む。

## hash
- da24e922e6a1930a64a5667c2c3867e90de41524c59de1c97005abece970b630
