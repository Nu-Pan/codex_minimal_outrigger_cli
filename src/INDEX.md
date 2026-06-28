# `acp`

## Summary
- AI agent 呼び出しに関わる実装をまとめた領域。呼び出し直前に渡すパラメータ構築と、プロンプトを構成する標準文書・規則部品の生成が主な入口になる。
- 対象は、各機能の role、goal、補助入力、ファイルアクセス権限、モデル・reasoning、Structured Output schema の選定と、oracle・realization・review・INDEX.md エントリーなどの標準プロンプト部品である。
- CLI の実行制御や git 操作、ファイル更新、結果の保存・表示そのものではなく、それらの処理が AI agent に依頼する内容と応答契約を組み立てる層を扱う。

## Read this when
- cmoc の機能が AI agent へ何を依頼し、どの制約・標準文書・Structured Output schema を付けて呼び出すかを確認または変更したいとき。
- 変更要約、実装所見調査、所見対応、INDEX.md エントリー生成、oracle レビュー、merge conflict marker 解消、TUI 実行条件選定など、個別の AI 作業依頼のプロンプト設計へ進みたいとき。
- ファイル読み書き制約、INDEX.md ルーティング規則、oracle と realization の基本概念、各種レビュー基準など、AI agent に渡す標準プロンプト部品の生成処理を探したいとき。
- AgentCallParameter に渡る role、summary、goal、aux_prompt、標準参照、file access mode、model class、reasoning effort の対応関係を、処理領域ごとに追いたいとき。

## Do not read this when
- サブコマンド登録、CLI 引数解析、実行順序、状態管理、git branch 操作、merge 実行、ファイルシステム走査や保存など、AI 呼び出し前後の制御フローだけを調べたいとき。
- StructDoc、Markdown rendering、path model、root token、AgentCallParameter、FileAccessMode など、プロンプトや呼び出し条件に埋め込まれる基礎型そのものを確認したいとき。
- oracle file、realization file、テスト、または実際に修正・レビューされる対象ファイルの本文を直接読みたいとき。
- AI 応答後の結果集約、保存、表示、適用可否判断、テスト実行、ユーザー通知、生成済み INDEX.md の描画・更新・保存だけを調べたいとき。

## hash
- c62355f2df833e43f5c3e8ed4d436cc9a0905e98f8227289a5443454bb3bf4bf

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
- cmoc の realization implementation における共有 runtime helper 群をまとめる領域。Codex 実行、設定読み書き、内容 hash、CLI 共通ライフサイクル、エラー表示、Git 操作、ログ、path、結果モデル、永続状態、INDEX.md 自動更新 preflight など、複数の上位 command から再利用される実行時支援を扱う。
- この階層は個別 command の業務ロジックではなく、外部プロセス実行、ファイル配置、ログ記録、例外変換、状態保存などの横断的な実装境界への入口である。集約 import 面と責務別の runtime 実装が並び、共通 API の公開面と実処理の所在を切り分けている。

## Read this when
- cmoc の複数 command から使われる共通 runtime API の所在を探すとき。
- Codex exec/TUI 呼び出し、profile、schema、quota/capacity retry、call log、preflight の制御を確認または変更したいとき。
- CLI サブコマンドの共通実行フロー、標準出力サマリー、終了コード化、例外表示、サブコマンドログ設定を追うとき。
- 設定ファイル、内容 hash 保存、Git worktree/branch/ignore 操作、runtime path、JSON Lines logging、結果データ、session state の読み書きなど、横断 helper の具体実装を探すとき。
- INDEX.md 自動更新の preflight、対象列挙、既存エントリーの hash 検証、Codex によるエントリー生成、更新 commit 作成条件を確認したいとき。
- 上位 command 実装から呼ばれる共通処理の入出力、副作用、失敗時の CmocError 化、ログ記録の責務境界を確認したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、利用者向け業務フロー、状態遷移の高レベル制御だけを調べたいとき。その場合は command 層へ進む。
- cmoc の正本仕様断片、path 概念、oracle/realization の定義、INDEX.md の規範そのものを確認したいとき。その場合は oracle 側の本文を読む。
- 生成済みの INDEX.md やログ、設定、状態ファイルの内容を読むだけで、生成・保存・検証ロジックを追う必要がないとき。
- 単一の helper の詳細だけが必要なことが明確なときは、この階層全体ではなく該当する責務別 runtime 実装へ直接進む。
- テスト期待値や fixture の更新だけを行うとき。ただし共通 runtime の外部挙動やエラー条件を確認する必要がある場合は該当実装を読む。

## hash
- c0933dd64dd56a60a77367ef90baf7a734f17d3f6d63bcb55faf57904c8f82d0

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
- cmoc の各サブコマンド実行本体をまとめる実装領域。初期化、INDEX maintenance、TUI 起動、session lifecycle、apply run、review oracle など、利用者操作ごとの CLI runtime 呼び出しとオーケストレーションへ進む入口になる。
- 各サブコマンドは共通 runtime、git 操作、state 更新、Codex 実行、worktree・branch 管理、report 生成などを組み合わせ、操作ごとの事前条件確認、失敗時処理、利用者向け出力を担う。
- session、apply、review oracle のように複数段階の操作を持つ領域では、下位モジュールが対象列挙、実行 loop、merge・cleanup、conflict 処理、report rendering などの具体処理を分担している。

## Read this when
- 特定の cmoc サブコマンドが CLI runtime へどのように接続され、どの command name、argv、preflight、Codex 実行関数を渡しているか確認・変更したいとき。
- init、indexing、tui、session、apply、review oracle の利用者操作について、実行条件、git 操作順序、state 遷移、worktree・branch の扱い、標準出力や report 出力を実装側から追いたいとき。
- session branch の作成・join・abandon、apply branch の fork・join・abandon、review oracle 用 worktree の作成・merge・cleanup など、サブコマンド固有の lifecycle 制御を調べたいとき。
- apply finding の列挙・適用 loop、編集禁止対象差分の rollback、commit subject 生成、join 時の想定外差分検出や force-resolve、実行中 process の停止補助を確認・変更したいとき。
- review oracle の対象 oracle file 列挙、finding の enumerate/merge/validate/judge loop、INDEX.md 差分だけの commit・merge、review report 生成の呼び出し関係をたどりたいとき。
- TUI の prompt 編集、実行パラメータ解決、完全 prompt 保存、エディタ選択、Markdown 見出しの構造化から Codex TUI 起動までの流れを確認したいとき。

## Do not read this when
- サブコマンドの外部仕様や正本仕様断片だけを確認したいときは、実装ではなく対応する oracle doc を読む。
- トップレベル CLI へのコマンド登録、Typer app 全体の構成、または import 配線だけを確認したいときは、CLI entrypoint や登録側を読む。
- 共通 runtime の path 解決、config 読み込み、git wrapper、state file schema、worktree helper、ログ基盤、clean worktree 判定そのものを調べたいだけのとき。
- Codex に渡す prompt や Structured Output parameter の具体的な組み立てだけを調べたいときは、各 builder 側を読む。
- INDEX.md の本文生成、更新対象探索、lock、commit など indexing 共通処理の詳細を調べたいときは、共通 indexing 実装側を読む。
- session state や apply state のデータモデル、path token の定義、reports directory や timestamp の共通仕様そのものを変更したいだけのとき。

## hash
- 8e8932360d1d8c77732543afba6812dc7e5e4555e2c11f86483f2a02fd2e2169
