# `acp`

## Summary
- AI エージェント呼び出しに関わる実装をまとめる領域。呼び出しパラメータを組み立てる処理と、その入力になる共通プロンプト部品・標準文書生成処理への入口になる。
- AI に渡す role、summary、goal、補助入力、ファイルアクセス制約、モデル・reasoning、Structured Output schema、標準プロンプト片の組み合わせを扱い、各サブコマンドや処理段階がどの契約で AI を呼び出すかを確認するための階層である。
- 変更要約、実装所見調査・所見対応、INDEX.md エントリー生成、oracle レビュー、merge conflict marker 解消、TUI 実行パラメータ選定など、AI への作業依頼内容と応答形式を追うための上位入口になる。

## Read this when
- cmoc の機能が AI エージェントへ何を依頼し、どの入力・制約・Structured Output schema で呼び出しているかを調べたいとき。
- 個別機能の AgentCallParameter 構築処理と、その前提になる共通プロンプト部品・標準文書生成処理のどちらへ進むべきかを判断したいとき。
- AI 呼び出しに含まれる role、summary、goal、aux_prompt、file access mode、model class、reasoning effort、標準文書参照、応答 schema の対応関係を確認または変更したいとき。
- INDEX.md エントリー生成、oracle review、apply review、merge conflict marker 解消、TUI の権限選定など、AI に渡す依頼文や構造化応答契約を起点に調査したいとき。

## Do not read this when
- サブコマンド登録、CLI 引数解析、実行順序、状態管理、git 操作、ファイルシステム走査、保存、表示など、AI 呼び出し前後の制御フローだけを調べたいとき。
- StructDoc、Standard、Requirement、path model、AgentCallParameter、FileAccessMode など、基礎型やレンダリング処理そのものを確認したいとき。
- oracle file や realization file の本文、標準文書の内容、または実際にレビュー・修正される対象ファイルの仕様や実装を直接読みたいとき。
- AI 応答後の結果集約、適用可否判断、レビュー結果の保存、テスト実行、ユーザー通知などの後続処理だけを調べたいとき。
- 生成済み INDEX.md の描画・更新・保存や、リポジトリ全体のルーティング文書管理だけを確認したいとき。

## hash
- a8fe09742ac81dc210efc2e304618124042366f17226ea2c6fcc90e254cf325b

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
- cmoc の realization implementation のうち、複数の CLI サブコマンドや runtime 層から共有される実行時 helper 群をまとめる領域。Codex 呼び出し、preflight、設定、ファイル内容保存、エラー表示、Git 操作、ログ、パス解決、結果モデル、session state など、上位機能が横断的に利用する基盤処理への入口になる。
- 責務別の runtime 実装に分かれており、集約入口だけでなく、Codex exec/TUI の起動制御、profile 生成、Structured Output 検証、quota/capacity retry、INDEX 更新 preflight、サブコマンド共通 wrapper、JSON Lines event log、永続 state の読み書きなどを個別に追える。

## Read this when
- CLI サブコマンドから共通利用される runtime 処理の実装場所を探すとき。
- Codex CLI 呼び出し、profile・schema・出力 JSON・resume・quota/capacity retry・call log など、cmoc と Codex CLI の境界処理を調査または変更したいとき。
- INDEX.md 更新 preflight、対象探索、既存エントリー検証、hash による鮮度判定、Codex によるエントリー再生成、自動 commit の流れを追いたいとき。
- サブコマンド実行時の共通ライフサイクル、stdout/stderr の扱い、終了コード化、例外表示、runtime event log、quota wait 集計を確認または変更したいとき。
- 設定ファイルの読み書き、内容 hash 保存、binary 判定、Git worktree・branch・ignore 操作、標準 runtime path、session state の JSON 入出力など、複数機能から共有される低レベル helper を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、画面表示、永続データ更新、ファイル生成内容を知りたいだけのとき。その場合はコマンド層や該当機能の実装を読む。
- cmoc の正本仕様断片、path keyword の定義、ログや出力形式の仕様判断を確認したいとき。その場合は oracle 側の該当文書を読む。
- テスト期待値や fixture を確認したいとき。その場合は realization test 側を読む。
- 共有 runtime helper の利用箇所だけを見たいとき。呼び出し元のサブコマンドや上位 module から読み始める方が直接的。
- 特定責務がすでに絞れており、設定、Git、Codex exec、Codex TUI、ログ、パス、state などの個別 module に直接進めるとき。この階層全体を読む必要はない。

## hash
- 87e6998dcb5e2dcd083302138af227655e1516c35390c9e57b7c71a3ff2e8882

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
- CLI サブコマンドごとの実行入口と、各サブコマンド固有の制御フローをまとめる実装領域。共通 CLI runtime に処理を接続し、事前条件検査、worktree/branch/state の操作、Codex 呼び出し、レポート生成、標準出力や終了コードの組み立てをサブコマンド単位で扱う。
- 扱う範囲は、session の開始・取り込み・破棄、apply の実行・取り込み・破棄、oracle review、INDEX.md maintenance、初期化、対話的 TUI 起動である。共通 runtime や schema そのものではなく、それらを利用者操作としてどう組み合わせるかを確認する入口になる。
- apply、session、review のように複数ファイルへ分かれたサブコマンド群では、個別操作の実装へ進むための上位入口にもなる。単体のサブコマンド実装では、runtime wrapper への接続、preflight、実行順序、利用者向け出力を確認する対象になる。

## Read this when
- 利用者が実行するサブコマンドの挙動、実行可能条件、実行順序、標準出力、終了コード、状態遷移、cleanup、rollback を確認・変更したいとき。
- session branch の作成、home branch への merge、merge せず破棄する流れ、または session state と apply state の事前条件をサブコマンド境界から追いたいとき。
- apply run の isolated worktree 作成、finding 適用、commit/report 生成、join 時の想定外差分検出、force-resolve、merge conflict、running process 停止、pid file 管理を調べたいとき。
- review oracle の active session branch 前提、scope 検証、review worktree 作成、対象 oracle 列挙、finding loop、INDEX.md 変更 commit/merge、review report 出力、後片付けの大きな流れを確認したいとき。
- INDEX.md maintenance、cmoc 初期化、または TUI 起動について、共通実装へ渡す前後の preflight、lock、commit、設定同期、prompt 保存、パラメータ解決、Codex CLI/TUI 呼び出しの接続を確認したいとき。
- 各サブコマンドが共通 runtime、git helper、state file、config、Codex parameter builder、report helper をどの地点で呼び出しているかをたどりたいとき。

## Do not read this when
- 共通 CLI runtime、git command wrapper、repo/work root 解決、path model、config schema、state schema、timestamp、report root など、サブコマンドに依存しない基盤の詳細だけを調べたいとき。
- Codex に渡す prompt parameter や Structured Output parameter の本文、AgentCallParameter の汎用構築規則、StructDoc の Markdown レンダリング仕様だけを確認したいとき。
- oracle file の正本仕様、oracle/realization の一般ルール、INDEX.md エントリー生成基準、または review finding の仕様そのものを確認したいとき。
- サブコマンドの外部挙動をテスト観点だけで確認したいときは、対応するテストを読む方が直接的である。
- INDEX.md の内容生成、差分検出、lock、commit、個別ファイル走査など、共通 indexing 実装そのものを調べたいとき。
- パッケージ初期化時の副作用や公開シンボルの有無だけを確認したい場合を除き、具体的なサブコマンド処理を読まずにこの領域全体を読む必要はない。

## hash
- f2dbe99c012cf0e1462ca0a0dd88110776b19a07c6de9e8ad827d5c1438f6160
