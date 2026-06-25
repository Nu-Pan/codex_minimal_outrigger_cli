# `_support.py`

## Summary
- テスト内で共通利用する補助関数群をまとめた realization test の支援モジュール。git リポジトリ作成、テスト用 CODEX_HOME 設定、ブランチ取得、apply 用 worktree 解決など、CLI テストの前提環境を小さく構築する入口になる。
- Typer のテスト runner や主要な cmoc 実装モジュールを同じ場所から参照できるようにし、複数テストで共有される setup と状態参照を集約している。

## Read this when
- CLI テストで一時 git リポジトリ、初期 commit、oracle 配下の fixture、または追跡済み ignore 対象ファイルを用意する helper を確認・追加したいとき。
- テスト中に CODEX_HOME を一時ディレクトリへ向ける処理や、認証ファイルを含む最小の Codex home fixture を再利用したいとき。
- apply 系テストで保存状態から apply branch の worktree path を復元する共通処理を確認したいとき。
- 複数のテストファイルにまたがって同じ subprocess git 操作や CLI runner setup が重複しそうなとき。

## Do not read this when
- 個別サブコマンドの期待出力、エラー条件、状態遷移を確認したいだけなら、該当するテスト本文を直接読む。
- プロダクト実装の CLI 定義、runtime 処理、path token 解決、sandbox mode 変換の挙動を変更したいときは、対応する実装側の本文を読む。
- oracle file の正本仕様断片や仕様文書を確認したいときは、このテスト支援モジュールではなく oracle 側の本文を読む。

## hash
- 177bd3430c87ab5f9b7100c81bd29747aefe79b9e5248eaa456c01e737e6345d

# `test_apply_abandon_cli.py`

## Summary
- apply run を破棄する CLI 挙動を検証する realization test。apply 用 worktree と branch の削除、apply 状態の ready への戻し、永続状態からの apply_branch・apply_worktree・apply_process_id の消去、利用者向け出力の要点を扱う。
- cleanup 対象が既に無い場合の warning、running 状態の apply process 停止、process id が無い running 状態の許容、apply worktree 上からの実行時に元 root へ戻る挙動を検証する。
- 破棄対象を特定できない apply_branch や、現在の apply branch が active apply run と異なる stale branch の場合に、状態と cleanup 対象を壊さずエラーにする境界を検証する。

## Read this when
- apply abandon の正常系、cleanup、状態更新、警告出力、エラー境界を変更・確認したいとき。
- apply fork 後に作られる apply branch・apply worktree・session state のライフサイクルをテスト側から追いたいとき。
- running 中の apply を abandon する際の process id file、stop 処理、cleanup 順序に関わる挙動を確認したいとき。
- apply worktree 内から CLI を実行する場合や、stale apply branch から誤って abandon する場合の保護挙動を確認したいとき。

## Do not read this when
- apply abandon 以外の apply サブコマンド、session 操作、init 操作そのものの仕様や実装を調べたいとき。
- Codex exec の出力品質や findings 内容そのものを検証したいとき。
- git worktree や branch 操作の低レベル helper 実装だけを調べたいとき。
- oracle file の正本仕様断片を確認したいとき。

## hash
- 1f1d569b4a676d9882640619423f66d878c7207b4c3b7194fd434a6a7c84fa40

# `test_apply_fork_cli.py`

## Summary
- apply fork コマンドの realization test。session fork 後の apply 実行が Codex ループ、apply branch/worktree、session state、report、commit message、change summary、終了コードをどう扱うかを CLI 経由で検証する。
- apply fork 周辺の制御ロジックとして、設定読み込み失敗時に apply run を開始しないこと、既存の ignore 設定を不要に書き換えないこと、編集対象にできるファイルと禁止対象差分の扱い、dirty file の再検査、rolling 実行時の前回 join commit 利用を確認する。

## Read this when
- apply fork の CLI 挙動、終了コード、session state の apply セクション、apply branch/worktree の生成規則、report 出力の期待値を変更・調査する時。
- apply fork が Codex exec をどの purpose で呼び、所見列挙、所見適用、commit message 生成、change summary 生成をどう組み合わせるかをテスト観点から確認したい時。
- apply fork が repository root の ignore 設定、root 直下の memo 除外、ネストした memo ディレクトリ、編集禁止対象差分をどう扱うべきかを確認する時。
- apply join 後に oracle 側だけが変わった状態で、次回 apply fork がどの変更対象を再検査するかを確認する時。

## Do not read this when
- apply fork 以外の apply サブコマンド、session fork 自体、init 自体の基本仕様だけを調べたい時。
- CLI テストではなく、apply fork の実装関数の内部構造や helper の責務分割を直接変更するために読む入口を探している時。
- Codex CLI や LLM の出力品質そのものを検証したい時。ここでは Codex 実行は fake に置き換え、cmoc 側の制御と副作用を検証している。
- oracle file の正本仕様を確認したい時。この対象は realization test であり、正本仕様の代替ではない。

## hash
- 5581aa37603436b33e703e541542087b1a4597749f215898037dc2534011e6ba

# `test_apply_join_cli.py`

## Summary
- `apply join` コマンドの realization test。apply 用 worktree と branch の cleanup、session state の復帰、join commit 記録、report 生成を、正常系と失敗系の CLI 挙動として検証する。
- apply worktree 側から実行した場合の root への復帰、dirty な apply worktree の拒否、ログ保存先、stderr/stdout の出力先など、実行場所に依存する join 処理の境界を扱う。
- 想定外の apply 差分、force resolve による差分破棄、merge conflict の残存報告、`INDEX.md` conflict の通常解決継続など、join 中の差分検出・conflict 処理の回帰を押さえる。

## Read this when
- `apply join` の成功時 cleanup、状態更新、report 出力、join commit 記録に関する外部挙動を変更・確認する場合。
- apply worktree から `apply join` を実行する経路、dirty worktree の拒否、ログ出力先、stdout/stderr の出し分けを調べる場合。
- apply 側で発生した想定外差分、`.gitignore` や oracle 側変更の扱い、`--force-resolve` の破棄挙動を確認する場合。
- merge conflict の報告、report への conflict 記録、`INDEX.md` conflict を通常 mode で解決して join を継続する挙動を変更する場合。

## Do not read this when
- `apply fork` の Codex 実行内容そのものや LLM 出力品質を確認したいだけの場合。
- session 作成、初期化、git helper、path model など、`apply join` の CLI 外部挙動ではない共通基盤を調べる場合。
- join 後の report 本文形式の網羅的な仕様を調べる場合。ただし report ファイルの生成有無や conflict 記録の有無だけを確認するなら読む価値がある。

## hash
- 3fb78f609c3d0941b87751ca971181aee89a49c4f40be36780a08f792d4c01db

# `test_basic_runtime.py`

## Summary
- 基本ランタイムと CLI 起動前後の共通挙動を検証する realization test。パス表記への変換、時間表示、repo root と work root の判別、既定設定、構造化エラー出力、session branch 形状、CLI エラーの stderr 出力、補完プローブ時の副作用抑止、`.cmoc` の ignore 設定、file access mode と Codex profile の権限生成を扱う。
- 個別サブコマンドの詳細仕様よりも、cmoc 全体で共有される実行環境・設定・エラー処理・ファイルアクセス制御が壊れていないかを確認する入口になる。

## Read this when
- パス token 解決、`<cmoc-root>` 表記、repo root と work root の区別、linked worktree 上の root 判定を変更または確認するとき。
- 実行時間表示、既定の model class・reasoning effort・並列数、構造化エラー markdown の形式を変更または確認するとき。
- CLI の引数解析エラー、preflight、work root 強制、detached HEAD 時のエラー、補完プローブ時の副作用抑止を変更または確認するとき。
- `.cmoc` を `.gitignore` に追加する処理、既存 ignore pattern を尊重する処理、file access mode の文字列表現や sandbox mode 変換を変更または確認するとき。
- Codex profile に含める read/write/deny_read/read_only/writable_roots などの権限生成を変更または確認するとき。

## Do not read this when
- 特定サブコマンド固有の正常系フロー、セッション状態の詳細、または Git 操作の高水準シナリオだけを確認したいときは、該当するより直接のテストを読む。
- oracle file の正本仕様や文書構成を確認したいときは、対象となる oracle doc または oracle test を読む。
- 内部 helper の分割、命名、局所的な実装整理だけで、このファイルが検証する外部挙動・制御ロジックに影響しないと分かっているとき。

## hash
- d21c5e428fc7c531de0bced90850f2e6225e0f7a5c7fb237d5efbb9fc6e993aa

# `test_cli_init_tui.py`

## Summary
- CLI の初期化、対話起動、Markdown プロンプト解析に関する realization test。`init` が `.cmoc` の追跡解除、`.gitignore` 更新、既存 staging の保護、linked worktree での保存先分離、既定設定生成と既存設定の同期を行うことを検証する。
- `tui` がエディタで編集された依頼文から不要コメントを除去し、resolve 用 Codex 実行で起動パラメータを決め、完成プロンプトを保存して Codex TUI を呼ぶ流れを検証する。linked worktree では実リポジトリ root と作業 cwd、schema・log の保存先が分かれることも扱う。
- Markdown プロンプト解析について、fenced code block 内の見出し風行を見出し扱いしないこと、先頭見出し前の本文を保持することを検証する。

## Read this when
- `init` サブコマンドの Git 副作用を変更・調査する。特に `.cmoc` の ignore、追跡解除、cleanup commit、既存 staged/unstaged 変更の保護、linked worktree 上の初期化挙動を確認したいとき。
- `.cmoc/config.json` の既定値、既存ユーザー値を上書きしない defaults sync、設定項目追加時の期待テストを確認したいとき。
- `tui` サブコマンドのエディタ起動、依頼文整形、parameter resolve、Codex TUI 起動、完成プロンプト保存、log/state/schema の配置を変更・調査するとき。
- linked worktree で `init` または `tui` の保存先、Git root と cwd の扱い、root 側 `.cmoc` と worktree 側 `.cmoc` の分離を確認したいとき。
- Markdown 依頼文 parser の heading 抽出、fenced code block、見出し前 preamble の扱いを変更・調査するとき。

## Do not read this when
- CLI コマンドの実装詳細だけを読みたい場合は、まず実装側の対象へ進めばよい。この対象は外部挙動と制御結果を検証するテストである。
- `init`、`tui`、Markdown プロンプト解析に関係しないサブコマンドやドメイン機能のテストを探している場合は読まなくてよい。
- Codex CLI やエディタ実行そのものの品質、実際の LLM 出力内容を評価したい場合は対象外である。この対象は fake 実行や monkeypatch によって cmoc 側の制御と保存結果を検証している。
- INDEX 生成、oracle review、apply fork など、この対象内で設定項目名として触れられるだけの機能本体を調査する場合は、より直接の実装・テストへ進む方がよい。

## hash
- 9de769ced8a3bb018342e8a5c9888ecaac1b15e9fe71a081cdddfad6a92d7336

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 呼び出し runtime の realization test。exec 経路が prompt を標準入力で渡し、schema・profile・call log・stdout/stderr log・subcommand log を期待どおり生成することを検証する。
- worktree を cwd にした exec 呼び出しで、schema 保存先が root ではなく作業 cwd 側の state 配下になることを確認する。
- TUI 経路が exec サブコマンドを使わず prompt を argv 末尾に渡し、CODEX_HOME・workspace write profile・call log・戻り値を設定することを検証する。
- repository config の codex model と reasoning effort が exec 用 profile に反映されることを確認する。

## Read this when
- Codex CLI を外部プロセスとして起動する runtime の argv、stdin、cwd、環境変数、profile 生成、ログ生成を変更する。
- structured output schema の一時保存場所、特に worktree や cwd と root の関係を扱う挙動を確認する。
- TUI 呼び出しと exec 呼び出しの違い、prompt の渡し方、出力 capture の有無を変更または調査する。
- codex model や reasoning effort の repository config 読み込みと profile 反映を変更する。

## Do not read this when
- Codex CLI runtime 以外のサブコマンド、oracle 文書、INDEX.md 生成、path model などの挙動だけを調べる。
- 実際の Codex CLI や LLM 出力品質そのものを検証したい。ここでは fake codex と monkeypatch による呼び出し制御だけを扱う。
- Git 操作一般、worktree 作成一般、pytest fixture 全般を調べたい。ここでの git worktree は schema 保存先検証のための補助条件に限られる。

## hash
- ee8f42edbf30d992cc13f83d08948cf30473e258ffbfdfcdc76643ded6545c6a

# `test_codex_runtime_home.py`

## Summary
- Codex runtime wrapper の CODEX_HOME default、既存 CODEX_HOME 維持、missing home、file home、missing auth.json の事前失敗を検証する realization test。

## Read this when
- Codex CLI 呼び出し前の CODEX_HOME 解決、環境変数引き継ぎ、auth.json validation、事前エラー文面を変更する。

## Do not read this when
- subprocess stdin/log/schema 保存や quota retry/resume の挙動を確認したい。

## hash
- edede0989727c4367d407b9fa2be3dfac723e7f2300fb9f5fda3bd51396503f4

# `test_codex_runtime_retry.py`

## Summary
- Codex 実行ラッパーの再試行制御を検証する realization test。schema 検証失敗時の再実行、capacity エラー時の再試行ログ、quota 超過時の availability probe と resume または通常再実行、並列実行時の代表 probe 集約を、fake Codex CLI とログ副作用で確認する。

## Read this when
- Codex CLI 呼び出しの retry・polling・resume 挙動を変更する。
- schema validation 失敗、capacity、quota exceeded の扱いと、それぞれの再試行時に記録される call log、stdout/stderr/output path、subcommand log event を確認したい。
- quota availability probe の argv、stdin、CODEX_HOME、console 表示、並列実行時の probe 数制御に関わるテストを探している。

## Do not read this when
- 通常成功する Codex 実行の基本的な argv 組み立てや sandbox/profile 設定だけを確認したい。
- Codex 以外のサブコマンド、リポジトリ作成、path model、oracle/realization 分類の仕様を調べたい。
- retry 制御ではなく、ログ基盤そのものの汎用仕様や helper fixture の定義を確認したい。

## hash
- 5655c16688d15dfb44a5eeb4af41c7ea35ed96eddcdcc587c4181007d8fe782f

# `test_indexing_cli.py`

## Summary
- indexing コマンドと indexing preflight の realization test。INDEX 生成・更新・commit 対象の限定、既存 hash による再生成 skip、不正 entry の再生成、同階層 entry の並列生成、root 直下 memo 除外と入れ子 memo 対象化、linked worktree 対象化、Codex 呼び出し前の indexing 実行、lock 待機、特定 purpose での preflight skip を検証する。
- merge conflict 解決時に INDEX を削除して merge commit を成立させる挙動と、未初期化 clean repo で indexing が非 INDEX 差分を残さず失敗する挙動も扱う。

## Read this when
- indexing コマンドの外部挙動、commit される path、dirty worktree の扱い、未初期化 repository での失敗条件を変更・確認するとき。
- INDEX entry 生成のための Codex structured output 呼び出し、fresh hash による再生成 skip、不正または欠落した entry の再生成判定を変更・確認するとき。
- worktree 上で indexing がどの repository を対象にするか、Codex exec/tui 呼び出し前に indexing preflight が走る条件、または preflight を skip する purpose 条件を変更・確認するとき。
- indexing lock の待機、同階層 entry 生成の並列化、root 直下 memo と入れ子 memo の indexing 対象境界を変更・確認するとき。
- INDEX merge conflict の解決処理が conflict path を削除して commit する制御を変更・確認するとき。

## Do not read this when
- INDEX.md のルーティング文書としての書式や entry 文面の仕様だけを確認したいとき。正本仕様断片または schema の方が直接の入口になる。
- Codex 呼び出し一般の parameter 定義、model class、reasoning effort、file access mode の意味を確認したいだけのとき。support module や実装側の型定義がより直接の入口になる。
- indexing 以外の CLI サブコマンド、session/apply/review などの挙動を確認したいとき。ただしそれらが Codex 呼び出し前の indexing preflight と接続する場合は読む。
- git helper、repository fixture、runner fixture の作りそのものを変更したいとき。共通 test support の定義がより直接の入口になる。

## hash
- 7f919eed81196ee108970e3921c3fd2b0d09c423f1a8c148b30477a7364d9190

# `test_prompt_parts.py`

## Summary
- プロンプト構築部品と関連するパラメータビルダーのテストをまとめる realization test。レビュー基準、ルーティング規則、ファイルアクセス規則、INDEX エントリー基準、実現基準、レビュー oracle 基準が StructDoc と markdown 出力に期待語句を含むことを検証する。
- complete prompt の標準部品の常時・任意挿入、TUI パラメータ解決用 schema とプロンプト内容、indexing・review oracle merge finding・session join conflict resolution のモデル種別、reasoning effort、file access mode の選択を確認する入口になる。

## Read this when
- プロンプト部品の文言、タイトル、markdown レンダリング結果、または complete prompt に含める標準セクションの有無を変更する。
- file access mode ごとの禁止・許可文言や、TUI で選択可能な file access mode と boolean flag の schema を変更する。
- index entry、review oracle merge finding、session join conflict resolution などのビルダーが返す model class、reasoning effort、file access mode、prompt 内容の期待値を確認したい。
- レビュー基準、ルーティング規則、実現基準、INDEX エントリー基準、レビュー oracle 基準の主要キーワードがテストで固定されているかを調べたい。

## Do not read this when
- 個別の標準文書やプロンプト部品の実装ロジック自体を理解・修正したいだけで、テスト上の期待値を確認する必要がない。
- CLI 実行、作業ディレクトリ操作、永続状態、Git 操作など、プロンプト構築部品やパラメータ選定と無関係な挙動を調べている。
- INDEX.md 生成処理の内部実装を追う必要があり、テストで固定された期待語句ではなくビルダー本体や schema 定義を直接確認すべき状況。

## hash
- cc6c38730cc38e454b232d230d947ae8920ed5ddd0297e9501901bf0fceaa75d

# `test_review_oracle_cli.py`

## Summary
- `review oracle` コマンドの realization test。レビュー対象 oracle の列挙、scope 指定、gitignore 対象の除外、レポート生成、レビュー用 worktree からの INDEX.md 変更取り込み、処理失敗時の error report、INDEX.md 以外の差分拒否を、CLI 実行結果と生成レポートの内容で検証する。

## Read this when
- `review oracle` の外部挙動、レポート出力、scope の既定値や短縮オプションを変更・確認する時。
- oracle file のレビュー対象選定で、gitignore 対象や session/full scope の扱いを確認する時。
- レビュー処理中の Codex structured output 呼び出し、finding の判定失敗、処理失敗時のエラーレポートを変更・確認する時。
- レビュー用 worktree で生成された INDEX.md 変更の取り込みや、INDEX.md 以外の変更を拒否する制御を変更・確認する時。

## Do not read this when
- 通常の `init`、`session fork`、git helper、fixture 作成そのものの詳細だけを調べたい時。
- oracle の正本仕様本文を確認したい時。
- `review oracle` 以外の review サブコマンドや、一般的な CLI コマンドの挙動だけを確認したい時。

## hash
- 6ee141f5b42cdc53e0c03c910b696dcf1f6549383ccbacec10c34881ef2252e1

# `test_session_cli.py`

## Summary
- session 系 CLI の realization test。session fork が session branch と session state を作ること、session abandon が home branch へ戻って state を abandoned にすること、session join が conflict resolution 用 Codex 実行や branch cleanup を含めて期待どおりに完了することを検証する。
- Git repository fixture 上で `cmoc init` 後の session lifecycle を外部挙動として確認し、branch の作成・切替・削除、`.cmoc` 配下の session state、標準出力・標準エラー、conflict 解消後の staging 状態を扱う。

## Read this when
- `cmoc session fork`、`cmoc session abandon`、`cmoc session join` の CLI 挙動や regression test を確認・変更する場合。
- session branch 名、session home branch、session state file、abandon 時の rollback、join 時の conflict resolution、session branch 削除失敗時の警告出力に関するテストを探している場合。
- Git branch 操作を伴う session lifecycle の外部副作用と、Codex conflict resolution 実行時の file access mode をテストで確認したい場合。

## Do not read this when
- session 以外の CLI サブコマンド、設定読み込み、path model、oracle/realization 分類などの仕様や実装を調べたい場合。
- session CLI の実装本体を変更する入口を探している場合は、まず実装側の session command や main command 定義を読む。
- test helper、repository fixture、runner、git wrapper、Codex 実行 wrapper そのものの定義や共通挙動を調べたい場合は、このテストではなく共通 test support を読む。

## hash
- ad1614306782bf18a512c58f7775dc53c78e3079d59d20d5d2de7abb7a962108
