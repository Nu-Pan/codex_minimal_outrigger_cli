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
- cmoc の realization implementation のうち、CLI 実行基盤と Codex 呼び出しを支える共有 runtime helper 群をまとめる領域。設定読み書き、内容ハッシュ、エラー表示、git 操作、ログ、パス、実行結果、永続 state、Codex exec/TUI 実行制御、indexing preflight など、複数の上位コマンドから使われる共通処理への入口になる。
- 個別の業務サブコマンドではなく、外部コマンド実行・Codex 呼び出し・状態保存・ログ記録・パス解決・設定管理といった横断的な実行時責務を扱う。集約 import 面と責務別実装の両方を含むため、共通 runtime API の公開面を確認してから下位の具体実装へ進むための起点になる。
- ルーティング文書の自動更新 preflight とエントリー生成制御もこの領域に含まれ、対象列挙、鮮度判定、欠落エントリー生成、Markdown 描画、専用 commit 化など、Codex 実行前に INDEX.md を整える処理の実装入口にもなる。

## Read this when
- CLI サブコマンドの共通ライフサイクル、work root 検査、終了コード化、標準サマリー出力、例外時の利用者向けエラー表示を確認または変更したいとき。
- Codex exec または Codex TUI の起動環境、profile、CODEX_HOME、sandbox/cwd、file access policy、call log、retry、quota/capacity 制御、Structured Output 検証、保護領域書き込み検出を扱うとき。
- cmoc 全体で共有される設定読み書き、内容 hash 保存、binary 判定、git subprocess 境界、linked worktree 操作、ignore 判定、runtime path、timestamp、ログ、実行結果モデル、session state 永続化を調べるとき。
- 上位コマンドから利用する共通 runtime API の import 面を整理し、どの機能群が共有入口から公開されているかを確認したいとき。
- Codex 実行前の indexing preflight、INDEX.md 更新対象の選別、既存エントリーの再利用判定、エントリー生成用 Codex 呼び出し、ルーティング文書更新 commit の流れを確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、CLI 引数定義、利用者向けレポート本文、画面出力の固有仕様だけを調べたいとき。その場合はコマンド層の対象へ進む。
- path keyword や oracle/realization の正本仕様上の定義そのものを確認したいとき。その場合は oracle 側の基本仕様を読む。
- 設定モデル、ACP 型、入力 schema、状態仕様など、データ構造の正本または型定義だけを確認したいとき。その場合はそれぞれの定義を持つ対象へ直接進む。
- Codex CLI 自体の外部仕様、モデル挙動、生成品質、プロンプト本文の意味内容だけを調べたいとき。この領域は cmoc から Codex を呼び出す runtime 境界を扱う。
- 特定ディレクトリ配下で実際にどの本文を読むべきか選びたいだけのとき。この領域の indexing 実装ではなく、その階層のルーティング文書または対象本文を読む方が直接的である。

## hash
- 36299c152110aca5904decd63c07ec32e7c2228ce41bc3bc24bee89a976d041f

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
