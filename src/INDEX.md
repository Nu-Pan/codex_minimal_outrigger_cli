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
- cmoc の realization implementation のうち、複数サブコマンドや上位処理から共有される runtime helper 群を集めた領域。Codex CLI 呼び出し、preflight indexing、CLI 実行 wrapper、設定入出力、内容 hash、共通エラー、Git 操作、ログ、runtime path、結果型、session state など、実行時の横断的な支援機能への入口になる。
- この階層は、具体的な業務サブコマンドそのものではなく、サブコマンドや workflow 実装が共通利用する低レベルから中位の runtime API を責務別に分けて保持する。複数領域をまとめて公開する集約入口と、Codex exec/TUI や logging などの責務別実装が同居している。

## Read this when
- cmoc の runtime 共通機能がどの責務に分かれているかを把握し、Codex 実行、設定、Git、path、ログ、状態、エラー処理などの読む先を選びたいとき。
- 新しいサブコマンドや workflow 実装から共有 runtime API を使う、または既存の共通 helper の責務境界や import 面を確認したいとき。
- Codex CLI 呼び出し前後の preflight、exec/TUI 実行、quota/capacity retry、Structured Output、call log、subcommand event など、Codex runtime 周辺の実装へ進む入口を探しているとき。
- CLI サブコマンドの共通ライフサイクル、利用者向けエラー表示、設定ファイル、runtime 生成物の hash 保存、Git worktree/branch 操作、runtime path、session state JSON 入出力など、複数箇所で再利用される実行時基盤を変更・調査するとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI option 定義、入力解析、利用者向けの通常出力だけを調べたいとき。その場合はコマンド層や該当サブコマンド実装へ直接進む。
- パス概念、設定モデル、AgentCallParameter、FileAccessMode などの基本定義や正本仕様断片そのものを確認したいとき。その場合は basic 層または oracle 側の該当本文を読む。
- INDEX.md エントリーの品質基準やルーティング文書の仕様だけを確認したいとき。この階層は生成・更新 runtime は含むが、正本仕様の本文ではない。
- テスト期待値や外部挙動の検証方法だけを確認したいとき。その場合は test 配下の該当 realization test を読む。

## hash
- 411bc7cae97e51fd6ef6577360b8cfaa567f9cd180ae6f7250dba2ef4c25011e

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
- CLI の各サブコマンド実装を集める領域で、session、apply、review、indexing、init、tui などの利用者操作を runtime 上で起動する入口になる。
- 各サブコマンドは共通 runtime、git helper、状態管理、Codex 実行、report 生成、worktree・branch 操作などを組み合わせ、利用者向けコマンド単位の事前条件検査と制御順序を担う。
- サブコマンド固有の詳細は下位 package や module に分かれており、この階層はどの操作の実行入口またはサブ領域へ進むかを選ぶための案内点になる。

## Read this when
- cmoc の利用者向けサブコマンドについて、どの実装または下位領域を読むべきかを選びたいとき。
- session の開始・終了・破棄、apply の fork・join・drop、review oracle、indexing、init、tui など、CLI 操作単位の実行フローや事前条件検査を追いたいとき。
- CLI runtime に渡す command 名、argv、preflight、work root runtime、Codex exec callback など、サブコマンド入口での接続方法を確認・変更したいとき。
- サブコマンド実行に伴う branch/worktree 操作、clean worktree 要求、state 更新、report 出力、cleanup、失敗時 rollback の責務境界を把握したいとき。
- apply、review、session のように下位 module が複数ある機能で、対象列挙、merge、conflict 処理、process 管理、report rendering などの具体処理へどこから入るかを探したいとき。

## Do not read this when
- Typer app へのトップレベル登録、全体の CLI dispatch、共通引数定義だけを調べたいときは、CLI entrypoint や共通 registration 側を読む。
- repo root、work root、path token、git command wrapper、clean worktree 判定、cmoc ignore、report root、lock など、複数機能にまたがる runtime primitive の詳細だけが必要なときは、共通 runtime 側を読む。
- session state や apply state の schema、branch 名規則、設定モデル、Codex prompt builder、Structured Output parameter の定義そのものを確認したいときは、それぞれの model や builder 側を読む。
- INDEX.md の内容生成、oracle file と realization file の一般仕様、ルーティング文書の品質基準を調べたいだけで、サブコマンドの実行時挙動に関心がないとき。
- テスト、fixture、oracle 側の正本仕様断片、または個別 helper の低レベル実装を探しているときは、対応する test、oracle、共通 module を直接読む。

## hash
- 92c75301068b8a84d91d43676ee1bd0587fe7bb6333f09d808169b4b1333313b
