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
- `codex exec` を呼ぶ側が、起動前の前提確認・引数上書き・プロンプト受け渡し・実行結果保存の扱いを決めるときに読む。
- Codex CLI をどう呼ぶかという入口仕様だけを押さえたい場合に読む。個別の `AgentCallParameter` builder の値決定や下位実装の分割は、ここではなく builder 側を読む。

## Read this when
- cmoc から Codex CLI を起動する経路を実装・修正するとき。
- `$CODEX_HOME` の扱い、事前検証、`--model` や `--config` による上書き、stdin 経由のプロンプト受け渡し、実行ログ保存の方針を確認したいとき。
- Structured Output の使い方や、呼び出し失敗時のリトライ・待機・再開の方針を確認したいとき。

## Do not read this when
- `AgentCallParameter` の具体的な生成規則や設定解決の細部だけを知りたいとき。
- Codex CLI の一般的な使い方や他サブコマンドの仕様だけを探しているとき。
- ファイルアクセス制限の具体的な値や prompt 文面の詳細だけを知りたいとき。

## hash
- e3f8f5ef0d4afee0c3c0859808f0bad776aae21835e0ab9576361b6fe9f332e5

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
- doctor preprocess の責務は、`cmoc` 共通の起動前前提をまとめて検証・修復し、各サブコマンド本体の前に環境を整えること。ここでは特に、`/.cmoc/local` の追跡除外、`.agents` の追跡状態確保、cmoc managed ollama の利用可能性確認、そして修復後差分のコミットまでを扱う。
- 同階層の他文書ではなくこの文書を読むべきなのは、サブコマンド個別ではなく全体共通の事前処理を扱い、かつ修復不能時の終了条件まで含むから。cmoc managed ollama の具体的な可用性判定だけは別文書を参照する。

## Read this when
- `cmoc` の各サブコマンドを起動する前に必要な共通前処理の責務を確認したいとき。
- `.cmoc/local` を追跡対象外にする条件や、`.agents` を差分の出ない状態に保つ条件を確認したいとき。
- 前提チェックで失敗した場合に、その場で終了するか修復を試みるかの境界を確認したいとき。

## Do not read this when
- サブコマンド固有の事前条件を確認したいときは、doctor preprocess ではなく各サブコマンド側の文書を読む。
- cmoc managed ollama の有効化や検証の細部だけを知りたいときは、`<work-root>/oracle/doc/app_spec/cmoc_managed_ollama.md` を読む。
- 個別の実装詳細やコミット手順の内訳だけを追いたいときは、この文書ではなく該当する実装側へ進む。

## hash
- b439874df502422792f7f2cbaef9ea5c257ecc7ebe7d26612f35e8533b5274bb

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
- サブコマンド呼び出しごとの run を、人間が触る作業ツリーから隔離するための正本仕様断片。run と session branch/run branch/run worktree の関係、run 作業を記録する branch と checkout 先 worktree、完了後のマージ規則がサブコマンドごとに異なることを扱う。
- run 作業の読み書き範囲は原則として run root 内に閉じるが、ログ・ステートファイルのように repo root 配下へ書くべき例外がある、という境界も示す。

## Read this when
- サブコマンド 1 回の実行単位である run の作業場所、branch、worktree の扱いを確認したいとき。
- run 開始時にどの HEAD から run 用 branch を作るべきか、run 作業をどこに記録すべきかを実装・検証するとき。
- run worktree 上で run branch を checkout して作業する制御を実装・レビューするとき。
- run 完了後に run branch を session branch へどう反映するかについて、サブコマンドごとのマージ規則との接点を確認したいとき。
- run 作業が run root 外へ書き込んでよい例外条件、特に実行中ログやステートファイルの保存先を判断したいとき。

## Do not read this when
- サブコマンド固有の具体的な branch 名、worktree 名、または個別のマージ手順そのものを確認したいときは、各サブコマンドの仕様を直接読む。
- path placeholder の一般定義や repo root/run root/work root の意味だけを確認したいときは、path model の仕様へ進む。
- run 隔離とは無関係な CLI 引数、出力形式、プロンプト、レビュー内容の仕様を調べるとき。

## hash
- 09080d9369142ee34fc3e3f62417f75bf96a43acc236dab7c9677f750598f972

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
- `cmoc` の各サブコマンド仕様をまとめる案内。`apply`、`session`、`review`、`doctor`、`indexing`、`tui` の正本仕様断片へ進む入口を与える。

## Read this when
- サブコマンド全体の一覧から、読むべき個別仕様を選びたいとき。
- 新しいサブコマンド仕様を追加・整理するときに、この階層へ案内を足すべきか確認したいとき。
- 個別仕様の所属先が不明で、`apply` 系、`session` 系、`review` 系、`doctor` 系、`indexing` 系、`tui` 系のどれを読むか切り分けたいとき。

## Do not read this when
- 個別サブコマンドの挙動を実装・修正・検証したいときは、該当する個別仕様を直接読む。
- パスや用語の定義だけを確認したいときは、用語・パスモデルの仕様を読む。
- この階層の案内だけで十分な場合に、下位の個別仕様へ進む必要はない。

## hash
- f62a22ad0fd11740b4b6570cb8db25eff45d9d74f7af105178f0e8c3ccc0ca31

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
