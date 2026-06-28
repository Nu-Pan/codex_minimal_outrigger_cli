# `acp`

## Summary
- AI エージェント呼び出しに関わる realization implementation の上位領域であり、呼び出しパラメータを組み立てる処理と、その complete prompt に差し込む標準プロンプト断片の構築処理を収める。
- 各機能が AI に渡す role、summary、goal、補助入力、ファイルアクセス制約、標準参照、モデル・reasoning、Structured Output schema をどのように定めるかを追うための入口になる。
- 変更要約、実装所見調査、INDEX エントリー生成、oracle review、merge conflict marker 解消、TUI 実行パラメータ選定など、AI に依頼する作業の呼び出し条件と応答契約へ進む起点になる。

## Read this when
- cmoc の処理が AI エージェントを呼び出す直前に、どの入力・権限・モデル設定・Structured Output schema を渡しているかを確認または変更したいとき。
- AI 呼び出し用 complete prompt に含まれる基本情報、ファイルアクセス制約、ルーティング規則、oracle/realization の概念、レビュー基準、INDEX エントリー規範の生成箇所を探したいとき。
- 変更差分要約、レビュー所見列挙、所見対応、INDEX エントリー生成、oracle 関連レビュー、merge conflict marker 解消など、個別の AI 作業依頼のプロンプト設計や応答 schema を調べたいとき。
- AI 呼び出しの入口と、そこから利用される標準プロンプト断片の関係を同じ領域で把握したいとき。

## Do not read this when
- サブコマンド登録、CLI 引数解析、実行順序、状態管理、git 操作、ファイル更新、結果保存・表示など、AI 呼び出し前後の制御フローだけを調べたいとき。
- path model、StructDoc、Markdown rendering、AgentCallParameter、FileAccessMode などの基礎型や汎用構造化文書処理そのものを確認したいとき。
- oracle file や realization file の本文仕様、または実際にレビュー・修正される対象ファイルの内容を直接読みたいとき。
- 生成済みの INDEX.md の保存・更新・描画や、リポジトリ全体のルーティング文書管理だけを調べたいとき。

## hash
- 63862674c39d794f60eebc7f8c42cce2cd8120e1cca897c9bea5d72afcc91b6b

# `basic`

## Summary
- cmoc の実装全体で共有される基礎モデルと小さな文書処理ユーティリティを置く領域。エージェント呼び出し条件、ルートトークン付きパス解決、規範文書モデル、階層文書から Markdown への変換といった、特定の CLI サブコマンドより下位の共通概念を扱う。
- バックエンド固有の API 値、個別コマンドの実行フロー、ファイル読み書きそのものではなく、それらの上位処理が参照する抽象的な型・変換・検証・レンダリングの入口として位置づけられる。

## Read this when
- モデルクラス、reasoning effort、ファイルアクセスモード、Structured Output schema の有無など、AI コーディングエージェント呼び出し条件をコード上でどう保持するか確認したいとき。
- ルートトークン付きパス表記を実パスへ解決する挙動、または実パスをルートトークン付き表記へ戻す挙動を確認・変更したいとき。
- main worktree、linked worktree、現在の worktree、Git common dir などを使った cmoc 固有のルート探索や失敗条件を調べたいとき。
- 規範文書を構成する見出し、背景、要求、判断例、要求項目ラベルを実装上のモデルとしてどう検証・保持するか確認したいとき。
- 規範文書モデルや階層化された自然言語文書を、表示・文書用の構造化表現または Markdown 文字列へ変換する処理を確認したいとき。
- 文書本文やコードブロックのインデント正規化、空行整理、Markdown 見出し階層の扱いを確認・変更したいとき。

## Do not read this when
- 個別サブコマンドの CLI 引数、出力 schema、実行順序、ユーザー向け入出力を調べたいとき。
- エージェントプロセスの起動、外部コマンド実行、API 呼び出し、バックエンド固有のモデル名や権限表現への変換処理を探しているとき。
- ファイル内容の読み書き、INDEX 生成、oracle file と realization file の分類、永続状態操作など、基礎モデルを使った業務ロジックを調べたいとき。
- 自然言語で書かれた個別の規範本文や正本仕様断片そのものを読みたいとき。
- 生成された Markdown の保存先、利用元、CLI からの呼び出し経路だけを確認したいとき。
- テストで期待される外部挙動だけを確認したい場合で、共通モデルや内部変換の詳細まで不要なとき。

## hash
- d1d69ef3a0bf213c284d4c2b95623804491fbf9ff997ac57263f1648cb474fbe

# `cmoc_runtime.py`

## Summary
- 公開モジュール名を既存の実体モジュールへ差し替えるだけの互換レイヤー。実装本体は別モジュールに委譲し、この入口から import する利用者にも同じ実体を見せるために、実行時のモジュール登録を置き換える。
- 既存の呼び出し元や配布設定が古い import path を参照している期間だけ残す移行用コードであり、責務別の実行時モジュールまたは実体モジュールへ参照元が移った後は削除対象になる。

## Read this when
- 公開されている古い import path と実体モジュールの対応関係を確認したいとき。
- 互換 import path を残す理由、削除条件、または移行状況を調べるとき。
- この入口を import した場合に、どのモジュール実体が利用されるかを確認したいとき。

## Do not read this when
- 実行時処理そのもののロジック、設定解釈、状態操作、CLI 挙動を調べたいとき。この対象は実装本体ではなく委譲だけを行う。
- 新しい実行時機能を追加・修正したいとき。互換入口ではなく、実体側または責務別の実行時モジュールを読む方が直接的である。
- 互換 import path の削除可否と無関係な一般的なモジュール探索やパス定義を調べたいとき。

## hash
- a36ad0b5d09cbe7d2be546fdafcd27ff3ddaf803744331274a69fb25f15cd7ee

# `commons`

## Summary
- cmoc の実行時共通 helper 群をまとめる実装領域。Codex CLI 呼び出し、preflight indexing、CLI サブコマンド共通ライフサイクル、設定、内容 hash、エラー表示、Git 操作、ログ、パス、結果モデル、session state など、上位コマンドから再利用される runtime 基盤を扱う。
- この階層は、個別サブコマンドの業務ロジックではなく、複数の command や runtime 経路から共有される下位機能への入口である。集約 import 面と責務別 runtime 実装の両方が含まれるため、共通処理の公開面を確認してから具体実装へ進む起点になる。

## Read this when
- Codex exec/TUI の起動、profile 準備、Structured Output 検証、quota/capacity retry、call log、preflight indexing など、Codex 呼び出し runtime の共通挙動を確認または変更したいとき。
- CLI サブコマンドの共通実行フロー、work root 検査、標準サマリー出力、終了コード化、例外表示、サブコマンドログの設定・解除を扱う変更をしたいとき。
- 設定ファイルの読み書き、内容 hash 保存、binary 判定、利用者向けエラー表示、Git 状態確認や worktree/branch/ignore 操作など、複数箇所で使われる基盤 helper を探すとき。
- 実行時 path、timestamp、ログ・レポート・設定・state の保存先、memo 判定、現在のサブコマンド logger、実行結果データ構造、session state 永続化の責務境界を確認したいとき。
- ルーティング文書の自動更新 preflight、対象候補の列挙、既存エントリーの hash 検証、Codex によるエントリー生成、更新 commit 作成条件を調べたいとき。
- 上位 command 実装を読む前に、共通 runtime API と責務別 helper のどこへ進むべきかを切り分けたいとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務ロジック、画面出力、永続状態をいつ更新するかという高レベルな制御フローだけを調べたいとき。その場合は command 側の実装へ進む。
- パス概念そのものや `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の正本定義を確認したいだけのとき。その場合は基本層の path model や対応する oracle を読む。
- oracle file の仕様意図、ルーティング文書の品質基準、session state などの正本仕様断片だけを確認したいとき。この階層は realization 側の runtime 実装であり、正本仕様そのものではない。
- 生成済みのルーティング文書、ログ、レポート、state file の内容を読むだけで、生成・保存・検証の runtime ロジックを追う必要がないとき。
- テスト期待値や fixture のみを変更したいとき。runtime の外部挙動を確認する必要がなければ、対応する test 領域へ直接進む。

## hash
- 0994057a667b42bd1d5ad7599db66dd38b4236553ab33b164562416dfffbc200

# `config`

## Summary
- リポジトリごとに変わる cmoc の挙動設定を集約する領域で、永続化される設定 JSON に対応する Python 側の設定データ構造と既定値を扱う。
- AI エージェント呼び出しの並列数、Codex CLI に渡すモデル名・reasoning effort 名の対応、apply fork や review oracle の処理上限など、設定として調整される値の入口になる。

## Read this when
- リポジトリごとの cmoc 設定項目、既定値、設定データ構造を確認または変更したいとき。
- 永続化される設定 JSON と Python 側の設定クラスとの対応を追いたいとき。
- Codex CLI に渡すモデル種別や reasoning effort の対応表を確認または変更したいとき。
- AI エージェント呼び出しの並列数や、apply fork・review oracle などのサブコマンド挙動を調整する設定値を確認または変更したいとき。

## Do not read this when
- 設定ファイルの読み書き、JSON 変換、初期化時の同期処理そのものの実装を探しているとき。
- モデル種別や reasoning effort の概念定義そのものを確認したいとき。
- 各サブコマンドの実行ロジック、レビュー所見の生成・マージ・検証処理を確認したいとき。
- cmoc のパス語彙、oracle file、realization file などの基本概念を調べたいとき。

## hash
- a242e188b7c03be1ee0f0161de15a75b353c820a470ff59f3bab33bcd903ffd8

# `main.py`

## Summary
- cmoc の最上位 CLI を構成し、Typer アプリケーション、`session`・`apply`・`review` のサブコマンドグループ、各 CLI コマンドから実装関数への委譲を定義する実装入口。
- 通常の CLI 引数解析エラーを cmoc 形式のエラーレポートへ変換する Typer group を定義し、補完実行時だけ通常の Click/Typer 処理へ逃がす。
- console script から `cmoc` としてアプリケーションを起動するためのトップレベル関数を持つ。

## Read this when
- cmoc の公開 CLI コマンド構成、サブコマンド名、option 名、デフォルト値、各コマンドがどの実装関数へ委譲されるかを確認または変更したいとき。
- CLI 引数解析エラーを cmoc の `CmocError` と `render_error` で表示する挙動、または shell completion 時の例外処理分岐を確認または変更したいとき。
- `cmoc` console script 起動時に Typer app がどの `prog_name` で呼ばれるか、またはトップレベル app とサブ Typer app の接続を確認したいとき。

## Do not read this when
- 個別サブコマンドの本体処理、永続状態操作、git 操作、worktree 操作、レビュー処理、INDEX.md 更新処理の詳細を知りたいだけのときは、各サブコマンド実装を直接読む。
- CLI から呼ばれる実装関数の内部エラー生成、ドメインロジック、入出力ファイルの内容を調べたいだけのときは、この入口ではなく委譲先を読む。
- Typer や Click の一般的な使い方、または cmoc 外のパッケージ設定だけを調べたいときは、この対象を読む優先度は低い。

## hash
- 8e9205551785f5e63cb72c666b12049b600ee51d0e204d4198c7d568ba55a7a3

# `sub_commands`

## Summary
- cmoc の主要サブコマンド実行本体を収める領域。初期化、indexing、TUI、session lifecycle、apply lifecycle、review oracle などを CLI runtime 経由で起動し、事前条件検査、branch/worktree/state 操作、Codex 呼び出し、report 出力、利用者向け標準出力までを各サブコマンド単位で結びつける。
- 下位には、session の fork/join/abandon、apply の fork/join/abandon と process/report 補助、review oracle の対象列挙・finding loop・INDEX 反映・report 生成が分かれており、サブコマンド固有の制御フローへ進む入口になる。

## Read this when
- cmoc のサブコマンド実行本体のうち、どの実装へ進むべきかを切り分けたいとき。
- 初期化、indexing、TUI、session、apply、review oracle のいずれかについて、CLI runtime への渡し方、command 名、実行前 preflight、利用者向け出力の流れを確認したいとき。
- session branch と home branch の作成・合流・破棄、session state の更新、merge conflict 解消、branch 削除や rollback の扱いを調べたいとき。
- apply 用 branch/worktree の作成、finding 列挙・適用 loop、編集禁止対象差分の rollback、commit subject 生成、apply run の join・abandon・process 停止・cleanup を確認したいとき。
- apply join での想定外差分検出、force-resolve、INDEX.md conflict の機械解決、merge conflict report、apply fork/join report の生成を追いたいとき。
- review oracle の active session 前提、scope 検証、review worktree 作成、oracle file 対象列挙、finding の enumerate/merge/validate/judge、INDEX.md 変更の commit/merge、review report 出力を確認したいとき。
- TUI の利用者 prompt 編集、エディタ選択、完全 prompt 保存、resolve parameter 結果からの AgentCallParameter 構築、Codex TUI 起動までの流れを調べたいとき。

## Do not read this when
- トップレベル CLI の Typer 登録、サブコマンド名から実装関数への dispatch だけを確認したいときは、CLI entrypoint 側を読む。
- git 実行 wrapper、CLI runtime、path 解決、config/state schema、report directory、timestamp、worktree helper など、複数サブコマンドにまたがる共通基盤の詳細だけが目的のときは、共通 runtime 側を読む。
- Codex に渡す prompt や Structured Output parameter の本文、model/file access mode の選択肢定義だけを調べたいときは、parameter builder や基礎 model 側を読む。
- INDEX.md の文章生成、更新対象探索、lock、commit 処理など indexing 共通処理そのものを調べたいときは、indexing 共通処理側を読む。
- oracle file の正本仕様、サブコマンドの外部仕様、review/apply の期待挙動を仕様として確認したいだけのときは、実装ではなく oracle 側を読む。
- テスト観点、fixture、期待される外部挙動の検証内容を確認したいだけで、サブコマンド本体の制御フローを読む必要がないときは、対応するテスト領域へ進む。

## hash
- 73acd49ea902f1dce2587b05cd78a1bb25aa258c029eb355b020721f3a93cb05
