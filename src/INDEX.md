# `acp`

## Summary
- oracle src 側の agent call parameter builder を正本に保ちながら、realization 側で旧来の acp 系 import 互換を維持するための入口階層。実体実装の複製ではなく、canonical builder への委譲、再公開、薄い wrapper、module alias、削除条件の確認に使う。
- apply、review、session、tui、indexing、quota probe などの builder 領域について、既存公開面や realization 側参照を壊さず oracle 側実装へ接続する境界を扱う。

## Read this when
- acp 系 import path を oracle 側 canonical 実装または実体 module へ移行する作業で、互換入口を残す理由、委譲先、削除条件を確認したいとき。
- realization 側または利用者向け公開面に残る acp 系参照について、再公開境界、薄い wrapper、限定補正、runtime 補助処理の扱いを判断したいとき。
- agent call parameter builder の旧 import 互換が、apply、review、session、tui、indexing、quota probe などの領域ごとにどこで維持されているかを追跡したいとき。

## Do not read this when
- agent call parameter の具体的な構築仕様、prompt、出力条件、人間意図を確認したいとき。対応する oracle 側 canonical builder を読む。
- 各機能全体の実行フロー、CLI 引数処理、状態操作、画面構成、git 処理を調べたいとき。それぞれの上位実装または直接の機能実装を読む。
- 公開型、汎用 path model、git helper、oracle file 定義、INDEX.md エントリー生成仕様など、builder import 互換以外の共通概念を調べたいとき。それぞれの共通実装や正本仕様へ進む。
- acp 系参照が全公開面と realization 側から消えていることを確認済みで、互換入口の削除判断や移行経緯を読む必要がないとき。

## hash
- 8a30e62ad6cd17ae3ca589daf06896998e85eb44f41619fe332bbdaa54f7663c

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
- cmoc の実行時に複数箇所から使われる共通 runtime helper 群をまとめる実装領域。
- Codex 実行、INDEX 更新 preflight、CLI 共通 runner、設定読み書き、doctor 前処理、git 操作、ログ、path 解決、Ollama 準備、状態管理、apply process 管理など、サブコマンド横断の基盤処理への入口となる。

## Read this when
- CLI サブコマンドや agent orchestration から共有される runtime 処理の実装場所を探すとき。
- Codex exec/TUI 起動、profile 生成、quota/capacity retry、Structured Output 検証、call log、INDEX 更新 preflight のいずれかを確認・変更したいとき。
- work root 解決、`.cmoc/local` 配下の path、config JSON、session state、subcommand log、git worktree、oracle file 判定などの共通基盤を調べたいとき。
- doctor preprocess、Ollama 自動準備、apply process 追跡、共通エラー表示、外部コマンド結果型など、複数サブコマンドにまたがる補助処理を確認したいとき。

## Do not read this when
- 個別サブコマンドの利用者向け仕様、引数定義、業務処理、出力契約だけを確認したいときは、そのサブコマンド実装または対応する oracle doc を読む。
- runtime helper の正本仕様断片、自然言語プロンプト、Structured Output schema、path keyword の概念定義だけを確認したいときは、oracle 側の該当文書や定義を読む。
- 特定の runtime API の詳細が既に分かっているときは、この領域全体ではなく、対応する下位要素を直接読む。

## hash
- cd541fac8b38642e01730510e2b5f04e6fe4aeca79287e1a457879e3f735f8a5

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
- CLI サブコマンド実装の入口をまとめるディレクトリ。apply、session、review、indexing、tui、init、doctor、eval oracle などの個別コマンド実装へ進むための起点になる。
- 各サブコマンドは、CLI runtime や共通処理への薄い委譲入口、または branch/worktree/state/report などを扱う orchestration 層として分かれている。

## Read this when
- CLI サブコマンドの実装を調べる際に、どのコマンド配下または入口ファイルへ進むべきか切り分けたいとき。
- apply、session、review oracle、indexing、tui など、利用者が呼び出すコマンドから実処理・共通 runtime・下位 helper へどう接続されるかを確認したいとき。
- branch、worktree、state、process、report、INDEX.md 更新、preprocess 委譲など、サブコマンド単位の実行制御の入口を探したいとき。

## Do not read this when
- CLI runtime 共通処理、git wrapper、path model、state schema、Codex 実行 wrapper など、サブコマンド横断の基盤だけを調べたいとき。
- oracle file や realization file の定義、INDEX.md 生成規則、サブコマンド仕様そのものなど、正本仕様断片を確認したいとき。
- 特定サブコマンド内で読むべき下位ファイルがすでに分かっており、その本文へ直接進めるとき。

## hash
- 88d939be3ed0d3bd4612ac3d7dbbb261087bb94e192a6aeca412f76a2fc5fa8c
