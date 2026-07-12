# `acp`

## Summary
- `acp` 系の公開入口をまとめる上位領域。`oracle.acp_builder` 側の正本実装へつなぐ互換導線と、配下の機能別入口を読むための分岐点として使う。
- この階層は実装本体ではなく、旧 `acp.*` 参照をどこへ維持するか、どこから実体実装へ進むかを判断するための案内に限定される。

## Read this when
- `acp.*` の旧 import 互換を残す必要があるか、削除できるかを判断したいとき。
- 正本側の実装を保ちながら、この領域がどの機能入口を公開しているかを確認したいとき。
- 互換入口の削除条件や、配下の機能別入口へ進むべきかを選びたいとき。

## Do not read this when
- 正本の実装内容そのものを確認したいときは、ここではなく実体側の領域を読む。
- 個別機能の挙動や内部処理を調べたいときは、上位の互換案内ではなく該当する下位領域を読む。
- `acp.*` 参照がすでに不要かどうかだけを確認済みで、互換導線の詳細が不要なとき。

## hash
- 3681d21e3acf193cc38bf135dd703e4f4882dcd64a572df3d32f6219be206ab9

# `basic`

## Summary
- oracle src 側の基本 API を realization 側の既存公開面から再公開する互換層。ACP 型、path model、構造化文書 API などを複製せず、正本側定義への参照として維持する入口をまとめる。
- 既存の `basic.*` import 経路を残すための領域であり、削除可否は realization 側と利用者向け公開面から対応する互換参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- realization 側で `basic.*` 経由の公開 import 経路や互換維持を確認したいとき。
- oracle src 側の正本定義を複製せず、既存参照へ再公開している箇所を探したいとき。
- ACP 型、path model、構造化文書 API の互換再公開を残す理由、公開名、削除条件を確認したいとき。

## Do not read this when
- ACP 型、path placeholder、構造化文書処理そのものの仕様や実装詳細を確認したいとき。その場合は再公開先の正本側実装を読む。
- `basic.*` 互換参照や公開 import 経路ではなく、一般的な CLI 挙動、テスト挙動、path 変換仕様の検討をしているとき。
- 新しい基本 API や公開面を追加する実装場所を探しているとき。

## hash
- ad0cfb03fb2c682437a55ec2ac464197bd2fc5eb3bb3da22e79f7473d62523e7

# `cmoc_runtime.py`

## Summary
- runtime 実装を別モジュールへ委譲し、既存の import 経路を一時的に維持する互換 shim。公開名と実体の移行期間にだけ意味を持つ。

## Read this when
- runtime module の import 経路、公開 module 名、または互換 alias の残存理由を確認したいとき。
- 呼び出し元を移行した後に、この互換 shim を削除できるか判断するとき。

## Do not read this when
- runtime の具体的な処理内容や責務分割を調べたいとき。この対象は実装本体ではなく委譲だけを扱う。
- 新しい runtime 挙動を追加・変更したいとき。実体側の runtime 実装を読む方が直接的。

## hash
- a36ad0b5d09cbe7d2be546fdafcd27ff3ddaf803744331274a69fb25f15cd7ee

# `commons`

## Summary
- cmoc の実行基盤を横断的に共有する共通 runtime helpers の集約点。設定、git、path、logging、results、state、Codex 実行、Ollama、doctor、apply、indexing などの下位実装を、利用側が一箇所から参照できるように束ねる。
- 個別の振る舞いはここでは定義せず、共通基盤の入口としてどの runtime helper 群へ進むべきかを判断するために読む。

## Read this when
- cmoc 実行時に複数モジュールから共通利用する helper 群の配置や公開入口を確認したいとき。
- 設定、git、path、ログ、state、Codex 実行、preflight、doctor、apply の横断的な共通処理へ進む前に、この領域が shared runtime のまとまりであることを確認したいとき。

## Do not read this when
- 特定 helper の実装、入出力、失敗時挙動を確認したいとき。該当する下位実装を直接読む。
- CLI コマンド固有の手順、画面、ドメイン仕様を調べたいとき。共有 runtime helper ではなく、より直接その責務を持つ対象へ進む。

## hash
- 151719ff188df250513406a2b0c6a5ce6e75fac6db97fd8f278a2fae124f78b2

# `config`

## Summary
- oracle src 側の設定実装を正本に保ちながら、realization 側に残る旧来の `config.*` import を受け止める互換入口をまとめるディレクトリ。
- 設定定義や設定ロジック本体は持たず、正本側の定義を複製せず再公開する境界を確認する入口になる。

## Read this when
- 旧来の `config.*` import が realization 側でどこに受け止められているか確認したいとき。
- 正本側の設定実装を複製せず参照・再公開する互換方針に関わる変更を行うとき。
- 既存の公開参照や互換 import を削除・置換できる条件を判断したいとき。

## Do not read this when
- 設定値の定義、意味、読み込み、検証などの本体挙動を確認したいとき。
- oracle src 側の正本となる設定実装そのものを確認したいとき。
- 互換 import の維持や再公開経路に関係しない設定項目追加・実装変更を行うとき。

## hash
- 97eb1bfd8f73945ab835c22962809b5a59009f2d7e1581a56e7058b6c8c786a4

# `main.py`

## Summary
- Typer ベースの cmoc CLI 入口を定義し、root command と session/apply/review 配下の subcommand を各実装関数へ接続する。
- CLI 引数解析エラーを cmoc のエラーレポート形式に変換する group、補完時の例外処理回避、console script からの起動責務を持つ。
- scope option の公開値や alias command など、利用者が直接触れる command 面の薄い配線を扱う。

## Read this when
- CLI command、subcommand、option、alias、console script 起動の追加・変更・削除を確認したいとき。
- Typer/Click の引数解析エラーが cmoc 形式で表示される経路、または shell completion 時の挙動を確認したいとき。
- CLI 入口からどの sub command 実装へ委譲されるか、scope option が実装へどう渡るかを確認したいとき。

## Do not read this when
- 各 command の実処理、git 操作、worktree 操作、review/apply/session の制御内容を知りたいだけなら、対応する sub command 実装を直接読む。
- cmoc 共通 error 型や error 表示本文の構造を変更したいだけなら、runtime 側の定義を読む。
- oracle や INDEX 更新の仕様本文を確認したいだけなら、仕様文書または該当実装へ進む。

## hash
- e8d8163fd3e7c5f366a20e21707b54b8ee05450bce0e135bf7b3b5493681c4e6

# `oracle.py`

## Summary
- `src` だけを import 対象にした起動時にも、正本側の `oracle` package を解決できるようにする package shim。packaged realization tree の外にある oracle source directory を `__path__` に設定し、見つからない場合は import 失敗として明示する。

## Read this when
- `src` 起点の実行環境で `oracle.*` import を成立させる仕組みを確認したいとき。
- realization code から正本側 oracle module を参照する import 経路や package shim の挙動を調べるとき。
- `oracle package source was not found` という import error の原因を確認するとき。

## Do not read this when
- oracle source の個別 module の仕様や実装内容を確認したいときは、正本側の該当 module を直接読む。
- CLI command、状態管理、入出力処理など cmoc 本体の realization implementation を調べたいときは、それぞれの担当 module を読む。
- oracle file と realization file の定義やパス概念そのものを確認したいときは、対応する正本仕様文書を読む。

## hash
- b6f4097cc1550a057bef77dda6b9e5434b394da2d2831fb96ccbf3d319c4222d

# `sub_commands`

## Summary
- `cmoc` のサブコマンド実装への入口をまとめる階層。`apply`・`doctor`・`eval_oracle`・`indexing`・`review`・`session`・`tui` の各処理に進む前のルーティング地点として使う。
- 個別ファイルは、実行制御・評価委譲・INDEX 更新・review 系・session 系・TUI 起動で責務が分かれているため、作業対象のサブコマンドや処理段階に応じて読む先を絞る。

## Read this when
- `cmoc` のどのサブコマンド実装へ進むべきかを切り分けたいとき。
- `apply`・`doctor`・`eval_oracle`・`indexing`・`review`・`session`・`tui` のうち、対象の実行経路を特定したいとき。
- サブコマンド変更で、開始条件・委譲先・実行順序・状態更新・後始末のどれに触れるかを判断したいとき。

## Do not read this when
- `cmoc` 以外の CLI 群の仕様を知りたいとき。
- 共通の Git 操作や worktree 管理だけを追いたいときは、より下位の共通実装を直接読むべきとき。
- 個別サブコマンドの内部 helper や詳細な処理だけを知りたいときは、この階層ではなく対応する専用ファイルへ進むべきとき。

## hash
- 95462015f25c15ea3cb26f63032ce378d365cafc7128de6d27d5a6ad15c458b5
