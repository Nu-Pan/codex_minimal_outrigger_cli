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
- cmoc の realization implementation のうち、複数のサブコマンドや上位処理から使われる共通 runtime helper 群を収める領域。Codex 呼び出し、設定、内容 hash、CLI 実行 wrapper、エラー表示、Git 操作、runtime log、path、結果型、session state、indexing preflight など、実行基盤の横断機能への入口になる。
- この階層は個別機能の業務ロジックではなく、サブコマンド実装や indexing、Codex 実行経路などが共有する低レベルから中レベルの実行時支援を責務別に分けて扱う。

## Read this when
- サブコマンドや上位 workflow から共通利用される runtime API、結果型、例外表示、ログ、path、Git、設定、状態管理の実装先を探すとき。
- Codex CLI の exec/TUI 呼び出し、profile/schema 準備、quota/capacity retry、resume、Structured Output 検証、call log、preflight の制御を調査または変更するとき。
- INDEX.md 生成 preflight、対象列挙、entry hash 検証、Codex によるエントリー生成、Markdown 描画、更新 commit 条件など indexing の実行経路を確認するとき。
- CLI サブコマンド共通 wrapper の stdout/stderr 契約、終了コード化、work root 検査、サブコマンド event log、開始・完了サマリー、例外の利用者向け表示を確認するとき。
- cmoc が参照する repo/work/cmoc root、.cmoc 配下の標準保存先、timestamp、duration、memo 判定、session state file、run worktree や branch 操作などの共有 runtime 挙動を追うとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、入力解析、出力内容、永続データ更新、ファイル生成内容だけを調べたいとき。その場合はコマンド本体や該当する上位実装へ進む。
- oracle file の正本仕様、path 概念そのもの、INDEX.md の品質基準、ログや CLI 出力の外部仕様だけを確認したいとき。その場合は対応する oracle 側の本文を読む。
- 特定の runtime helper の具体的な入出力、副作用、例外条件だけが目的で、読む対象がすでに分かっているとき。その場合はこの階層全体ではなく責務に対応する本文へ直接進む。
- Typer のコマンド登録、CLI option 宣言、利用者向けサブコマンド構成だけを探しているとき。
- Codex や Git や path を使わない、単一機能内に閉じた realization implementation または realization test の変更を行うとき。

## hash
- e7948d48260fda4076f0e95ae89ea6227e16cb9a73ca398704db6af26dcbc27e

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
- CLI の個別サブコマンド実装を集める領域であり、init、indexing、tui、session、apply、review などの利用者操作を runtime へ接続する入口になる。
- 各サブコマンドは、実行前提の検査、worktree や branch/state の扱い、Codex 呼び出し、report 出力、cleanup などを操作単位に分けて担い、詳細処理は apply・session・review の下位 package や共通 runtime/indexing 実装へ委譲される。
- サブコマンド単位でどの実装へ進むべきかを選ぶための階層であり、apply run、session lifecycle、review oracle、INDEX maintenance、初期化、対話 TUI の入口を切り分ける。

## Read this when
- 利用者が実行する CLI サブコマンドから、どの実装ファイルまたは下位 package に進むべきかを選びたいとき。
- init、indexing、tui、apply、session、review oracle の実行順序、preflight、runtime wrapper、利用者向け出力、失敗時処理の入口を調べ始めるとき。
- session branch、apply worktree、review worktree、一時 branch、state 更新、merge、cleanup、report 生成など、サブコマンド操作に紐づく制御の所在を切り分けたいとき。
- Codex exec callback や TUI 起動、review loop、INDEX 更新など、AI 呼び出しを伴うサブコマンドがどこから共通処理へ接続されるかを確認したいとき。
- CLI の外部挙動を変更する前に、対象サブコマンド固有の orchestration と、共通 runtime・git helper・設定・path model 側へ委譲される責務の境界を把握したいとき。

## Do not read this when
- CLI 全体の parser 構成、command dispatch の共通基盤、repo/work root 解決、git 実行 wrapper、設定読み込みなど、サブコマンド固有でない runtime primitive だけを調べたいとき。
- state schema、path token、branch 名規則、Codex parameter builder、StructDoc、report 保存先 helper など、データ構造や共通 helper の定義そのものを確認したいとき。
- INDEX.md の本文生成、差分検出、lock、commit といった indexing の内部処理だけを調べたいときは、共通 indexing 実装を直接読む。
- apply、session、review の詳細な lifecycle 実装をすでに特定している場合は、それぞれの下位 package または該当モジュールへ直接進む。
- 実装ではなく正本仕様断片、oracle/realization の一般ルール、INDEX.md エントリー生成基準を確認したいときは、oracle 側の文書を読む。

## hash
- 1baefa039ff2bb40c69bbdff29922b754095d4a05ad141cd5851dc157277ca5a
