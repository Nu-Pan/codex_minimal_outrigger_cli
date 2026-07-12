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
- cmoc がローカルの Ollama を user systemd で管理し、Codex CLI の `cmoc` provider に接続するための運用仕様をまとめる。サービスの起動・再利用・修復、モデル取得、GPU 推論の利用可否確認、CLI 呼び出し時の設定固定が主題で、実装やテストはこの仕様に合わせる。

## Read this when
- `CodexModelSpec.model_provider` が `cmoc` のときに、事前保証すべき Ollama の可用性や GPU 推論条件を確認したいとき。
- cmoc が user systemd 配下の Ollama サービスをどう準備・起動・再利用・修復するかを実装または変更するとき。
- Codex CLI から `127.0.0.1:11434` の Ollama を使うための固定設定や禁止事項を確認したいとき。

## Do not read this when
- `cmoc` 以外の model provider の仕様を探したいとき。
- Ollama 本体の一般的な使い方や GPU 推論の一般論だけを確認したいとき。
- サービス管理やモデル配置ではなく、別の CLI サブコマンドや別機能の仕様を追いたいとき。

## hash
- fef7d8affc3c262acb8ea23ba8577825dd33bc650f163018809b01f2947ac04f

# `codex_exec_rule.md`

## Summary
- `codex exec` で cmoc から Codex CLI を呼ぶときの実行規約を定める文書。呼び出し形、`$CODEX_HOME` の扱い、事前検証、引数による上書き、プロンプトの渡し方、ログ保存、Structured Output、失敗時の再試行や待機の方針を確認したいときに読む。
- Codex CLI 呼び出しの実装方針を決めるときの正本であり、個別の `AgentCallParameter` builder 仕様へ進む前に、この呼び出し境界で何を固定し、何を上位の builder に委ねるかを把握する入口になる。

## Read this when
- cmoc から Codex CLI を起動する実装を追加・修正するとき。
- `$CODEX_HOME` の解決、preflight validation、`--model` や `--config` による上書き、stdin でのプロンプト受け渡し、`--json` や `--output-last-message` を含む呼び出し周辺を確認したいとき。
- Codex CLI の失敗時の再試行、quota 枯渇時の待機、サーバー一時不調時のリトライ条件を確認したいとき。

## Do not read this when
- `AgentCallParameter` の具体的な値決定や builder 内部の詳細だけを知りたいときは、より直接の builder 側の正本を読む。
- Codex CLI 呼び出しではなく、一般の cmoc 設定や別のサブコマンドの入出力を扱うだけなら、この文書は先に読まなくてよい。
- ファイルアクセス制限の事後検証やリカバリ方針を実装したい場合は、この文書ではなく該当する制御箇所を読む。

## hash
- 11df9873b79d4dcf58d511d048daece8416da6246a4ad3662e7a57cb3b03470b

# `console_and_file_log.md`

## Summary
- `console_and_file_log.md` は、cmoc のサブコマンド実行時に人間へ見せるコンソールログと、追跡用の JSON Lines ログをどう出すかを決める正本断片。時間・パスの表記、必須イベント、開始時通知、完了サマリーの出力要件が必要なら読む。
- この文書は出力の見た目と記録内容の境界を定めるための入口であり、ログの保存先や即時 flush、ステップ番号つきの見出し形式など、実装差を避けたい出力規則を確認したいときに進む。

## Read this when
- サブコマンドのコンソール表示やログファイルの出力形式を実装・変更するとき。
- 開始通知、ステップ侵入通知、Codex CLI 呼び出し通知、完了サマリーに含める情報を確認したいとき。
- 時間表示の整形やパスの囲み方など、ログ出力の表記規則を合わせたいとき。

## Do not read this when
- サブコマンドの内部処理手順や具体的なログ収集実装だけを確認したいときは、まずその実装側の本文を読む。
- この文書は出力規則の断片に限るので、他のサブコマンド仕様や別種の入出力仕様を探す目的では読まない。

## hash
- 7edd768c574fed88f782dc8bee7468a04cb5c4619d48fb154528d689ac49bdf8

# `doctor_preprocess.md`

## Summary
- cmoc 起動前に行う共通の事前検証と修復を扱う。`.cmoc/gu` の追跡外化、`.agents` の追跡可能化、`.cmoc/gt/ar/config.json` の追跡状態確保、必要時の managed ollama 可用性確認、差分の commit までが対象で、個別サブコマンド固有の前提確認はここでは扱わない。

## Read this when
- サブコマンド実行前の共通前処理を実装・変更したいとき。
- `.cmoc/gu` の ignore 設定や tracked 状態の整理、`.agents` の初期化、`.cmoc/gt/ar/config.json` の生成・追跡追加を確認したいとき。
- managed ollama を使う前提の可用性確認や、その失敗時に cmoc を止める条件を確認したいとき。

## Do not read this when
- 各サブコマンド固有の入力検証や本処理の流れを見たいときは、各サブコマンドの仕様を読む。
- 共通事前処理の後に行う個別前提や機能別の挙動を見たいときは、該当する機能側の仕様を読む。
- 起動前の環境整備ではなく、通常実行時のコマンド振る舞いだけを確認したいとき。

## hash
- 631962b52a08945fd832125650aa8d4e9d9a61f2417464acf305092304179f68

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
- cmoc の横断的な補助仕様を扱う。実装ファイルの機械的な列挙範囲、操作対象リポジトリへの前提、実行時のカレントディレクトリ、タイムスタンプ形式、管理対象 branch 上で発生した変更の範囲を定義する。

## Read this when
- 実装ファイルをどの範囲・除外条件で列挙するかを確認したいとき。
- cmoc が操作対象リポジトリに何を前提としてよいかを確認したいとき。
- cmoc 実行時の pwd や、タイムスタンプ文字列の桁数・区切り・timezone を確認したいとき。
- 管理対象 branch 上の変更として、commit 履歴・working tree・staging area・削除済みファイル・rename をどう扱うか確認したいとき。

## Do not read this when
- 個別コマンドの入出力、終了条件、状態遷移を確認したいとき。
- path placeholder 自体の意味や `<cmoc-root>`, `<repo-root>`, `<run-root>`, `<work-root>` の関係を確認したいとき。
- oracle file と realization file の所有者、編集可否、責務境界を確認したいとき。

## hash
- 7253cac67a1f25770f2a03fa9755061f17885ed1886b8a92ae9c0300b1bec402

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
- cmoc の run を他の操作と衝突させないための隔離規則を扱う。run ごとの branch と worktree の作り方、run 中の作業場所、run-root 外への書き込み例外を確認したいときの入口になる。
- サブコマンド実装で、作業環境の分離や run 完了後の session 側への戻し方を決める前に読む。
- 個別サブコマンドの入出力や UI ではなく、run の実行環境と永続先の境界を知りたいときに読む。

## Read this when
- cmoc のサブコマンドがどの branch と worktree で実行されるべきかを決めるとき。
- run 中の変更がどこに記録され、どこへマージされるべきかを確認したいとき。
- run-root の外に書ける例外を整理したいとき。

## Do not read this when
- サブコマンドの引数、出力形式、エラー文言などの個別仕様だけを確認したいとき。
- git branch や worktree ではなく、別の機能の保存形式やデータモデルを確認したいとき。
- run の隔離ではなく、実装内部の helper 分割やコマンド組み立てだけを見たいとき。

## hash
- da0e339241d7aef60122b871cd7617fbe5fed2abcf27eac5adfe5ae189bad582

# `session_state.md`

## Summary
- cmoc の session state を永続化する正本仕様断片。fork と join の遷移に関わる状態名、初期値、どの情報をステートに持つかという境界を確認したいときに読む。

## Read this when
- cmoc session / cmoc apply の状態遷移や永続化内容を実装・修正するとき。
- fork 元ブランチ、fork 元コミット、最後に join した oracle snapshot commit の扱いを確認したいとき。
- session state に何を保存し、何をその場で解決する前提にするかを判断したいとき。

## Do not read this when
- cmoc のコマンド体系全体や他のサブコマンドの責務だけを知りたいときは、より直接の仕様断片を読む。
- JSON の機械的な形や保存先のパスだけを探しているときは、この断片ではなく実装側の該当箇所を先に確認する。
- fork / join 以外の永続状態や別の session ファイル形式を扱うとき。

## hash
- 45858e4190eaced2325df570adda3e0c20c7a5b3283c38a1b31441dcb6d25277

# `sub_command`

## Summary
- `cmoc` の個別サブコマンド全体の入口をまとめた正本仕様群。各コマンドの起動条件、事前条件、状態遷移、終了コード、出力の境界を確認したいときに最初に読む。
- この対象はコマンド間の役割分担を示す案内であり、個別の実行手順や下位処理の詳細を読む場所ではない。必要な場合は、対象コマンドの正本仕様へ進む。

## Read this when
- サブコマンドの入口や責務分担を確認したいとき。
- 特定のコマンドの実行条件、状態遷移、出力、終了条件のうち、コマンド単位の外部仕様を見たいとき。
- どの正本仕様へ進むべきかを、対象コマンドごとに切り分けたいとき。

## Do not read this when
- 個別サブコマンドの内部手順や細かな分岐を知りたいときは、該当コマンドの正本仕様を直接読む。
- agent call の個別引数や下位処理の仕様だけを見たいときは、対応する正本へ進む。
- CLI 全体の共通ルーティングだけを確認したいときは、より上位の案内を読む。

## hash
- ec4b989c452c1d0ffa688ce3b396356a37e7c77babb0ab6b73b451f692204400

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
- cmoc を人間が実際に呼び出すための基本手順と、session fork から oracle 改訂、apply fork/join、session join までの標準的な作業ループを説明する。
- PATH への追加、初回の `cmoc dector`、各コマンドがブランチや oracle snapshot に対して担う役割を確認する入口となる。

## Read this when
- cmoc の利用者向けワークフロー全体を確認したいとき。
- `cmoc session fork`、`cmoc apply fork`、`cmoc apply join`、`cmoc session join` をどの順で呼ぶか判断したいとき。
- oracle を改訂してから実装へ追従させる通常の作業サイクルを確認したいとき。
- apply 実行中に session 側で進めた oracle 変更が、実行中の apply に反映されるか確認したいとき。

## Do not read this when
- 各コマンドの内部実装、引数解析、git 操作の詳細を確認したいとき。
- oracle file と realization file の責務境界や定義そのものを確認したいとき。
- 特定のブランチ名、run root、work root などのパス・ブランチ語彙の定義を確認したいとき。

## hash
- f7d3283563008aadaf1418cedfcb7d995ce0af62d6c26edd242e1fe47766f3eb
