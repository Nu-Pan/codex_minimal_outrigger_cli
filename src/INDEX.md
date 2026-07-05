# `acp`

## Summary
- ACP builder 互換領域への入口。oracle 側 builder を正本に保ちながら、既存の acp 系 import 経路を維持する互換入口と、agent call parameter 構築に関する用途別の中継・適合境界を束ねる。
- この領域の責務は、正本側実装への委譲、旧公開名前空間の再公開、realization 側公開型への限定的な適合、互換 shim の残存理由と削除条件の確認にある。builder の正本仕様や生成内容そのものはこの領域ではなく oracle 側に置かれる。

## Read this when
- ACP builder 周辺で、旧 import 経路や公開名前空間が oracle 側の正本実装へどう接続されているかを確認したいとき。
- apply fork、quota probe、review、session、TUI などの agent call parameter 構築について、realization 側の互換層、変換境界、fallback、削除条件を調べたいとき。
- 既存の acp 系参照を oracle 側または実体 module へ移行する作業で、互換入口を残す理由、残存参照、canonical 実装への中継先を確認したいとき。
- realization 側または利用者向け公開面に残る acp 系 import の扱いを判断したいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容、builder 正本仕様など、人間意図そのものを確認したいときは、対応する oracle 側の仕様または canonical builder を読む。
- apply、review、session、TUI など各機能の実行フロー、CLI 引数処理、branch 操作、画面構成、quota 管理など、builder 以外の実装詳細を調べたいときは、対象機能の実装へ進む。
- 汎用 git helper、path model、ACP parameter 公開型、file access mode 全体、ログディレクトリ定義など、builder 互換入口以外の共通定義を調べたいときは、それぞれの定義元を読む。
- 新しい acp 機能や API 仕様を追加する場所を探しているとき。この領域は互換維持と正本側への中継が中心であり、機能追加の入口ではない。
- acp 系参照がすでに全公開面と realization 側から消えていることだけを確認済みで、互換入口や削除条件の詳細を読む必要がないとき。

## hash
- cc339a0181d1f27864f4435d3249f64c08d108196048df3f60c68cdd5b1bb454

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
- cmoc の実行時共通機能をまとめる領域。Codex 実行、CLI 共通 runner、config、content hash、doctor preprocess、error、git、logging、path、result、state、apply process、INDEX 更新 preflight など、複数の実装から使われる runtime helper 群への入口になる。
- 共有 runtime API の再公開入口と、個別責務を持つ helper 実装が同じ領域に置かれているため、共通処理の配置先や既存 helper の責務境界を確認する起点になる。

## Read this when
- 複数のサブコマンドや runtime 実装から使う共通 helper の配置先、公開入口、責務分担を確認したいとき。
- Codex exec/TUI 呼び出し、profile、preflight、call log、quota/capacity retry、Structured Output、process tracking など Codex 実行境界の実装を調べたいとき。
- CLI サブコマンド共通の実行ライフサイクル、doctor preprocess、エラー表示、ログ、終了コード変換、完了サマリーを扱う実装を確認したいとき。
- config JSON、session/apply state、git worktree、branch、path、hash、外部コマンド結果など、runtime の永続状態や基盤 helper を確認・変更したいとき。
- INDEX.md の自動更新 preflight、entry の hash 検証、再生成、indexing commit、対象列挙、既存 entry parse の実装を調べたいとき。

## Do not read this when
- 個別サブコマンドの業務処理、引数定義、利用者向け workflow だけを確認したいときは、そのサブコマンド実装へ直接進む。
- oracle file にある正本仕様断片、prompt builder、path model、file access policy、indexing 標準そのものを確認したいときは、対応する oracle 側を読む。
- 特定 helper の細かな入出力や失敗時挙動がすでに分かっている場合は、この領域全体ではなく該当する下位要素の本文を直接読む。
- テスト期待値や外部挙動だけを確認したいときは、対応する realization test または仕様側の対象へ進む。

## hash
- bf5688983dfabce2e65aabf47ba9fe55a41481bef1d0e7bf78035a32d4fa9ce6

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
- Typer を使って cmoc の最上位 CLI と session/apply/review 配下のサブコマンドを定義し、各コマンドを対応する実装関数へ接続する入口。
- 補完時を除く通常の CLI 引数解析エラーを cmoc 形式のエラーレポートへ変換し、console script からアプリを起動する責務も持つ。

## Read this when
- CLI のコマンド構成、サブコマンド名、option 値、alias、または console script 起動経路を確認・変更したいとき。
- CLI 引数解析エラーがどの形式で表示され、どの exit code で終了するかを確認したいとき。
- session/apply/review/indexing/tui/doctor/init 系の CLI 入口から、どの実装関数へ委譲されるかを追いたいとき。

## Do not read this when
- 各サブコマンドの実際の処理内容、branch 操作、review 実行、INDEX 更新処理を調べたいだけなら、対応するサブコマンド実装を直接読む。
- cmoc 共通エラー型やエラー表示の詳細を調べたいだけなら、runtime 側のエラー処理を直接読む。
- oracle review や apply fork の仕様本文を確認したいだけなら、対応する oracle document を読む。

## hash
- 3a536c929d494656041b6c50acfda23036429fd908dc4ab4a2ae71061f613d39

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
- CLI サブコマンドの実行本体をまとめる領域。初期化・修復、index maintenance、TUI、session 操作、apply workflow、review workflow など、利用者向け command を runtime や下位 helper へ接続する入口になる。
- 各 command 固有の preflight、branch/worktree/state/report 制御、cleanup、CLI 表示、共通処理への orchestration を確認するための上位ルーティング対象。

## Read this when
- 特定の CLI サブコマンドの実行本体がどの下位領域または module にあるかを選びたいとき。
- 利用者向け command が runtime、git 操作、state、report、Codex 呼び出し、INDEX maintenance などの共通処理へどう接続されるかを追いたいとき。
- session、apply、review、初期化・修復、indexing、TUI のいずれかに固有の実行条件、状態遷移、cleanup、出力、失敗時挙動を調べる入口を探しているとき。

## Do not read this when
- CLI runtime、git wrapper、path model、state schema、report directory、Codex 実行 wrapper などの共通基盤だけを直接確認したいとき。
- oracle file、realization file、INDEX.md 生成規則、path model などの正本仕様そのものを確認したいとき。
- prompt 文面、Structured Output schema、低レベルの state 読み書き、worktree 操作、INDEX.md 本文生成など、下位の専用 helper が直接担う詳細だけを調べたいとき。

## hash
- e92060d92738616a54c1692f13b07d67629d831b65f0cde1f7e843f8b560c05b
