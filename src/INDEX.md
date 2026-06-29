# `acp`

## Summary
- ACP 関連の realization implementation をまとめる領域。oracle 側 ACP 実装と互換の import 経路を実行側から成立させる入口であり、実処理の多くは oracle 側実装の再公開または薄い実行時補正として提供される。
- ACP builder 系の agent 呼び出しパラメータ構築、Structured Output schema 参照、prompt 構築、review・apply・session・indexing・TUI 向けの下位構成へ進むための起点になる。

## Read this when
- ACP 名前空間または ACP builder 系を realization implementation 側から import する経路を確認したいとき。
- review、apply、session、indexing、TUI などの ACP builder 領域のうち、どの下位実装へ進むべきかを切り分けたいとき。
- oracle 側 ACP 実装を実行側で再公開している箇所と、実行時契約に合わせて薄く補正している箇所の境界を確認したいとき。
- agent 呼び出しパラメータ、prompt、Structured Output schema、file access mode、model class など、ACP builder 呼び出し前の構築責務を追いたいとき。

## Do not read this when
- CLI コマンドの制御、fork 作成、作業ディレクトリ管理、git 操作、レポート保存など、ACP builder 呼び出し後の実行制御を調べたいとき。
- oracle file の正本仕様断片、path model、review standard など、人間が所有する仕様本文を確認したいとき。
- ACP と無関係な realization implementation、realization test、または補助ファイルの責務を調べたいとき。
- 個別の builder 処理内容や prompt・schema・判定ロジックを直接確認したいときは、この領域全体ではなく目的に対応する下位領域へ進む。

## hash
- 85c334b11f5598d0d753a16cb449a0a2e6a8c759368681151ea848ed0fbfd533

# `basic`

## Summary
- realization implementation 側の basic 領域で、正本側 basic との import 互換入口、正本側定義の再公開口、ACP 実行時に共有する呼び出しパラメータ型をまとめる場所。
- この領域自体の多くは独自ロジックではなく正本側実装への薄い接続を担い、例外的に ACP 呼び出し条件を実行時に受け渡すための型定義を持つ。

## Read this when
- realization implementation 側から basic 概念を import する経路や、正本側 basic との対応関係を確認したいとき。
- path model や構造化ドキュメント関連の公開名が、realization 側で独自実装されているのか正本側から再公開されているのかを切り分けたいとき。
- ACP のモデル区分、推論努力、ファイルアクセスモード、プロンプト、structured output schema path をまとめて渡す実行時パラメータ型を確認・変更したいとき。
- basic パッケージ全体の入口としての意図を確認し、個別の実装本文へ進むか正本側へ進むかを判断したいとき。

## Do not read this when
- path model の root token の意味、path 変換仕様、構造化ドキュメントの型・関数・検証規則など、再公開元の具体的な仕様や実装を確認したいとき。その場合は正本側の該当本文を読む。
- ACP パラメータ値を組み立てるロジック、モデル選択規則、実際のファイルアクセス制御や権限判定を調べたいだけのとき。その場合はそれらの処理を持つ対象へ進む。
- oracle file と realization file の一般定義、編集責任、正本仕様断片としての扱いを確認したいとき。その場合は基本概念を定義する正本仕様断片を読む。
- CLI 挙動、サブコマンド処理、永続状態、テスト観点など basic の import 入口や共有型と直接関係しない実装を調べたいとき。

## hash
- f1bb0596c35f80d43d7d62b5bccab057c120fc799ccda52f6c1e6b8fb0b8b870

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
- cmoc の realization implementation における共有 runtime helper 群をまとめる領域。Codex CLI 呼び出し、preflight indexing、CLI 共通ライフサイクル、設定、内容 hash、git 操作、ログ、パス、実行結果、永続 state、共通エラーなど、複数のサブコマンドや上位処理から使われる基盤処理を扱う。
- この階層は、共通 API の集約入口と責務別 runtime 実装の両方を含み、個別サブコマンド固有の業務ロジックではなく、cmoc 全体で共有される実行時境界・副作用・永続化・外部プロセス連携を読むための入口になる。

## Read this when
- Codex exec/TUI 呼び出し、profile・sandbox・CODEX_HOME・Structured Output・retry・quota/capacity 判定・call log など、Codex CLI との実行時境界を確認または変更したいとき。
- INDEX.md の自動検査・再生成、対象列挙、既存エントリーの鮮度判定、生成 Codex 呼び出し、Markdown rendering、排他 lock、git add/commit までの preflight indexing 処理を調べたいとき。
- CLI サブコマンド共通の開始・完了表示、終了コード化、例外表示、work root 検査、サブコマンド logger 設定、標準サマリー出力を確認または変更したいとき。
- 実行時設定の JSON 読み書き、既定値補完、不正設定の利用者向けエラー化、設定項目の追加・削除・改名に伴う変換処理を扱うとき。
- 内容 SHA-256、内容 hash 付きファイル保存、binary 判定、runtime 生成物や schema/profile などの内容ベース保存処理を確認したいとき。
- git subprocess 実行、clean worktree 条件、cmoc 管理 branch、linked worktree 作成・削除、branch 削除、.cmoc の ignore/exclude 保証を調べたいとき。
- サブコマンド単位の JSON Lines event、step timing、quota 待機時間集計、current logger、Codex 呼び出し完了サマリーなど runtime logging を扱うとき。
- repo/work/root の取得、.cmoc 配下の標準保存先、timestamp・duration formatting、memo 判定、一時的な cwd 変更など、実行時 path helper を確認したいとき。
- 外部コマンド結果や Codex exec 結果を運ぶ共有 result model、または session/apply state file の読み書き・検証・branch 名からの state 解決を調べたいとき。
- cmoc 共通例外と利用者向け Markdown error report の表示構造、next actions、detail、call stack の扱いを確認または変更したいとき。

## Do not read this when
- 個別サブコマンドの引数定義、業務ロジック、画面出力、状態遷移全体を調べたいだけのとき。その場合は対象サブコマンドの実装へ進む。
- 正本仕様断片、path keyword の定義、run isolation、INDEX.md の仕様、session state の仕様意図などを確認したいとき。その場合は対応する oracle 文書または基本層の仕様を読む。
- 設定モデルそのもの、AgentCallParameter、FileAccessMode、CmocError などの型定義だけを確認したいとき。その場合はそれらを定義する基礎モデルへ直接進む。
- 生成済みの特定 INDEX.md 本文、個別ファイルのルーティング文書内容、またはエントリー文章そのものを直したいとき。その場合は対象本文やエントリー生成指示・schema を読む。
- ログ・レポート・状態ファイルの生成物そのものを解析したいとき。この階層は生成・保存・記録の runtime helper が中心であり、生成済みデータの読み取り分析入口ではない。
- 単一の上位機能が共通 helper をどう呼ぶかだけを知りたいとき。共有 runtime 側ではなく、その上位機能の実装から読む方が直接的。

## hash
- 802e9986f62857bb6c47366904dc2548b282b82a302969314bc945e38b14b413

# `config`

## Summary
- 実装側の設定パッケージであり、正本側の設定定義へ互換的に到達するための import 入口を提供する。設定値の実体や読み込み・検証などの処理は持たず、正本側定義の再公開境界を扱う。

## Read this when
- 実装側から設定定義へ到達する import 経路を確認したいとき。
- 設定パッケージが正本側の設定定義を実体として委譲し、互換入口として機能しているか確認したいとき。
- 設定モジュールの公開名、再エクスポート範囲、設定パッケージ入口の責務を確認したいとき。

## Do not read this when
- 個々の設定項目の意味、既定値、制約を確認したいとき。ここは設定定義の実体ではなく、正本側定義への入口だけを扱う。
- 設定値の読み込み、解決、検証、変換、永続化などの処理ロジックを調べたいとき。
- 正本仕様として設定内容そのものを確認したいとき。実体を持つ正本側の定義を直接読む方が適切である。

## hash
- 7a2dcace2fd029ab73ce6de095eae0152577f065ea99bdef28edd0f27aa94095

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

# `oracle.py`

## Summary
- 通常起動時に `src` だけが import path にある場合でも、正本側 `oracle/src/oracle` package を `oracle.*` として解決するための互換 shim。
- realization 側に残る `oracle.*` 再公開入口を個別に複製せず、正本側 package への submodule search path だけを提供する。

## Read this when
- `PYTHONPATH=src` や `bin/cmoc` からの起動直後に、`oracle.other` や `oracle.acp_builder` の import がどう成立するか確認したいとき。
- `src/config`、`src/basic`、`src/acp/builder` の薄い再公開 module が正本側実装へ到達する import 境界を確認・変更するとき。
- oracle src を realization 側へ複製せずに、既存互換 import path を成立させる理由を確認したいとき。

## Do not read this when
- 個別の正本仕様断片、prompt builder、設定定義、path model、ACP builder の本文を確認したいとき。その場合は `oracle/src/oracle` 配下の該当本文を読む。
- CLI サブコマンドや runtime helper の実処理を調べたいとき。この対象は import 境界だけを扱う。
- apply fork の個別 prompt 構築や AgentCallParameter の値を確認したいときは、該当 builder を直接読む。

## hash
- b6f4097cc1550a057bef77dda6b9e5434b394da2d2831fb96ccbf3d319c4222d

# `sub_commands`

## Summary
- cmoc の利用者向けサブコマンド実装をまとめる階層で、初期化、indexing、TUI、session、apply、review などの CLI 操作入口を扱う。
- 各対象は CLI runtime への接続、実行前条件、状態・branch・worktree 操作、Codex 呼び出し、利用者向け出力や report 生成など、サブコマンドごとの orchestration へ進むための入口になる。
- 共通 runtime や git wrapper、path model、state 永続化、INDEX.md 生成本体などは別階層へ委譲され、この階層では利用者操作単位の制御境界から読む先を選ぶ。

## Read this when
- 特定の cmoc サブコマンドが CLI から起動された後、どの runtime helper や下位処理へ渡されるかを確認・変更したいとき。
- 初期化、indexing、TUI、session、apply、review の実行条件、preflight、clean worktree 要求、branch/worktree 操作、state 更新、cleanup、利用者向け出力をサブコマンド単位で追いたいとき。
- session branch の作成・破棄・join、apply run の fork・abandon・join、review oracle の対象列挙から report 生成までなど、利用者操作に対応する制御フローの入口を探したいとき。
- サブコマンド実装から、Codex subprocess 実行、INDEX.md maintenance、review loop、report writer、merge conflict 処理などの詳細実装へどこで分岐するかを確認したいとき。
- CLI 全体の登録層ではなく、各サブコマンドが受け持つ実行時副作用や失敗時処理の責務境界を把握したいとき。

## Do not read this when
- Typer app へのサブコマンド登録、トップレベル CLI entrypoint、共通の CLI runtime 規約だけを確認したいとき。
- git 実行 wrapper、path model、config load、state file schema、timestamp、reports directory、cmoc ignore 判定などの共通部品そのものを調べたいとき。
- oracle doc 上のサブコマンド正本仕様や利用者向け要求そのものを確認したいときは、実装階層ではなく oracle 側を読む。
- INDEX.md の文章生成、差分検出、更新対象探索、ルーティング文書規約、Codex prompt builder の詳細だけを調べたいとき。
- 個別サブコマンドのさらに低レベルな処理だけを調べたい場合は、この階層全体ではなく apply、session、review、review_loop、review_index、review_report、review_targets など目的に直結する下位対象へ進む。

## hash
- f98a874160b4b4d24fa9e2d4fef9a44d28f4413fd76047124324c76f095d78cd
