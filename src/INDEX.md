# `acp`

## Summary
- 旧来の `acp.*` import 面を維持するための realization 側互換入口を扱う階層。oracle 側 acp builder 実装を正本に保ちつつ、再公開 package、薄い adapter、module alias、移行期間中の公開 import path を収める。
- agent call parameter builder 群について、oracle 実装への接続、realization 側公開型への最小変換、互換入口の残存理由や削除条件を確認する起点になる。
- oracle 側 builder を持たない quota 回復確認用のような realization-only の最小 builder も含む。

## Read this when
- `acp.*` または `acp.builder.*` の旧 import path 互換性、再公開入口、module alias、削除条件を確認したいとき。
- apply fork、review、session、TUI、indexing などの agent call parameter builder が oracle 側実装へどう接続されるかを調べるとき。
- oracle 側 builder の生成結果を realization 側公開型や既存 caller 向け import surface にどう適応しているか確認・変更したいとき。
- quota availability probe や quota 回復確認用の最小 agent call parameter builder を確認・変更したいとき。

## Do not read this when
- agent prompt、出力条件、parameter 生成内容などの正本仕様や人間意図を確認したいときは、対応する oracle 側 builder を読む。
- acp builder の実装本体や生成処理そのものを調べたいときは、互換入口ではなく実体 module へ進む。
- apply fork、review、session、TUI など各機能全体の実行フロー、CLI 引数処理、状態操作、画面構成を調べたいときは、それぞれの上位実装や呼び出し元を読む。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort、path model、git helper などの共通型・共通処理そのものを調べたいときは、該当する共通実装を読む。
- 新しい acp 機能や通常の機能実装場所を探しているだけで、既存 import 互換や builder 入口に関係しないときは、対象機能の実装階層へ直接進む。

## hash
- 0217d13bdb1a329a3082db807c50d3888537d232abdbe92e5df3aeca3aa3cbed

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
- Codex 実行、設定、git、path、logging、状態管理、doctor 前処理、INDEX 更新 preflight など、CLI サブコマンド横断の共通処理への入口となる。

## Read this when
- cmoc の実行時共通処理を変更・調査するため、どの runtime helper に進むべきか判断したいとき。
- Codex exec/TUI 実行、profile、quota retry、call log、preflight、Structured Output 検証など Codex 呼び出し基盤に関わる実装を探すとき。
- config、path、git、error、logging、result、state、content hash、doctor preprocess など、複数サブコマンドで共有される runtime 基盤を確認したいとき。
- INDEX.md 自動更新、entry hash 検証、indexing commit、または Codex 呼び出し前の indexing preflight の実装へ進みたいとき。

## Do not read this when
- 個別サブコマンドの引数、出力、業務処理、利用者向け workflow だけを確認したいときは、該当するコマンド実装や app spec を読む。
- 正本仕様断片、自然言語プロンプト、path model、config 型定義など oracle 側の内容そのものを確認したいときは、対応する oracle file を読む。
- 特定 helper の詳細な入出力、失敗時挙動、永続状態、外部コマンド制御をすでに特定できているときは、この領域全体ではなく該当する下位要素を直接読む。

## hash
- 19d3b15e5b4c71d02115ff39d3e2f2df5298ce64a9049c941c587de19be77bdc

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
- CLI の利用者向けサブコマンド実装をまとめる階層。session、apply、review、indexing、TUI、init、doctor、oracle 評価などの実行入口を束ねる。
- 各サブコマンド固有の実行制御、runtime や共通 helper への委譲、branch/worktree/state/report などの上位 orchestration を扱う入口として位置づけられる。
- 具体的な挙動はサブコマンド別の下位対象に分かれており、この階層はどの実装領域へ進むべきかを切り分けるための入口になる。

## Read this when
- CLI サブコマンドの実装入口を探し、対象操作に対応する下位対象を選びたいとき。
- session lifecycle、apply run、review oracle、INDEX maintenance、TUI 起動、init/doctor preprocess、oracle 評価のいずれに関わる処理かを切り分けたいとき。
- サブコマンドから CLI runtime、git 操作、worktree/state 管理、Codex 呼び出し、report 生成などの共通処理へどう接続されるかを確認したいとき。
- 利用者向けサブコマンドの事前条件、失敗時挙動、状態更新、branch/worktree 操作、出力や report の入口を確認または変更したいとき。

## Do not read this when
- CLI runtime、git wrapper、path model、session state schema、INDEX 生成ロジック、Codex 実行 wrapper などの共通実装そのものを調べたいときは、それぞれの共通実装へ直接進む。
- oracle file や realization file の定義、INDEX.md 生成規則、path model などの正本仕様を確認したいときは、対応する oracle doc または oracle src を読む。
- 特定サブコマンド内の対象列挙、review loop、report 描画、merge 処理、prompt/schema builder など、読むべき下位対象がすでに分かっているときは、その対象へ直接進む。
- Typer などへのトップレベル command 登録や CLI 全体の dispatch だけを確認したいときは、CLI entrypoint や登録側の実装を読む。

## hash
- c5e25ac55e8182acb0ca9ca39a84bb14a7da15a6475061ed75865865dac01462
