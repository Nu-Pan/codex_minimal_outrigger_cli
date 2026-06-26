# `acp`

## Summary
- AI エージェント呼び出しに関わる領域。呼び出しパラメータの構築と、そこへ組み込む標準プロンプト部品の生成を扱う。
- 処理ごとの role、goal、対象本文、補助文脈、ファイルアクセス条件、モデル設定、推論量、Structured Output schema などを組み立てる側と、oracle・realization・レビュー・ルーティング・INDEX.md エントリーなどの標準文書を構造化プロンプトとして生成する側への入口になる。
- cmoc のサブコマンドや TUI 実行前処理で、AI に何を読ませ、どの権限で作業させ、どの形式で出力させるかを確認するための実装群を探す起点になる。

## Read this when
- AI エージェントへ渡すプロンプト、標準文書、補助文脈、対象本文、出力 schema、モデル設定、reasoning effort、file access mode の組み立てを確認または変更したいとき。
- cmoc apply fork、cmoc indexing、cmoc review oracle、cmoc session join、TUI 実行前パラメータ解決などで、AI 呼び出し前の入力契約や出力契約を実装・テストしたいとき。
- oracle file と realization file の責務境界、レビュー標準、ルーティング規則、ファイルアクセス規則、INDEX.md エントリー標準などを AI 向けプロンプトへどう組み込むか確認したいとき。
- Codex CLI 向けの語句・ルート置換、作業ルート解決失敗時の扱い、git 操作禁止条件、realization 書き込み可否など、AI に提示する実行前条件を追いたいとき。

## Do not read this when
- 各サブコマンド全体の CLI 引数解析、実行順序、状態更新、git コマンド実行、保存処理など、AI 呼び出しパラメータ構築より外側の制御フローを調べたいとき。
- oracle file、realization file、review standard、apply review standard、INDEX.md 運用規則など、標準本文そのものや正本仕様断片を確認したいとき。
- Markdown レンダリング、構造化文書表現、パス解決、AgentCallParameter 型、モデル種別、ファイルアクセスモード、読み書きモード列挙値など、呼び出し構築を支える共通基盤そのものを調べたいとき。
- 個別の変更対象ファイル、実際の差分検出、分類アルゴリズム、conflict marker 検出、TUI 表示や入力取得など、AI に渡すパラメータ以外の具体処理を確認したいとき。

## hash
- e181774a219554e4c9e15efd7acaf4936fea24fdc32d675e776dc1999d0f3e76

# `basic`

## Summary
- cmoc の実装全体で共有される基礎的な型・変換ヘルパーをまとめる領域。エージェント呼び出しパラメータ、ルートトークン付きパス解決、規範データ構造、構造化文書から Markdown へのレンダリングを扱う。
- 特定の CLI サブコマンドや業務フローではなく、複数の上位実装から参照される抽象値、パス表現、仕様・文書表現の共通部品を確認する入口になる。

## Read this when
- エージェント呼び出しに渡す論理的なモデル指定、Reasoning effort、ファイルアクセスモード、Structured Output schema パスなどの共通パラメータ構造を確認・変更したいとき。
- cmoc で使う `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` 付きパス表記と実パスの相互変換、ルート探索、相対パス入力の扱いを確認・変更したいとき。
- 規範をコード上で表すデータ構造、要求ラベル、要求本文、判断例、構造化ドキュメントへの変換を確認・変更したいとき。
- 階層化された自然言語文書、仕様断片、レポート、プロンプトなどを Markdown 見出し・本文・コードブロックとしてレンダリングする共通処理を確認・変更したいとき。
- 上位機能で使う前提となる、型定義、入力検証、文書表現、Markdown 出力の境界を先に把握したいとき。

## Do not read this when
- CLI サブコマンドの引数定義、画面出力、終了コード、利用者向けコマンド挙動だけを調べたいとき。
- バックエンドが実際に受理する具体的なモデル名や Reasoning effort、ファイルアクセス指定への変換処理を探しているとき。
- プロンプト本文の生成ロジック、タスク別テンプレート、呼び出し実行の制御フローを調べたいとき。
- 個別機能がどの作業ディレクトリでファイルを作成・更新するか、永続状態や Git 操作をどう扱うかという業務ロジックを確認したいとき。
- 既存 Markdown の解析、INDEX.md のルーティング規則そのもの、正本仕様断片の内容や編集方針を確認したいとき。
- テスト構成、fixture、テストケース追加先を探しているとき。

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
- cmoc の実行時共通処理を集めた共有 helper 群の領域。CLI サブコマンド実行ラッパー、Codex CLI 呼び出し、preflight、profile 生成、設定読み書き、内容 hash、共通エラー、Git 操作、実行ログ、root/path 解決、結果型、session state など、複数の上位機能から利用される runtime 支援を扱う。
- 個別サブコマンドの業務処理ではなく、その周囲で共通に必要になる外部プロセス実行、ログ、設定、状態、path、例外変換、終了コード化、Codex 呼び出し制御への入口として使う。

## Read this when
- サブコマンド実行時の共通ライフサイクル、開始・完了表示、終了コード化、例外表示、サブコマンドログ設定を確認または変更したいとき。
- Codex CLI の exec/TUI 起動、profile・permission profile・schema・call log・resume token・quota/capacity retry・Structured Output 検証の runtime 境界を調べたいとき。
- `.cmoc` 配下の設定、ログ、state、schema、worktree、report などの実行時保存先や root path 解決を追いたいとき。
- cmoc 全体で共有される Git 操作、ファイル内容 hash、binary 判定、外部コマンド結果型、Codex 実行結果型、共通エラー整形、session state 永続化を確認または変更したいとき。
- 複数のサブコマンドや上位モジュールから使われる runtime helper を追加・公開・整理する必要があるとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務フロー、利用者向けコマンド構成だけを調べたいとき。その場合は対象サブコマンドの実装へ進む。
- path keyword の概念定義、oracle/realization の正本仕様、または root 種別そのものの説明を確認したいだけのとき。その場合は仕様側または path model 定義を読む。
- ログ、設定、state、Git、Codex 呼び出しなどの利用者向け結果を確認したいだけで、共通 runtime 実装や helper の挙動を変更しないとき。
- INDEX.md 生成ロジック、ルーティング文書のプロンプト、ファイル探索規則そのものを調べたいとき。
- テスト観点から期待挙動を確認する方が直接的な場合や、特定 helper の呼び出し元だけを調べれば足りる場合。

## hash
- da9f0f370fa21084a3b55429be3ced6156a5ded15ae4e36a9281208c2d30b659

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
- CLI のサブコマンド実装を集約する領域で、初期化、INDEX 更新、TUI 起動、oracle review、session 操作、apply 操作などの利用者向け command lifecycle への入口になる。
- 各サブコマンドは共通 runtime helper や下位 helper module を呼び出し、実行前条件の検査、branch/worktree/state の操作、Codex 呼び出し、report や stdout の生成を CLI 層として接続する。
- apply・session のような下位ディレクトリに分かれた大きな業務領域と、review 系 helper のような段階別 module が同階層に並ぶため、どのサブコマンドまたは処理段階へ進むかを選ぶための入口になる。

## Read this when
- cmoc の利用者向けサブコマンドがどの実装領域に分かれているかを把握し、調査対象の command lifecycle へ進みたいとき。
- init、indexing、TUI、oracle review、session fork/join/abandon、apply fork/join/abandon など、CLI から起動される処理の責務分担や入口 module を探したいとき。
- サブコマンド実装が git branch/worktree、session/apply state、Codex 実行、INDEX 更新、report 生成、stdout 表示をどこで orchestration しているか切り分けたいとき。
- oracle review の対象列挙、finding loop、INDEX merge、report rendering のように、ひとつのサブコマンド内で分割された処理段階の読む先を選びたいとき。

## Do not read this when
- CLI 全体の Typer app 構成、コマンド登録、共通 dispatch やログ保存ラッパーだけを調べたいときは、より上位の CLI 実装へ進む。
- git wrapper、path model、設定同期、ignore 判定、timestamp、report directory、Codex 低レベル実行など、複数サブコマンドから使われる共通基盤の内部だけを調べたいときは runtime や utility 側へ進む。
- session state や apply state の schema、状態ファイル path、branch 判定など状態モデルそのものを確認したいときは、状態定義や管理 helper 側へ進む。
- Codex に渡す prompt、Structured Output schema、AgentCallParameter builder の定義自体を変更したいときは、サブコマンドではなく prompt/acp builder 側へ進む。
- サブコマンドの外部挙動を検証するテスト、fixture、期待出力だけを調べたいときは、対応する test 領域へ進む。

## hash
- dd13266f4f175cb871047a15c15c1c699dd5c2a11111605856852944195bd4e2
