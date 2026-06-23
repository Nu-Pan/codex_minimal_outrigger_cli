# `acp`

## Summary
- AI エージェント呼び出しに渡すプロンプト、実行パラメータ、ファイルアクセス制約、モデル設定、reasoning effort、Structured Output schema を扱う実装領域。レビュー、適用、目次生成、セッション結合時の競合解消、TUI 実行前のパラメータ選定など、cmoc が AI に何を依頼し、どの構造で結果を受け取るかを追う入口になる。
- 共通プロンプト部品として、role、summary、goal、読み書き規則、INDEX.md によるルーティング規則、oracle file と realization file の基本概念、各種 standard を組み立てる処理も含む。個別サブコマンドの実行フロー本体ではなく、AI 呼び出しの依頼文・補助文脈・出力契約を確認するためのまとまり。

## Read this when
- AI 呼び出しごとの AgentCallParameter、モデル種別、reasoning effort、ファイルアクセスモード、Structured Output schema の対応関係を確認または変更したいとき。
- レビュー所見の列挙・検証・採否判定、実装所見の列挙・整理・適用、変更要約、INDEX.md エントリー生成、merge conflict marker 解消、TUI 実行前パラメータ選定など、用途別に AI へ渡す依頼内容を追いたいとき。
- 対象パス、対象本文、git diff、所見リスト、個別所見、conflict 対象ファイル、ユーザー入力プロンプトなどの補助文脈が、AI 用プロンプトへどう埋め込まれるか確認したいとき。
- ファイルアクセス規則、ルーティング規則、oracle/realization の基本概念、oracle review、apply review、INDEX.md エントリー品質基準など、AI に提示する共通判断基準の構成や組み立て順を確認したいとき。
- 新しい AI 呼び出しを追加する、既存の呼び出し条件や schema を変更する、または共通プロンプト部品をどの呼び出しへ含めるべきか判断したいとき。

## Do not read this when
- 各サブコマンドの CLI 引数解析、サブコマンド登録、実行制御、外部プロセス起動、git 操作、ファイル走査、保存・集約・表示など、AI 呼び出しの外側にある通常フロー本体を調べたいとき。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、StructDoc、path model などの共通型やユーティリティそのものの定義・挙動を詳しく調べたいとき。
- oracle file の正本仕様断片、realization implementation、realization test、個別サブコマンドの仕様本文や実装本文を確認したいとき。
- レビュー、適用、目次生成、競合解消、TUI などの具体的な対象がすでに決まっており、該当する下位領域や個別ファイルへ直接進めるとき。
- 生成済みプロンプトを実際に実行する処理、AI 応答の保存、後続の差分適用、画面表示、セッション状態管理などを確認したいとき。

## hash
- 137f2257f2f0da15d0a3d217906539450bb391ddd8bf9b4c3c443d1f1ac11a68

# `basic`

## Summary
- cmoc の realization implementation のうち、複数機能から共有される基本データ構造と小さな変換ヘルパーを集めた領域。エージェント呼び出し条件、ルートトークン付きパス、規範データ、階層化文書の Markdown 生成といった、上位の CLI や制御処理が利用する基礎概念への入口になる。
- バックエンド固有処理や利用者向けコマンドの実行ロジックより手前で、cmoc 内部の論理モデル、パス解決、仕様・文書表現をどの型と変換規則で扱うかを確認するための下位要素を持つ。

## Read this when
- エージェント呼び出しパラメータ、パス表記、規範オブジェクト、構造化 Markdown 出力など、複数の上位機能にまたがる基本型や変換処理の読む先を選びたいとき。
- バックエンド実行や CLI サブコマンドの詳細へ進む前に、cmoc 内部で共有される論理的なモデルや入力検証の境界を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` のようなルートトークン付きパス表記、またはその実パス変換に関わる実装を探しているとき。
- 規範や説明文をコード上の構造として保持し、Markdown へ変換する小さな文書生成部品の責務を確認したいとき。

## Do not read this when
- 利用者向け CLI コマンドの引数、画面出力、終了コード、プロセス起動、入出力処理を確認したいとき。より上位のコマンド実装や実行制御の領域を読む方が適切。
- バックエンドが実際に受理するモデル名、権限指定、Reasoning effort へ解決する処理や、エージェント実行結果の解析を調べたいとき。この領域は主に前段の論理型を扱う。
- 個別の正本仕様断片の本文、oracle file と realization file の管理規則そのもの、または人間が所有する仕様内容を確認したいとき。正本仕様側の文書を読む方が適切。
- テスト構成、fixture、テストケース追加先、または既存テストの外部挙動を確認したいとき。テスト領域を直接読む方が適切。

## hash
- 0677409fe6067d0591ef0b36f3a03ca6bb950d881c1c141a40b99d58659d0030

# `cmoc_runtime.py`

## Summary
- 上位互換用の薄い転送モジュールであり、実体のランタイム実装を別モジュールへ委譲する。
- このモジュール自身は処理ロジックを持たず、インポートされたモジュール名を実装本体へ差し替える入口として機能する。

## Read this when
- 旧来または短い import 経路からランタイム実装へ到達する仕組みを確認したいとき。
- モジュール別名化、互換 import、公開 import 経路と実装本体の対応を調べるとき。

## Do not read this when
- ランタイムの具体的な挙動、関数、状態管理、CLI 実行時処理を調べたいとき。その場合は委譲先の実装本体を読む。
- 互換 import 経路ではなく、実装ロジックやテスト対象の詳細を変更したいとき。

## hash
- 81ecd7098ca82b3aab203450f5599ed486313c7b477ea88f527c4b7356c81e04

# `commons`

## Summary
- cmoc の複数 subcommand から共有される実行時支援を集めた領域。共通エラー、外部コマンド結果、Codex 呼び出し結果、ログ、session/apply 状態、設定の読み書き、管理 branch 判定、worktree 操作、実行用パス、Codex profile 生成、CLI/TUI 呼び出し、retry、schema 検証、hash・binary・ignore 判定など、個別 command の業務フローより下位の共通基盤を扱う。
- 現時点ではパッケージ入口自体に公開 import や初期化処理はなく、実質的な処理は共通 runtime 実装に集約されている。

## Read this when
- cmoc 全体で共有される runtime helper、git・filesystem・設定・状態・Codex 実行の共通処理を探しているとき。
- repository root、cmoc root、session/report/log/worktree/schema/config など、実行時に使う標準的な保存場所やパス生成規則を確認・変更したいとき。
- 管理 branch、session id、active session、session/apply 状態ファイル、worktree 作成・削除、branch 削除、git ignore 判定など、複数 command にまたがる git・状態操作を扱うとき。
- cmoc config の読み込み、同期、書き込み、既定値補完、型変換エラー、dict 変換など、設定の共通処理を扱うとき。
- Codex home の検証、Codex profile 生成、sandbox mode 変換、Codex subprocess 環境、CLI/TUI 呼び出し、JSONL/stdout/stderr/output/call log、structured output schema、semantic retry、capacity retry、quota polling/resume を調べるとき。
- 共有 runtime helper 群のパッケージ境界や、パッケージ読み込み時の初期化処理・上位へ再公開される名前の有無を確認したいとき。

## Do not read this when
- 個別 subcommand の利用者向け手順、引数定義、command 固有の orchestration を知りたいだけのとき。その場合は該当 command の実装へ進む。
- agent 呼び出しパラメータ、設定 dataclass、path keyword、oracle、INDEX 生成規則など、共通 runtime から参照されるモデルや正本仕様そのものを確認したいとき。その場合は各定義元や oracle document を読む。
- テストケースの期待値、外部挙動の検証観点、特定の report や log の内容を調べたいとき。その場合は対応する test や生成物を直接読む。
- 個別 helper の具体的な関数・クラス・定数だけを探しており、共通 runtime 基盤全体の位置づけやパッケージ境界を確認する必要がないとき。

## hash
- 36f3d9f6820aae6f2bce3121f5cbabdedbe636b9a3825039c0b87b2194987922

# `config`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の設定データ構造を扱う領域。
- 永続化される設定の最上位構造、Codex CLI に渡すモデル名・推論 effort 名への対応、apply 系および review oracle 系ループ回数上限の入口になる。

## Read this when
- 開発対象リポジトリごとの cmoc 設定項目、既定値、設定データクラスの構造を確認・変更したいとき。
- Codex CLI 呼び出しに使うモデル名または reasoning effort 名への対応を確認・変更したいとき。
- apply fork の apply ループや所見リスト改善ループの上限回数を確認・変更したいとき。
- review oracle の所見列挙・マージ・検証ループの上限回数を確認・変更したいとき。
- 永続化される config の dataclass 構造や Enum 系設定値を文字列値へ変換する前提を追うとき。

## Do not read this when
- CLI 引数の定義、サブコマンドの実行フロー、または設定値を実際に読み書きする処理だけを調べたいとき。
- モデル区分や推論 effort 区分そのものの定義・意味を確認したいとき。
- 個別サブコマンドの処理内容や所見リストの生成・改善・検証ロジックを調べたいとき。
- リポジトリルート、作業ディレクトリ、実行ディレクトリなどのパス概念の定義を確認したいとき。

## hash
- a00a59142486c0b666d65e7da06ffecc853826b95c867ddee77e89591c4bb50b

# `main.py`

## Summary
- Typer ベースの cmoc CLI の最上位エントリーポイントであり、root command と session/apply/review のサブコマンドを登録し、各コマンドを実装モジュールへ委譲する薄い接続層。
- サブコマンド実行共通処理として、work root 実行確認、subcommand log の開始・終了記録、進行表示、例外の整形、returncode の Typer 終了への変換を担う。
- Codex 呼び出し前の INDEX 更新、apply fork の finding 列挙・対象正規化・禁止差分検査・commit message 生成・report 生成、review oracle や indexing の実装関数へのラッパーをまとめる入口。

## Read this when
- CLI サブコマンドの登録名、Typer option、root/session/apply/review/indexing/tui の起動経路を確認・変更したいとき。
- サブコマンド実行時の共通ログ出力、作業ディレクトリ制約、例外表示、returncode 処理、apply branch 実行時のログ保存先切り替えを追うとき。
- Codex 実行前に INDEX 更新が走る条件、indexing 用 Codex 呼び出しや conflict resolution でそれをスキップする条件を確認するとき。
- apply fork のループ周辺で、対象ファイルの列挙・正規化、finding の収集、禁止対象の差分検出、変更要約 report、エラー report、commit message 生成の接続関係を調べるとき。
- review oracle や indexing の CLI から、実際の処理実装へどの関数・callback が渡されるかを確認するとき。

## Do not read this when
- 個別サブコマンドの中核ロジックそのものを変更したいだけのときは、委譲先の sub_commands 配下の実装を直接読む方が適切。
- 設定読み込み、状態ファイル、git 実行、ログディレクトリ、path model、エラー型などの runtime 共通部品の詳細を調べたいときは、runtime 側の実装を読む方が適切。
- INDEX エントリーの生成・解析・render・commit の詳細だけを確認したいときは、indexing 実装を直接読む方が適切。
- apply/review の report 本文フォーマットの利用者向け意味を仕様として確認したいときは、実装ではなく対応する oracle 文書を優先する。

## hash
- 8396fb6b677984c1c39f66f206a340066ec7c24f7bc7ff4d6e073316edd1c2b4

# `sub_commands`

## Summary
- cmoc の各サブコマンドに対応する実処理モジュール群であり、初期化、session、apply、review、indexing、TUI 依頼解決の主要な制御フローへの入口になる。
- 各モジュールは Typer への登録そのものよりも、対象サブコマンドの実行条件、状態遷移、worktree・branch 操作、Codex CLI 呼び出し準備、出力生成、エラー条件などの実処理を担う。
- サブコマンド単位で読む先を選ぶ階層であり、低レベルな git・state・config・path helper や prompt/schema builder の内部仕様へ進む前に、利用者向け操作の流れと副作用を把握するための起点になる。

## Read this when
- cmoc の特定サブコマンドがどの順序で runtime helper、state、git worktree/branch、Codex CLI 呼び出し、report/index 出力を扱うかを確認または変更したいとき。
- `cmoc init`、session fork/join/abandon、apply fork/join/abandon、oracle review、INDEX.md maintenance、TUI 依頼入力のいずれかの実行条件、状態遷移、副作用、CLI 出力、cleanup 挙動を調べたいとき。
- サブコマンドの外部挙動に関わる CmocError 条件、復旧案、merge conflict 解決、unexpected changes 判定、INDEX.md だけの差分取り込みや conflict 解消を追いたいとき。
- finding の列挙・統合・refine・検証・判定・適用 loop や、それに伴う report/error report の生成タイミングをサブコマンドの流れの中で確認したいとき。
- 現在の work root や active session branch を前提にした branch/worktree ライフサイクル、clean worktree 確認、`.cmoc` ignore 確保、設定同期、更新差分 commit の制御を調べたいとき。

## Do not read this when
- CLI アプリ全体の command 登録、Typer app への接続、引数や option の宣言位置だけを確認したいときは、サブコマンド登録側を読む。
- git 実行 wrapper、worktree 操作、branch 判定、state file の path 規則、config 読み込み、binary 判定、ignore 判定などの共通 helper の内部実装だけを確認したいときは、runtime 側を読む。
- Codex CLI に渡す prompt 文面、AgentCallParameter、Structured Output schema、apply/review/session conflict resolution 用 parameter 構築の詳細だけを確認したいときは、builder 側を読む。
- oracle file の正本仕様内容、path keyword の定義、INDEX.md エントリーとして何を書くべきかの規則そのものを確認したいときは、oracle 側の仕様断片を読む。
- 生成済み report、過去の review/apply 結果、または個別 run の成果物だけを確認したいときは、該当する出力先の生成物を読む。

## hash
- 87bec77778ad21d579ed445e6e06dca124055db341336ec5f760bf2c76be5505
