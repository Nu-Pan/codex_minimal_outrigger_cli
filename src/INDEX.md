# `acp`

## Summary
- 補助 AI 呼び出しの ACP 構築領域で、用途別の依頼パラメータを作る実装と、そのプロンプトを構成する標準部品群を収める。
- 適用支援、ルーティング文書生成、oracle file レビュー、session join の conflict 解消などで、補助 AI に渡す role、goal、読み書き制限、参照標準、model 設定、Structured Output schema を確認する入口になる。
- 上位の CLI 実行や git 操作そのものではなく、上位処理から呼び出される agent call の入力契約と、agent に提示する規範文の組み立てを扱う。

## Read this when
- 補助 AI に渡す AgentCallParameter の内容、用途別 prompt、model、reasoning effort、応答 schema を確認または変更したいとき。
- INDEX.md エントリー生成、apply review、oracle file review、session join の conflict 解消などで、agent にどの制約・標準・対象本文が渡されるかを追いたいとき。
- agent 用プロンプトに含まれる基本概念、ファイルアクセス規則、ルーティング規則、oracle / realization / review / INDEX.md エントリー生成標準の文面や組み立てを確認したいとき。
- 補助 AI 呼び出し仕様と、そこへ注入される標準プロンプト部品の対応関係を同じ領域から確認したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、通常の実行制御、git command 実行、merge、branch 作成、差分取得など、外部操作や上位フローそのものを調べたいとき。
- INDEX.md のファイル走査、生成結果の保存、レビュー結果の集約、通知、UI など、AI 呼び出し後の処理を調べたいとき。
- path keyword、root path、FileAccessMode、AgentCallParameter、StructDoc、標準変換など、複数領域で使う共通型や共通 helper 自体を変更したいとき。
- 個別の oracle file や realization file の本文、各標準の正本仕様断片、テスト対象の具体的な期待挙動を確認したいとき。
- 対象本文がすでに特定できており、agent call の依頼内容や標準プロンプト生成を確認する必要がないとき。

## hash
- 70459d2469b9df2b888d33951b42f6169887046ad5e4e8dd115a1467daf65162

# `basic`

## Summary
- cmoc の実装全体から参照される基礎的な型・小規模ヘルパーを置く領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパス表記、規範データ構造、構造化文書の Markdown 化といった、上位機能の前提になる共有部品への入口になる。
- バックエンド実行、CLI 制御、個別の正本仕様本文ではなく、cmoc 内部で値や文章構造をどう表現し、他の層へ渡すかを確認するための下位要素へ進む起点になる。

## Read this when
- エージェント呼び出しに渡すモデル種別、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output 要求有無などの共有データ構造を確認したいとき。
- cmoc 内のパス文字列や Path を、ルートトークンの意味に従って絶対パスへ解決したり、実パスをルートトークン付き表記へ戻したりする挙動を確認したいとき。
- 規範をコード上で保持するためのクラス、要求ラベル、判断例、構造化文書への変換処理を確認したいとき。
- 階層化された自然言語文書、見出し付きノード、コードブロック、複数行文字列の正規化を Markdown 出力へ組み立てる処理を確認したいとき。
- 上位の CLI、realization、テストから共有される基礎型や文書生成補助の責務境界を確認してから、より具体的な実装へ進みたいとき。

## Do not read this when
- 利用者向け CLI サブコマンドの引数、画面出力、終了コード、コマンド実行フローを確認したいだけのとき。
- 論理的なモデル種別やファイルアクセスモードを、特定バックエンドが受理する実値へ変換する処理を探しているとき。
- 実際にエージェントを起動するプロセス制御、外部コマンド実行、入出力処理を確認したいとき。
- 個別の正本仕様断片、oracle file と realization file の所有関係、編集可否、ファイルアクセス規則そのものを確認したいとき。
- Markdown の解析、既存 Markdown からの構造復元、HTML・JSON・YAML など Markdown 以外の出力処理を探しているとき。
- テスト構成、fixture、テストケース追加先を探しているとき。

## hash
- 69954679dba159a9b9c60034de86c2380953a718fe5f8862597af9835c21bf28

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
- cmoc の複数サブコマンドから利用される共有ランタイム helper 群。パッケージ入口自体は初期化や公開 import を持たず、実体は実行時共通基盤の実装に集約されている。
- 例外表現、サブコマンドログ、git・worktree・branch/session state、`.cmoc` 配下の永続補助ファイル、config JSON 変換、Codex CLI subprocess 呼び出し、quota/capacity retry、structured output 検証、hash・binary・gitignore 判定など、低レベルな副作用付き共通処理へ進む入口。

## Read this when
- 個別コマンドではなく、複数サブコマンドで共有される runtime helper の責務範囲やパッケージ境界を確認したいとき。
- git command 実行、branch 判定、clean worktree 要求、managed branch 判定、worktree 作成・削除、branch 削除などの共通挙動を確認または変更するとき。
- session state、session/apply branch からの session-id 抽出、state file の読み書き、active session 検索を扱うとき。
- `.cmoc` 配下の config、session、report、log、worktree、schema 保存先や `.gitignore` への除外処理を扱うとき。
- cmoc config の dict 変換、JSON 読み込み、既定値同期、不正設定時のエラー化を確認または変更するとき。
- Codex CLI を subprocess として呼び出す処理、profile 生成、CODEX_HOME 検証、structured output schema 準備、stdout/stderr/output/call log 記録を扱うとき。
- Codex CLI の capacity retry、quota polling、resume token 抽出、quota wait の共有制御、呼び出し結果の検証失敗時 retry を確認または変更するとき。
- CmocError、利用者向けエラー表示、subcommand logger の event 記録、実行時間・quota 待ち時間の記録を扱うとき。
- file hash、text hash、binary 判定、git ignore 判定など、複数箇所で使う小さな runtime helper の挙動を確認するとき。

## Do not read this when
- 個別サブコマンドの CLI 引数、コマンド固有の処理順、利用者向け出力 schema だけを確認したいとき。その場合は該当サブコマンド実装や対応する schema へ進む。
- config dataclass、AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort の定義そのものを確認したいとき。その場合は各定義元へ進む。
- oracle file や oracle standard の正本仕様内容を確認したいとき。その場合は oracle 側の本文へ進む。
- path keyword や `<cmoc-root>` などの用語モデルを確認したいとき。その場合は path model の定義元へ進む。
- テスト観点や既存テストケースを探すとき。その場合は対応する test 側の対象へ進む。
- 純粋な文字列整形、JSON schema 本体、または command 固有の prompt 生成だけを変更するとき。共有 runtime に触れる必要があるかを先に絞り込む。

## hash
- e1686301c7c49179b94889c31d23d82380e8f3a30ea936baff35c8d13977301b

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
- Typer ベースの CLI エントリーポイントとして、トップレベルおよび `session`、`apply`、`review` のサブコマンドを登録し、各コマンドを対応する実装モジュールへ委譲する。
- 各コマンド実行前後の共通処理として、work root 検証、サブコマンドログ記録、進捗表示、エラー整形、終了コード処理をまとめて扱う。
- Codex 実行前の自動 indexing、apply fork の所見列挙・変更要約レポート・commit message 生成、apply 対象候補の正規化、review oracle 関連処理の委譲など、複数サブコマンドをつなぐ薄い調停層を担う。

## Read this when
- CLI で公開されるサブコマンド名、Typer への登録、オプション、またはコマンドから実装関数への接続を確認・変更したいとき。
- すべてのサブコマンドに共通する実行ラッパー、ログ出力、work root 制約、例外表示、終了コード処理の挙動を確認したいとき。
- Codex 実行前に indexing が走る条件、indexing 中や conflict resolution 時にそれを抑止する条件を確認したいとき。
- apply fork が所見を列挙する対象、関連パスの抽出、編集禁止差分の検出、変更要約レポートや commit message 生成の呼び出し関係を追いたいとき。
- review oracle や apply/session/indexing の実装本体ではなく、CLI 層から各サブコマンド実装へ渡される依存関数を確認したいとき。

## Do not read this when
- 個別サブコマンドの中核ロジックや状態更新の詳細を調べたいだけなら、委譲先のサブコマンド実装を直接読む。
- 設定値の読み込み、状態ファイル形式、ログディレクトリ、git 実行、path モデルなどの基盤処理そのものを調べたいだけなら、runtime や utility 側の実装を読む。
- INDEX.md エントリーの生成・解析・描画アルゴリズムそのものを確認したいだけなら、indexing の実装を直接読む。
- apply fork の AI プロンプト定義や構造化出力 schema の詳細を確認したいだけなら、builder 側の該当定義を読む。

## hash
- 4ffeaada81485fe023bf4515f2466e0f5dc722731ac506c5125e5d9290553f6b

# `sub_commands`

## Summary
- cmoc の各サブコマンドについて、CLI 登録より内側の実行処理を集めた実装群。session、apply、oracle review、INDEX.md maintenance、初期化の各操作で、事前条件確認、状態更新、git/worktree 操作、Codex CLI 呼び出し、利用者向け Markdown 出力を runtime helper や builder と接続する層になっている。
- サブコマンドごとの外部挙動や制御フローを追る入口であり、低レベルな git/state/path/config helper や prompt/Structured Output parameter の詳細実装へ進む前に、どの操作がどの helper をどの順序で呼ぶかを確認するためのまとまり。

## Read this when
- cmoc の session fork/join/abandon、apply fork/join/abandon、oracle review、INDEX.md maintenance、初期化の実行条件、状態遷移、副作用、終了時出力を確認または変更したいとき。
- サブコマンドが clean worktree 確認、ignore 同期、branch/worktree 作成削除、merge conflict 処理、INDEX.md 差分の扱い、report 生成をどの流れで実行するかを追いたいとき。
- Codex CLI を使う apply/review/session join conflict 解決で、finding loop、validation/judge loop、conflict resolution、Structured Output の適用結果がサブコマンド処理にどう反映されるかを確認したいとき。
- INDEX.md maintenance や review/apply join で、INDEX.md だけを特別扱いする差分検査、commit、merge conflict 解消の制御を調べたいとき。
- サブコマンド利用者に返す Markdown 出力、report 内容、warning、CmocError の条件と復旧案を変更したいとき。

## Do not read this when
- Typer app への command 登録、引数・option 宣言、CLI ルート構成だけを確認したいときは、登録側の実装を読む。
- git wrapper、state file のデータ構造、path keyword、worktree 操作、config 読み込み、ignore 判定、binary 判定など、共通 runtime helper 自体の内部仕様を確認したいときは runtime 側を読む。
- Codex CLI に渡す prompt 文面、AgentCallParameter、Structured Output schema、finding 生成・merge・validate・judge 用 parameter の詳細を確認したいときは builder 側を読む。
- oracle file の正本仕様内容、INDEX.md エントリーとして何を書くべきか、path keyword の定義などの仕様断片を確認したいときは oracle 側を読む。
- 個別サブコマンドの実装位置がすでに分かっており、その 1 操作だけを局所的に変更したいときは、該当する下位ファイルへ直接進む。

## hash
- 7bec7d3dd7a7a4f41c4ddfb0838c916b60b0efd1c2d50d2096f4d21c99b6b5fe
