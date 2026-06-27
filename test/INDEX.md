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
- cmoc の基礎 runtime 契約を固定する realization test。path token 解決、linked worktree と run/work root の扱い、config 既定値、構造化 error report、session/apply branch 形状、CLI preflight と completion probe、`.cmoc` ignore、file access mode と Codex sandbox profile、binary 判定を横断的に検証する。
- runtime の利用者向け出力、sandbox 設定、worktree 判定、永続 state の branch 解釈など、複数の基礎 module にまたがる外部挙動の回帰確認入口として位置づく。

## Read this when
- path token、repo root、run root、work root の解決契約を変更または確認するとき。
- CmocError の Markdown report、CLI error の stdout/stderr 振り分け、Click parse error の変換、completion probe 時の副作用抑制を扱うとき。
- session branch または apply branch から session id/run id/state を解釈する処理を変更するとき。
- `.cmoc` の gitignore 追加、file access mode の永続化値、Codex sandbox mode/profile の writable roots を変更するとき。
- binary 判定の読み取り量や config の model class/reasoning effort 既定値に関わる基礎挙動を確認するとき。

## Do not read this when
- 個別サブコマンドの通常フローや詳細 UI 文言だけを調べたいときは、そのサブコマンド固有の実装またはテストを先に読む。
- oracle 正本仕様そのもの、INDEX.md 生成規則、ドキュメント構成を確認したいときは、対応する oracle file または文書系テストを読む。
- 単一 helper の内部実装だけを変更し、このファイルが検証する外部契約や制御境界に影響しないことが明らかなとき。

## hash
- 639e0c7946768daf52f03097b36d3dd704b9fac144390b5df04766d331e82e92

# `test_cli_init_tui.py`

## Summary
- CLI の初期化と TUI サブコマンドに関する realization test。初期化時の `.cmoc` 管理除外、`.gitignore` 更新、既存 staged/unstaged 変更の保持、linked worktree での保存先・commit 対象、既定設定 JSON の生成と既存設定値の保持を検証する。
- TUI について、エディタ起動後の markdown prompt 整形、parameter 解決、Codex 呼び出しパラメータ、prompt ログ保存先、linked worktree での root/cwd/schema/log の扱い、subcommand log の記録先を検証する。
- markdown prompt parser について、fenced code block 内の heading 風行を見出し扱いしないことと、見出し前の本文を保持することを検証する。

## Read this when
- `init` サブコマンドの git 操作、`.cmoc` の ignore、cleanup commit、既存 index/worktree の変更を壊さない挙動を変更・調査する。
- 初期設定ファイルの default 値追加、既存ユーザー設定との merge、設定ファイルを git 管理対象にしない挙動を変更・調査する。
- `tui` サブコマンドのエディタ連携、prompt 補完ファイル生成、parameter 解決、Codex exec/TUI 呼び出し、ログ保存先、linked worktree 対応を変更・調査する。
- markdown prompt の heading 分割や fenced code block の扱いを変更・調査する。

## Do not read this when
- CLI 全体のルーティングやコマンド定義だけを確認したい場合は、実装側の CLI entrypoint や該当サブコマンド実装を先に読む。
- `init` や `tui` に関係しないサブコマンド、oracle 文書生成、review/apply 系の挙動を調査する場合は、該当するテストまたは実装へ直接進む。
- Codex 実行基盤そのもの、model class、reasoning effort、file access mode の一般的な変換規則だけを確認したい場合は、共通 parameter 実装やその専用テストを読む。
- markdown parser 以外の markdown 文書処理や INDEX.md 生成規則を調査する場合は、その責務を持つ実装・テストを読む。

## hash
- c285f00e235fcf9c365be0c766e2410bbc968e7fcbfea409619185808c3c6d0d

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出しの runtime wrapper に対する realization test。exec 呼び出しでは prompt を標準入力で渡すこと、schema と出力 JSON の扱い、CODEX_HOME/profile/log 生成、stdout/stderr 分離、subcommand logger とコンソール表示を検証する。
- worktree を cwd にした exec 呼び出しで schema が作業 cwd 側の状態領域へ保存され、call log は repo 側に残ることを検証する。
- repo write 権限の exec 呼び出し後に `.agents` 配下が変更された場合の拒否、TUI 呼び出しの argv/env/profile/sandbox/log、repo config による Codex model/reasoning effort 反映を検証する。

## Read this when
- `run_codex_exec` の argv、標準入力、`--output-schema`、`--output-last-message`、output JSON 読み取り、stdout/stderr ログ、call log、prompt log、subcommand logger、コンソール表示の期待挙動を確認または変更するとき。
- Codex 実行時の `CODEX_HOME`、一時 profile 名・profile file、repo config からの model/reasoning effort 読み込み、sandbox profile 生成を変更するとき。
- worktree cwd での schema 保存場所、repo 側 log 保存場所、`.agents` 配下変更検出、TUI 呼び出しで prompt を引数として渡す挙動を変更するとき。

## Do not read this when
- Codex CLI wrapper ではなく、一般的な git 操作、path model、設定 schema 自体、または他サブコマンドの入出力だけを調べるとき。
- LLM の応答品質、Codex CLI 本体の内部仕様、または実際の Codex 実行結果の内容を検証したいとき。ここでは fake executable と monkeypatch による wrapper の制御ロジックだけを扱う。
- runtime の外部挙動ではなく、support fixture の実装詳細や repository 作成 helper の挙動を調べるときは、対応する test support 側を直接読む。

## hash
- 183a101ddafe11c9f38d6506c26571eaed2f5fede8855814e521600ffa420d9d

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
- session サブコマンドの realization test。session fork / abandon / join が Git branch、worktree、session state、エラー出力、競合解決時の Codex 実行 profile をどう扱うかを、CLI 経由の外部挙動として検証する。
- 一時 repository を作り、実際の git 操作と CLI runner を組み合わせて、session branch の生成・削除、home branch への復帰、linked worktree 上の挙動、状態 JSON の更新、stdout / stderr の出力先を確認する。

## Read this when
- session fork が session branch と状態ファイルを作る条件、session-id 衝突時の retry / 失敗時 rollback、cmoc ignore 初期化とログ生成の関係を確認したいとき。
- session abandon が home branch へ戻ること、session branch を削除すること、home branch 不在や cleanup 失敗時に状態と branch をどう保つかを確認したいとき。
- session join が session branch の変更を home branch へ取り込むこと、linked worktree で作業 branch をどう扱うか、join 後の状態更新や session branch 削除失敗時の warning を確認したいとき。
- join の merge conflict 解決で Codex に渡す file access mode、writable roots、oracle file だけを書き込み対象にする制御、delete conflict 解決後の staging を確認したいとき。
- session 系コマンドのエラー報告が stdout と stderr のどちらへ出るべきか、想定内エラーと merge 後の予期しないエラーの違いを確認したいとき。

## Do not read this when
- session 以外のサブコマンド、設定読み込み、path model、または一般的な runtime helper の挙動だけを調べたいとき。
- session の正本仕様断片そのものを確認したいとき。この対象は realization test であり、仕様判断の起点には oracle file を読む。
- session 実装の内部関数分割や helper の責務を詳しく追いたいとき。まず対応する implementation を読む。
- 単に CLI の登録構造や Typer app 全体の command wiring を確認したいとき。

## hash
- 0788461ab94b4159f1e650765b0d78c8db53d8d0d9899edb52ee3a0a8f7c52cc
