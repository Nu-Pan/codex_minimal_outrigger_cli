# `acp`

## Summary
- AI エージェント呼び出しに関する実装をまとめる領域。用途別の呼び出しパラメータ構築と、プロンプトを構成する標準部品の生成を扱う。
- apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成などで、agent に渡す role、goal、補助入力、ファイルアクセス条件、モデル設定、Structured Output 契約を確認する入口となる。
- 実際のサブコマンド実行、git 操作、対象ファイル探索、永続状態操作そのものではなく、それらの結果や標準文書を agent prompt としてどう渡すかを扱う。

## Read this when
- cmoc の各機能が AI エージェントを呼び出す際に、どの入力、制約、モデル設定、出力 schema を組み合わせているか確認・変更したいとき。
- apply 系の差分要約、realization file 所見列挙、検出済み所見への修正依頼など、apply 後段の agent 呼び出し条件と出力契約を追いたいとき。
- oracle review で新規所見、理由追加、採否判定、所見整理を生成させる prompt と、正本仕様断片を根拠にした Structured Output の接続を確認したいとき。
- session join の conflict marker 解消や、TUI 実行前のファイルアクセスモード・標準参照要否判定など、特定用途の事前判断を agent に依頼する実装を調べたいとき。
- agent prompt に含めるファイルアクセス規則、INDEX.md ルーティング規則、oracle/realization の基本概念、レビュー基準などの標準部品や、それらの最終プロンプトへの組み込み方を調べたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の実行順序、git 操作、フォーク作成・統合、merge conflict marker 検出、生成結果の保存など、agent 呼び出しパラメータ構築の外側を調べたいとき。
- oracle file、realization file、review standard、apply review standard、realization standard など、prompt に含められる標準文書の正本本文そのものを読みたいとき。
- StructDoc の基盤データ構造、Markdown rendering、パス解決 helper、AgentCallParameter の基本定義だけを確認したいとき。
- 個別の所見カテゴリ、レビュー判断の材料作成、対象ファイル探索、git diff 生成、変更ファイル抽出アルゴリズムなど、agent に渡す前の入力を作る側の詳細を調べたいとき。
- 生成済み INDEX.md の内容評価や、ルーティング文書一般の書き方だけを確認したいとき。

## hash
- dec8f9607b8dcc288bebb81c5bf42ec37f296b22643f26eccddc794dcdcd998f

# `basic`

## Summary
- バックエンド非依存の基礎データ構造と小さな文書生成ヘルパーを集めた実装領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパス解決、規範文書モデル、構造化文書の Markdown レンダリングを扱う。
- 上位の CLI・制御処理・仕様生成処理から共有される基本型や変換処理を確認する入口であり、具体的なバックエンド実行、コマンド UI、個別仕様本文、テスト構成へ進む前に基礎表現を確認するための対象。

## Read this when
- cmoc 内部で共有されるモデル区分、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema パスなど、エージェント呼び出し入力の保持形式を確認または変更したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` を含むパス表記の意味、探索規則、実パスとの相互変換、ルートトークンなし相対パスの拒否条件を確認したいとき。
- 規範文書をコード上で表す型、要求ラベル、要求本文の保持単位、規範オブジェクトから構造化ドキュメントを生成する処理を確認したいとき。
- 見出しツリー、本文文字列、コードブロックを組み合わせた構造化文書から Markdown を生成する処理や、空行整理・コードフェンス・インデント正規化の挙動を確認したいとき。
- 複数の上位機能から使われる基礎表現の責務境界を確認し、変更先が呼び出し制御、パスモデル、規範モデル、Markdown レンダリングのどれに属するか切り分けたいとき。

## Do not read this when
- 具体的なバックエンド名、実モデル名、CLI 引数、外部コマンド呼び出し、権限指定への変換ロジックを確認したいだけのとき。
- CLI サブコマンドの利用者向け挙動、画面出力、終了コード、永続状態操作、ファイル走査の業務ロジックを調べたいとき。
- 個別の正本仕様断片や oracle file の本文内容、仕様管理上の所有関係や編集責務だけを確認したいとき。
- Structured Output schema ファイル自体の内容、JSON schema の仕様、または特定コマンドの出力 schema を確認したいとき。
- プロンプト本文の組み立て、テンプレート内容、タスク種別ごとの文章生成ルール、または生成済み Markdown 文書の内容そのものを調べたいとき。
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
- cmoc の実行時共通処理を集めた実装領域。Codex CLI 呼び出し、CLI サブコマンド共通ライフサイクル、設定入出力、content hash、エラー表示、Git 操作、ログ、path 解決、外部コマンド結果型、session/apply 状態永続化など、複数機能から共有される runtime helper を扱う。
- 個別 helper の実装に加えて、複数の runtime 領域の公開 API をまとめて再公開する入口や、旧 import path を保つ薄い互換入口も含む。

## Read this when
- CLI サブコマンド全体に共通する実行順序、進捗表示、終了コード化、例外時表示、実行ログ記録の入口を確認または変更したいとき。
- Codex exec/TUI 呼び出しの profile 準備、schema 配置、subprocess 実行、call log、Structured Output 検証、quota/capacity retry、resume 継続、preflight 実行制御を追いたいとき。
- cmoc 設定ファイルの読み書き、既定値補完、不正 JSON や不正値の利用者向けエラー化を扱うとき。
- 内容ハッシュ、ハッシュ付きファイル書き込み、binary file 粗判定など、生成物や入力内容を扱う小さな共通処理を探すとき。
- cmoc 共通の例外表現、利用者向けエラー文面、Git repository 状態検査、worktree/branch 後始末、`.cmoc` の ignore 検証を確認したいとき。
- サブコマンド実行ログ、Codex 呼び出し完了サマリー、quota 待機時間、context-local logger の扱いを確認または変更したいとき。
- 実行時 root、`.cmoc` 配下の保存先、timestamp、duration 表示、作業ディレクトリ一時変更、session/apply 状態 JSON の保存形式や branch 名との対応を調べたいとき。
- 複数の runtime helper を利用する呼び出し側で、どの共通 API を集約入口から import できるかを確認したいとき。

## Do not read this when
- 個別サブコマンド固有の業務処理、引数定義、dispatch、利用者向け出力だけを調べたいときは、そのサブコマンド実装へ進む。
- path keyword の概念定義や `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の仕様そのものを確認したいときは、path model の正本仕様または定義実装へ進む。
- 設定モデル、AgentCallParameter、FileAccessMode、CmocConfig などのデータ構造そのものを確認したいだけのときは、各モデル定義へ進む。
- INDEX.md 生成ロジック、エントリー生成プロンプト、ファイル探索ルール、oracle/realization の仕様文書を調べたいときは、それぞれの仕様・indexing 実装へ進む。
- ログや状態を読む側、集計する側、表示する側の仕様だけを調べたいときは、それらの機能実装へ進む。
- テスト期待値や fixture から特定挙動を確認する方が直接的な場合は、対応するテスト領域へ進む。

## hash
- 1ed0e3e99cee19f83fd86568f2c8249fc1001f0f3d5db48636e0b5602c9bd8eb

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
- cmoc の Typer ベース CLI の最上位エントリーポイントであり、通常起動時にトップレベルコマンドと session/apply/review 配下のサブコマンドを登録する。
- CLI 引数解析エラーを cmoc 共通のエラー表示形式へ変換する TyperGroup 拡張を持ち、シェル補完実行時だけ通常の Typer/Click 処理へ委ねる。
- 各コマンド本体の処理はサブコマンド実装へ委譲し、この対象は公開 CLI の配線、既定 option、コマンド名、起動関数の入口を扱う。

## Read this when
- cmoc のコマンド一覧、サブコマンド階層、コマンド名、CLI option の既定値や公開面を確認・変更したいとき。
- CLI 引数解析に失敗した場合のエラー表示、終了コード、シェル補完時の例外処理分岐を確認・変更したいとき。
- パッケージ実行や console entry point から呼ばれる起動入口がどのように Typer アプリケーションを実行するか確認したいとき。
- 新しいサブコマンド実装を CLI に接続する、または既存サブコマンド実装への委譲先を差し替えるとき。

## Do not read this when
- 個別サブコマンドの業務処理、状態更新、git 操作、ファイル生成などの実装詳細を調べたいだけのときは、対応するサブコマンド実装を直接読む。
- cmoc 共通エラー型やエラー表示文字列の構造そのものを変更したいときは、共通ランタイム側を読む。
- Typer/Click の一般的な使い方や外部ライブラリ仕様を調べたいだけのときは、この対象ではなくライブラリ文書を参照する。

## hash
- 1d335758bd3acb952f8c1ac069bceb844903688c51741aed8d46a4f83f846171

# `sub_commands`

## Summary
- CLI サブコマンド実装を集める領域で、初期化、TUI 起動、ルーティング目次更新、review oracle、session 操作、apply 系実行ライフサイクルなど、利用者が直接呼び出す機能の入口になる。
- 各サブコマンドは共通 CLI 実行ラッパー、indexing preflight、git/worktree/session state 操作、Codex 実行、利用者向け Markdown 出力や report 生成などを接続する orchestration を担い、詳細な共通処理や helper 実装へ進む前の切り分け点になる。

## Read this when
- どのサブコマンド実装を読むべきか未確定で、初期化、目次更新、TUI、review oracle、session fork/join/abandon、apply 系操作の責務境界を比較したいとき。
- 利用者向け CLI コマンドの入口、実行前提、共通 runner との接続、サブコマンド固有の状態遷移、出力や report 生成までの高レベルな制御順序を追いたいとき。
- review oracle の対象列挙・実行 loop・INDEX 差分 commit・report、または apply run の開始・破棄・join・process 管理・結果 report など、複数 helper を束ねる実行フローを調べる入口が必要なとき。
- session branch の作成・取り込み・破棄、作業ツリー初期化、ルーティング目次生成、Codex TUI 起動など、サブコマンド単位の外部挙動や失敗時挙動を確認または変更したいとき。

## Do not read this when
- git 実行 wrapper、path model、設定読み込み、状態ファイル I/O、worktree 操作、ignore 判定、timestamp 生成など、サブコマンドから呼ばれる共通 runtime 実装そのものを調べたいとき。
- oracle file、realization file、ルーティング文書、session state schema、prompt 構築、Structured Output schema など、CLI サブコマンド入口ではない仕様・データ構造・生成パラメータを確認したいとき。
- 特定のサブコマンドや下位 helper が読む対象として既に分かっており、この階層で責務境界を比較する必要がないとき。
- 自動テストや oracle 側の正本仕様断片を調べたいだけで、実装側のサブコマンド orchestration を追う必要がないとき。

## hash
- e88a96512118de2d78ef961a780a081abb2f3cd2ee0b2c1e83d26b4f3d170cf6
