# `_support.py`

## Summary
- CLI テストで使う共通補助関数群。最小構成の Git リポジトリ作成、ブランチ状態確認、Codex ホームのテスト用設定、Codex profile 生成の差し替え、偽の Python 実行ファイル作成、apply 用 worktree path 解決をまとめて提供する。
- 外部コマンドとしての Git と Codex 実行制御を伴うテストの前提準備を集約し、個別テストが fixture 作成や monkeypatch の詳細を重複して持たないための入口になる。

## Read this when
- CLI テストで一時 Git リポジトリ、初期 commit、oracle 配下の最小ファイル、追跡済みかつ ignore 対象の oracle ファイルを用意する方法を確認したいとき。
- Codex CLI 実行を伴うテストで、認証済みの最小 CODEX_HOME や profile 生成差し替えの仕組みを使う、または変更するとき。
- テスト内で現在の Git ブランチ名、Git コマンド実行結果、apply 状態から導かれる worktree path を検証する補助処理を探すとき。
- 外部コマンドの代替として実行可能な Python スクリプトをテスト中に生成する必要があるとき。

## Do not read this when
- 個別サブコマンドの期待挙動、CLI 出力、終了コード、状態ファイルの仕様を確認したいだけなら、該当するテスト本文または実装を直接読む。
- pytest の個別ケースやアサーション内容を探しているだけなら、この共通補助関数群ではなく対象機能のテストを読む。
- Codex profile 生成や apply worktree 解決の本体実装を変更する場合は、ここではなく実装側の該当モジュールを読む。
- oracle file や realization file の正本上の定義・標準を確認したい場合は、このテスト補助ではなく oracle 側の文書を読む。

## hash
- 54cf181de55105f9065ad7f515d614e2705529029548b38b874d2326362e0b59

# `test_acp_builder_parameters.py`

## Summary
- ACP builder が生成する AgentCallParameter のモデル種別、reasoning effort、file access mode、prompt 埋め込み内容、structured output schema 参照を検証する realization test。
- apply fork、TUI parameter resolution、index entry、review oracle、session join conflict resolution の builder 出力が、期待される権限・schema・oracle src 参照と一致するかを確認する。

## Read this when
- ACP builder の parameter 設定、prompt 内容、structured output schema path、または oracle schema との一致を変更する。
- TUI resolve parameter、apply fork、review oracle、indexing index entry、session join conflict resolution の builder 実装を変更した後に、既存テスト観点を確認する。
- oracle src に置かれた ACP builder schema を realization 側 builder が正しく参照しているかを調べる。

## Do not read this when
- ACP builder 以外の CLI 挙動や永続状態だけを調べる場合。
- structured output schema の正本内容そのものを確認したい場合は、対応する oracle src の schema を直接読む。
- 個別 builder の実装詳細を修正する入口を探している場合は、対象 builder の realization implementation を直接読む。

## hash
- 3d6cf517dbdce70e881a1f179d3712ec99a5d4f966c9ac9d26b9ca1bdb98079f

# `test_apply_abandon_cli.py`

## Summary
- active apply run を CLI 経由で破棄する外部挙動を検証する realization test。worktree、branch、session state の cleanup、cleanup 対象欠落時の警告、running process 停止、実行位置判定、linked session worktree との境界条件を同じ abandon 操作の文脈で扱う。
- apply process identity の読み取り、child process group を含む停止順序、PID reuse や race 済み終了の扱いなど、abandon 前処理として必要な process 停止ロジックの制御境界も検証する。
- 16,000 文字を超えるが、active apply run の破棄という単一責務に閉じ、同じ state fixture と境界条件を共有するため、分割せず読み取り文脈を一箇所に保っている。

## Read this when
- apply abandon の CLI 挙動、出力、終了コード、state 遷移、apply worktree と apply branch の削除を変更または確認するとき。
- running apply を abandon する際の process identity 読み取り、tracked child process group の停止、PID reuse 防止、終了 race の扱いを変更または確認するとき。
- apply worktree 内、linked session worktree、linked apply worktree、stale apply branch など、abandon 実行位置ごとの許可・拒否条件を調べるとき。
- cleanup 対象がすでに存在しない場合の警告成功、または破損 state や process identity 欠落時に cleanup 前で拒否する挙動を確認するとき。

## Do not read this when
- apply abandon 以外の apply サブコマンドの通常フローや Codex 実行結果の品質を調べたいとき。
- session fork、init、git helper、runner などの共通 fixture や補助 API 自体の実装を確認したいとき。
- oracle file の正本仕様や実装標準を確認したいとき。
- active apply run の破棄に関係しない一般的な worktree、branch、session state の挙動を調べたいとき。

## hash
- ec0375e8de29f038d1dc8b4010eae864fadb5ba208f43ab7385d198d6ddc6158

# `test_apply_fork_cli.py`

## Summary
- apply fork コマンドの CLI 経由の実行、Codex 呼び出し、session state 更新、apply branch/worktree 作成、設定読み込み失敗時の中断、.gitignore の扱い、対象 path 正規化を検証する realization test。
- apply fork が session branch と現在の HEAD を基準に apply run を開始し、完了時に一時的な pid や旧 apply worktree 表現を残さないことを確認する。
- realization file 判定に関わる memo、oracle、管理ディレクトリ、INDEX/AGENTS、binary file、tracked ignored file の対象選別を確認する入口になる。

## Read this when
- apply fork の外部挙動、state 遷移、apply branch 名、apply worktree 配置、Codex loop 呼び出し順を変更する。
- linked worktree 上で apply fork を実行する挙動や、oracle snapshot commit と apply branch の起点を確認する。
- apply fork 実行時の .cmoc ignore 保証、session 側 .gitignore の非破壊性、apply branch 側での .gitignore 編集可否を変更または検証する。
- apply fork の設定ファイル読み込みエラー時に apply run を開始しない挙動、標準出力へのエラー表示、pid/state/branch の未生成を確認する。
- apply fork の対象正規化で、root 直下 memo、管理 path、INDEX/AGENTS、oracle path、binary file、tracked ignored file の扱いを確認する。

## Do not read this when
- apply fork 以外のサブコマンドの CLI 挙動だけを確認したい。
- Codex 実行器そのものの統合挙動や LLM 出力品質を確認したい場合で、apply fork 側の呼び出し・状態更新は関係しない。
- path model や realization/oracle file の定義そのものを確認したい場合は、正本仕様側を先に読む。

## hash
- 8132fa30a1ec010f5fecea77ff23e4bf3b34c02c05eaad6deab39af8f9353f9b

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 実行について、所見列挙、所見適用、commit、変更要約、report 生成、session state 更新、再検査制御をまとめて検証するテスト。
- change summary / file finding enumeration / finding application の ACP builder が src 単体 PYTHONPATH や packaged layout から import できること、oracle source の schema を参照すること、標準 prompt と path placeholder を含むことを確認する。
- apply fork report の converged / unconverged / error 表示、変更要約、未追跡 file・削除 file の差分扱い、変更 file 再調査、file access rule violation recovery、rolling apply fork の対象 commit 選択を CLI 経由で検証する。

## Read this when
- apply fork の report 内容、終了コード、収束判定、未収束判定、error report、変更要約生成の挙動を確認・変更したいとき。
- apply fork が所見適用後の変更 file を再調査する制御、新規 directory 配下の展開、所見適用が差分を作らない場合の扱いを確認したいとき。
- apply fork 関連 ACP builder の import 可能性、prompt 構成、structured output schema 参照、packaged layout 対応を変更したいとき。
- apply fork の commit 作成、session state の apply branch 更新、file access rule violation recovery、rolling fork が前回 apply join 後の変更だけを対象にする挙動を検証したいとき。

## Do not read this when
- apply fork 以外の CLI サブコマンドや session fork / join 単体の挙動だけを確認したいとき。
- apply fork の内部 helper の局所的な純粋関数だけを確認する場合で、CLI 経由の report・再検査・state 更新まで追う必要がないとき。
- Codex CLI や LLM 出力品質そのものを検証したいとき。

## hash
- dd0c7c5f5b265d7071b5a91321c9ca416fc6ac144a256bc1c1e29f49d1b2abbd

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証するテスト群。正常 join、apply worktree からの実行、linked session worktree への反映、後片付け、state 更新、report 生成を扱う。
- join 可否を分ける境界条件として、stale apply branch、dirty apply worktree、想定外差分、force resolve、削除差分、rename target、memo 判定、gitignore 変更、merge conflict、INDEX.md conflict の扱いを同じ文脈で確認する。
- ファイル自体は大きいが、同じ fixture と git 状態を使う apply join の成功条件・拒否条件を一箇所で読むための凝集したテストとして位置づけられている。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 内容、state 更新、worktree/branch cleanup を変更または確認したいとき。
- apply join が session worktree と apply worktree のどちらから実行されたかで cleanup や merge 先がどう変わるかを確認したいとき。
- apply join で許可される差分と拒否される差分の境界、または --force-resolve による revert 挙動を確認したいとき。
- apply join の merge conflict 検出、INDEX.md conflict の自動解決、想定外差分 report の内容を変更または検証したいとき。
- apply join 周辺の helper が、変更パスの抽出、memo 判定、expected apply/session change 判定をどう扱うべきか確認したいとき。

## Do not read this when
- apply fork の Codex 実行や apply worktree 作成そのものを確認したいだけのとき。
- session fork、init、repository fixture など join 前提を作る別 CLI の単独挙動を確認したいとき。
- apply join の内部実装だけを局所的に読みたい場合で、外部挙動テストの期待値を確認する必要がないとき。
- oracle 正本仕様や realization standard の本文を確認したいとき。
- INDEX.md ルーティング文書の生成規則や他ファイルへの入口を確認したいとき。

## hash
- 46beb0d4dff71ffe132541609d84cd7a44f9f350ad4618a383b8daf3c40c943f

# `test_basic_runtime.py`

## Summary
- cmoc の基礎 runtime 契約を横断的に検証する realization test。root placeholder と worktree 解決、config 既定値と検証、CmocError の表示、CLI preflight と parse error、subcommand log、`.cmoc` ignore、FileAccessMode から Codex sandbox/profile への変換、binary 判定、session state の branch 名検証を同じ実行前提として扱う。
- 個別サブコマンドより下位の共通 runtime 境界をまとめて確認するための回帰テスト群であり、root 状態・共通 fixture・権限 profile の相互作用を一箇所で追う入口になる。

## Read this when
- root placeholder、repo root、run root、work root、linked worktree、管理対象 worktree の作成・削除条件に関わる挙動を変更または調査するとき。
- CmocError、CLI error report、Click parse error、stdout/stderr の扱い、preflight 失敗時の副作用抑止、completion probe の初期化回避を確認するとき。
- config の既定値、codex model/reasoning effort 名の検証、duration 表示、subcommand log の生成衝突回避、`.cmoc` の ignore 追加を扱うとき。
- FileAccessMode の永続化値、sandbox mode 変換、Codex profile の writable/readable root、追加書き込み許可 path、session join conflict target の許可・拒否条件を扱うとき。
- session/apply branch 名から session id や state を読む制御、または binary 判定の読み取り範囲を変更するとき。

## Do not read this when
- 個別サブコマンド固有の业务ロジック、プロンプト構築、indexing 内容、session fork/join の詳細仕様だけを確認したいときは、より直接その領域のテストや実装へ進む。
- oracle file の正本仕様そのもの、oracle doc/src/test の構成、または INDEX エントリー生成規則を確認したいときは、oracle 側の該当文書を読む。
- 単一 helper の内部実装だけを局所的に確認でき、共通 runtime 契約や CLI 実行前提との相互作用を追う必要がないとき。

## hash
- 78014a9810f8e9f8ca85a83b14ef378d8c1a71e7bcf35945aeec24069581f907

# `test_cli_init_tui.py`

## Summary
- init と TUI 起動直前の CLI 前処理を対象に、repository/runtime 準備の外部挙動を検証するテスト。
- .cmoc ignore、既存 staged/unstaged 差分保護、初期設定同期、linked worktree、Markdown prompt 整形、Codex TUI 起動 parameter 構築が同じ利用開始直後の境界で期待通り動くかを確認する。

## Read this when
- init の外部挙動、コミット対象、.gitignore 更新、.cmoc 追跡除外、設定ファイル初期化や既存値保持を変更・確認するとき。
- TUI 起動前の editor 実行、prompt 保存、resolve parameter、launch_tui schema、file access mode、Codex 呼び出し parameter を変更・確認するとき。
- linked worktree 上で init または TUI を実行したときの root/cwd、ログ保存先、ignore 設定、schema 生成先を確認するとき。
- subcommand 実行ログの記録形式や保存場所が init/TUI 境界で維持されるかを確認するとき。

## Do not read this when
- init や TUI 起動前処理に関係しないサブコマンドの挙動だけを確認するとき。
- Codex/LLM の出力品質そのものや TUI 起動後の対話内容を検証したいとき。
- 設定値の定義元や prompt 構築仕様そのものを読みたいときは、対応する実装または oracle 側の根拠を直接確認する。

## hash
- 001f4f4228a451b5eec2906718bdc49f53ad9f91119a4b58b6794652f8fd69d7

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行・TUI 起動の runtime 境界を検証するテスト群。プロファイル生成、作業ディレクトリ、sandbox writable roots、schema 出力先、プロンプト stdin、call log、subprocess process group、missing CLI や nonzero exit のエラー報告を扱う。
- agent 呼び出し後のファイルアクセス規則検査とリカバリを重点的に検証する。oracle、blocked runtime root、git directory、cmoc log、readonly realization diff、ignored temporary cache、preexisting forbidden diff、session join conflict 許可対象などの差分判定を扱う。

## Read this when
- Codex runtime の exec/TUI 起動引数、CODEX_HOME profile、cwd、stdin、output schema、call log の挙動を変更・確認する。
- FileAccessMode ごとの読み書き許可、post-call diff 検査、違反時リカバリ、許容される一時キャッシュや ignored file の扱いを変更・確認する。
- Codex subprocess wrapper の process group、apply process tracking env の扱い、Codex CLI 不在や終了コード異常時のエラー表示を変更・確認する。

## Do not read this when
- agent call parameter の値オブジェクト自体、model class、reasoning effort、file access mode の定義だけを確認したい場合。
- Codex runtime ではなく、通常の git 操作 helper、repo fixture 作成、テスト支援 executable 生成の実装だけを確認したい場合。
- oracle 文書や realization 実装の内容そのものを変更する作業で、Codex CLI 呼び出し後のアクセス検査や runtime 境界に関係しない場合。

## hash
- e217e0d227d85d08873b2b1cb1275442b7b4564116d374a0a846a3c03a0a1378

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を扱う realization test。環境変数未設定時の既定値、相対値の解決基準、プロファイル配置、呼び出しログへの記録、Codex CLI 起動前に失敗すべき認証環境不備を検証する。

## Read this when
- Codex CLI 呼び出しに渡す CODEX_HOME、プロファイル、作業ディレクトリ、呼び出しログの挙動を変更または確認したいとき。
- Codex home が存在しない、ディレクトリではない、認証情報がない場合のエラー文言や失敗タイミングを変更または確認したいとき。
- file access mode によって Codex CLI の実行 cwd が変わるケースで、相対 CODEX_HOME の解決挙動を確認したいとき。

## Do not read this when
- Codex CLI の標準出力イベント処理、capacity wait、一般的な agent call 結果処理だけを確認したいとき。
- Codex home ではなく、repository path、oracle path、run root、work root の一般的なパスモデルを確認したいとき。
- CLI 利用者向けコマンド定義や設定ファイル全体の schema を確認したいとき。

## hash
- b92995fbdd0a93c847ae8a31d4ea6534df7c8b4185810379c129ee1b456241d7

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 後の `run_codex_exec` の retry 状態機械を検証するテスト。quota availability probe、resume token、再実行、call log、subcommand log、`CODEX_HOME` と cwd、並列呼び出し時の代表 probe 共有を同じ外部挙動として扱う。
- ファイルは大きいが、quota 待機から復帰する Codex exec の観測点を一箇所で追うための凝集した回帰テストとして位置づけられている。

## Read this when
- Codex exec が quota exceeded を返した後の probe、resume、rerun、poll limit、失敗時挙動を変更・調査する。
- quota retry に関する codex call log、subcommand log、prompt/stdout/stderr/output log の記録内容や順序を変更・確認する。
- `CODEX_HOME` が相対パスの場合の cwd、file access mode ごとの `--cd`、quota 待機中のファイルアクセス違反回復を調査する。
- 複数の `run_codex_exec` が同時に quota 待機した場合に、probe を代表 1 回だけ実行し、待機中の呼び出しが同じ結果で復帰または失敗する挙動を確認する。

## Do not read this when
- 通常の Codex exec 成功系、引数構築、JSON 出力読み取りだけを確認したい。
- quota exceeded と関係しない runtime error、設定読み込み、CLI サブコマンド全般のテストを探している。
- oracle builder の定義そのものや quota probe prompt の正本仕様を確認したい。

## hash
- 086d72d3abbcb3b4b80e74660e39a46911e0c77921b18e6598bafd3ff8ebb7c7

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 挙動を検証する realization test。Structured Output の schema 不一致・出力欠落・空出力・JSON parse failure、capacity error、file access violation 復旧、stdout JSONL 以外の error marker の扱いを、fake Codex 実行ファイルとログ検査で確認する。
- agent call の出力 JSON、call log、prompt log、stdout log、subcommand log event が retry ごとに期待通り記録されるかを確認する入口になる。

## Read this when
- Codex CLI 呼び出しの retry 条件、retry 回数、成功時 result、失敗時 CmocError の外部挙動を変更または確認したいとき。
- Structured Output の schema validation、出力ファイルの欠落・空・不正 JSON に対する再試行とログ内容を確認したいとき。
- capacity error の検出、sleep を伴う再試行、capacity retry log event の扱いを変更または確認したいとき。
- realization write 実行中に oracle 側へ書き込みが発生した場合の復旧順序や、capacity retry より前に file access violation を処理する挙動を確認したいとき。
- stdout JSONL の structured event ではない stderr や通常 stdout 上の文字列を、capacity/quota retry marker として扱わないことを確認したいとき。

## Do not read this when
- Codex CLI 起動コマンドの組み立て、実際の subprocess 実装、ログファイル生成処理そのものを変更したいだけなら、対応する implementation を直接読む。
- agent call parameter の型、model class、reasoning effort、file access mode の定義を確認したいだけなら、基本型定義側を読む。
- repository fixture、Codex home stub、fake executable 作成 helper の詳細を変更したいだけなら、test support 側を読む。
- INDEX.md 生成規則や oracle/realization の概念定義を確認したいだけなら、この retry テストではなく正本仕様断片を読む。

## hash
- 8313d00d0611f65598134671436e71a2d2672817c7c23087ee8913235ceba802

# `test_indexing_cli.py`

## Summary
- INDEX.md 生成・更新、indexing preflight、indexing subcommand、INDEX.md conflict 解決の外部挙動を検証する回帰テスト群。
- 対象列挙、hash 再利用、Codex 生成、commit 対象、dirty worktree 拒否、linked worktree、空ディレクトリ、並列生成、memo 除外、symlink cycle 回避を routing document 更新ワークフローとしてまとめて扱う。

## Read this when
- indexing CLI が INDEX.md を生成・更新・commit する条件を確認したいとき。
- indexing preflight と通常の indexing subcommand で dirty worktree、linked worktree、repo config、commit 対象の扱いがどう違うかを確認したいとき。
- 既存 INDEX.md entry の hash 再利用、malformed entry の再生成、Structured Output schema 不一致の拒否を変更・検証するとき。
- INDEX.md conflict 解決、空ディレクトリへの INDEX.md 配置、並列生成、root 直下 memo 除外、入れ子 memo 対象化、directory symlink cycle 回避に関わる実装を変更するとき。

## Do not read this when
- INDEX.md entry の自然言語内容そのものを設計・更新したいだけで、CLI 境界や git 状態の回帰確認が不要なとき。
- routing document 生成に関係しない subcommand、設定、agent call、apply join の挙動を調べたいとき。
- 単体 helper の内部実装だけを確認したく、外部 CLI 挙動、commit、worktree、git conflict の観測が不要なとき。

## hash
- ba84ba2a5f8fac06dd16494e65b04728e1b72568d45ca51a5e25aa2604e2bf43

# `test_indexing_preflight.py`

## Summary
- Codex 実行前の indexing preflight が、exec/TUI 呼び出し前に INDEX.md 更新を実行し、必要な commit と worktree 選択を行うことを検証する realization test。
- repository lock 待機、index entry 生成や conflict resolution 用途で preflight を skip する条件も扱う。

## Read this when
- Codex 呼び出し前に indexing preflight が走る順序、commit、clean worktree を確認・変更する。
- cwd が別 worktree 配下にある場合、root ではなく cwd 側 worktree を index 更新対象にする挙動を確認・変更する。
- indexing lock の排他待機や、特定 purpose で preflight を skip する条件を確認・変更する。

## Do not read this when
- INDEX.md の本文生成ロジックやエントリー内容の仕様を確認したい場合。
- Codex 実行ラッパーではなく、個別の git helper や repository fixture の詳細を確認したい場合。
- oracle file の正本仕様や INDEX.md ルーティング規則そのものを確認したい場合。

## hash
- 5549e75d6493464e59f5f4cb68232c1fbd9fc7d03b85ee5f6cb6ea3ad4e04099

# `test_packaged_import.py`

## Summary
- packaged layout から review oracle enumerate builder を import できることと、packaging 設定が oracle package を期待した配置で公開していることを検証するテスト。
- 一時的な import 環境を組み立て、builder が schema path と prompt を正しく返せることをサブプロセスで確認する。

## Read this when
- packaged layout、setuptools package-dir、oracle package の import 境界を変更する。
- review oracle enumerate builder の依存関係、schema 参照、prompt 組み立てが配布後の import 環境で壊れていないか確認する。
- oracle src と realization src の配置分離に関わるテスト失敗を調査する。

## Do not read this when
- builder の prompt 本文や schema 内容そのものの詳細仕様を確認したい場合。
- 通常の CLI 動作、入出力、状態管理など packaged import 境界と無関係な挙動を調査する場合。
- 単体の helper ロジックを直接検証するテストを探している場合。

## hash
- cccc21d8925cdcc0798ceaddea1bf75e25fbadf671e8b6ee5e76317db75fb27f

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立て結果を検証する realization test。各 standard builder が期待する見出し・本文断片を返すこと、complete prompt が指定された standard 群・routing rule・file access rule・root placeholder を適切に含めるまたは省くことを確認する。

## Read this when
- prompt parts の出力内容、見出し、含まれるべき語句のテストを確認・変更する。
- complete prompt が routing rule、file access rule、各種 standard、補助 prompt、root placeholder をどう組み込むかの期待挙動を確認・変更する。
- file access mode ごとの prompt 文言や、standard の既定での省略・明示指定時の追加に関するテストを探している。

## Do not read this when
- prompt parts や complete prompt の実装を変更したいだけで、テスト期待値を確認する必要がない場合は、対応する実装側を直接読む。
- StructDoc や markdown rendering の汎用仕様を確認したい場合は、その構造化文書処理の実装やテストを読む。
- oracle file の正本文言そのものを確認したい場合は、対応する oracle 側の文書または生成元を読む。

## hash
- b9fef4ddaeb2f0e1b881f9a3685913297160ea4124bfa48ab10ce916c6c54096

# `test_review_oracle_cli.py`

## Summary
- review oracle コマンドの CLI 経由の外部挙動を検証する realization test。対象 oracle file の列挙、report 生成、所見の列挙・検証・judge・merge、上限到達時や処理失敗時の report、review 用 worktree からの INDEX.md 変更の取り込み、非 INDEX.md 差分の拒否を扱う。

## Read this when
- review oracle の report 形式、件数、section 順、accepted/rejected finding の出力、error/no_targets/fatal/ok verdict を変更または確認したいとき。
- review oracle が full scope または session scope でどの oracle file を対象にするかを変更または確認したいとき。
- review oracle の所見 loop、challenger/advocate/judge/merge の制御、prompt に渡す既存所見の範囲、merge operation の契約を変更または確認したいとき。
- review oracle が linked worktree、session branch、review worktree、join commit、INDEX.md 変更の merge conflict をどう扱うかを変更または確認したいとき。
- review oracle 実行中に Codex が作成した差分のうち、INDEX.md だけを許し、それ以外を拒否して元 worktree を汚さない挙動を確認したいとき。

## Do not read this when
- review oracle 以外の review サブコマンドや通常の session 操作だけを扱うとき。
- 実装内部の helper 分割や型定義だけを確認したく、CLI 実行結果、report 内容、git/worktree 副作用を検証する必要がないとき。
- oracle file の正本仕様本文を確認したいとき。

## hash
- 1a8726db12b961d86532ae2594f48bb2d46607622497863717b193de359e1c47

# `test_session_cli.py`

## Summary
- session の分岐作成・統合・破棄に関する CLI 外部挙動を、Git branch と session state のライフサイクルとしてまとめて検証する realization test。
- linked worktree 上での branch/state 操作、session-id 衝突、状態ファイル破損、dirty worktree 拒否、cleanup 失敗時の rollback、conflict 解消 agent の権限と差分制限、branch 削除可否、stdout/stderr へのエラー出力先を扱う。
- 同じ session branch/state fixture を共有する回帰観点を一箇所に集約し、分割よりも session CLI の状態遷移を通しで追うことを優先している。

## Read this when
- session の fork・join・abandon の CLI 挙動、出力、終了コード、Git branch 操作、session state 更新を変更または確認するとき。
- session 操作が linked worktree でどの branch を基準に動くか、root worktree への影響を受けるかを確認するとき。
- session state file の生成・破損検出・abandoned/joined/active 遷移・cleanup 失敗時の復旧挙動を確認するとき。
- join 時の merge conflict 解消 agent、oracle conflict write 権限、conflict marker 検出、delete conflict staging、余計な差分の拒否を変更するとき。
- session 完了処理でのエラー報告先、サブコマンドログ付き完了表示、branch 削除失敗時の警告表示を確認するとき。

## Do not read this when
- session 以外の CLI サブコマンド、設定読み込み、agent call の一般処理だけを確認したいとき。
- session の内部 helper 単体の細部だけを調べたい場合で、対象 helper の実装やより小さい単体テストを直接読めるとき。
- oracle file の正本仕様そのものを確認したいとき。この対象は realization test であり、正本仕様ではない。

## hash
- 05c54f4da38117724999b77fb2ed1e5490a1f0f1bac67603844556163a9c18f8

# `test_struct_doc_rendering.py`

## Summary
- StructDoc の Markdown renderer が本文中の連続空行を正規化する挙動を検証する単体テスト。通常テキストとコードブロックを対象に、過剰な空行が折りたたまれ、期待される Markdown 文字列になることを確認する。

## Read this when
- StructDoc の Markdown 出力で空行の扱いを変更・確認したいとき。
- 通常テキストまたはコードブロック内の連続空行がどのように描画されるべきかをテストから確認したいとき。
- render_as_markdown の整形挙動に関するテストを追加・修正したいとき。

## Do not read this when
- StructDoc のデータ構造そのものや renderer 全体の実装を確認したいときは、実装側を読む。
- Markdown renderer 以外の prompt builder 分割根拠や正本仕様を確認したいときは、対応する oracle 側の文書を読む。
- CLI 挙動、ファイル操作、永続状態など StructDoc の Markdown 整形と無関係な挙動を調べたいとき。

## hash
- 51580019f3a5f35c894b459980668eec4b098eecee22f1645f571c7c2084f811
