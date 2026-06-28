# `acp`

## Summary
- AI エージェント呼び出しに関わる実装領域への入口。呼び出しパラメータを組み立てる処理と、その呼び出しで使う標準プロンプト部品の生成処理を下位に持つ。
- 各機能が AI に何を依頼し、どの role、goal、補助入力、ファイルアクセス権限、モデル設定、Structured Output schema、標準文書を渡すかを追うための上位ルーティングになる。
- 変更要約、レビュー、INDEX.md エントリー生成、merge conflict marker 解消、TUI 実行条件など、AI 作業依頼の呼び出し条件とプロンプト規範の対応を調べる起点になる。

## Read this when
- cmoc の機能が AI エージェントを呼び出す直前に、どのようなパラメータやプロンプト部品を構築しているかを調べたいとき。
- AI 呼び出しの complete prompt、標準プロンプト、aux_prompt、file access mode、model class、reasoning effort、Structured Output schema の関係を追いたいとき。
- 個別の AI 作業依頼そのものの設定を調べるべきか、標準プロンプトや規範文書の生成処理を調べるべきかを切り分けたいとき。
- INDEX.md エントリー生成、oracle review、apply review、merge conflict marker 解消、TUI 向け権限選定など、AI に渡す依頼内容や判断基準の入口を探したいとき。

## Do not read this when
- CLI サブコマンドの登録、引数解析、実行順序、git 操作、ファイル保存、状態管理など、AI 呼び出しの前後にある制御フローだけを調べたいとき。
- oracle file や realization file の本文、実際にレビュー・修正される対象ファイルの仕様や実装を直接確認したいとき。
- AgentCallParameter、FileAccessMode、path model、StructDoc、Markdown rendering など、基礎型や共通文書構築の低レベル実装そのものを確認したいとき。
- AI 応答を受け取った後の結果集約、保存、表示、適用可否判断、テスト実行、ユーザー通知を調べたいとき。
- 生成済みの INDEX.md の保存・描画・更新や、リポジトリ全体のルーティング文書管理だけを確認したいとき。

## hash
- 6e72f37e10d76d7b2eec6a715e92138c2a2c312459c4c0de9f8c81648ceedebc

# `basic`

## Summary
- cmoc の基礎的な実装モデルを集める領域。エージェント呼び出し条件、ルートトークン付きパス、規範文書モデル、構造化文書から Markdown への変換といった、上位機能から共有される小さな中核データ構造と変換処理を扱う。
- 外部コマンド実行、CLI 表示、永続状態、ファイル入出力そのものではなく、それらの前提になる抽象パラメータ、パス表現、文書モデルを確認するための入口となる。

## Read this when
- cmoc 内部で共有される基本的な型、列挙、データ構造、変換 helper の責務を確認したいとき。
- AI コーディングエージェント呼び出しに渡す抽象パラメータ、モデル区分、Reasoning effort、ファイルアクセスモードの表現を確認・変更したいとき。
- ルートトークン表記と絶対パスの相互変換、各 root の検出、git worktree に関わるパス解決を確認・変更したいとき。
- 規範文書を realization code 上で表すモデル、要求項目、判断例、構造化ドキュメントへの変換を確認・変更したいとき。
- 見出し階層、本文、コードブロックを組み立てて Markdown 文字列へレンダリングする小さな文書生成処理を確認・変更したいとき。

## Do not read this when
- CLI コマンドの引数定義、サブコマンド、利用者向け表示、JSON 出力 schema などの公開インターフェースを調べたいとき。
- エージェントプロセスの起動、外部コマンド実行、API 呼び出し、実際のファイル読み書きや永続状態操作を調べたいとき。
- 個別タスクのプロンプト生成内容、Structured Output schema の具体的な中身、生成された Markdown の保存先や利用先を調べたいとき。
- 自然言語で書かれた個別の oracle 規範本文そのもの、または oracle file と realization file の一般定義だけを確認したいとき。
- テストケースの期待値や検証観点だけを確認したいとき。

## hash
- 66bbd3e6c8104062e5f092ec021362cdb2daf050525e0e6fe7b0f72db231c419

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
- cmoc の realization implementation における共有 runtime helper 群の入口となる領域。CLI サブコマンド実行、Codex exec/TUI 呼び出し、preflight indexing、設定、内容 hash、エラー表示、git 操作、ログ、path、結果型、session state 永続化など、複数の上位機能から再利用される共通実行時処理を扱う。
- この階層は個別サブコマンドの業務ロジックではなく、上位処理が共通して使う外部プロセス境界、保存先解決、例外変換、実行結果モデル、監査ログ、状態読み書きなどの基盤を確認するための入口である。

## Read this when
- CLI サブコマンドに共通する実行ライフサイクル、終了コード化、標準出力サマリー、例外時のエラー表示、サブコマンドログ設定を確認または変更したいとき。
- Codex CLI の exec または TUI 呼び出しについて、profile・sandbox・CODEX_HOME・cwd・schema・retry・quota/capacity 制御・call log・保護領域書き込み検出などの runtime 境界を追いたいとき。
- Codex 呼び出し前にルーティング文書を自動更新する preflight、対象列挙、エントリー鮮度判定、欠落エントリー生成、専用 commit 作成の流れを調べたいとき。
- 設定ファイル、内容 hash、binary 判定、git worktree/branch 操作、git ignore 保証、runtime path、timestamp、ログ、結果型、session state file など、複数機能から共有される低層 helper の責務分担を探したいとき。
- 上位のコマンド実装やテストから、共通 runtime API の公開面、互換 import 入口、または既存 helper の再利用先を確認したいとき。

## Do not read this when
- 特定サブコマンドの引数定義、画面出力、業務ロジック、状態遷移全体を調べたいだけのとき。その場合はコマンド層や該当機能の実装へ直接進む。
- path keyword の正本定義、session state などの仕様意図、INDEX.md 生成方針そのものを確認したいとき。その場合は対応する oracle 側の正本仕様断片を読む。
- 個別のルーティング文書エントリー本文を作成・理解したいだけのとき。この階層は自動生成や preflight の実装を含むが、各エントリーの意味内容の正本ではない。
- 外部の Codex CLI 自体の仕様、モデル挙動、出力品質、一般的な subprocess や git の使い方を知りたいだけのとき。ここで扱うのは cmoc runtime へ寄せた境界処理である。
- 単一の上位機能に閉じた保存条件、レポート生成、表示文言、テスト期待値だけを変更したいとき。まずその機能の本文を読み、共通 helper の変更が必要になった場合にこの階層へ戻る。

## hash
- 4ec3262ed9d9f8465a6fddd1543aa2a3208caa74176113adfb148dc94b2bac38

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
- cmoc の各利用者向けサブコマンドを CLI runtime 上で実行するための実装領域であり、初期化、indexing、TUI 起動、session 操作、apply 操作、review oracle 実行の入口をまとめる。
- 各サブコマンドで必要な実行前条件の検査、work root/repository root の選択、session state の確認・更新、branch/worktree 操作、Codex exec/TUI 呼び出し、利用者向け出力や report 生成への接続を扱う。
- 個別コマンド固有の大きな制御は下位 package または補助モジュールに分かれており、この階層はサブコマンド単位で読む先を選ぶための入口になる。

## Read this when
- cmoc のサブコマンド実装がどこから起動され、CLI runtime、preflight、command name、command argv、Codex 実行 callback へどう接続されるかを確認・変更したいとき。
- 初期化、indexing、TUI、session、apply、review oracle のいずれかの利用者向けコマンドについて、実行条件、状態遷移、branch/worktree 操作、成功時出力、失敗時処理の入口を探したいとき。
- session branch の作成・破棄・join、apply 用 worktree での finding 適用と取り込み、review 用 worktree での oracle review と INDEX.md 反映など、サブコマンド横断で CLI 操作の流れを比較したいとき。
- サブコマンドが共通 runtime、indexing 共通処理、prompt builder、report renderer、git helper、設定読み込み、状態ファイル操作へどこから依存しているかをたどりたいとき。
- 利用者が実行するコマンドの外側の配線ではなく、コマンド本体に近い orchestration と、その下位処理への分岐点を確認したいとき。

## Do not read this when
- Typer app へのトップレベル登録、CLI 全体のコマンドツリー構成、entrypoint の import 配線だけを確認したいとき。
- git command wrapper、path model、設定モデル、state file の低レベル読み書き、共通 logging、report directory、timestamp など、サブコマンド固有でない runtime helper の詳細だけを調べたいとき。
- Codex に渡す prompt builder、Structured Output schema、AgentCallParameter の共通仕様、complete prompt 生成など、ACP 構築そのものの詳細だけを確認したいとき。
- oracle file の正本仕様断片、CLI 外部仕様、INDEX.md エントリー生成規約、review や apply の判断基準そのものを確認したいとき。
- 特定の session/apply/review 操作の内部処理だけを調べたいことが既に分かっている場合は、この階層全体ではなく該当する下位 package または補助モジュールへ直接進む。

## hash
- 461f2545a1c9e9286cae4c76c0282f103dabdb4b09dcf066ef46b70df5e8a7b5
