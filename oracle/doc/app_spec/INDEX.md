# `cli_auto_completion.md`

## Summary
- CLI 自動補完プローブの扱いを定める正本仕様断片。環境変数で補完呼び出しを判定し、通常実行向けの前処理・検査・副作用・独自エラー出力を補完処理より前に混ぜない境界を示す。
- 補完時の標準出力・標準エラー出力を CLI ライブラリが必要とする補完出力に限定するための入口となる。

## Read this when
- シェル補完や CLI ライブラリの補完処理に関わる起動経路を実装・修正・テストするとき。
- 通常の CLI 実行前処理、サブコマンド未指定判定、作業ディレクトリ変更、状態検査、ログ作成、索引更新、独自エラー出力をどのタイミングで実行してよいか判断するとき。
- 補完プローブ時に stdout/stderr へ余計な出力や副作用が混入していないか確認するとき。

## Do not read this when
- 通常実行時のサブコマンド仕様、状態ファイル仕様、ログ仕様、索引更新仕様そのものを調べたいだけのとき。
- 補完プローブではない通常の CLI エラー形式や出力 schema を確認したいとき。
- CLI 自動補完に関係しない oracle file と realization file の一般的な役割分担や品質基準を調べたいとき。

## hash
- 480051b6d39bcaaf30039ef43ae1a8853e51bcadc27cd83c7c39a44cf76ef3c4

# `codex_exec_rule.md`

## Summary
- cmoc が Codex CLI を呼び出す際の実行規約を定める正本仕様断片。`codex exec` を前提に、`CODEX_HOME` の引き継ぎと補完、事前検証、動的 profile 生成、ファイルアクセス制限や model 設定の渡し方、プロンプトを stdin で渡す制約、ログ・stdout・stderr・最終出力・Structured Output schema の保存と検証、並列実行上限、失敗時の retry・quota 待機・resume 方針、編集禁止領域の扱いをまとめている。
- 個別の呼び出し引数の詳細は AgentCallParameter builder を正本とし、この文書は cmoc 全体として守るべき Codex CLI 呼び出しの横断ルールを確認する入口になる。

## Read this when
- cmoc から Codex CLI を起動する処理、呼び出し引数、profile 生成、環境変数、preflight validation、ログ保存、stdout/stderr の扱い、Structured Output、並列実行、失敗時の retry・resume・quota 待機を実装または変更するとき。
- Codex CLI 呼び出しでどの情報を argv、stdin、profile、プロンプト、ログ、出力ファイルのどこへ渡すべきか判断したいとき。
- Codex CLI のレスポンスが仕様不一致、quota 枯渇、レートリミット、サーバー一時不調、その他想定外エラーになった場合の cmoc 側制御フローを確認したいとき。
- `.agents` 配下を cmoc 経由で扱えるか、または Codex CLI のファイルアクセス制限をどの層で指定・通知するかを確認したいとき。

## Do not read this when
- 個別の `codex exec` 呼び出しごとの具体的な AgentCallParameters、引数組み立て、profile 内容の正本を確認したいだけなら、AgentCallParameter builder 側を直接読む。
- Codex CLI 呼び出しとは無関係な cmoc のサブコマンド仕様、通常の path model、oracle/realization の一般原則、またはテスト配置だけを調べたい場合。
- Structured Output のスキーマ自体の項目定義や、特定ログファイルの具体的な JSON 内容を調べたい場合は、その schema や生成・検証実装を読む。

## hash
- c0880a02e4612e985aa861f5ff60db0d8831e61275481b897e84a1f6feca8f4b

# `console_and_file_log.md`

## Summary
- cmoc のコンソール出力とサブコマンド単位のログファイル出力について、表示形式・出力先・イベント粒度・最低限含める情報を定める仕様断片。
- stdout に出す時間表示とパス表示の共通フォーマット、サブコマンドログを JSON Lines として保存する要件、人間向けコンソールログを markdown 形式で出す要件を扱う。
- サブコマンド実行の開始、ステップ進入、Codex CLI 呼び出し、終了サマリーを、利用者確認用出力と追跡用ログにどう残すかを判断する入口になる。

## Read this when
- サブコマンド実行中または終了時に、stdout・stderr へ何をどの形式で出すべきかを確認したいとき。
- サブコマンドごとのログファイルの保存場所、JSON Lines 形式、イベント単位、flush 方針を実装またはテストするとき。
- ステップ開始通知、Codex CLI 呼び出し通知、完了サマリーに含めるべき情報や表示形式を確認するとき。
- ログやコンソール出力内で時間・経過時間・ファイルパスをどう表記するかを確認するとき。

## Do not read this when
- CLI 引数、サブコマンド構成、設定ファイル、作業ディレクトリモデルなど、ログ出力以外の仕様を確認したいとき。
- Codex CLI 自体の実行方法や呼び出しログの内部内容など、サブコマンドログに記録される対象の詳細仕様を確認したいとき。
- 実装内部の helper 分割、具体的な JSON key 一覧、イベント項目の完全な schema など、本文が実装者裁量として残している詳細だけを決めたいとき。

## hash
- 12a896e8767c83c9b3518ceba5148d23610aca8eb3b02013ad2f37499098749c

# `error_handling.md`

## Summary
- 仕様ごとの個別指示がない場合に適用される、cmoc 全体のデフォルトのエラー処理方針を定める正本仕様断片。
- 処理中断、stdout へのエラーレポート出力、エラー終了を示すステータスコード返却を、特別な記載がない失敗時の共通規則として扱う。
- 個別仕様に特別なエラー処理指示がある場合は、その個別指示を優先する境界も示す。

## Read this when
- ある失敗条件について、個別仕様に専用のエラー処理規則が見つからず、cmoc としての標準的な失敗時挙動を確認したいとき。
- エラー発生時に処理を継続するか中断するか、利用者へ何を出力するか、終了ステータスをどう扱うかを実装・テストする必要があるとき。
- 新しい仕様断片や実装で、個別のエラー処理を明示しない場合に従うべき共通のフォールバック規則を確認したいとき。
- 個別仕様のエラー処理指示と共通規則の優先関係を確認し、どちらを根拠にすべきか判断したいとき。

## Do not read this when
- 対象の個別仕様に、失敗時の出力・継続可否・終了コードなどが明示されており、その個別規則だけで判断できるとき。
- エラー処理ではなく、正常系の CLI 挙動、パス定義、状態管理、ファイル分類などを確認したいとき。
- stdout に出すエラーレポートの具体的な文字列、JSON schema、フォーマット詳細など、この断片に書かれていない出力仕様を探しているとき。
- 例外クラス設計、内部 helper の分割、try 文の配置など、共通の外部挙動から実装裁量で決められる内部構造だけを検討しているとき。

## hash
- bfaceea1701755cbe1f24db75ea9044ad4d4ed7dc98edef844bc94e39c3bbdf8

# `indexing.md`

## Summary
- <work-root> 配下に配置されるルーティング用 INDEX.md の自動生成・更新・除外対象を定義する正本仕様断片。
- INDEX.md の配置対象ディレクトリ、目次作成対象、エントリの意味情報と hash の形式、更新判定、削除・再生成条件を扱う。
- インデクシング処理の順序、目次情報生成 agent call の単位、並列実行条件、自動コミット対象、実行タイミング、排他制御の入口になる。

## Read this when
- <work-root> 上の INDEX.md をいつ・どこに作るか、どのファイルやディレクトリを目次対象から除外するかを確認するとき。
- INDEX.md エントリの Summary、Read this when、Do not read this when、hash の生成仕様や更新判定を実装・修正するとき。
- インデクシング処理を深いディレクトリから進める順序、同一階層や非祖先関係での並列化、子ディレクトリ INDEX.md 参照の扱いを確認するとき。
- インデクシング後の git 自動コミット範囲、既存差分の扱い、INDEX.md 以外をコミットしない制約を確認するとき。
- Codex CLI 実行前のインデクシング実行条件、例外となる呼び出し、同時起動時の直列化・排他制御を扱うとき。

## Do not read this when
- oracle file と realization file の基本定義や責務境界だけを確認したいとき。
- 個別の CLI サブコマンド、出力 JSON、実行環境、パスモデルなど、INDEX.md 自動生成以外の仕様を調べるとき。
- INDEX.md エントリ本文の品質基準だけを確認したいとき。自動生成処理や hash 更新条件を扱わないなら、より直接の基準文書を読む。
- 実装ファイルやテストの肥大化抑制、抽象化、依存関係追加の判断を行うだけで、インデクシング仕様に触れないとき。

## hash
- af05b433d23be570cf65b8a6ae8871a7c7e69e96efdaedf1c4e0a8b9b3746e4b

# `misc_spec.md`

## Summary
- cmoc の横断的な雑則をまとめる仕様断片。実装ファイル列挙の機械的条件、操作対象リポジトリへの前提、実行時カレントディレクトリ、追跡対象外にする作業用状態領域、タイムスタンプ形式、管理ブランチ上で発生した変更の範囲を定義する。
- 個別サブコマンドの詳細挙動ではなく、複数機能から参照される前提・用語・判定範囲を確認するための入口として位置づける。

## Read this when
- 「実装ファイルを列挙する」と表現された処理で、対象に含めるファイル、除外するファイル、gitignore や INDEX.md の扱いを確認したいとき。
- cmoc が操作する作業対象リポジトリにどのような前提を置いてよいか、特に git 管理、断片的な正本情報、作業ノウハウの所在を確認したいとき。
- cmoc 実行中のカレントディレクトリをどこに固定するか確認したいとき。
- 作業用状態領域を git 追跡対象外にする理由や、初期化処理が保証すべき除外状態を確認したいとき。
- ログ名や生成物名などに使うタイムスタンプの桁数、区切り、ローカル timezone の扱いを確認したいとき。
- 管理ブランチ上で変更・発生した事象に、作成元 commit 以降の commit、working tree、staging area、削除済みファイル、rename 後パスをどう含めるか判断したいとき。

## Do not read this when
- 特定サブコマンドの入出力、エラー条件、セッション生成、レビュー処理などの詳細仕様を知りたいときは、その機能を直接扱う仕様を読む。
- パスキーワード自体の意味やルート種別の体系を確認したいときは、パスモデルを定義する仕様・実装を読む。
- 正本仕様断片、実現ファイル、INDEX.md エントリーの一般原則を確認したいだけなら、各標準を扱う仕様を読む。
- 実装やテストの具体的なコード構造、関数名、既存挙動を調べたいときは、対象の実装ファイルまたはテストを読む。

## hash
- 69c963981887477d4763539bc1d4d802043f5e3795d0dc6c923a41eab08016c7

# `prompt_standard.md`

## Summary
- agent に渡すプロンプトに含めてよい概念と言語を定める、cmoc 固有のプロンプト規範を扱う。
- cmoc 特有のメタ概念を依頼先 agent に見せず、具体的なパスや環境前提へ解決してから渡すべき境界を確認する入口になる。
- Codex CLI で人間が読む自然言語部分を原則日本語にする方針と、識別子・schema key・ログ原文など英語のまま扱える例外を確認できる。

## Read this when
- agent に渡す入力プロンプト、作業レポート、レビューレポート、エラー説明などの文面を生成・変更する。
- プロンプト内に cmoc 固有のパス表記、内部概念、呼び出し元へのメタ認知、作業環境の特定 skill 前提を含めてよいか判断する。
- Codex CLI が扱う自然言語部分を日本語にすべきか、識別子・ファイルパス・コマンド・JSON schema key・ログ原文などを英語のまま残してよいか判断する。
- INDEX.md の Summary / Read this when / Do not read this when など、人間が読むルーティング文書の言語方針を確認する。

## Do not read this when
- oracle file と realization file の責務、編集主体、正本仕様断片としての扱いを確認したいだけなら、より基本的な分類定義を読む。
- 実装ファイルやテストの肥大化抑制、抽象化、依存関係、公開面の増加抑制について判断したいだけなら、realization file 向けの規範を読む。
- INDEX.md エントリーそのものの情報量、根拠、読む条件の書き方を確認したいだけなら、INDEX.md エントリー向けの規範を読む。
- 内部 helper の分割、テスト追加、CLI オプション追加など、agent へ渡すプロンプト文面や自然言語の扱いと直接関係しない実装判断だけを行う。

## hash
- 4272e79eb379a5d79ef2edcd8744caa2a29353df0f2f264785a1ecf9208a10d8

# `run_isolation.md`

## Summary
- サブコマンド呼び出しごとに発生する run の作業隔離について、git branch と git worktree を使って人間の直接作業領域との衝突を避ける規則を述べる。
- run 開始時の session branch から run branch を作り、run worktree 上で作業し、完了後の session branch への反映はサブコマンドごとの規則に従う、という責務境界を扱う。
- 原則として run 作業の読み書き範囲を run root 内に閉じつつ、ログや状態ファイルなど明示された例外では repo root 配下への書き込みを許す、という隔離例外の入口になる。

## Read this when
- サブコマンド実行時に作業用 branch や worktree をどの時点・どの基準で作成し、どこで作業を記録するかを確認したいとき。
- run root、repo root、cmoc session branch、cmoc run branch、cmoc run worktree の関係を前提に、作業隔離の実装やテストを設計するとき。
- 人間が直接触る作業領域と cmoc が実行中に触る作業領域を分離する必要がある変更を行うとき。
- run 作業が原則の書き込み範囲を越えて repo root 配下へログや状態ファイルを書いてよいかを判断したいとき。
- サブコマンドごとに異なる具体的な run branch、run worktree、完了後マージ規則を定義する前に、共通の隔離モデルを確認したいとき。

## Do not read this when
- 個別サブコマンドの具体的なブランチ名、worktree 名、またはマージ手順そのものだけを確認したいときは、そのサブコマンド固有の仕様を直接読む。
- path キーワードの一般定義や repo root、run root、work root などのパスモデルだけを確認したいときは、パスモデルの仕様を直接読む。
- oracle file と realization file の責務分離、編集権限、正本性の規則を確認したいだけのときは、oracle と realization の基本規則を読む。
- 実装ファイルやテストの分割、抽象化、依存追加などの realization 品質基準を判断したいだけのときは、realization standard を読む。

## hash
- 4ce051fea17daf64aa2c0285f4381244608cf0dd073cac8d85e6990a94db17d4

# `session_state.md`

## Summary
- cmoc のセッション状態ファイルに永続化する最小限の状態情報を定義する仕様断片。
- fork と join の挙動を一意に決めるため、セッション全体の状態、fork 元ブランチ・コミット、最後に join した oracle snapshot、apply 処理の状態・作業ブランチ・参照コミットを扱う。
- 永続化する値と、その場で解決できるため保持しない値の境界を確認する入口になる。

## Read this when
- セッションの fork、join、abandon、error などの状態遷移に関わる実装やテストを変更する時。
- セッション状態として何を永続化するべきか、または永続化しないべきかを判断する時。
- セッション新規作成直後の初期値を確認する時。
- apply 処理の ready、running、completed、error の扱いや、apply 用ブランチ・oracle snapshot commit の保存条件を確認する時。
- join 済み apply の oracle snapshot commit をどのフィールドで追跡するかを確認する時。

## Do not read this when
- path キーワードやルートディレクトリ概念そのものの定義だけを確認したい時。
- oracle file と realization file の責務分担や編集権限だけを確認したい時。
- CLI の表示形式、サブコマンド一覧、引数仕様など、永続化されるセッション状態以外の公開面を調べたい時。
- git 操作一般やブランチ命名一般を調べたいだけで、セッション状態ファイルに保存される値を扱わない時。
- INDEX.md の生成方針やルーティング文書の書き方を確認したい時。

## hash
- 3e56c02becb452f6181e383b125f3aff1f3010d8158e2ab309df379bead1824b

# `sub_command`

## Summary
- cmoc の利用者向けサブコマンド仕様断片をまとめた領域。セッション開始・完了・破棄、apply の開始・取込・破棄、oracle レビュー、初期化、明示インデクシング、AI Agent CLI/TUI 起動など、CLI として見える挙動の正本仕様へ進む入口となる。
- 各サブコマンドの事前条件、状態遷移、branch/worktree 操作、未コミット差分の扱い、agent call や Codex CLI に委ねる境界、レポートや stdout 出力、終了・失敗時の扱いを確認するための階層。

## Read this when
- cmoc のサブコマンド単位で、CLI 引数、実行前提、外部挙動、状態更新、git 操作、出力、失敗時の扱いを実装・修正・テストする。
- session lifecycle のうち、現在 branch から session を作る、home branch へ join する、または home branch へ取り込まず abandon する挙動を確認する。
- apply lifecycle のうち、隔離 branch/worktree で修正ループを実行する、成果物を session 側へ join する、または未 join の apply run を abandon する挙動を確認する。
- oracle file のレビュー用サブコマンド、作業ルートの初期化、明示インデクシング、cmoc 規則を注入して AI Agent CLI/TUI を起動する処理の仕様を探す。
- サブコマンドから見た agent call、Codex CLI 呼び出し、Markdown report、stdout、終了コードの責務境界を確認したい。

## Do not read this when
- サブコマンドから呼ばれる共通処理の内部実装、parameter builder、run 隔離実行、path model、状態ファイル schema などの詳細だけを確認したい場合は、それぞれの正本仕様や実装へ直接進む。
- oracle file、realization file、path keyword、root model など、cmoc 全体の基礎概念定義だけを確認したい。
- インデクシングで生成・更新される内容そのものや、INDEX.md 生成規則を確認したい場合は、インデクシング全体またはルーティング文書生成の仕様を読む。
- 通常の git 操作一般、任意 branch の汎用 merge、join 済み結果の rollback、旧サブコマンド互換など、現行サブコマンド仕様が対象外としている機能を探している。
- 実装ファイルやテストファイルの配置、既存 helper の分割、コード構造だけを調べたい場合は、realization 側の該当領域へ進む。

## hash
- f67324eaf5d87f269456bedfe36a4d921464c92d6e4750a4fd381298eaac04d7

# `usage.md`

## Summary
- cmoc を利用者がどの順序で呼び出すかを示す使用手順の仕様断片。初回初期化、セッション開始、oracle 改訂とレビュー、apply の fork/join、セッション終了までの標準ワークフローにおける人間と cmoc の役割分担を扱う。
- 利用者が操作する公開コマンドの呼び出し順と、その各段階で記録・作成・マージされるブランチや oracle snapshot の関係を確認するための入口となる。

## Read this when
- エンドユーザーが cmoc をどのコマンド順で使うべきかを確認したいとき。
- 初回利用時の初期化操作や、セッションを開始・終了する操作の位置づけを確認したいとき。
- 作業ブランチ、セッション用ブランチ、apply 用ブランチがワークフロー中でどのように作成・記録・マージされるかを確認したいとき。
- oracle の改訂、レビュー、コミット、実装追従作業をどの順序で繰り返すかを確認したいとき。
- apply 実行開始時点の oracle snapshot が実装追従作業の正本になることや、実行中に進んだ oracle 改訂がその実行へ反映されない境界を確認したいとき。

## Do not read this when
- 個別コマンドの詳細な引数仕様、出力形式、エラー条件だけを知りたいとき。
- パスキーワードやブランチ名プレースホルダーの定義そのものを確認したいとき。
- oracle file と realization file の一般的な責務分担や編集権限を確認したいとき。
- cmoc の内部実装構造、テスト設計、補助ファイルの配置を調べたいとき。

## hash
- 2cef745a630a8dce3041828d8b8004564a124ada78f21dbe0a55d79302081d95
