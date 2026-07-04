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
- cmoc が Codex CLI を `codex exec` で呼び出す際の正本規約を扱う。環境変数、preflight validation、動的 codex profile、ファイルアクセス制限、プロンプト受け渡し、ログ保存、Structured Output、並列実行、失敗時の retry・quota 待機・resume、編集禁止領域の扱いを定める。
- 個別の呼び出し仕様や具体的な profile 設定は AgentCallParameter builder を正本とし、この対象は呼び出し全体の境界条件、保存先、失敗処理、Codex CLI へ渡す情報と渡してはいけない情報を判断する入口になる。

## Read this when
- cmoc から Codex CLI を起動する実装、テスト、設計判断を扱うとき。
- `CODEX_HOME` の決定、auth の事前確認、動的 codex profile の生成、`--profile`・`--json`・`--output-last-message`・`--output-schema` の使い方を確認したいとき。
- Codex CLI に渡すプロンプト本文をどこまで加工してよいか、argv・stdin・ログ保存をどう分けるかを判断するとき。
- Codex CLI 呼び出しの stdout、stderr、output、call 情報、schema、prompt の保存先や同一呼び出し内の timestamp 一致条件を確認するとき。
- Structured Output の要求方法、schema 保存、cmoc 側での機械的検証を実装または検証するとき。
- Codex CLI 呼び出しの失敗時に、レスポンス検証失敗、quota 枯渇、レートリミット、モデル capacity、想定外エラーをどう扱うかを確認するとき。
- quota 待機時のポーリング、並列呼び出し時の代表ポーリング、resume 対象セッション ID の取得、resume 失敗時の再実行方針を扱うとき。
- Codex CLI に対するファイルアクセス制限を profile とプロンプトでどう伝え、事後検証を行わない理由を確認するとき。
- `.agents` 配下を cmoc から編集対象にしてよいか判断するとき。

## Do not read this when
- AgentCallParameter builder が定める個別パラメータの具体的な構築ロジックだけを確認したいときは、builder 側を直接読む。
- cmoc の一般的なパス用語や `<cmoc-root>`、`<repo-root>`、`<work-root>`、`<run-root>` の定義だけを確認したいときは、パスモデルの正本を読む。
- Codex CLI 呼び出しと無関係なサブコマンド、内部データ構造、UI 表示、通常のファイル走査ロジックだけを扱うとき。
- Codex CLI 自体の一般的な利用方法や外部ドキュメント上の仕様だけを調べたいとき。
- oracle file と realization file の所有関係、編集責務、INDEX.md エントリー作成規則だけを確認したいとき。

## hash
- c0e2ede26482c4cb97d2b0455c403f538aeffb04674676da87479b74d41600c5

# `console_and_file_log.md`

## Summary
- コンソール表示、パス・時間の表記、サブコマンドごとの JSON Lines ログファイル、サブコマンド実行状況を人間が読むための markdown 形式コンソールログについて定める正本仕様断片。
- ログファイルの出力先、即時 flush、必須イベント、ステップ開始・Codex CLI 呼び出し・完了サマリーでコンソールに出す最低限の情報を確認する入口。

## Read this when
- stdout や stderr に出すログの形式、時間表示、パス表示を実装・変更・検証する。
- サブコマンド単位のログファイル作成、保存場所、JSON Lines 形式、イベント記録、flush 方針を扱う。
- サブコマンド実行中のステップ通知、Codex CLI 呼び出し通知、完了サマリーのコンソール出力を扱う。

## Do not read this when
- ログ以外の CLI 引数、サブコマンド構成、作業ディレクトリ構造そのものを確認したい。
- Codex CLI 呼び出しログファイル自体の内部形式だけを確認したい。
- oracle file と realization file の一般的な責務境界や編集規則だけを確認したい。

## hash
- aa330ad885fd644d57380e4babe3dd24c7f26e386cca778036e7bc1efd864ed9

# `doctor_preprocess.md`

## Summary
- 各サブコマンドの本命処理前に必ず走る doctor preprocess の責務を定義する。cmoc 実行前に必要な共通検証・修復として、ローカル状態の git ignore 保証、agent 禁止領域の追跡保証、ollama による LOCAL_SLM サーブ可能性の保証、修復差分の commit を扱う。

## Read this when
- サブコマンド共通の事前検証・自動修復の順序や責務境界を確認したいとき。
- `.cmoc/local` を git 追跡対象外に保つ処理、`.gitignore` への追加、tracked file の index 除外条件を実装・変更するとき。
- `.agents` を存在させ、必要に応じて `.gitkeep` を作成し、git 追跡対象にする処理を実装・変更するとき。
- cmoc 起動前に ollama 接続可否や LOCAL_SLM モデルの serve 可能性を検証・修復する流れを確認するとき。
- doctor preprocess が修復困難な場合に cmoc をエラー終了する条件や、修復後差分を commit する方針を確認するとき。

## Do not read this when
- 個別サブコマンド固有の事前条件や本命処理だけを確認したいとき。
- ollama による SLM サーブ仕様そのものを確認したいときは、ollama SLM server の正本仕様を直接読む。
- path keyword の意味や `<work-root>`、`<repo-root>`、`<cmoc-root>` の定義だけを確認したいとき。
- doctor preprocess 後に実行される通常のコマンド処理や出力形式だけを調べたいとき。

## hash
- cdc846b3d54af7449e093af294e923b847e07d2c88c2b8b34722da6f124e4166

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
- `<work-root>` 配下のディレクトリへ `INDEX.md` を自動配置し、同階層の目次情報を生成・更新する仕様を定義する。
- 配置対象ディレクトリ、目次作成対象、目次情報フォーマット、ハッシュ判定、深い階層からの処理順、自動コミット範囲、agent call によるエントリー生成、並列実行、実行タイミングを扱う。
- `INDEX.md` が既に最新の場合は機械的チェックだけで目次生成を実行しない、というメンテナンス時の挙動も定義する。

## Read this when
- `INDEX.md` の自動生成・更新・削除条件を確認するとき。
- インデクシング対象に含めるファイルやディレクトリ、除外するパスやバイナリ扱いを判断するとき。
- 目次情報のフォーマット、参照ハッシュ、ディレクトリハッシュの計算方法を実装・検証するとき。
- インデクシング処理の順序、並列化可能な範囲、自動コミット対象を実装・テストするとき。
- 本命の agent call 前にインデクシングを実行する条件や、最新状態でのスキップ挙動を確認するとき。

## Do not read this when
- 個別ファイルや個別ディレクトリの `INDEX.md` エントリー文面だけを作成するとき。
- `INDEX.md` 以外の oracle file、realization file、memo、git 管理対象の定義を確認したいとき。
- agent call の具体的なパラメータ定義そのものを確認したいとき。
- 通常の CLI コマンド仕様や、インデクシング以外の実行フローを調べたいとき。

## hash
- e6dde01d8bb1df856e9151bafaf24975302e022db1fc9cfd2df3e5f8297adc6c

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

# `ollama_slm_server.md`

## Summary
- ローカルの Ollama 実行環境で SLM をサーブし、cmoc が Codex CLI 用バックエンドとして利用するための仕様を扱う。モデル名のロード元、Ollama の取得・展開、ローカルアドレスでの起動、生成する Codex profile、doctor preprocess によるインスタンス寿命管理の境界を示す。

## Read this when
- cmoc からローカル SLM を使うための Ollama インストール、起動、接続設定を確認または実装するとき。
- Codex CLI に渡す profile で Ollama 互換エンドポイントをどう設定するか、また `--oss` や組み込み provider ID に依存しない方針を確認するとき。
- doctor preprocess で Ollama を準備する処理、同一 repo 内での単一インスタンス共有、利用終了時の停止条件を扱うとき。
- ローカル SLM のモデル名を cmoc 設定からどのように取得するかを確認するとき。

## Do not read this when
- doctor preprocess 全体の実行順序や他の前処理項目を確認したいだけなら、doctor preprocess の仕様を直接読む。
- Codex CLI 全般の argv 構築や profile 生成のうち、Ollama 固有でない設定を扱う場合は、その責務を持つ仕様または実装を読む。
- 外部クラウドモデルや Ollama 以外の model provider の仕様を確認したい場合は、この対象ではなく該当 provider の仕様を読む。

## hash
- d673067d5a926743218bc4aac4388ac07f758e7207ab9e0ad4518d3a1eeb3f9e

# `prompt_standard.md`

## Summary
- cmoc が agent call に渡すプロンプトについて、oracle src の `build_*_parameter` 関数で動的構築した内容を原則そのまま渡すべきことを定める oracle doc。
- realization file 側でのプロンプト加工を原則禁止し、oracle src 側のバグを補う必要がある場合だけ最小限の加工を許容する境界を示す。
- Codex CLI が扱う自然言語的な文章は原則日本語としつつ、個別仕様、識別子、英語由来語、ログ原文、引用文、人間が直接読まない思考言語などの例外を定める。

## Read this when
- agent call に渡すプロンプトの生成元、加工可否、realization file 側で許される補正範囲を確認したいとき。
- 入力プロンプト、作業レポート、レビューレポート、調査結果、エラー説明、次アクション案内など、人間が読む自然言語部分の使用言語を判断したいとき。
- Structured Output の schema key、コード識別子、ファイルパス、コマンドライン、ログ原文、引用文などを日本語化すべきかどうか迷うとき。

## Do not read this when
- oracle file と realization file の基本的な役割分担、正本仕様断片としての扱い、編集責任の境界を確認したいだけのとき。
- プロンプト内容そのものではなく、個別コマンドの実装、テスト、ファイル配置、path model の詳細を調べたいとき。
- 一般的な oracle file の書き方、realization code の品質基準、INDEX.md エントリー生成基準を確認したいとき。

## hash
- 5c643a3eb609c61d07df6326f40fe70bb1f85548772b574e6af052a3d6aea860

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
- cmoc のセッション状態ファイルに永続化する最小情報と JSON 構造を定める正本仕様断片。
- fork 元ブランチ、fork 元コミット、最後に join した oracle snapshot、apply の状態・作業ブランチ・oracle snapshot commit など、session/apply の状態遷移で保持する値の意味と初期化条件を扱う。

## Read this when
- セッション状態ファイルの保存先、責務、永続化する情報の範囲を確認したいとき。
- `cmoc session fork`、`cmoc apply join`、apply state の ready 遷移などが、状態ファイルの各フィールドをどう初期化・更新するか確認したいとき。
- fork、join、apply の挙動を一意にするために必要な session/apply state の JSON schema を実装・テストする とき。

## Do not read this when
- oracle file と realization file の一般的な責務境界や編集規則だけを確認したいとき。
- パスキーワード一般の定義を確認したいとき。
- セッション状態ではなく、他の永続状態・CLI 出力・サブコマンド仕様を確認したいとき。

## hash
- 5df81738a7b7d744d2c6708e1822bb7a68bea88de3cf1407cec7aa6c964fe8cf

# `sub_command`

## Summary
- cmoc のサブコマンド仕様断片を集めた領域。session の開始・完了・破棄、apply の実行・取り込み・破棄、oracle review、indexing、doctor、TUI 起動など、利用者が直接呼び出す CLI 挙動の正本仕様へ進む入口になる。
- 各サブコマンドの事前条件、状態遷移、git 操作、agent call との境界、stdout report、終了条件、cleanup 対象など、外部挙動として実装差を避けたい事項を扱う。

## Read this when
- cmoc のサブコマンド単位の CLI 引数、実行順序、事前条件、終了コード、標準出力、レポート保存、状態更新を確認したいとき。
- session または apply の lifecycle に関わる開始、実行、join、abandon の仕様へ進みたいとき。
- doctor、indexing、oracle review、TUI 起動など、利用者が明示実行するコマンド入口の仕様を探すとき。
- サブコマンド実装やテストの変更前に、対象コマンドの正本仕様断片を特定したいとき。

## Do not read this when
- path placeholder、oracle file、realization file、managed branch、state file などの一般定義だけを確認したいときは、用語やパスモデルの仕様を読む。
- agent call の詳細な prompt、Structured Output、parameter builder のみを確認したいときは、対応する agent call 定義へ直接進む。
- 隔離実行、doctor preprocess、indexing 生成規則など、サブコマンドから呼ばれる共通処理そのものの詳細だけを確認したいときは、その共通仕様を読む。
- 実装ファイルの責務分割、内部 helper、git command wrapper の設計だけを確認したいときは、realization code 側を読む。

## hash
- 6e86e14345912a52ef710d6db2903cdb08e43538ed7f9ccbb36cc2e3b15666fe

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
