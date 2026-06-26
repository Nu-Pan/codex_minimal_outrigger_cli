# `acp`

## Summary
- AI エージェント呼び出しに関わる実装領域。各工程の AgentCallParameter と Structured Output schema を組み立てる処理と、プロンプトを構成する標準部品の生成処理を扱う。
- サブコマンドや工程ごとの role、summary、goal、補助文脈、標準文書、ファイルアクセス規則、model class、reasoning effort、返却 schema を追う入口になる。
- 差分要約、レビュー所見、所見対応、正本仕様断片レビュー、merge conflict marker 解消、TUI 実行前のパラメータ解決、ルーティング文書エントリー生成など、AI 呼び出し境界と共通プロンプト規範を確認するためのまとまり。

## Read this when
- AI エージェントへ渡す prompt、実行条件、Structured Output schema の対応を、機能領域別に探し始めたいとき。
- apply fork、review oracle、session join、tui、indexing などの工程で AgentCallParameter がどのように構築されるか確認または変更したいとき。
- oracle、realization、レビュー、INDEX.md、ファイルアクセス、ルーティングに関する標準文書や規則文書が、agent prompt にどう含まれるかを調べたいとき。
- AI 呼び出しごとのファイルアクセス権限、モデル種別、推論強度、標準文書断片、補助入力の埋め込み方を比較したいとき。

## Do not read this when
- AI 呼び出しより上位の CLI 引数解析、サブコマンド実行順序、状態保存、git 操作、対象ファイル探索などの実行制御を調べたいとき。
- StructDoc、Markdown rendering、AgentCallParameter、FileAccessMode、path 解決、complete prompt 生成など、複数領域で使われる共通基盤の型や helper を調べたいとき。
- 生成済みのレビュー所見、差分要約、INDEX.md エントリーなど、AI 呼び出し結果の保存・表示・利用側の挙動を確認したいとき。
- 個別サブコマンドの CLI 挙動、状態ファイル、path model、入出力 schema など、プロンプト部品や AI 呼び出し境界ではない機能仕様・実装を探しているとき。

## hash
- 0e7d135f26551118a732c2882542545038d7374f0be00db8e84bf9aa1a8506bc

# `basic`

## Summary
- cmoc 内部で広く使われる基礎的な値オブジェクトと文書生成部品を置く実装領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパス解決、規範データ構造、構造化文書の Markdown レンダリングを扱う。
- CLI コマンドや個別ワークフローの表層ではなく、それらから参照される共通概念を確認する入口になる。

## Read this when
- エージェント呼び出しで使うモデル階層、reasoning effort、ファイルアクセス権限、Structured Output schema などの論理的な指定値を確認・変更したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` 付きパス表記と実パスの相互変換、ルート探索、相対パス検証の挙動を確認したいとき。
- 規範をコード上で表すクラス、要求ラベル、規範オブジェクトから構造化ドキュメントを作る処理を確認したいとき。
- 内部で組み立てた階層的な自然言語文書を Markdown 見出し、本文、コードブロックとしてレンダリングする処理を確認したいとき。
- 上位実装を読む前に、cmoc 全体で共有される小さな基礎概念や値表現の責務境界を把握したいとき。

## Do not read this when
- 利用者向け CLI サブコマンドの引数、出力、終了コード、具体的なワークフロー実装を探しているとき。
- エージェント呼び出しを実際の backend 用モデル名や実行設定へ変換する処理、プロセス起動、標準入出力、結果解析を確認したいとき。
- oracle file と realization file の正本関係、編集責務、仕様管理方針そのものを確認したいとき。
- 既存 Markdown の解析、ファイル走査、Git 操作、永続状態管理など、基礎データ構造や Markdown レンダリング以外のアプリケーション挙動を調べたいとき。
- 個別の規範本文、プロンプト本文、Structured Output schema ファイル、またはそれらを選択するコマンド実装を確認したいとき。

## hash
- dccc7abf3f5e9949eccb65058d2076632e0253825977ef0a16753150e01943c7

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
- cmoc の実行時共通処理を集めた共有 helper 群。CLI サブコマンド実行の共通ラッパー、Codex exec/TUI 呼び出し、Codex profile・preflight・call log 表示、設定ファイル入出力、内容 hash、共通エラー、Git 操作、実行ログ、root/path 解決、外部コマンド結果型、session/apply state 永続化など、複数の上位機能から利用される runtime 基盤への入口になる。
- 個別の業務フローを実装する場所ではなく、サブコマンドや workflow 実装が共通利用する低レベルから中間層の runtime 部品を責務別に分けている。公開 import 面だけを束ねる入口と、実際の副作用や状態遷移を持つ実装が混在するため、まず扱いたい共通責務を絞って下位要素へ進むための階層である。

## Read this when
- cmoc の実行時共通 helper がどの責務領域に分かれているかを把握し、CLI、Codex、設定、Git、logging、path、state、結果型、エラー処理のどこへ進むべきか判断したいとき。
- サブコマンド実装や workflow 実装から利用する runtime 共通 API の公開面、または共有 helper の追加・削除・移動先を検討したいとき。
- Codex CLI 呼び出しに関わる exec/TUI 起動、profile 生成、Structured Output 検証、retry、quota/capacity 制御、preflight、call log 表示のうち、どの責務の実装を読むべきか切り分けたいとき。
- cmoc 全体で共通化されている設定ファイル処理、ファイル内容 hash、利用者向けエラー整形、Git repository/worktree 操作、実行ログ、root/path 解決、永続 state 読み書きの入口を探すとき。
- 複数のサブコマンドや上位 module から使われる処理を共有 module に置くべきか、既存の共通 helper で足りるかを確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、利用者向けコマンド構成、業務処理の詳細、workflow 全体の高レベルな制御順序だけを調べたいとき。その場合は各 command や workflow の実装へ進む。
- path keyword や root/work/run の概念定義そのものを確認したいとき。その場合は path model の正本仕様または path model 実装を読む。
- INDEX.md の内容生成ロジック、エントリー生成プロンプト、ファイル探索ルールそのものを調べたいとき。
- ログや状態ファイルを読む側、集計する側、表示する側の仕様を調べたいだけで、実行時にログや state を生成・保存する共通処理を扱わないとき。
- Codex や Git など外部コマンドの利用者向け挙動をテスト観点から確認したいだけで、runtime wrapper の入力・出力・副作用・失敗時変換を変更しないとき。

## hash
- a22a33676d346ce8dab919b744536ceb9f7ab84b0ed4843f97c635b699652da8

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
