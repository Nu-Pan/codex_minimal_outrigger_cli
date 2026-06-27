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
- active apply run を破棄する CLI 操作の外部挙動を検証する realization test。completed/running apply の worktree・branch・state cleanup、cleanup 対象欠落時の警告、running process 停止、process identity 異常時の拒否を扱う。
- apply worktree 内、linked session worktree、linked apply worktree、同一 session の stale apply branch など、実行位置によって abandon 対象を誤らないことを固定する。
- 16,000 文字を超えるが、active apply run の abandon に伴う state fixture、cleanup、process 停止、実行位置判定の境界条件を一箇所で読むための凝集したテストファイルとして位置づけられている。

## Read this when
- apply abandon の CLI 出力、終了コード、state 遷移、apply worktree 削除、apply branch 削除の期待挙動を確認または変更するとき。
- running apply process の停止順序、PID reuse、終了済み process、process identity 欠落時の扱いを確認または変更するとき。
- apply abandon を repo root 以外の worktree から実行する場合の対象 session 判定、linked session の dirty check、stale apply branch 拒否を調べるとき。
- apply fork が作る active apply run の状態を前提に、abandon 側の cleanup 境界条件をテストで再現したいとき。

## Do not read this when
- apply abandon 以外の apply サブコマンドの通常動作や生成物を調べたいだけのとき。
- session fork、init、git helper、runner fixture の基本的な作りを確認したいだけで、abandon の境界条件に関心がないとき。
- oracle file の正本仕様や設計意図を確認したいとき。このファイルは realization test であり、正本仕様ではない。

## hash
- 1db3b4e4890f7a53b80955f8c6f6e24062a948b6905b638417f421c4b02ae69e

# `test_apply_fork_cli.py`

## Summary
- apply fork コマンドのテスト群。Codex 実行を fake に差し替え、apply run の完了状態、apply branch と worktree の作成先、session state の更新、pid など旧状態項目の不在、所見列挙呼び出しを検証する。
- linked worktree 上で開始した session branch と HEAD を apply run の起点にすること、session 側の既存 ignore 表現を壊さず必要時は git exclude で `.cmoc` を ignore して clean に保つこと、設定読み込み失敗時に apply run を開始しないことを確認する。
- 所見対象として `.gitignore` を apply branch 側で編集できること、apply 対象正規化で root 直下の private な memo を除外しつつ入れ子の memo directory と binary file を残すことを検証する。

## Read this when
- apply fork の CLI 挙動、state 遷移、apply branch/worktree の配置、完了時の後始末に関するテストを確認・変更したいとき。
- linked worktree からの apply fork、session 側 `.gitignore` の保持、`.cmoc` ignore の付与方法、設定ファイル読み込み失敗時の rollback 境界を扱うとき。
- apply 対象の列挙・正規化、`.gitignore` を所見対象に含める挙動、root 直下 memo の除外と入れ子 memo/binary file の扱いを検証したいとき。

## Do not read this when
- apply fork 以外の apply サブコマンド、review、session fork、init などの CLI 挙動を調べたいだけのとき。
- Codex CLI や LLM 出力品質そのもの、実際の Codex 実行内容、所見 schema の詳細を確認したいとき。
- 実装本体の制御フローや helper の責務を変更するために読む場合で、まず対応する実装モジュールや正本仕様断片から確認すべきとき。

## hash
- 8f80ee95c01fc38152054a76eeb0c86ea80176eb50ca170fdabd61c01aa18bed

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 実行を通じて、所見列挙から適用、commit、変更要約、report 生成、session state 更新までの制御を検証する realization test。
- 収束、未収束、error、変更ファイル再調査、編集禁止対象の差分検出、rolling apply fork の対象選定を、同じ loop と report schema の観測結果としてまとめて扱う。
- 16,000 文字を超えるが、apply fork report の期待値文脈を一箇所に保つため、分割せず凝集性を優先している。

## Read this when
- apply fork の report 内容、終了コード、収束判定、未収束判定、error report の挙動を確認・変更したいとき。
- apply fork が Codex 応答から所見を列挙し、所見適用後に commit message と変更要約を生成し、apply branch と session state を更新する流れを検証したいとき。
- apply 後の変更ファイル再調査、INDEX.md の再調査除外、差分なし適用時の扱い、調査対象なしの場合の report 表示を確認したいとき。
- 編集禁止対象への差分が検出された場合に、error state、stderr、report、未 commit 差分を含む変更要約がどう扱われるかを確認したいとき。
- rolling apply fork が前回 apply join 後の変更だけを対象にする制御を確認したいとき。

## Do not read this when
- apply fork 以外の apply join、session fork、init などの個別コマンド実装そのものを調べたいとき。
- report renderer や session state 永続化の内部 helper 単体の詳細だけを確認したいとき。
- Codex CLI や LLM の実出力品質を検証したいとき。ここでは fake 応答を使って cmoc 側の制御と観測結果を検証している。
- 一般的な test fixture、repository 作成 helper、git wrapper、CLI runner の使い方だけを調べたいとき。

## hash
- 931332ad9a54f022bfb36dfbc9c3724c8948a76d18f73b1dd4efba82900895cc

# `test_apply_join_cli.py`

## Summary
- apply run を session へ join する CLI 外部挙動を検証する realization test。成功時の apply worktree と apply branch の後片付け、session state 更新、report 生成、apply worktree からの実行、linked session worktree への merge を扱う。
- join を拒否または中止する境界条件として、古い apply branch、dirty apply worktree、想定外差分、削除・rename を含む managed branch 差分判定、gitignore 変更、merge conflict と index conflict 解決後の継続を同じ操作文脈で確認する。

## Read this when
- apply join の CLI 成功条件、後片付け、state 更新、report 出力を変更または確認したいとき。
- apply join を session worktree、apply worktree、linked session worktree のどこから実行できるかを確認したいとき。
- apply join が dirty worktree、古い apply branch、想定外差分、merge conflict をどう検出し、どの状態を残すかを確認したいとき。
- apply join の差分判定で、削除パス、rename 先、gitignore 変更、oracle 配下の想定外変更をどう扱うかを確認したいとき。

## Do not read this when
- apply fork の Codex 実行、apply worktree 作成、apply state 初期化だけを確認したいとき。
- session fork や init の基本挙動だけを確認したいとき。
- join の CLI 経由の外部挙動ではなく、内部 helper の小さな単体仕様だけを確認したいとき。ただし managed branch の変更パス判定に関する確認は対象に含まれる。
- oracle file の正本仕様そのものや、INDEX.md 生成ルールを確認したいとき。

## hash
- e233fb4e7319fc4c0ddc648b190cce2111bb5fc24a37dff2e43fab24a68eee66

# `test_basic_runtime.py`

## Summary
- cmoc の基本ランタイム契約を広く固定する realization test。path token と worktree 判定、既定 config、構造化エラー表示、session/apply branch 名と状態読み込み、CLI preflight と completion probe、起動 wrapper の call stack 表示、`.cmoc` ignore、file access mode と Codex sandbox profile、binary 判定の外部挙動を検証する。
- 単一機能の詳細テストというより、runtime・path・state・CLI エラー処理・sandbox profile など基礎部品の統合的な回帰検知入口として位置づく。

## Read this when
- cmoc の root token path、repo root、run root、work root、linked worktree 判定、main worktree 拒否の挙動を変更・確認したいとき。
- CmocError の Markdown report、CLI 想定エラー、Click 引数解析エラー、stdout/stderr の出し分け、completion probe 時の preflight skip を変更・確認したいとき。
- session branch 名、apply branch 名、branch からの session state 読み込み、状態ファイル読み書きの異常系を扱うとき。
- `.cmoc` の `.gitignore` 追記、file access mode の永続化値、Codex sandbox mode 変換、Codex profile の writable_roots や保護領域拒否を変更・確認したいとき。
- binary 判定の読み取り量や、起動 wrapper の missing venv report における root token path 表示を変更・確認したいとき。

## Do not read this when
- 個別 CLI サブコマンドの成功系 workflow や利用者向け機能仕様だけを調べたい場合は、そのサブコマンド専用の実装・テストを優先する。
- oracle 正本仕様断片そのものを確認・変更したい場合は、この realization test ではなく対応する oracle file を読む。
- テスト支援 fixture、git repo 作成 helper、runner の実装詳細だけを調べたい場合は、支援モジュールを直接読む。
- 特定 module の内部実装方針だけを調べたい場合は、ここを入口にせず対象の runtime・state・config・content・profile 実装を直接読む。

## hash
- 68478ab08cb111704caaee49b12305876b825fc0f448c58579d99277d1640ece

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と対話型起動処理に関する realization test。初期化時の .cmoc 管理、.gitignore 追記、既存 staged/unstaged 変更の保護、linked worktree での保存先、既定設定の生成・同期、サブコマンドログ、TUI のプロンプト編集・パラメータ解決・Codex 起動、Markdown プロンプト解析の挙動を検証する。

## Read this when
- 初期化コマンドが既存の .cmoc 配下ファイルを git 管理から外し、.cmoc を ignore し、必要な cleanup commit を作る挙動を確認・変更したいとき。
- 初期化コマンドが利用者の既存 staged 変更や .gitignore の staged/unstaged 変更を勝手に commit しないことを確認・変更したいとき。
- linked worktree 上で初期化や TUI を実行した場合の、repository root と作業 tree 側それぞれの .cmoc、.gitignore、ログ、schema、commit 対象の扱いを確認・変更したいとき。
- 既定設定ファイルの生成内容や、既存の人間設定を残したまま不足する既定値を補う同期挙動を確認・変更したいとき。
- TUI が editor で編集された Markdown からコメントを除去し、パラメータ解決用 Codex 呼び出しと TUI 用 Codex 呼び出しへ適切な AgentCallParameter を渡す流れを確認・変更したいとき。
- TUI の file access mode 解決結果が空の場合の既定値、または fenced code block や見出し前本文を含む Markdown プロンプト解析を確認・変更したいとき。

## Do not read this when
- 初期化や TUI の利用者向け外部挙動ではなく、個別 helper の内部実装だけを確認したいときは、該当する実装側の対象を先に読む。
- CLI 全体のコマンド登録、共通 runner、fixture、git 操作 helper の一般的な仕組みを調べたいだけのときは、共通サポートや実装エントリの対象を先に読む。
- oracle file の正本仕様断片を確認・変更したいときは、この realization test ではなく対応する oracle 側の対象を読む。
- TUI 以外のサブコマンド、または初期化処理と無関係な設定・ログ・worktree 処理のテストを探しているときは、より直接その挙動を検証するテストへ進む。

## hash
- 7648b5e7f2fca5395ad3a389129ffeda859b8b54fe7cf234ad970de5379333e4

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行経路の realization test。exec 実行時の profile 生成、標準入力、sandbox 設定、出力取得、呼び出しログ、保護領域変更の拒否、TUI 起動前の追加読み取りパス検査、Codex CLI 欠落時のエラー化を検証する。
- テスト用リポジトリ、CODEX_HOME、stub 化した codex 実行ファイルを組み合わせ、実際の外部 Codex CLI ではなく制御された subprocess 挙動を通して runtime 層の制御ロジックを確認する。

## Read this when
- Codex CLI を起動する runtime 実装、profile 生成、sandbox_mode や writable_roots の組み立て、exec/TUI の起動前検査を変更するとき。
- Codex 呼び出しログ、失敗時 status、returncode、call_log_path、console 出力など、subcommand logger 連携の挙動を確認または変更するとき。
- 保護領域への書き込み検出、追加読み取りパスの拒否条件、Codex CLI が見つからない場合の CmocError を扱う実装を変更するとき。
- Codex subprocess をテストで stub する方法や、runtime 層の外部コマンド依存を切り離した検証例を探すとき。

## Do not read this when
- Codex CLI の実行経路ではなく、別サブコマンドの入出力、oracle 文書処理、path model などの仕様や実装を調べたいとき。
- 実際の Codex CLI や LLM の出力品質そのものを検証したいとき。この対象は stub された subprocess と runtime 制御のテストであり、モデル応答の品質評価は扱わない。
- profile 内容や保護領域の期待値ではなく、テスト fixture の基本的な作成 helper 自体を変更したいときは、support 側の定義を直接確認する。

## hash
- a9f1f66261226cc3e58aeafcffd3b71369baf30d7b2fd02cee4f6ce932a1ae1e

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 呼び出し時の Codex home 解決と事前検証を扱う realization test。環境変数未設定時に通常のホーム配下を使うこと、環境変数で指定された相対パスを保持して実行しつつ記録上はリポジトリ基準で解決すること、Codex home や認証情報が不正な場合に CLI 実行前に利用者向けエラーになることを検証する。

## Read this when
- Codex CLI 実行処理で CODEX_HOME、既定の Codex home、auth.json、プロファイル配置先、呼び出しログに関する挙動を変更または確認するとき。
- Codex home が存在しない、ディレクトリでない、認証情報がない場合の CmocError の summary、detail、next_actions を確認するとき。
- Codex CLI を実際に起動せず、fake executable と monkeypatch で実行環境を組み立てるテスト例を探すとき。

## Do not read this when
- Codex CLI の出力 JSON、ターン完了判定、容量待機、モデルや推論努力の引数変換だけを確認したいとき。
- Codex home 以外のリポジトリ作成 helper、プロファイル stub、Python 実行ファイル生成 helper の実装詳細を確認したいとき。
- oracle file に書くべき正本仕様や設計方針を探しているとき。このファイルは realization test であり、正本仕様そのものではない。

## hash
- 93e187f3d5ae928a9accdef37c14910cf4c9d9da4dbf4762954d601b4e8b4606

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex 実行ラッパーが quota 超過を検出した後、quota availability probe を挟んで再実行または resume する制御を検証する realization test。
- 疑似 codex 実行ファイルを使い、呼び出し引数、標準入力、CODEX_HOME、出力 JSON、call log、SubcommandLogger イベント、コンソール表示まで含めて quota retry 周辺の外部挙動を固定する。
- 並列に quota 超過した複数呼び出しで、代表となる probe が 1 回だけ実行され、それぞれの呼び出しが resume で完了することも検証する。

## Read this when
- Codex 実行中の quota 超過検出、quota availability probe、再実行、resume token 利用の挙動を変更または調査するとき。
- quota retry 時に生成される call log、stdout/stderr/prompt/output のログパス、SubcommandLogger の codex_call イベント、コンソール出力の形式や status を確認するとき。
- quota availability probe が readonly 実行中に .agents 配下を変更した場合の拒否処理と、その失敗ログの扱いを確認するとき。
- 複数スレッドから同時に quota retry が発生した場合の probe 集約と、各呼び出しの再開挙動を確認するとき。

## Do not read this when
- 通常の Codex 実行成功、quota 以外の失敗、または基本的なコマンドライン組み立てだけを確認したいときは、より直接それを扱う実装やテストを読む。
- 設定ファイルの読み込み、プロファイル生成、リポジトリ作成 fixture そのものの仕様を調べたいときは、それらを定義する補助コードを読む。
- oracle file の正本仕様や quota retry 以外のサブコマンド仕様を確認したいときは、対応する oracle doc または対象サブコマンドのテストへ進む。

## hash
- 0da8839aa5bc911c9380a39020b6feaadf6bab589dfbea0e41923aa494287b86

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行のリトライ制御を検証する realization test。構造化出力の schema 検証失敗時の再試行、capacity エラー時の再試行、stdout JSONL 以外に現れる capacity/quota 文言をリトライ条件として扱わないことを確認する。
- fake の Codex 実行ファイル、呼び出しログ、subcommand log、出力 JSON、retry 回数を組み合わせて、外部 CLI 呼び出しまわりの制御ロジックとログ記録の境界を検証する。

## Read this when
- Codex CLI 呼び出しの retry 条件、retry 後の成功扱い、または retry 上限到達時の失敗扱いを変更する。
- 構造化出力 schema に合わない応答を受けた場合の再実行、call log の残し方、最終結果がどの call log を指すかを確認する。
- capacity エラーの検出元、capacity retry のログ status、returncode、error detail の扱いを変更する。
- quota/capacity を示す文字列が stdout JSONL 以外に出た場合の扱いを確認する。
- Codex CLI 実行のテスト用 stub、PATH 差し替え、Codex home/profile の setup を使った runtime テストを追加・修正する。

## Do not read this when
- Codex CLI 呼び出しではないサブコマンド処理、設定読み込み、path model、repository 作成処理だけを調べたい。
- retry やログ記録に関係しない通常成功時の出力変換だけを確認したい。
- oracle file の正本仕様そのものを確認したい。
- テスト支援 helper の実装詳細だけを変更したい場合は、支援 helper 側を直接読む。

## hash
- 04ff178d04eb9548f0f9b2df64a3aef8b1cbb54c933cdda4848cf77b2186ca61

# `test_indexing_cli.py`

## Summary
- indexing サブコマンドと indexing 共通処理の realization test。INDEX 生成・更新・コミット、未初期化/dirty repo の拒否、linked worktree/apply worktree での対象 root と設定参照、既存 hash による再生成スキップ、semantic entry の検証、兄弟エントリー並列生成、root 直下 memo 除外と nested memo 対象化を外部挙動として検証する。
- apply 側の index conflict 解消が、衝突した INDEX を削除して merge commit を成立させる挙動も扱う。

## Read this when
- indexing の CLI 挙動、preflight、INDEX 更新、INDEX commit の対象制御、dirty repo 判定、worktree 上での indexing 対象 root、repo config の参照元を変更・調査する時。
- index entry の render/update ロジックで、必須 semantic field、空リスト/空文字の拒否、hash が fresh でも malformed な entry を再生成する条件を確認する時。
- INDEX 生成対象の走査で、兄弟要素の並列処理や memo ディレクトリの除外/対象化境界を変更・確認する時。
- apply/join の merge conflict 処理のうち、INDEX 衝突を自動解消して commit する挙動を確認する時。

## Do not read this when
- indexing の正本仕様断片や用語定義だけを確認したい時。oracle 側の該当文書を先に読む。
- indexing の実装詳細、Codex 呼び出しの組み立て、git 操作 helper の本体を変更する時。対応する実装ファイルを直接読む。
- indexing 以外のサブコマンド、通常の apply フロー全体、または CLI エントリポイント全般の挙動を調べる時。より対象範囲の近いテストまたは実装へ進む。
- LLM 出力品質そのものや生成される自然文の妥当性を検証したい時。このテストは structured output の受け渡しと制御ロジックを fake で検証している。

## hash
- 8b7c456348c35f9982daf2f75ae72d3a400cd7fead91f7dc6ef6ebc656ab1c02

# `test_indexing_preflight.py`

## Summary
- Codex 実行・TUI 呼び出しの直前に indexing preflight が実行される制御を検証する realization test。preflight が対象 worktree を選ぶ順序、生成された index 変更の commit と clean 状態、repository lock 待機、特定 purpose での preflight skip を扱う。
- 実際の index 本文生成品質ではなく、Codex 呼び出しラッパーと indexing preflight の実行順序・副作用・抑止条件の入口として位置づけられる。

## Read this when
- Codex exec または TUI 呼び出し前に indexing preflight を走らせる制御を変更する時。
- root と cwd が異なる場合に、どの worktree を indexing 対象にするかを確認・変更する時。
- indexing preflight が作った変更を `cmoc indexing` として commit し、作業ツリーを clean に戻す挙動を確認する時。
- 複数処理の同時実行に対する indexing lock の待機挙動を変更する時。
- index entry 生成や conflict resolution のように indexing preflight を skip する purpose 判定を変更する時。

## Do not read this when
- INDEX.md の本文生成アルゴリズム、要約文の品質、ディレクトリ走査規則そのものを調べたい時。
- Codex 実行ラッパーを通らない純粋な indexing API の入力・出力だけを確認したい時。
- git worktree、commit、lock、purpose-based skip のいずれにも関係しない通常の CLI サブコマンド挙動を調べたい時。

## hash
- 001ef8bbaefb02a24c6e94426c4a65388bb8db8a8c91af26d0c0624eb1f5af8d

# `test_prompt_parts.py`

## Summary
- agent prompt と structured output schema の組み立て結果を横断的に検証する realization test。prompt parts の markdown 描画、routing/file access/各種 standard の注入、ACP builder の model・reasoning・file access mode・schema path・schema 内容の期待値をまとめて扱う。
- 標準 prompt、routing、file access、builder parameter が最終 prompt の同じ読解文脈で結合されることを回帰確認するための入口であり、複数 builder や prompt part にまたがる期待値を一箇所で追う。

## Read this when
- prompt parts の文言、markdown render、blank line 折り畳み、standard doc の注入有無に関するテスト期待値を確認・更新したいとき。
- ACP builder が返す model class、reasoning effort、file access mode、structured output schema path、prompt 内の必須文言を横断的に確認したいとき。
- builder が生成する JSON schema と oracle 側 schema の一致、または jsonschema validate の代表入力を確認したいとき。
- file access rule、routing rule、index entry standard、review oracle standard、realization standard、apply review standard の回帰テストを探すとき。
- apply fork、review oracle、session join、TUI resolve parameter、indexing index entry など複数領域の builder 変更が共通 prompt/schema 期待値へ影響するか確認したいとき。

## Do not read this when
- 単一 builder の実装詳細や prompt 生成ロジック自体を修正したいだけで、まず該当する実装ファイルを直接読む方がよいとき。
- oracle schema の正本内容そのものを確認したいとき。このテストは schema 一致を検証する側であり、正本 schema の本文ではない。
- 個別機能の外部挙動テストだけを探しており、prompt 構築や structured output schema の期待値に関係しないとき。
- INDEX.md エントリー生成の仕様や routing 文書の書き方そのものを確認したいとき。このファイルはそれらの一部文言を回帰検証するテストであり、標準本文ではない。

## hash
- 9e850d504d13ee4e76b707fbbf54800d4a0a4902e306e692c0fd69b706f5a356

# `test_review_oracle_cli.py`

## Summary
- review oracle の CLI 経由の外部挙動と、所見列挙・検証・judge・merge の制御 loop を検証する realization test。report の生成内容、accepted/rejected finding の集計、scope ごとの対象選択、linked worktree 上の review、INDEX 変更の取り込み、処理失敗時の error report、review 実行中に許可される差分境界を扱う。
- 16,000 文字超のテストファイルだが、同じ review run の状態、fake Codex 応答、report 文脈を共有する oracle review の挙動確認として凝集している。

## Read this when
- review oracle コマンドの report 出力、result 判定、finding の採否集計、error report の挙動を変更・確認するとき。
- review oracle の full scope/session scope における oracle 対象選択、gitignored oracle file の除外、binary file や oracle 配下の memo 形状ディレクトリの扱いを確認するとき。
- review oracle が linked worktree、session branch、review worktree、review_fork_commit、review_join_commit をどう扱うべきかを確認するとき。
- 所見の列挙 loop が対象 oracle ごとに関連 finding だけを prompt 文脈へ渡すこと、または merge operation の delete/replace/merge 契約と不正操作拒否を変更するとき。
- review oracle 実行中に生成された INDEX 変更だけを session 側へ取り込み、INDEX 以外の差分を拒否・巻き戻す挙動を確認するとき。

## Do not read this when
- review oracle 以外の review サブコマンド、または一般的な session/init/git helper の仕様だけを確認したいとき。
- Codex CLI の実出力品質や LLM の推論内容そのものを検証したいとき。このテストは fake Codex 応答で制御 flow と外部挙動を確認する。
- oracle file の正本仕様や oracle review の人間向け要求を調べたいとき。まず oracle 側の正本仕様断片を読むべきで、この realization test だけから仕様を逆算しない。
- 単体の merge helper 実装詳細だけを読む場合で、期待する契約が既に明確なときは対象実装を直接読む方が早い。

## hash
- 257e87798cdeb89c1d51d8923c92d5475e3ee4ee3e08f6e9fe69ce0e5738a579

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork / abandon / join について、Git branch・worktree・session state JSON・標準出力/標準エラー・conflict 解決時の Codex 実行条件を、実リポジトリ操作に近い形で確認する。
- session state の生成・更新、session branch と home branch の遷移、linked worktree 上での操作、cleanup 失敗時の rollback、join 時の conflict marker 判定や削除 conflict 解決など、session lifecycle の外部挙動を読む入口になる。

## Read this when
- session fork が session branch と state をどのように作り、session-id 衝突時に既存 state を壊さず retry または失敗するかを確認したいとき。
- session abandon が home branch へ戻る条件、session branch 削除、state の abandoned 化、home branch 不在時や cleanup 失敗時のエラー出力・rollback を確認したいとき。
- session join が session branch の変更を home branch に統合し、linked worktree、branch 削除失敗 warning、未コミット差分エラー、merge 後の予期しない conflict marker 残存エラーをどう扱うかを確認したいとき。
- oracle 配下の conflict 解決で Codex 実行に REALIZATION_WRITE profile と対象ファイルの extra writable path が渡ること、また解決後の conflict marker 検出条件を確認したいとき。
- session サブコマンドの利用者向け出力が stdout と stderr のどちらに出るべきか、成功・失敗時の report 項目がどう検証されているかを確認したいとき。

## Do not read this when
- session 以外のサブコマンドや、CLI 全体の option parsing・command 登録だけを確認したいとき。
- session state の schema や path モデルの正本仕様を確認したいときは、対応する oracle file または実装側の state/path 定義を直接読む。
- Git helper、test fixture、runner、temporary repository 作成方法そのものを調べたいときは、共通 test support を読む。
- Codex 実行 wrapper の一般仕様や file access mode 全体の意味を確認したいだけのときは、runtime や basic.acp 側を読む。

## hash
- ae141d375590381560fd4e95d8616f4ed3ce06bd3b0199ca58742db2f87d7c87
