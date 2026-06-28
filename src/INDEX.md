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
- cmoc の realization implementation のうち、複数の CLI サブコマンドや上位処理から共有される実行時 helper 群を収める領域。Codex 呼び出し、preflight indexing、設定、内容 hash、CLI 実行ライフサイクル、エラー表示、git 操作、ログ、path、結果型、session state など、横断的な runtime 基盤への入口になる。
- この階層には、単一責務の runtime 実装本体に加えて、複数の runtime API を一つの import 面へ集約する入口や、互換 import path を維持する薄い橋渡しも含まれる。

## Read this when
- CLI サブコマンド間で共通利用される runtime API、データ型、エラー、ログ、path、git、設定、状態管理の実装場所を探すとき。
- Codex exec/TUI 呼び出しの起動環境、profile、sandbox、CODEX_HOME、Structured Output、retry、quota/capacity 制御、call log、保護領域書き込み検出を確認または変更したいとき。
- Codex 実行前にルーティング文書を自動更新する preflight、indexing 対象選別、エントリー生成呼び出し、Markdown 描画、専用 commit 作成の流れを追うとき。
- サブコマンドの共通実行フロー、work root 検査、標準サマリー、終了コード化、例外時の利用者向けエラー表示、サブコマンドログの設定を扱うとき。
- 設定ファイル、内容 hash 保存、binary 判定、git worktree/branch 操作、JSON Lines event log、runtime path、実行結果モデル、session state file のような共有基盤の具体実装を読む必要があるとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI 引数定義、画面出力、状態更新の上位フローだけを調べたいとき。その場合はコマンド層の対象へ進む。
- 正本仕様断片、path keyword の概念定義、session state の仕様意図、FileAccessMode の仕様文などを確認したいとき。その場合は oracle 側の該当本文を読む。
- 特定の runtime 領域だけを変更することが分かっているときは、この階層全体ではなく、その責務を持つ下位実装へ直接進む。
- Codex CLI 自体の外部仕様、LLM の出力品質、モデル挙動を知りたいだけのとき。ここは cmoc から Codex を呼び出す runtime 境界を扱う。
- 生成済みログやレポートの解析、個別ルーティング文書エントリーの意味内容、テスト側の期待値だけを確認したいときは、それぞれの読み取り側、対象本文、またはテスト領域へ進む。

## hash
- 094b38c515100f62489a9a58f49375e8c0b405c038ca719f382e054fa4ce453b

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
