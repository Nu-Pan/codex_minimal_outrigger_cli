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

# `test_apply_abandon_cli.py`

## Summary
- apply abandon を CLI 経由で実行したときの active apply run 破棄の外部挙動を検証する realization test。
- completed/running apply run の worktree・branch・session state cleanup、cleanup 対象欠落時の警告、running process と記録済み child process の停止順、PID reuse や raced exit の扱いを固定する。
- repo root、apply worktree、linked session/apply worktree、stale apply branch など実行位置ごとの abandon 境界条件を扱う。

## Read this when
- apply abandon の成功時に apply worktree・apply branch・state・process id 記録がどう削除または ready 化されるかを確認したいとき。
- running apply process の停止、child process group の停止順、pidfd signal、PID reuse、終了済み process の許容に関する制御ロジックを変更するとき。
- apply abandon をどの worktree から実行できるか、linked session の state をどう正として扱うか、stale apply branch をどう拒否するかを確認するとき。
- cleanup 対象が先に消えている場合の warning 出力や、破損 state・process identity 欠落・dirty linked session worktree の拒否条件を変更するとき。

## Do not read this when
- apply fork の生成処理そのもの、Codex 実行結果の解釈、findings の扱いを調べたいだけのとき。
- apply abandon 以外の session fork、init、merge などの CLI 挙動を確認したいとき。
- oracle の正本仕様断片を確認したいとき。この対象は realization test であり、正本仕様ではない。
- process 停止や worktree cleanup を伴わない単純な path model、INDEX 生成、補助 fixture の責務を調べたいとき。

## hash
- f7e3591b4969ab79a729de5928c6ee1e9d8461e0eacdbfe6f0afb89f877c50a7

# `test_apply_fork_cli.py`

## Summary
- apply fork サブコマンドの realization test。Codex 実行を fake に差し替え、apply run の開始・完了、session state 更新、apply branch/worktree 作成、linked worktree 上の HEAD 起点、設定読み込み失敗時の中断、.gitignore の扱い、target 正規化を検証する。
- CLI 経由の統合的な挙動確認と、apply fork module の一部関数を直接呼ぶ境界条件確認の両方を含むため、apply fork の外部副作用や state/worktree/branch のライフサイクルを調べる入口になる。

## Read this when
- apply fork の実装変更により、session state の apply 状態、apply branch 名、apply worktree 配置、PID file 削除、完了判定が変わる可能性があるとき。
- linked worktree 上で apply fork を実行した場合の起点 commit、session branch、apply branch、worktree 配置の期待挙動を確認したいとき。
- apply fork 実行前の cmoc config 読み込み失敗時に、apply run を開始しないことやエラー出力先を確認したいとき。
- apply fork が .cmoc ignore を確保する処理、session 側の .gitignore を dirty にしない処理、または apply branch 側で .gitignore を編集対象にできる処理を変更するとき。
- apply fork の対象 path 正規化で、root 直下の memo 除外、入れ子の memo directory の保持、binary file の保持を確認したいとき。
- Codex 呼び出しを伴う apply fork loop の呼び出し目的、所見列挙、所見適用、変更要約の制御をテスト上で追いたいとき。

## Do not read this when
- apply fork 以外の apply 系サブコマンドや session fork 単体の仕様を調べたいだけのとき。
- Codex CLI や LLM 出力内容そのものの品質を検証したいとき。この対象は Codex 実行結果を fake にして制御フローと副作用を検証する。
- path model、oracle/realization の概念定義、INDEX routing の規約を確認したいとき。
- apply fork の内部 helper 実装そのものを読みたいとき。この対象は期待される外部挙動と重要な境界条件を示すテストであり、実装詳細の入口ではない。

## hash
- 299d8a600d3ab3b419a47ee298117556c499bfbbc77d3d80778aeade1dded333

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 実行を通じて、所見列挙、所見適用、commit、変更要約、report 生成、session state 更新までの一連の制御を検証する realization test。
- 未収束、収束、error、変更ファイル再調査、未追跡ファイルの変更要約、調査対象なし、rolling apply fork の基準 commit などを、report と副作用からまとめて確認する。
- Codex 実行は fake に差し替え、作業 tree・git branch・session state・生成 report を観測して apply fork の外部挙動を検証する。

## Read this when
- apply fork の report 内容、終了コード、収束判定、未収束判定、error report の挙動を確認したいとき。
- apply fork が所見適用後に変更ファイルを再調査する条件や、再調査対象から除外される対象を確認したいとき。
- apply fork の変更要約が commit 済み差分、未 commit 差分、未追跡ファイルをどう扱うかを確認したいとき。
- apply fork 実行後に session state や apply branch の commit がどう更新されるかを確認したいとき。
- apply fork 用の ACP builder が標準 prompt、structured output schema、root token 展開、対象 path 検証を満たしているかを確認したいとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にする制御を確認したいとき。

## Do not read this when
- apply fork の実装内部だけを変更したいが、CLI 経由の report、git 副作用、session state 副作用を確認する必要がないとき。
- apply fork 以外の subcommand の挙動や、汎用 CLI runner の使い方だけを調べたいとき。
- ACP builder の個別 prompt 生成ロジックそのものを詳しく変更する作業で、外部挙動テストではなく builder 実装を直接読む方が適切なとき。
- git helper、test fixture、runner の共通実装だけを調べたいとき。
- INDEX.md 生成やルーティング文書の仕様を調べたいとき。

## hash
- a3db69fe3a20b856dfe11fd7000f116ef91f86cc2a4412f440f70aea162ee185

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。正常 join、apply worktree からの実行、linked session worktree への反映、cleanup、state 更新、report 生成を扱う。
- join 可否の境界条件として、stale apply branch、dirty apply worktree、想定外差分、削除・rename を含む managed branch path 判定、root memo の分類、gitignore 変更、merge conflict の報告と index conflict 解決後の継続を一箇所で確認する。
- 16,000 文字を超えるが、apply join の成功条件と拒否条件が同じ fixture、session state、git worktree/branch 状態の文脈に強く結合しているため、分割せず外部挙動のまとまりとして読む対象である。

## Read this when
- apply join の CLI 挙動、終了コード、標準出力、report 生成、state 更新、apply worktree と apply branch の cleanup を変更・確認したいとき。
- apply join が dirty worktree、stale apply branch、想定外差分、merge conflict をどの条件で拒否し、何を残すべきかを確認したいとき。
- apply join が session worktree、apply worktree、linked session worktree のどの作業ツリーへ反映し、current cwd によって cleanup 可否がどう変わるかを確認したいとき。
- apply join の managed branch path 分類、memo 配下の扱い、gitignore 変更の許可、削除 path や rename target の扱いを変更する前に既存の期待挙動を確認したいとき。

## Do not read this when
- apply fork の Codex 実行内容や apply run の生成処理そのものを調べたいだけのとき。
- session fork、init、基本的な repository setup の仕様や実装を調べたいだけのとき。
- apply join の内部 helper 実装だけを局所的に変更し、CLI から観測される join 成功・拒否条件や git/state/report 副作用を確認する必要がないとき。
- oracle file の正本仕様を確認したいとき。この対象は realization test であり、正本仕様そのものではない。

## hash
- 4d09bd57be56809c77766c5a899573b645e7d033020eed65c0071cd990cbd42a

# `test_basic_runtime.py`

## Summary
- cmoc の共通 runtime 契約を横断的に固定する realization test。root/worktree 解決、config 既定値と検証、CmocError の Markdown 表示、CLI error の stdout 化、subcommand log、FileAccessMode から Codex sandbox/profile への変換、binary 判定など、個別サブコマンドより下位の実行前提をまとめて検証する。
- 16,000 文字超の大きなテストだが、共通 fixture と root 状態の文脈を共有して崩れやすい basic runtime 回帰を一箇所で扱うための凝集した入口になっている。

## Read this when
- runtime の基礎契約、特に repo root と run/work root の扱い、linked worktree、main worktree 拒否、managed worktree 外の保護を確認または変更する時。
- config の既定値、codex model/reasoning effort 名の検証、FileAccessMode の永続化値、sandbox mode、Codex profile の writable roots 制御を変更する時。
- CmocError の表示形式、CLI の想定済み error や Click parse error の stdout report 化、shell completion probe の preflight 回避、subcommand log の失敗記録を扱う時。
- `.cmoc` の ignore 設定、起動 wrapper の call stack 表示、binary 判定の読み取り範囲など、個別コマンドではなく runtime 共通の副作用・安全境界を確認する時。

## Do not read this when
- 特定サブコマンド固有の正常系・業務ロジック・入出力仕様だけを調べる時は、そのサブコマンドの実装または専用テストを先に読む。
- oracle 文書そのものの正本仕様や用語定義を確認したい時は、対応する oracle file を読む。
- 単体の小さな helper の内部実装だけを変更し、runtime 境界や CLI 表示、sandbox/profile、worktree 安全性に影響しないことが明らかな時は、対象 helper とその近接テストを優先する。

## hash
- eebacc7913c758aaa3b699815f409ac318d991034639822114fa39836ad93d68

# `test_cli_init_tui.py`

## Summary
- init と対話起動前処理の外部挙動を検証する realization test。cmoc 管理領域の ignore 化、既存 staged/unstaged 差分の保護、初期設定生成と同期、linked worktree での初期化・ログ保存・schema 配置、Markdown prompt からの TUI parameter 解決と Codex 起動引数構築を扱う。
- 利用開始直後の CLI 境界で共有される repository/runtime 準備を一続きの回帰として確認するための入口であり、初期化済み状態を前提に TUI 起動へ進む挙動まで同じ文脈で読む対象。

## Read this when
- init の外部挙動、特に cmoc 管理領域を git tracking から外す処理、ignore 設定、cleanup commit、サブコマンドログ記録を確認・変更する時。
- init が利用者の既存 staged 変更や unstaged 変更、既存の ignore ファイル変更を壊さないことを確認・変更する時。
- 初期設定ファイルの default 値、既存の人間設定を保持した defaults 同期、設定項目追加時の初期化回帰を確認する時。
- linked worktree 上で init または TUI を実行した時の repository root と worktree cwd の扱い、ignore 設定、ログ保存先、schema 配置、git status の汚れ防止を確認する時。
- TUI 起動前のエディタ実行、HTML comment 除去を含む prompt 整形、parameter 解決用 Codex 呼び出し、file access mode の default、最終 prompt 保存、TUI 用 Codex parameter 構築を確認・変更する時。

## Do not read this when
- 個別サブコマンドの business logic や内部 helper の詳細だけを調べたい時。この対象は init/TUI 起動境界の外部挙動回帰に絞られている。
- Codex CLI や LLM の出力品質そのものを検証したい時。この対象は呼び出し引数・保存先・制御境界を stub で確認する。
- 一般的な test support、repository fixture、fake executable 作成 helper の実装を調べたい時。ここではそれらを利用する側の回帰だけを扱う。
- TUI 実行後の対話 UI 内部挙動を調べたい時。この対象は対話起動前の parameter 構築と起動呼び出しまでを扱う。

## hash
- 52aa8bc9dca127f656fd33da495d4ea1e1e7ffe9c5666c332a30912fc5b3584f

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行基盤の realization test。Codex subprocess の起動環境、process group tracking、profile 生成、sandbox 設定、作業ディレクトリ、schema 出力先、TUI 起動前検証、失敗時エラー報告を、stub codex と一時 repo で検証する。
- `run_codex_exec` と `run_codex_tui` が file access mode や linked worktree に応じて、Codex CLI の引数・cwd・profile・ログ・schema path をどう扱うかを確認する入口になる。

## Read this when
- Codex CLI 呼び出し周りの実行制御、profile 生成、sandbox writable roots、read-only / repo-write / pure-oracle-read の切り替えを変更する時。
- `commons.runtime_codex` または `commons.runtime_codex_profile` の subprocess 起動、apply process tracking、`CODEX_HOME` profile、`--cd`、`--output-last-message`、`--output-schema` の扱いを確認する時。
- TUI 実行で extra read path の許可判定、linked worktree からの完全 prompt 読み込み、Codex CLI 非ゼロ終了や CLI 不在時の `CmocError` 報告を変更・調査する時。

## Do not read this when
- Codex CLI 呼び出しではなく、一般的な CLI command parsing、oracle 文書、path model、config schema そのものの仕様を調べる時。
- LLM 出力品質や Codex 本体の振る舞いを検証したい時。この対象は cmoc が Codex CLI をどう起動・制御するかを stub subprocess で検証する。
- runtime 以外の realization test、または pytest helper / fixture の一般構造だけを探す時は、より直接の test support や該当機能のテストへ進む。

## hash
- 1f0890b94acc48a58c6dfd2f451c9ef58a54b01b3e034d5510fb5f236831be09

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行時の Codex home 解決と事前検証を対象にした realization test。環境変数が未設定の場合の既定 home、環境変数で指定された home の保持、Codex 実行 cwd に対する相対 home の解決、home や認証情報が不正な場合に Codex CLI 起動前に失敗することを検証する。

## Read this when
- Codex CLI 呼び出しで使用する CODEX_HOME の決定、相対パス解決、実行結果へ記録される codex_home や profile_path の挙動を確認・変更するとき。
- Codex home が存在しない、ディレクトリではない、auth.json がない場合の CmocError の summary・detail・next_actions を確認・変更するとき。
- ファイルアクセスモードによって Codex CLI の作業ディレクトリが変わる状況で、相対 CODEX_HOME がどこから解決されるかを検証するとき。

## Do not read this when
- Codex CLI の容量待機、標準出力イベント処理、プロンプト生成など、Codex home の解決や検証に直接関係しない実行制御を調べるとき。
- 実際の Codex CLI や LLM の出力品質を検証したいとき。ここでは fake executable を使い、home 解決と事前検証の制御ロジックだけを扱う。
- oracle file 側の正本仕様を確認・変更したいとき。この対象は realization test であり、正本仕様そのものではない。

## hash
- f113426a3f92145e9b5bff3bfd809dd949834c6dbb9c2471815903cec09de7fe

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex exec が quota exceeded になった後、quota availability probe を挟んで resume または再実行へ進む retry 状態機械の外部挙動を検証する realization test。
- probe の共有、resume token の利用有無、call log と subcommand log、CODEX_HOME と cwd の扱いを、fake Codex 呼び出し列とログ出力を通じて確認する。
- 並列実行時に代表 probe が 1 回だけ実行されること、代表 probe 失敗時に待機中の呼び出しも失敗して resume しないことを扱う。

## Read this when
- Codex exec の quota exceeded 検出後の待機、probe、resume、再実行の制御を変更・調査する場合。
- quota availability probe の引数、標準入力、出力ファイル、ログ記録、subcommand event の期待値を確認したい場合。
- CODEX_HOME が相対パスのとき、Codex 呼び出し cwd と --cd がどこを指すべきかを確認する場合。
- 複数の Codex exec が同時に quota 待機へ入ったときの probe 共有や、probe 失敗時のエラー伝播を変更・検証する場合。

## Do not read this when
- quota retry と無関係な通常の Codex exec 成功系、プロンプト構築、モデル選択、ファイルアクセスモード全般だけを調べる場合。
- Codex CLI そのものの出力品質や LLM 応答内容を検証したい場合。
- ログ基盤全体の形式や保存先だけを調べる場合で、quota exceeded 後の probe/resume/retry に関係しない場合。
- oracle file や正本仕様断片の内容を確認したい場合。

## hash
- 3fc5e457350652875417908918966047c9e87c2f7592e8078ab436bb3861593c

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 制御を検証する realization test。構造化出力の schema 不一致、出力ファイル欠落・空・不正 JSON、容量エラー JSONL に対して再試行し、成功時の結果・呼び出しログ・イベント状態が期待どおり記録されることを確認する。
- stderr や通常 stdout に出た容量・quota 風メッセージを retry 判定に使わず、Codex CLI 失敗として扱う境界も検証する。

## Read this when
- Codex CLI 呼び出しの再試行条件、schema validation retry、capacity retry、quota/capacity marker の解釈境界を変更する。
- 呼び出しごとの call log、prompt log、stdout log、subcommand logger の codex_call event に含める status・returncode・error・call_log_path の期待値を確認したい。
- 構造化出力の読み取り失敗や JSON Schema 検証失敗から成功に回復する挙動をテストで確認・修正したい。

## Do not read this when
- Codex CLI に渡す引数構築、profile 設定、sandbox 設定など、再試行後のログ・出力検証に関係しない通常呼び出し経路だけを調べたい。
- repository 作成、Codex home 設定、fake executable 作成などの test fixture 自体の実装を調べたい場合は、support 側の helper を直接読む。
- INDEX 生成、oracle/realization の分類、またはルーティング文書の仕様を調べたいだけで、Codex runtime の retry 挙動を扱わない。

## hash
- 4756b71f801ab3d2753b1ac5ab73749a3bb338f0e6f7a177a3daa1c7451cab3b

# `test_indexing_cli.py`

## Summary
- indexing の preflight と CLI サブコマンドが routing document を生成・更新し、INDEX.md conflict、hash 再利用、Codex 呼び出し、commit 対象、linked worktree、dirty worktree をどう扱うかを外部挙動として検証する realization test。
- semantic entry の妥当性検証、 malformed entry の再生成、兄弟 entry の並列生成、root 直下 memo 除外と nested memo 対象化まで含め、indexing 更新ワークフローの回帰観測点を一箇所に集約している。

## Read this when
- indexing サブコマンドや indexing preflight の成功・失敗条件、git 差分がある場合の停止条件、INDEX.md 更新後の commit 条件を確認・変更するとき。
- INDEX.md conflict 解決、既存 hash が新鮮な場合の Codex 呼び出し省略、malformed entry の再生成、semantic field のバリデーションを確認するとき。
- linked worktree や apply worktree 上で indexing がどの root/config/cwd を使い、どの worktree に INDEX.md を作成するかを確認するとき。
- routing document 更新対象の列挙、兄弟 entry の並列生成、root 直下 memo と nested memo の扱いを変更するとき。

## Do not read this when
- 個別の indexing 実装ロジックや helper の責務を知りたいだけなら、対応する実装ファイルを読む。
- init、apply、join など indexing の回帰観測点として現れる範囲を超えたサブコマンド仕様を調べるだけなら、より直接の CLI テストや実装を読む。
- INDEX.md エントリーの文章生成規則や正本仕様断片を確認したいだけなら、oracle 側の該当文書を読む。

## hash
- f054171afce78e8df4c108ca283958c3d8bcaa6f3256b7eff69b64068e45fc9a

# `test_indexing_preflight.py`

## Summary
- Codex 呼び出し前に索引更新を走らせる preflight 制御の realization test。exec/TUI 経由の実行順、更新後コミット、作業ツリー選択、リポジトリロック待機、特定 purpose での索引更新スキップを検証する。

## Read this when
- Codex 実行ラッパーが索引更新を先に行うか、更新後に専用コミットを作って作業ツリーを clean に戻すかを確認・変更したいとき。
- root と cwd が異なる場合に、どの worktree を索引更新対象にするかを確認・変更したいとき。
- 索引更新の排他ロック取得待ち、または索引エントリー生成・衝突解決の purpose で preflight をスキップする条件を扱うとき。

## Do not read this when
- 索引本文の生成内容、ディレクトリ走査、エントリー構造化出力そのものを確認したいだけのとき。
- Codex 実行パラメータの定義や runtime 実行関数の通常動作だけを調べたいとき。
- Git worktree やロックを伴わない一般的なテスト補助関数だけを探しているとき。

## hash
- 5549e75d6493464e59f5f4cb68232c1fbd9fc7d03b85ee5f6cb6ea3ad4e04099

# `test_prompt_parts.py`

## Summary
- prompt part と ACP builder が生成する prompt、file access rule、routing rule、各種 standard 文書、structured output schema、実行パラメータの組み合わせを横断的に検証する realization test。
- 標準 prompt の構成要素が期待語句を含むこと、root placeholder や動的テキストを保持すること、builder が正しい model class・reasoning effort・file access mode・schema path を返すことを確認する。
- 単一ファイルとしては大きいが、agent prompt と structured output schema の構築結果を同じ読み取り文脈で検証するため、共通の render/schema 期待値を一箇所に集約している。

## Read this when
- prompt builder の出力内容、markdown rendering、routing/file access/index entry/review/apply/realization standard の挿入条件や期待語句に関する回帰テストを確認・更新したいとき。
- ACP builder が生成する AgentCallParameter の model class、reasoning effort、file access mode、prompt 内容、structured output schema path の期待値を確認したいとき。
- review oracle、apply fork、session join、TUI parameter resolution、indexing index entry など複数 builder にまたがる schema 一致や prompt 組み立ての挙動を検証したいとき。
- root token、work root placeholder、oracle root 表記、動的入力文字列が prompt 内で置換されるべきか保持されるべきかを判断したいとき。

## Do not read this when
- 個別 builder の実装ロジックそのものを変更したいだけで、テスト期待値や横断的な prompt/schema 契約を確認する必要がないとき。
- StructDoc や render_as_markdown の内部実装だけを調べたいときは、実装側の構造化文書・rendering module を先に読む方が直接的である。
- oracle 側 JSON schema の正本内容を確認したいときは、このテストではなく対応する oracle schema 本文を直接読む方が適切である。
- 単一機能の CLI 動作や外部挙動だけを確認したいときは、その機能に対応するより限定されたテストを先に読む方がよい。

## hash
- 02494b156e4edff1335366ca4e99f6751c05b333b57bf26a41243cbc0a5c4f1c

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動と、所見の列挙・検証・judge・merge を含む評価 loop の制御を検証する realization test。report の構成、scope ごとの対象選択、linked worktree での review 実行、INDEX.md 変更の取り込み、エラー report、想定外差分の拒否まで、同じ review run の状態と出力を共有する観点をまとめて扱う。
- 対象は 16,000 文字を超えるが、fake Codex 応答、report 文脈、review worktree の状態確認が強く結びついているため、oracle review の読み取り文脈を一箇所に保つ構成になっている。

## Read this when
- review oracle command の report 出力、判定結果、件数表示、エラー時 report、または stdout/stderr の振る舞いを変更・確認する。
- oracle review の所見 loop について、enumerate、challenger/advocate validation、judge、merge の呼び出し順・入力文脈・結果反映を変更・確認する。
- full scope または session scope で、review 対象 oracle の選択、gitignored oracle、binary、symlink、memo 配下との境界、対象 0 件時の挙動を確認する。
- linked worktree 上の session branch、review 用 worktree、fork commit、join commit、INDEX.md 変更の merge、conflict 解決に関する挙動を変更・確認する。
- review oracle 実行中に生成された INDEX.md 以外の差分を拒否し、元の作業ツリーへ戻さない保証を確認する。

## Do not read this when
- review oracle 以外の command や、一般的な session/init/fork の基本挙動だけを調べたい場合。
- Codex 実行 wrapper、設定 loader、git helper などの低レベル実装だけを変更しており、review oracle の外部挙動や loop 制御に影響しないことが明らかな場合。
- oracle file の正本仕様そのものを確認・編集したい場合。この対象は realization test であり、正本仕様の代替ではない。
- 単一 helper の純粋な入力検証だけを確認したい場合。ただし所見 merge operation の contract や reused target 拒否に関係する場合は読む。

## hash
- 27b2d74b61abecd54e93d474cec75368d64d7971b72b8b08cffd658587f2d053

# `test_session_cli.py`

## Summary
- session の fork・join・abandon に関する CLI 外部挙動をまとめて検証する realization test。session branch と session state のライフサイクルを軸に、状態ファイル生成・更新・破損検出、home branch への復帰、branch 削除、linked worktree 上での操作、dirty worktree 拒否、join 時の conflict resolution とエラー出力先を扱う。
- 大きなテストファイルだが、session branch/state fixture を共有する回帰テスト群として凝集しており、分割せず同一文脈で読むべき理由が冒頭 docstring に明示されている。

## Read this when
- session fork が session branch と state file を作成する挙動、session-id 衝突時の retry・失敗・既存 state 保護、初期 ignore 設定や linked worktree の branch/head 扱いを確認・変更する時。
- session abandon が home branch へ戻り session branch を削除して state を abandoned にする挙動、home branch 欠落時や cleanup 失敗時の rollback・エラー報告を確認・変更する時。
- session join が home branch へ変更を取り込み state を joined にする挙動、oracle conflict resolution の Codex 呼び出し権限、delete conflict の staging、session branch 削除失敗時の警告、dirty worktree や merge 後の予期しないエラー出力先を確認・変更する時。
- session completion 系コマンドが不正な session state file を拒否する共通挙動や、conflict marker block 検出ロジックの期待値を確認する時。

## Do not read this when
- session 以外の CLI サブコマンド、設定読み込み、runtime profile 生成、git helper 単体の挙動だけを調べる時。
- session コマンドの内部実装構造や関数分割を確認したいだけで、CLI 実行結果・branch/state 副作用・エラー出力の回帰観点を必要としない時。
- Codex CLI や LLM の出力品質そのものを検証したい時。このテストは join conflict resolution 呼び出しの権限・副作用を fake で観測するだけで、生成品質は対象にしない。

## hash
- 4c336e5cd265ec18d7aec7006ea53cd2b83a40be57438e6e92ff26b6291f0726
