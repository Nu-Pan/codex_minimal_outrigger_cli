# `acp`

## Summary
- AI エージェントへ渡すプロンプト部品と呼び出しパラメータ構築を扱う領域。共通の作業規則・標準文書を構造化プロンプトとして生成する下位要素と、それらを各機能の具体的な agent call、権限、model class、reasoning effort、Structured Output schema に接続する下位要素への入口になる。
- サブコマンドや TUI の実行制御そのものではなく、cmoc が AI に何を読ませ、何を依頼し、どの出力契約で返させるかを追うための上位ルーティング対象である。

## Read this when
- agent prompt に含める標準文書・作業規則・ファイルアクセス規則・ルーティング規則・INDEX.md エントリー規範の生成処理を確認または変更したいとき。
- apply fork、INDEX.md エントリー生成、oracle review、session join の conflict 解消、TUI 実行前パラメータ解決などで、AI エージェントへ渡す prompt、補助文脈、権限、model class、reasoning effort、Structured Output schema の対応を追いたいとき。
- 共通プロンプト部品と個別機能向け builder のどちらを読むべきか判断したいとき。
- AI 呼び出し時に、標準文書や対象ファイル情報がどのように文脈化され、読み取り・編集制約や構造化出力契約と結び付けられるかを調べたいとき。

## Do not read this when
- CLI 引数解析、サブコマンドの実行順序、保存、表示、集計、git 操作、merge 実行、conflict marker 検出など、AI 呼び出しパラメータ構築より外側または下位の処理を調べたいとき。
- oracle file、realization file、path model、各種 standard など、プロンプトへ含められる標準文書や正本仕様断片の本文そのものを確認したいとき。
- Markdown rendering、構造化文書表現、AgentCallParameter 型、パス解決など、prompt 部品や builder に閉じない共通基盤の実装を調べたいとき。
- 生成済み INDEX.md の内容、特定ディレクトリのルーティング判断、TUI 表示や対話 UI の挙動を確認したいとき。

## hash
- 98cf633b0a44c2fcb402d44e42fb111b2fded27e4f6661ab3d5639be059759b9

# `basic`

## Summary
- cmoc の実装で共通に使う基礎部品を集めた領域。エージェント呼び出し条件の抽象型、ルートトークン付きパスの解決、規範データの表現、構造化文書から Markdown へのレンダリングを扱う。
- 上位の CLI や個別ワークフローから直接利用される低水準のモデル・変換処理への入口であり、バックエンド固有処理や利用者向けコマンド挙動へ進む前に、共通データ構造や共通変換規則を確認する場所である。

## Read this when
- cmoc 内部で共有される基本的な型、値オブジェクト、文書構築ヘルパー、パス解決ヘルパーのどれを読むべきか判断したいとき。
- エージェント呼び出しに渡す論理的なモデル種別、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema 指定の表現を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` を含むパス表記を実パスへ解決する挙動や、実パスをルートトークン表記へ戻す挙動を確認したいとき。
- 規範をコード上のデータ構造として保持し、背景・要求・判断例を構造化文書へ変換する処理を確認したいとき。
- 階層化された自然言語文書やコードブロックを Markdown 見出し付きの文字列へレンダリングする処理を確認したいとき。

## Do not read this when
- 利用者向け CLI サブコマンドの引数、画面出力、終了コード、実行フローを調べたいとき。
- 具体的なバックエンドが受理するモデル名、reasoning effort 値、サンドボックス設定、サブプロセス起動方法への変換を調べたいとき。
- 個別の正本仕様断片そのもの、oracle file の編集方針、仕様管理上の所有関係を確認したいとき。
- 既存 Markdown を解析して構造化データへ変換する処理や、汎用 Markdown パーサを探しているとき。
- テスト構成、fixture、テストケース追加先、または個別機能の作業ディレクトリ上の副作用を調べたいとき。

## hash
- 8d94dca84d270b4fa4b33e15e66d16c39720978cb8732957988df4509bf46751

# `cmoc_runtime.py`

## Summary
- 互換用の薄い入口であり、実体のランタイム実装を別モジュールから読み込んで、この import path 自体を実装モジュールへ差し替える。
- 旧来の直接 import 経路や公開設定上の import 経路を残すための橋渡しで、責務固有のランタイム処理はここには置かない。

## Read this when
- トップレベルのランタイム import path がどの実装へ接続されるかを確認したいとき。
- 互換 import 経路の維持・削除条件や、直接 import している呼び出し元への影響を確認したいとき。
- ランタイム実装を移動・分割したあと、この互換入口を残す必要があるか判断したいとき。

## Do not read this when
- ランタイム処理そのものの挙動、引数処理、状態管理、出力生成を調べたいとき。その場合は実体の実装モジュールを読む。
- 新しいランタイム機能や責務固有の処理を実装したいとき。この互換入口ではなく実体側のモジュールを読む。
- パッケージ公開設定やエントリーポイント定義を確認したいだけのとき。その場合は設定ファイルを読む。

## hash
- 223b9df223b1746d08a7487389b45587c37917fa6e9b6d75d8dbb48985527074

# `commons`

## Summary
- cmoc の realization implementation のうち、複数サブコマンドや runtime 層から共有される実行時 helper 群を集める領域。Codex CLI 呼び出し、profile 生成、設定ファイル入出力、content hash、共通エラー、Git 操作、ログ、root/path 解決、外部コマンド結果型、session state など、機能実装の土台になる共通処理への入口になる。
- 個別 module は、公開 import 面だけを束ねるもの、サブコマンド実行ライフサイクルを包むもの、Codex exec/TUI を制御するもの、低レベルな path・git・logging・state・config 補助を担うものに分かれているため、cmoc の業務 workflow 本体ではなく共通 runtime の責務境界を確認するための階層である。

## Read this when
- サブコマンドや workflow 実装から再利用する runtime helper、共有データ型、共通エラー、ログ、path、Git、設定、状態管理、Codex 呼び出し周辺の実装を探したいとき。
- Codex exec/TUI の起動前準備、profile/schema/log path、Structured Output 検証、retry、quota/capacity 制御、call log、console/subcommand log event の責務分担をたどりたいとき。
- CLI サブコマンドの共通ラッパー、実行前チェック、開始・完了表示、終了コード化、例外表示、実行時間や quota wait を含む完了サマリーを確認または変更したいとき。
- cmoc 設定ファイルの永続化形式、content hash、binary 判定、CmocError 表現、Git repository/worktree 操作、JSON Lines 実行ログ、root/path 解決、CommandResult/CodexExecResult、session state の読み書きなど、横断的な runtime 基盤を確認または変更したいとき。
- 新しい共通 helper を置く場所、既存 helper の公開 import 面、または複数上位 module から共有される処理の責務境界を判断したいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、利用者向けコマンド構成、workflow 全体の高レベル制御だけを調べたいとき。その場合は該当 command や workflow 実装へ進む。
- path keyword や oracle/realization の正本仕様、INDEX.md 生成方針、仕様断片の意味を確認したいとき。その場合は oracle 側の仕様文書や path model 定義を読む。
- テスト期待値や fixture から外部挙動を確認する方が直接的なとき。この階層は主に実装共通部であり、テスト観点だけなら対応する realization test へ進む。
- 特定 helper の詳細な入力、出力、失敗時挙動を変更したい対象がすでに分かっているときは、この階層全体ではなく該当する責務別 module を直接読む。
- 公開 API でも共有 runtime でもない、単一機能内に閉じた小さな処理や UI/出力文言の業務固有ロジックを探しているとき。

## hash
- 697c673933c5697ef5f1696ef587eaaefd923a73689315dda55af126ed9e8172

# `config`

## Summary
- 開発対象リポジトリごとに変わる cmoc 設定を表す dataclass 群を扱う領域。
- AI エージェント呼び出しの並列数、Codex CLI 向けモデル名と reasoning effort、apply fork と review oracle のループ上限など、永続化される設定値の既定値を確認する入口になる。
- 人間が編集するリポジトリ別設定面に含まれる値の定義を追うための対象であり、設定ファイルの入出力処理そのものは別領域に分かれる。

## Read this when
- リポジトリ別に保持される cmoc 設定項目や既定値を確認・変更したいとき。
- 初期化時に生成・同期される設定ファイルへ含める値や、Enum 系の値を JSON 保存向けに扱う前提を確認したいとき。
- Codex CLI に渡すモデル名、reasoning effort 名、AI 呼び出し並列数、apply fork や review oracle の処理回数上限を調整したいとき。

## Do not read this when
- CLI 引数、サブコマンド構文、実行時の入出力フローを調べたいだけのとき。
- 設定ファイルの実際の読み書き、JSON 変換処理、または `.cmoc` 配下のパス解決処理を調べたいとき。
- oracle file、realization file、パスキーワード定義、INDEX.md 生成ルールそのものを確認したいとき。

## hash
- 324dfe3034cabedbb119cb79c0c59fcdd422ac0747dbbc5e095eba5140bb0d71

# `main.py`

## Summary
- cmoc の実行入口として Typer アプリケーションを構築し、トップレベルコマンドと `session`、`apply`、`review` 配下のサブコマンドを各実装関数へ接続する CLI 配線を担う。
- 通常の CLI 引数解析エラーを cmoc 共通のエラーレポート形式へ変換する TyperGroup 拡張を含み、シェル補完時は通常の Typer/Click 処理に委ねる。
- 個々のサブコマンドの業務ロジックは保持せず、各サブコマンド実装モジュールへの入口として位置づけられる。

## Read this when
- cmoc コマンド全体の起動経路、Typer アプリケーション構成、サブコマンド階層を確認したいとき。
- 新しい CLI サブコマンドや option を公開面として追加・削除・改名し、対応する実装関数との接続を変更したいとき。
- CLI 引数解析失敗時の表示形式、終了コード、補完時の例外処理回避を確認または変更したいとき。
- `init`、`tui`、`indexing`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracle` がどの実装関数へ委譲されるかを確認したいとき。

## Do not read this when
- 各サブコマンドの具体的な処理内容、状態更新、Git 操作、ファイル生成、レビュー判定の詳細だけを調べたいときは、対応するサブコマンド実装を直接読む。
- cmoc 共通エラー型やエラーレンダリングそのものの仕様・実装を調べたいときは、共通ランタイム側を読む。
- path keyword、oracle file、realization file などの正本仕様上の概念定義を調べたいときは、oracle 側の仕様断片を読む。
- テスト観点や期待される CLI 外部挙動を確認したいだけで、CLI 配線や引数定義を変更しないときは、対象サブコマンドに対応するテストを読む。

## hash
- b6ef09b427ea27ff526149b8d840553659470844d3284c42e959505fec5a9395

# `sub_commands`

## Summary
- CLI のサブコマンド実装を集める領域。初期化、ルーティング文書更新、対話的 Codex 起動、session 操作、apply run、oracle review など、利用者が直接起動する主要機能の実行入口を扱う。
- 各サブコマンドは、実行前条件の検証、状態や branch/worktree の操作、Codex 呼び出し、report や利用者向け出力、共通 runtime/helper への接続を担う。
- 複数段階に分かれる処理は下位 module や下位ディレクトリへ分割されているため、どのサブコマンドのどの段階を調べるかを決めてから詳細へ進むための入口になる。

## Read this when
- CLI サブコマンド単位で、利用者操作がどの実装入口へつながるかを確認したいとき。
- init、indexing、TUI 起動、session fork/join/abandon、apply fork/join/abandon、oracle review のいずれかの実行順序、前提条件、状態更新、出力、失敗時処理を調べたいとき。
- branch/worktree 操作、session state や apply state の更新、Codex 実行、report 生成、INDEX 更新 commit などが、サブコマンドの orchestration としてどう接続されるかを追いたいとき。
- 共通 runtime や builder の低レベル実装ではなく、CLI 層から各 helper へ渡される主要な値と責務分担を把握したいとき。

## Do not read this when
- CLI 全体の app 定義、サブコマンド登録、引数ツリー、共通 command dispatch だけを調べたいときは、上位の CLI 構成を扱う実装へ進む。
- git wrapper、path model、config、timestamp、binary 判定、git ignore 判定、状態 schema、report directory などの共通基盤そのものを確認したいときは、runtime や utility 側へ進む。
- Codex に渡す prompt、Structured Output schema、AgentCallParameter 構築の詳細だけを確認したいときは、該当する builder 側へ進む。
- 外部挙動の期待値や fixture を確認したいときは、対応するテスト領域へ進む。
- 特定サブコマンド内の詳細段階がすでに分かっている場合は、この階層を経由せず、その処理を担当する下位対象へ直接進む。

## hash
- a0b5eb9f5bed741e3f8bdeb5baa025b50deb5e2365a1555be23e7fdd6708fb76
