# `acp`

## Summary
- oracle src 側の acp builder 実装を複製せず、既存の `acp.*` と `acp.builder.*` import 参照を維持するための互換入口を担う。
- builder 配下の旧 import path、再公開 shim、module alias、fallback、削除条件を確認し、canonical oracle builder や realization 側 adapter への中継関係を判断する入口になる。

## Read this when
- `acp.*` または `acp.builder.*` の旧 import 経路互換、公開 import 面、oracle 側 builder への委譲関係を確認したいとき。
- apply fork、review oracle、session、TUI、indexing、quota probe の agent call parameter builder について、realization 側の互換境界や adapter の残存理由を調べたいとき。
- 正本 builder 追加後または旧参照移行後に、互換入口・fallback・wrapper を削除できる条件を確認したいとき。

## Do not read this when
- agent prompt、parameter 生成内容、builder 本体の正本仕様や canonical 実装を確認したいときは、oracle 側の該当 builder を直接読む。
- apply、review、session、TUI など各機能の実行フロー、CLI 引数処理、状態操作、画面構成を調べたいときは、それぞれの機能実装へ進む。
- 汎用 AgentCallParameter 型、git helper、path model、quota 判定ロジックそのものを調べたいときは、対象の共通実装や上位 package を読む。

## hash
- c2da7611d9aaefe922c89b414b5338a95aea22ce81bfb17b831cb06bf5147492

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
- Codex 実行、config、content hash、CLI 共通 runner、doctor preprocess、error、git、logging、Ollama、path、result、state、INDEX 更新 preflight など、サブコマンド横断で使う実行時基盤への入口となる。
- 領域直下には、薄い再公開入口と、各 runtime 責務を持つ実装モジュールが配置されている。

## Read this when
- cmoc のサブコマンド横断で使う runtime 共通処理の配置先を探したいとき。
- Codex exec/TUI 起動、profile、preflight、call log、quota retry、Structured Output 検証など Codex 実行基盤を確認したいとき。
- config 読み込み、doctor preprocess、git 操作、path 解決、logging、state file、Ollama 準備などの runtime helper を変更または調査したいとき。
- INDEX.md 自動更新、entry hash 検証、indexing commit、Codex による entry 生成の実装を確認したいとき。
- 複数 runtime モジュールの API をまとめて import する公開入口や再公開対象を確認したいとき。

## Do not read this when
- 個別 CLI サブコマンドの業務処理、引数定義、利用者向け出力だけを調べたい場合は、該当するサブコマンド実装を読む。
- 正本仕様断片、INDEX.md entry 生成プロンプト、path model、config 型の意味、console 表示仕様など oracle 側の定義を確認したい場合は、対応する oracle file を読む。
- 特定 runtime API の詳細が既に分かっている場合は、この領域全体ではなく該当モジュールを直接読む。
- テスト固有の期待値や外部挙動を確認したい場合は、対応する test 側へ進む。

## hash
- 449410780cd77c33de023d3744c831bba803b67c4e92c4ea5991456d69906d40

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
