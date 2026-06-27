# `_support.py`

## Summary
- CLI テストで使う共通のテスト補助関数を集めた realization test 支援モジュール。最小構成の Git リポジトリ作成、Git コマンド実行、現在ブランチ取得、追跡済みかつ ignore 対象の oracle ファイル作成、テスト用 Codex home 設定、偽 Python 実行ファイル作成、apply 用 worktree パス解決を提供する。
- 個別テスト本文ではなく、複数のテストから再利用される fixture 的な準備処理と外部コマンド実行の入口として位置づく。

## Read this when
- テストで一時 Git リポジトリ、初期 commit 済みの cmoc 対象 repo、oracle ディレクトリ、ignore された tracked oracle file を用意する方法を確認したいとき。
- CLI テストで `CliRunner`、Git サブコマンド実行、現在ブランチの検証、`CODEX_HOME` の monkeypatch、偽の外部 Python コマンドを使う補助処理を確認・変更したいとき。
- apply セッション状態から apply worktree のパスを解決するテスト補助の挙動を確認したいとき。

## Do not read this when
- 特定サブコマンドの期待出力、終了コード、状態ファイル内容など、個別の外部挙動を検証するテストケースを探しているとき。
- cmoc 本体の実装、CLI コマンド定義、状態管理、path model の仕様や実装を確認したいとき。
- pytest の一般的な実行方法やプロジェクト全体のテスト構成だけを知りたいとき。

## hash
- 752e74f2361757088f0364eaa53c106968cf0448216e34031eafbfe97eedf32a

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
- runtime の基礎契約を固定する realization test。path token 解決、run/work root 判定、既定 config、error report 整形、session/apply branch 名の検証、CLI preflight と completion probe、`.cmoc` ignore、file access mode と Codex sandbox profile、binary 判定など、cmoc の実行基盤を横断的に検証する。

## Read this when
- runtime 基盤の外部挙動を変更・確認するとき。特に path model、root 判定、error report、CLI 起動前検査、session state branch 解釈、`.gitignore` 更新、file access mode から sandbox 設定への変換を扱うとき。
- Codex profile 生成や sandbox 設定の互換性、completion probe 時の副作用抑制、起動 wrapper の call stack 表示など、利用者に見える CLI 実行時挙動の回帰を確認したいとき。
- runtime 関連の実装変更後に、既存テストへ観点を追加できるか、または同じ制御ロジックを重複検証していないか判断するとき。

## Do not read this when
- 個別サブコマンド固有の正常系 workflow、prompt 内容、oracle 文書生成、Git 操作の高水準仕様だけを確認したいときは、より直接その機能を検証する対象へ進む。
- UI 表示、ドキュメント本文、設定ファイルの網羅的な schema 定義、または runtime に依存しない純粋な helper の詳細だけを扱うときは、この横断的 runtime 回帰テストから読み始める必要はない。
- テスト対象ではなく正本仕様断片を確認したいときは、realization test ではなく対応する oracle file を読む。

## hash
- 9ab75d9226e98bb58fc9c0619f38ab8d412fc55f09c3ae156bc0559aae37c423

# `test_cli_init_tui.py`

## Summary
- CLI の初期化処理と対話型起動処理に関する realization test。初期化時の `.cmoc` 管理対象外化、`.gitignore` 更新、既存 staging の保全、既定設定の生成・同期、linked worktree での保存先や git 状態の扱いを検証する。
- 対話型起動では、エディタで編集された markdown prompt から不要コメントを除去し、解決された実行パラメータに基づいて Codex 呼び出しを組み立て、orig/cmpl prompt log や schema の配置が repository root と linked worktree の文脈で正しく分かれることを検証する。
- markdown prompt parser について、fenced code block 内の見出し風行を見出しとして扱わないこと、および見出し前の本文を独立した本文セクションとして保持することを検証する。

## Read this when
- `init` サブコマンドの git 操作、`.cmoc` の ignore 化、cleanup commit、既存 staged/unstaged 変更の保全、または linked worktree 初期化の挙動を変更・確認したいとき。
- 初期化で作成・同期される設定 JSON の既定値、既存利用者設定を上書きしない merge 挙動、または `.cmoc/config.json` の管理対象外化を確認したいとき。
- `tui` サブコマンドで editor 起動後の prompt 整形、parameter resolve 用 Codex 呼び出し、実行用 Codex 呼び出し、log 保存先、extra read path、linked worktree での cwd/root/schema 配置を変更・確認したいとき。
- markdown prompt を heading 単位に分解する parser の境界条件、特に fenced code block 内の `#` 行や heading 前 preamble の扱いを確認したいとき。

## Do not read this when
- CLI 全体のコマンド定義や共通 runner の基本構造だけを調べたい場合は、実装側の該当サブコマンドやテスト支援 fixture を先に読む。
- `tui` 以外のサブコマンド、または Codex 実行 wrapper そのものの低レベルな引数変換・プロセス実行を調べたいだけなら、より直接の実装ファイルや専用テストを読む。
- oracle file の正本仕様を確認したい場合は、この realization test ではなく対応する oracle doc または oracle test を読む。
- markdown parser の一般仕様ではなく、特定の CLI 入出力や git 状態変更だけを確認したい場合は、parser 関連の末尾テストまで読む必要はない。

## hash
- aa489f15c8b1bb7e134ca5194658d666d2e1c8f2e6e1fdd06e098a8f15e60227

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出し実行層の realization test。exec 実行でプロンプトを stdin に渡すこと、出力 schema と last message の扱い、ログ保存、profile 生成、CODEX_HOME、subcommand logger への記録、console 表示、TUI 起動時の引数・sandbox 設定、repo config の反映、禁止領域変更検出を検証する。
- 外部の本物の Codex CLI ではなく fake executable や subprocess の差し替えを使い、cmoc が Codex CLI をどう起動し、どこへログ・schema・profile を配置し、結果をどう返すかという制御ロジックを確認する入口になる。

## Read this when
- Codex CLI の exec/TUI 呼び出し引数、stdin 渡し、prompt の秘匿、`--output-schema`、`--output-last-message`、profile 名や profile ファイル配置の挙動を変更・確認したいとき。
- Codex 呼び出しログ、prompt/stdout/stderr/call log、subcommand logger の `codex_call` event、console に表示される呼び出し要約の仕様に関わる実装を変更するとき。
- Codex 実行時の `CODEX_HOME`、sandbox workspace、read/write mode、extra read paths、repo config 由来の model/reasoning effort 反映に関わる処理を確認するとき。
- worktree を cwd にした exec 実行で、schema 保存先が root 側ではなく cwd 側の作業状態配下になることを確認したいとき。
- Codex 実行後に保護された agent 関連領域への変更を検出してエラーにする挙動を変更・確認したいとき。

## Do not read this when
- Codex CLI 以外のサブコマンド、Git 操作、oracle/INDEX 生成、一般的な設定読み書きだけを調べたいときは、より対象に近い実装またはテストを読む。
- 実際の Codex CLI や LLM の出力品質、対話内容の妥当性、モデル性能そのものを検証したいとき。この対象は外部 CLI 呼び出しの制御と副作用を fake/stub で検証する。
- path model、oracle file、realization file などの概念定義や正本仕様を確認したいときは、oracle 側の該当文書を読む。
- Codex 呼び出しの利用側 API ではなく、低レベルの subprocess 実装詳細そのものを修正する場合は、まず対応する runtime 実装を読む。

## hash
- 7ff3c69f7d98647a5cef786bbca1a24fcb27687a9fa053a150c1c871c9e37038

# `test_codex_runtime_home.py`

## Summary
- Codex CLI 実行ラッパーが使用する Codex home の決定と事前検証を確認する realization test。環境変数が未設定の場合の既定 home、相対パスを含む環境変数指定の保持、存在しない・ディレクトリでない・認証情報がない Codex home に対する実行前エラーを扱う。

## Read this when
- Codex CLI 呼び出し時の CODEX_HOME 引き継ぎ、既定値、相対パス解決、profile 配置先、call log に記録される Codex home の挙動を確認・変更するとき。
- Codex home や auth.json の欠落・不正なファイル種別に対して、Codex CLI を起動する前に CmocError を返す制御とエラーメッセージを確認・変更するとき。
- Codex CLI 実行を fake executable で置き換え、引数・環境変数・最終メッセージ出力を検証するテストパターンを参照したいとき。

## Do not read this when
- Codex home 以外の Codex CLI 実行結果処理、LLM 出力内容、容量待機、別の環境変数やファイルアクセスモードの挙動を調べたいとき。
- リポジトリ作成 fixture や fake executable 作成 helper 自体の実装を確認したいとき。
- Codex home の正本仕様断片や利用者向け仕様を確認したいとき。

## hash
- dd5ed74f8d35c9de97fc92fd26a23c03fdf69680ca30178bc17d0aaa76b06fc6

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex 実行が quota exceeded で失敗した後、quota availability probe を挟んで再実行または resume する制御を検証する realization test。
- fake の Codex CLI、CODEX_HOME、通話ログ、標準入出力ログ、SubcommandLogger のイベントを使い、quota retry 時の外部挙動とログ記録の整合性を確認する。
- 単一実行だけでなく、resume token が無い場合の再実行、および並列実行時に代表 probe が 1 回だけ使われる制御も扱う。

## Read this when
- Codex 実行の quota exceeded 検出、quota availability probe、resume、または再実行の挙動を変更・調査する時。
- Codex 呼び出しログ、prompt/stdout/stderr/output のログファイル、SubcommandLogger の codex_call イベント、console 出力の quota retry 関連表示を確認する時。
- 複数の Codex 実行が同時に quota exceeded になった場合の probe 集約や、並列 retry 制御の回帰を調べる時。

## Do not read this when
- 通常の Codex 実行成功経路、quota と無関係な失敗処理、または CLI 引数全般だけを調べたい時。
- repository 作成、CODEX_HOME 準備、fake executable 作成などのテスト支援関数そのものの実装を確認したい時。
- INDEX.md 生成、oracle file の仕様整理、または quota retry 以外の routing 文書作成ルールを確認したい時。

## hash
- ac922fbdb31ab155a091861d1a0ea601a4551ae208afede89d194bdadaa25341

# `test_codex_runtime_retry.py`

## Summary
- Codex CLI 実行ラッパーの retry 制御を検証する realization test。schema validation 失敗後の再実行、capacity error の再試行ログ、stdout JSONL 以外に出た capacity/quota 文字列を retry 判定に使わないことを、fake codex 実行ファイルとログ内容で確認する。

## Read this when
- Codex CLI 呼び出しの retry 条件、retry 後の成功扱い、または retry 時の call log / prompt log / stdout log / subcommand log の記録仕様を変更・確認したいとき。
- structured output schema 検証失敗時に再実行される挙動や、再実行ごとに別のログ path が残る挙動を確認したいとき。
- capacity error を stdout JSONL の error event から検出して再試行する制御、またはその retrying/succeeded event のログ内容を確認したいとき。
- stderr や通常 stdout の文字列だけでは capacity/quota retry 扱いせず、通常の Codex CLI 失敗として扱う境界を確認したいとき。

## Do not read this when
- Codex CLI 実行ラッパー本体の実装、設定値、例外型、またはログ writer の定義を直接確認したいとき。
- retry と無関係なサブコマンド、repository 作成 helper、Codex home setup helper、または fake executable 作成 helper の一般仕様を調べたいとき。
- LLM 出力品質そのものや Codex CLI の実物の外部挙動を検証したいとき。

## hash
- 5601e9a26e88b8f2216424753c9ca37601cdd03e064506165391680164a26cab

# `test_indexing_cli.py`

## Summary
- cmoc の indexing 系の realization test。CLI 実行、preflight、INDEX 生成・再生成、git commit 対象、worktree 上の動作、既存 hash によるスキップ、エントリー構造の検証、並列生成、memo ディレクトリ扱いを外部挙動として確認する。
- indexing 実装が Codex に Structured Output schema でエントリー生成を依頼し、生成結果を INDEX に反映して commit する制御を検証する入口になる。
- apply 側の INDEX 競合解消について、競合した INDEX を削除して merge commit を成立させる挙動もこのテスト群で扱う。

## Read this when
- cmoc indexing コマンド、indexing preflight、INDEX 更新処理、エントリー描画・検証、hash freshness 判定、または commit 対象の制御を変更する。
- リンク worktree や apply 用 worktree で indexing がどの root と config を使うべきかを確認したい。
- 未初期化 repo、未コミット差分、既存 INDEX、malformed entry、memo 配下、並列生成など、indexing の境界条件に関する期待挙動を確認したい。
- INDEX 競合解消処理が削除・解決・commit まで行うかを確認したい。

## Do not read this when
- indexing と無関係な CLI サブコマンド、設定読み書き、path model、または一般的な git helper の詳細だけを調べる場合。
- Codex 実行の中身や LLM 出力品質そのものを検証したい場合。このテストは Codex 呼び出しを fake に置き換え、制御ロジックと副作用を検証している。
- INDEX.md エントリーの文章品質や oracle file の正本仕様を確認したい場合。対象は realization test であり、仕様本文の代替ではない。

## hash
- 1743ad69d9e574aa531a64b05e1a2b677c9bf9837aef7d073c1ead2bf624bab9

# `test_indexing_preflight.py`

## Summary
- Codex 実行や TUI 起動の直前に INDEX.md 更新を走らせる preflight の realization test。通常の実行経路、作業ツリー優先、ロック待機、特定 purpose でのスキップ条件を、Codex 本体呼び出し・git commit・作業ツリー状態への副作用として検証する。

## Read this when
- Codex 呼び出し前に indexing preflight が実行されるか、実行順序が indexing 先行になっているかを確認・変更したいとき。
- root と cwd が別の git worktree を指す場合に、どの作業ツリーへ INDEX.md 更新と commit を行うべきかを確認したいとき。
- indexing 用 repository lock の待機挙動や、同時実行時に更新が始まるタイミングを扱うとき。
- index entry 生成や conflict resolution など、preflight を再帰・競合回避のためにスキップする purpose 判定を変更するとき。
- preflight 実行後に cmoc indexing commit が作られ、対象 worktree が clean に戻ることをテストで確認したいとき。

## Do not read this when
- INDEX.md の内容生成ロジック、エントリー本文の schema、ルーティング文書の品質基準そのものを調べたいとき。
- apply join や conflict resolution の本体挙動を調べたいだけで、Codex 呼び出し前の indexing skip 判定に関心がないとき。
- 通常の indexing 更新処理の差分検出・ファイル走査・エントリー生成を変更する場合で、preflight から呼ばれる外側の制御に関心がないとき。
- Codex runtime の引数組み立てや subprocess 実行の詳細を調べたいだけで、preflight の挿入順序や副作用を確認しないとき。

## hash
- 8c91a6b5adc4c8be5e8caaabb2df7cb153fc2278af7ab2afc33fbb5c790762d6

# `test_prompt_parts.py`

## Summary
- prompt part と ACP builder が生成する prompt、標準文書、file access rule、routing rule、structured output schema、実行パラメータの期待値を横断的に検証する realization test。
- agent prompt と structured output schema の構築結果を同じ読み取り文脈で扱うため、標準 prompt、routing、file access、builder parameter の回帰観点を一箇所に集約している。

## Read this when
- prompt 構築、標準文書の markdown rendering、file access mode ごとの文言、routing rule の含有条件に関するテスト期待値を確認したいとき。
- ACP builder が返す model class、reasoning effort、file access mode、structured output schema path、prompt への標準文書埋め込みを変更・確認するとき。
- structured output schema の制約、oracle schema との一致、空配列拒否、論理 enum 値など、schema 生成結果の回帰を調べるとき。
- prompt 内の用語置換や sanitization、root path 展開、aux prompt と code block の扱いを確認するとき。
- 実行パラメータ解決、apply fork、review oracle merge finding、session join conflict resolution など複数 builder の統合的な期待値を追うとき。

## Do not read this when
- 個別 builder や prompt part の実装詳細だけを変更する場合で、対象実装ファイルの局所的な責務や内部処理を先に確認すれば足りるとき。
- CLI コマンド、永続状態、git 操作、path model など、prompt/schema 生成結果に直接関係しない挙動を調べるとき。
- 特定の標準文書や schema の正本内容そのものを確認したい場合。このテストではなく、対応する oracle file または実装側の生成元を読む方が直接的。

## hash
- c2e5ef07ba17f688f9c3c9d3e73ec27e7d493a7956af3c47313c9ff7b4db185d

# `test_review_oracle_cli.py`

## Summary
- eval-oracle の CLI 経由の外部挙動を検証する realization test。report 生成、scope 指定、oracle 対象選択、所見の列挙・検証・judge・merge、結果集計、エラー report、review 用 worktree と INDEX.md 変更の取り込み、想定外差分の拒否を扱う。
- oracle review の同一 run 状態と fake Codex 応答を共有する統合的なテスト群であり、所見 loop と report 文脈を一箇所で確認する入口になる。

## Read this when
- eval-oracle の CLI 出力、report 内容、scope の意味、対象 oracle の数え方や除外条件を変更・確認したいとき。
- oracle review の所見 loop、merge operation の契約、verdict と severity による report 並び順や集計を変更・確認したいとき。
- review 用 worktree、linked worktree、INDEX.md 変更の merge、conflict 解決、INDEX.md 以外の差分拒否に関わる挙動を確認したいとき。
- run_codex_exec を fake 化して eval-oracle の制御フローをテストする既存パターンを探すとき。

## Do not read this when
- oracle review の実装本体や report renderer の詳細を変更したいだけで、テスト観点ではなく処理定義を先に確認すべきとき。
- session fork、git worktree 操作、設定読み込みなど eval-oracle 以外の個別機能の単体挙動だけを調べたいとき。
- Codex CLI や LLM の実出力品質を検証したいとき。この対象は fake 応答による制御ロジックと外部挙動の検証に閉じている。
- oracle file の正本仕様そのものを確認・編集したいとき。realization test ではなく oracle 本文を読むべき。

## hash
- cc04a552b239086776e9968ea8266f03dd0cd716c4e8e0044da3e14769c2aae7

# `test_session_cli.py`

## Summary
- session サブコマンドの CLI 挙動を検証する realization test。session fork による session branch と session state 生成、session id 衝突時の retry/失敗、cmoc ignore 初期化、linked worktree 上での branch/head 扱いを確認する。
- session abandon の成功時 cleanup、home branch 不在時のエラー出力、cleanup 失敗時の rollback、linked worktree 上での復帰先 branch を検証する。
- session join の merge・conflict resolution・delete conflict staging・session state 更新・session branch 削除失敗時警告・stdout/stderr へのエラー出力先を、実リポジトリ操作と Codex 実行の差し替えで確認する。

## Read this when
- session fork/abandon/join の CLI 外部挙動、git branch/worktree 操作、session state JSON のライフサイクルを変更または確認するとき。
- session id 衝突、home branch 不在、cleanup 失敗、未コミット差分、merge conflict、conflict marker 残存など、session サブコマンドの異常系出力や rollback を調べるとき。
- session join の conflict resolution で Codex に渡す file access mode、writable roots、oracle conflict 解決後の staging 処理を変更または確認するとき。
- linked worktree から session サブコマンドを実行した場合に、root worktree と linked worktree の現在 branch がどう保たれるべきか確認するとき。

## Do not read this when
- session サブコマンド以外の CLI command、設定読み込み、path model、一般的な runtime 処理だけを調べたいとき。
- unit test helper や repository fixture の実装そのものを変更したいときは、支援コード側を直接読む方が適切。
- session サブコマンドの内部 helper の細かな実装構造だけを確認したいときは、対応する実装モジュールを直接読む方が適切。
- oracle file の正本仕様を確認したいときは、test ではなく oracle 側の該当文書を読む方が適切。

## hash
- 196c0353a7d236aff1a8c4e3e0746533b38216766c6e6ff87770060e869558a0
