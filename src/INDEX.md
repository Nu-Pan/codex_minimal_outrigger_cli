# `acp`

## Summary
- AI agent を ACP 経由で呼び出すためのプロンプト構築領域。用途別の呼び出しパラメータ生成と、agent prompt に注入するファイルアクセス規則・ルーティング規則・oracle/realization 基本説明・各種標準文書の構成部品を扱う。
- レビュー、適用後確認、ルーティング文書エントリー生成、競合解消、TUI 実行前判定などの補助エージェント依頼について、役割・目的・補助文脈・アクセス権限・モデル設定・Structured Output schema をどう組み立てるか確認する入口になる。

## Read this when
- 補助エージェントへ渡す最終プロンプトの内容、標準文書の注入条件、ファイルアクセス制約、モデル種別、推論強度、Structured Output schema の対応関係を確認・変更したいとき。
- 適用後の差分要約や所見列挙、oracle レビューでの新規所見抽出・支持理由・反証理由・採否判定・重複整理など、AI への依頼文と出力契約を追いたいとき。
- ルーティング文書エントリー生成で、対象本文を根拠にする条件、既存目次を読ませない制約、関連文書参照、読み取り専用条件、返却 schema を確認したいとき。
- merge conflict marker 解消や TUI 実行前の権限・標準文書要否判定など、実処理の前段で AI agent に判断や整形を依頼する呼び出し内容を調べたいとき。
- agent prompt に組み込まれるファイルアクセス規則、INDEX.md を使った読み進め方、oracle/realization の基本説明、各種標準文書の文面や注入順序を確認したいとき。

## Do not read this when
- CLI サブコマンド全体の実行順序、引数解析、git 操作、ブランチ操作、保存・表示・集計・通知など、ACP 呼び出しパラメータ構築より外側の制御フローを調べたいとき。
- oracle file、realization file、レビュー基準、INDEX.md エントリー標準など、agent prompt に組み込まれる標準本文の正本仕様そのものを調べたいとき。
- 実際の仕様違反判定、レビュー所見の妥当性判断、merge conflict の編集アルゴリズム、git diff や変更ファイル抽出の生成処理そのものを確認したいとき。
- ACP 呼び出し型、構造化ドキュメント表現、Markdown rendering、パス解決 helper など、prompt 構築領域から利用される共通基盤だけを確認したいとき。
- TUI の表示・対話、session join の統合処理、apply fork のフォーク作成・適用、review 結果の保存など、利用者向け操作や後続処理の実装を追いたいとき。

## hash
- 5e67c508cc366ca1b5ab081888a4ff70af4902054153d6cc2dabe258d4409116

# `basic`

## Summary
- cmoc の実装全体で共有される基本的な値オブジェクトと小規模ヘルパーを扱う領域。エージェント呼び出しの論理パラメータ、ルートトークン付きパス表記、規範データ構造、Markdown 向け構造化文書レンダリングなど、上位機能が前提として使う基礎部品を定義する。
- backend 実行、CLI コマンド、仕様管理、テスト実行などの具体的な業務フローへ進む前に、それらが依存する抽象的な入力値・パス解決・文書表現の責務境界を確認する入口になる。

## Read this when
- エージェント呼び出しに渡すモデル品質階層、reasoning effort、ファイルアクセス権限、プロンプト、Structured Output schema、追加書き込み許可パスなどの論理的な指定値を確認・変更したいとき。
- cmoc 内で扱うパス文字列を絶対パスへ解決する規則や、ルートトークン付き表記と実パスの相互変換を確認・変更したいとき。
- 規範をコード上のデータ構造として表現し、要求項目や判断例を構造化文書へ変換する処理を確認したいとき。
- 見出し階層を持つ自然言語文書やコードブロックを組み立て、Markdown 文字列として出力する小さな文書レンダリング処理を確認したいとき。
- 上位の CLI や realization 処理を読む前に、共有される基礎概念の型、入力検証、変換処理の責務を把握したいとき。

## Do not read this when
- 実際の backend が受理するモデル名、サンドボックス設定、プロセス起動、標準入出力、実行結果解析、エラー処理を探しているとき。
- 利用者向け CLI サブコマンドの引数、出力、終了コード、個別コマンドが組み立てるプロンプト本文を確認したいとき。
- oracle file と realization file の所有関係、編集権限、正本仕様断片としての内容そのものを確認したいとき。
- 個別機能がどの作業ディレクトリでファイルを作成・更新するかという業務ロジックや永続状態の扱いを調べたいとき。
- 既存 Markdown の解析、Markdown 以外の出力形式、または構造化文書モデルを必要としない単純な文字列整形を探しているとき。
- テスト構成、fixture、テストケース追加先を探しているとき。

## hash
- 4ed54299b1f479741f38c7c63bcb2752f40ccc691700bc40cb978066521796fc

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
- cmoc の実行時共通処理を集めた realization implementation 領域。Codex CLI 実行/TUI 起動、profile 準備、設定永続化、content hash、CLI サブコマンド共通ライフサイクル、エラー整形、Git 操作、JSON Lines ログ、runtime path、実行結果型、session state など、複数の上位機能から再利用される helper 群への入口になる。
- 集約 import 入口と責務別 runtime module が同居しており、呼び出し側が共通 API の公開面を確認する場合は集約層を、個別挙動や副作用を確認する場合は該当する責務別実装へ進むための階層である。

## Read this when
- cmoc の複数サブコマンドや上位処理から共有される runtime helper の配置と責務分担を確認したいとき。
- Codex CLI exec/TUI の起動、profile/schema/log 準備、retry、quota/capacity 制御、Structured Output 検証、call log 記録、preflight など Codex runtime 周辺の共通実装を探すとき。
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外処理、work root 検査、subcommand log 設定を確認または変更したいとき。
- 設定ファイルの読み書き、既定値補完、不正 JSON や不正値の利用者向けエラー化を扱う共通処理を探すとき。
- SHA-256 digest、内容アドレス型ファイル書き込み、binary file 判定など content hash 系 helper を探すとき。
- cmoc 共通の実行時エラー表現、利用者向けエラー文面整形、Git repository/worktree 操作、runtime path 導出、JSON Lines ログ、実行結果データ型、session state 永続化を確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI 引数定義、利用者向け入出力の具体内容を調べたいだけのときは、該当するサブコマンド実装へ直接進む。
- path keyword や root 種別そのものの正本仕様を確認したいときは、path model の仕様または定義側を読む。
- 設定データクラス、AgentCallParameter、FileAccessMode などの型定義そのものを確認したいだけのときは、モデル定義側を読む。
- INDEX.md 生成ロジック、oracle file の正本仕様、prompt、ファイル探索ルールを調べたいときは、それぞれの indexing や oracle 関連の対象へ進む。
- 特定機能の高レベルな制御順序やテスト期待値を確認したいときに、その機能専用の実装・テストがより直接の読む先として存在する場合。

## hash
- d728c2759472924a5d25cae13c00ceeb0541e4bfebc8390b3f2bcf8917475eb9

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
- CLI の各サブコマンド実装を集める領域。初期化、目次更新、TUI 起動、session 操作、apply 操作、oracle review とその補助処理を、利用者向けコマンドから runtime・git・Codex 実行 helper へ接続する入口になる。
- 各サブコマンドは、実行前条件、worktree や branch の状態確認、設定・session state・report・利用者向け出力との連携を扱う。複数ファイルに分かれる領域では、全体 orchestration と対象列挙、実行ループ、report 生成、INDEX 差分処理などの下位責務へ分岐する。
- サブコマンド単位で、どの処理が CLI 層にあり、どの処理が共通 runtime や個別 helper に委譲されるかを選び分けるための入口。

## Read this when
- cmoc のサブコマンド実装全体から、初期化、目次更新、TUI、session、apply、oracle review のどの実装へ進むべきかを選びたいとき。
- CLI サブコマンドが実行前条件、clean worktree 確認、branch/worktree 操作、session state 更新、Codex 実行、report 出力、commit/merge などをどの単位で扱うかを把握したいとき。
- session branch の作成・取り込み・破棄、apply run の開始・進行・join/abandon、oracle review の対象列挙・finding loop・report・INDEX merge など、利用者向け操作の制御フローを追いたいとき。
- 目次更新サブコマンドの対象走査、既存エントリー再利用、Structured Output 生成、ハッシュ検証、更新差分 commit の流れを調べたいとき。
- 対話的な依頼文編集から Codex TUI 起動までの parameter 解決、prompt 生成、エディタ起動、保存先 log 領域の扱いを確認したいとき。

## Do not read this when
- CLI 全体の Typer app 登録、共通 command wrapper、runtime helper、git wrapper、設定 schema、path model など、サブコマンド個別ではない基盤実装だけを調べたいとき。
- oracle file や realization file の正本仕様、INDEX.md の記述方針、ルーティング文書生成規則そのものを確認したいとき。
- Codex CLI に渡す prompt や Structured Output parameter の具体的な本文だけを確認したいときは、それを構築する prompt・parameter 側の実装へ直接進む。
- branch 操作、worktree 作成削除、state file 読み書き、report 保存先、process id 管理、git command 実行などの共通 helper 内部だけを変更したいときは、runtime 側へ直接進む。
- 調べるサブコマンドまたは補助責務がすでに決まっており、その本文へ直接進めるとき。

## hash
- 8537f2b77b21c80c563044694a441e0b937dbf55b4b958fd781dceef1c78c5f9
