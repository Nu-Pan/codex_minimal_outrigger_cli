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

# `cmoc_managed_ollama.md`

## Summary
- `cmoc managed ollama` の責務、ライフサイクル、利用可能性保証、`codex exec` からの接続方法をまとめて読むための入口。cmoc が何を自分で管理し、何を Codex agent に任せないかを確認したいときに進む。

## Read this when
- `CodexModelSpec.model_provider=="cmoc"` のモデルを使う経路を実装・修正するとき。
- `doctor preprocess` でサービス起動、待受確認、モデル準備、GPU 推論確認の保証を扱うとき。
- `cmoc-ollama.service`、`~/.cmoc/ollama` 配下の永続化資源、`127.0.0.1:11434` への接続方法を確認したいとき。
- Codex CLI に渡す `--model` と `--config` の上書き値、`--profile` や `--oss` を使わない制約を確認したいとき。

## Do not read this when
- 単純な `codex exec` の共通規約だけを見たいときは、より一般的な `codex_exec_rule` を先に読む。
- サービス管理ではなく、CLI 引数の組み立てやプロンプト整形だけを見たいときは、この文書より個別の `codex_exec_rule` や builder 側を先に読む。
- cmoc 以外の model provider や別の外部モデル連携を扱いたいとき。
- GPU 利用の一般論や Ollama 単体の使い方を知りたいとき。

## hash
- 229d722c09503b9b563c54a23ee8e4a850d5e057b76739987c78848a3acb3c56

# `codex_exec_rule.md`

## Summary
- `codex exec` を介して cmoc から Codex CLI を呼ぶときの実行規約をまとめる。引数上書き、`$CODEX_HOME` の扱い、preflight validation、プロンプトの渡し方、出力ログ保存、Structured Output、失敗時の再試行と待機を実装・変更する場合に読む。
- 個々の `codex exec` 呼び出しの組み立てや、CLI 実行前後の検証・保存・復旧が対象であり、cmoc 全体の一般的なサブコマンド設計や他の実行経路だけを変える作業では優先して読まない。

## Read this when
- `codex exec` の argv 生成、`$CODEX_HOME` の解決、preflight validation、プロンプト入力、ログ保存、Structured Output の参照先、失敗時の再試行・待機・resume のいずれかを変更する。
- Codex CLI に渡す設定上書きやファイルアクセス制限の表現方法を確認したい。
- Codex CLI 呼び出し失敗時の扱いを変える必要がある。

## Do not read this when
- `codex exec` 以外の cmoc 機能だけを変更する。
- 呼び出し規約ではなく、別の builder や別コマンドの仕様を確認したい。
- 単に既存のログや生成物の内容を確認したいだけで、呼び出し手順自体は変えない。

## hash
- b154f359f0af1503014774d4901c54247b5974bec9ee87d97dec66f6d590fe57

# `console_and_file_log.md`

## Summary
- 標準出力・標準エラーへの表示形式、ログファイルの出力先、必須イベント、完了サマリーのように、cmoc のコンソール表示とファイルログの外形仕様を決める文書。実装やテストで、時刻表記・パス表記・イベント記録・サマリー出力の互換性を確認するときに読む。

## Read this when
- サブコマンドの実行経過を人間向けにどう表示するかを実装・変更するとき。
- JSON Lines のサブコマンドログに、どのイベントをどの単位で書くかを決める必要があるとき。
- コンソール出力とファイル出力の間で、出力先・即時 flush・経過時間・戻り値の扱いを合わせる必要があるとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや入出力内容を決めたいだけのとき。
- ログの保存方式や表示形式ではなく、別の領域の設定やデータモデルを確認したいとき。
- 既に決まっている表示ルールを前提に、内部の関数分割や実装手段だけを詰めたいとき。

## hash
- eb26e061fe01f68d53bfb90f687d37fa59850c633b0887fe776704f5d901f267

# `doctor_preprocess.md`

## Summary
- cmoc を本番サブコマンド実行前に通す事前検証と修復の責務をまとめた正本断片。`.cmoc/gu` の追跡外化、`.agents` の追跡対象化、`.cmoc/gt/ar/config.json` の追跡対象化、必要時の managed ollama 可用性確認、そして途中で発生した差分のコミット方針を読む入口。
- 個別サブコマンドの機能仕様や実装詳細ではなく、起動前に共通で満たすべき環境条件と修復可否の境界を確認したいときに読む。

## Read this when
- cmoc の各サブコマンドを実行する前提条件や、起動前に共通で走る検証・修復の責務を確認したいとき。
- `.cmoc/gu` を追跡外にしたい理由、`.agents` を追跡対象に固定したい理由、`.cmoc/gt/ar/config.json` を追跡対象にしたい理由を確認したいとき。
- managed ollama の利用可否を起動前に保証する必要があるか、そこで失敗したらその場で終了すべきかを確認したいとき。

## Do not read this when
- doctor preprocess ではなく、個別サブコマンド固有の前提条件や本体処理を知りたいとき。
- cmoc の一般的なコマンド体系や出力形式だけを知りたいとき。
- `.cmoc/gu` や `.agents` の中身そのものの仕様、または ollama の詳細な実装仕様を知りたいとき。

## hash
- 456a872269e84de215902aa521fb1f4095a8a7af7366b23fba5692d0accff503

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

# `external_model_provider.md`

## Summary
- 外部 LLM provider との関係を、Codex CLI への委譲を前提に定義する正本仕様断片。cmoc は provider 固有仕様を実行時制御せず、実際の model 選択・認証・接続は Codex CLI の責務として扱う境界を示す。

## Read this when
- cmoc と外部 LLM provider の責務分担を確認したいとき。
- provider 固有の認証、接続、model 選択、API 差異を cmoc 側で扱うべきか判断したいとき。
- Codex CLI へ委譲する外部 model 実行まわりの実装境界を確認したいとき。

## Do not read this when
- cmoc の内部 command 構成や通常の CLI 入出力を確認したいだけのとき。
- 特定 provider の API 仕様、認証手順、model 名一覧を調べたいとき。
- 外部 provider ではなくローカル filesystem、path model、run/work directory の扱いを確認したいとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `indexing.md`

## Summary
- - `cmoc` による `{{work-root}}` 配下 `INDEX.md` 自動配置・自動更新の扱いを定める。
- - 配置対象のディレクトリ選別、目次情報の作成単位、並列化、実行タイミング、既存差分を含むコミット方針を扱う。
- - `INDEX.md` 1 件分の目次情報フォーマットと、生成時に参照した対象のハッシュ記録方法を定める。

## Read this when
- - `INDEX.md` の自動生成・再生成・更新条件を決めたいとき。
- - 配置対象ディレクトリや、目次に載せる/載せない対象の境界を確認したいとき。
- - 子ディレクトリ優先の処理順、並列実行可否、更新結果の自動コミット条件を確認したいとき。

## Do not read this when
- - `INDEX.md` の本文そのものを手で編集したいだけのとき。
- - 個別ファイルの実装仕様や CLI の一般的な操作方法を知りたいだけのとき。
- - すでに別のより具体的な配下文書で、対象ディレクトリ固有のルーティングが明示されているとき。

## hash
- 61ab6318a773747ce71141f365f5aaf26fec36e326e42a08c8cb699b32cd199e

# `misc_spec.md`

## Summary
- cmoc 全体で共有する雑多な運用前提をまとめた入口。`{{work-root}}` 配下の実装ファイル列挙方法、cmoc が置く作業前提、実行時のカレントディレクトリ、タイムスタンプ表記、`{{cmoc-managed-branch}}` 上での変更範囲の解釈を確認したいときに読む。

## Read this when
- `{{work-root}}` 配下のファイルをどう列挙するかを確認したいとき。
- cmoc がこのリポジトリをどう扱う前提で動くか、どこまでを cmoc の責務とみなすかを確認したいとき。
- ブランチ上の変更範囲の数え方、作業時の `pwd`、タイムスタンプ表記の前提を確認したいとき。

## Do not read this when
- 個別の実装手順、コマンドの使い方、ツール利用の細部を知りたいときは、該当する `.agents/skills` 側を読む。
- `{{work-root}}` 固有のノウハウや作業フローの実体を知りたいときは、この文書ではなく該当する実装・技能定義を読む。
- 正本仕様そのものや個別機能の詳細を確認したいときは、`oracle` 配下のより具体的な文書やソースを直接読む。

## hash
- 71b43ecc5c13c5360c32cd86aa230e0b1570780c5ebf75bda47569998a58599a

# `prompt_standard.md`

## Summary
- cmoc が agent に渡すプロンプトの作り方を定める正本仕様断片。プロンプトの構築元、Markdown ベースの記法、参照ブロックと参照記法、言語方針を確認したいときに読む。

## Read this when
- agent call に渡すプロンプトの生成・検査・整形の方針を決めたいとき
- `{{...}}` のプレースホルダや `cmoc_block` / `cmoc_ref` の参照構文を扱う実装・テスト・レビューをするとき
- Codex CLI で扱う自然言語の言語方針を確認したいとき

## Do not read this when
- 既存プロンプトの具体的な組み立て処理だけを追いたいときは、まず oracle src 側の `build_*_parameter` 実装を読む
- cmoc 固有ではない一般的な Markdown や文言表現の詳細だけを確認したいとき

## hash
- 2c29e51d5d2ffd5edb8fc0759db046a91d6ec2dfcded91e0d7ae8bc5d703ce59

# `run_isolation.md`

## Summary
- `cmoc` の run ごとに、作業を人間の作業領域と衝突させないための隔離方針を扱う。run 開始時に session branch から run branch を切り、作業は必ず run worktree 上で run branch を checkout して進める前提を確認したいときに読む。
- ここでは run の作業場所、branch の作成元と記録先、run 完了後に session branch へ戻す規則の骨子を押さえる。個別サブコマンドごとの merge 方式や worktree 名の具体名は、この文書だけでなく各サブコマンド側の実装確認が必要なときに進む。
- run-root 外への書き込みは原則禁止だが、実行中のログや state のように repo-root 配下へ置く例外がある。隔離境界や例外書き込みの要否を確認したいときに読む。

## Read this when
- `cmoc` のサブコマンド実行時に、どこで作業を行い、どの branch に記録し、どこまでを書き込み可能にするかを確認したい。
- run 開始時の branch 生成元や、run 完了後の session branch への反映方針を知りたい。
- 隔離された作業領域の外に、実行中のログや状態ファイルを置いてよいか判断したい。

## Do not read this when
- worktree の具体的な作成処理や merge 手順の詳細実装を追いたい場合は、対象サブコマンドの本文を読む。
- run の名前付けや branch 名の実体を確認したいだけなら、この文書ではなく該当サブコマンド側を読む。
- repo 全体のルーティングだけを見たい場合は、より上位の INDEX を優先する。

## hash
- 32259835b5cceab7790965ad988769f48ca3b8844a41418d379f29edae1b3c71

# `session_state.md`

## Summary
- cmoc の session 永続状態を読むための入口。fork と join をまたいで session/apply の状態遷移や初期化値を確認したいときに参照する。
- 一時情報ではなく、`session` と `apply` の状態・ブランチ・コミットの永続化ルールを定める。状態ファイルに何を残すか、何をその場で解決してよいかの境界を読むための文書。
- fork/join の実装や状態遷移の整合性を確認したい変更では読むべきだが、UI 文言や個別コマンドの細部だけを追う目的ではない。

## Read this when
- cmoc の session 状態ファイルに保存する項目、初期値、更新タイミングを確認したい。
- fork 直後や join 後に session/apply のどの値がどう変わるべきかを判断したい。
- 永続化すべき情報と、その場で再計算してよい情報の境界を確認したい。

## Do not read this when
- session 状態の保存先やスキーマではなく、CLI の引数や表示文言だけを確認したい。
- 具体的な fork/join の処理手順やアルゴリズムを知りたい。
- 個別の実装詳細より先に、より上位の session/apply 仕様や関連コマンドの文書を読むべき状況である。

## hash
- c26d92ba2c2bbdc16a14881700c67a47096e38f93287cfd2bb3cc6a941d90144

# `sub_command`

## Summary
- `cmoc` の各サブコマンド仕様を探す起点。apply/session/review/tui/doctor/indexing のように、実行条件・状態遷移・事前条件・後始末を確認したいときにこの階層から入る。
- 単一コマンドの細部ではなく、どのサブコマンドの正本仕様を読むべきかを切り分けたいときに使う。

## Read this when
- サブコマンドごとの実行条件、状態遷移、終了条件、後始末の入口を探したいとき。
- `apply` / `session` / `review` / `doctor` / `indexing` / `tui` のどれを読むべきか迷っているとき。
- コマンド間の責務境界を確認して、より直接の仕様文書へ進みたいとき。

## Do not read this when
- すでに読む対象のサブコマンドが決まっているときは、ここではなく該当コマンドの文書を直接読む。
- 個別のファイル保存形式や内部 helper の詳細だけを知りたいときは、この階層ではなく該当の正本仕様断片を読む。
- `INDEX.md` の生成や更新ルールだけを確認したいときは、本文仕様ではなくルーティング文書そのものを扱う。

## hash
- c4cb1b1a7658b2640f91eec12b80c5a1409e77d22aec5e2e60914fdf2b61619a

# `subcommand_interruption.md`

## Summary
- cmoc の中断要求を正常系として扱う条件、通知方法、完了時の共通動作、再開不可の方針を確認するための正本仕様断片。
- `cmoc apply fork` と `cmoc review oracle` の中断対応を実装・修正するときに読む。

## Read this when
- ユーザー中断要求を受け付けるべきか、受け付けた後に通常完了へ移るべきかを判断したい。
- 中断後に何を保持し、何を破棄し、どの処理を続けてよいかの境界を確認したい。
- 中断完了をエラーではなく正常系として扱う必要があるか、レポートや終了ログでどう区別するかを確認したい。
- 中断後に再開や checkpoint 保存をしてよいかを確認したい。

## Do not read this when
- `Ctrl+C` 以外の入力方法や一般的な端末入力処理の詳細だけを知りたい。
- 個別サブコマンドの通常処理内容や出力形式だけを確認したい。
- エラー終了時の一般規則だけを確認したい場合は、より直接のエラーハンドリング仕様を読む。

## hash
- fe0f3e04336f5c5cf846558298ec39d78fdb650eae19bf49cd3cb3271190508a

# `usage.md`

## Summary
- `cmoc` の利用手順を読む入口。初回の準備、セッション開始、oracle 反映と review/apply/join の往復、最終的なセッション統合までの流れを把握したいときに読む。

## Read this when
- `cmoc` をどう呼び出し、どの順で `session fork` / `review oracle` / `apply fork` / `apply join` / `session join` を進めるか確認したいとき。
- 人間が `oracle` を更新し、`cmoc` がどの時点の `oracle` を正本として実装へ追従させるかを確認したいとき。
- 初回だけ必要な準備や、作業ループの責務分担を確認したいとき。

## Do not read this when
- `cmoc` の内部実装や各サブコマンドの詳細仕様を知りたいときは、該当する実装側の文書を読む。
- `oracle` の書き方そのものや、個別の仕様断片を確認したいときは、`oracle` 配下の該当文書を直接読む。
- 一般的なリポジトリ構成や他ツリーの案内だけが欲しいときは、この文書ではなく上位の案内を読む。

## hash
- fe7509350bf677016679ba49878e301fbc712e3375ea1ebbd876b1ffcd68f9eb
