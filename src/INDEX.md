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
- cmoc の実行時に複数箇所から共有される runtime helper 群をまとめる領域。
- Codex 実行、設定、INDEX 更新 preflight、CLI 共通 runner、doctor 前処理、git/path/log/error/state など、サブコマンド横断の実行基盤へ進む入口になる。

## Read this when
- CLI サブコマンドや agent call 実装から共有 runtime API、共通 runner、状態管理、ログ、git/path 操作などの担当箇所を探したいとき。
- Codex exec/TUI 起動、profile/sandbox 準備、Structured Output、quota/capacity retry、call log、preflight など Codex 呼び出し周辺の runtime 実装へ進みたいとき。
- INDEX.md 自動更新、doctor preprocess、config 同期、session/apply state、apply process tracking など、複数機能にまたがる共通処理の配置を確認したいとき。

## Do not read this when
- 特定サブコマンド固有の引数、出力、業務処理、利用者 workflow を調べたいときは、そのサブコマンド実装や対応する仕様を直接読む。
- 正本仕様断片、prompt builder、path model、config 型定義など oracle 側の意味や要求を確認したいときは、対応する oracle file を読む。
- テスト固有の期待値や外部挙動だけを確認したいときは、runtime helper 群ではなく該当する realization test を読む。

## hash
- 3ebaed3e97d63f8c0fb217d12dbd43eb869d8d58dfb24a15d3647707b3dce11c

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
- cmoc の Typer ベース CLI 入口を定義し、root command、session/apply/review のサブコマンド、console script からの起動点を各実装関数へ接続する。
- CLI 引数解析エラーを通常実行時だけ cmoc 形式のエラーレポートへ変換し、shell 補完時は Click/Typer の標準処理に委ねる。
- apply fork、review oracle、eval-oracle の scope option 値を Enum で制限し、CLI で受けた値を対応する下位実装へ渡す。

## Read this when
- cmoc のコマンド名、サブコマンド構成、CLI option の公開面、または console script 起動処理を確認・変更したいとき。
- CLI 引数解析失敗時の表示形式、終了コード、補完時の例外処理を調べるとき。
- CLI 入口から各 sub_commands 実装へどの関数・引数が渡るかを確認したいとき。

## Do not read this when
- 各コマンドの具体的な処理内容、branch 操作、worktree 操作、review 実行、INDEX 更新処理を調べたいだけなら、対応する sub_commands 側を直接読む。
- cmoc 共通エラー型やエラー表示の組み立て自体を変更したいだけなら、runtime 側を読む。
- oracle の正本仕様や個別コマンドの仕様根拠を確認したいだけなら、対応する oracle doc を読む。

## hash
- 82896570c7fa80343f5da52a9458525259e99134c10a6d77d1b37d10ef89a0ad

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
- CLI サブコマンド実装をまとめる階層。apply、session、review、indexing、tui、init、doctor、eval oracle などの実行入口と、各 workflow を共通 runtime や下位処理へ接続する orchestration を扱う。
- 各サブコマンド固有の事前条件、状態遷移、委譲先、出力や report 生成への接続を切り分ける入口であり、詳細な生成ロジックや共通基盤の実装は下位または別階層へ進んで確認する。

## Read this when
- CLI サブコマンドごとの実装入口を探し、どの下位処理または共通 runtime へ進むべきか判断したいとき。
- apply run、session 操作、review oracle、INDEX maintenance、TUI 起動、preprocess 委譲など、利用者向けコマンドの実行フローを確認または変更したいとき。
- サブコマンド固有の preflight、branch/worktree/state 操作、report 出力、Codex 呼び出し、commit や merge への接続点を追いたいとき。

## Do not read this when
- CLI 全体の dispatch、Typer app 登録、共通 runtime、git wrapper、path model、設定 schema そのものを調べたいときは、それぞれの共通基盤側を読む。
- oracle file や realization file の定義、INDEX.md 生成規則、サブコマンド仕様の正本断片を確認したいときは、対応する oracle 側を読む。
- 特定サブコマンド内で読むべき下位処理がすでに分かっており、対象列挙、review loop、report 描画、INDEX 統合、parameter builder などの詳細だけを確認したいときは、その責務を持つ下位対象へ直接進む。

## hash
- 1bec1c02782b4d234c86a1ba7704f34d2e45021b3a2d0e424fecc84784a3e654
