# `acp`

## Summary
- oracle src 側の acp builder 実装を正本に保ちながら、旧来の `acp.*` / `acp.builder.*` import surface を維持する互換領域。
- 実装本体や正本仕様ではなく、canonical 実装への委譲、再公開、薄い wrapper、移行期間中の公開 import 面、削除条件を確認する入口になる。

## Read this when
- 既存の `acp.*` または `acp.builder.*` import path の互換性を確認・維持・削除判断したいとき。
- oracle 側 canonical builder 実装への委譲や再公開が realization 側でどのように保たれているかを調べるとき。
- apply、indexing、quota probe、review、session、TUI などの agent call parameter builder 入口を、旧 import surface から追跡したいとき。
- oracle src 由来の acp builder 互換 import がどこで維持され、どの範囲で公開型や module alias に適合しているか確認したいとき。

## Do not read this when
- acp builder の正本仕様、prompt、parameter 生成内容、canonical 実装の詳細を確認したいときは、対応する oracle 側の本文を読む。
- cmoc の apply、review、session、TUI など各機能全体の実行フローや CLI 処理を調べたいときは、それぞれの上位実装や呼び出し元を読む。
- AgentCallParameter のデータ構造、path model、git helper、INDEX.md 生成仕様など、builder 互換層以外の共通概念を調べたいときは、該当する共通実装や型定義を読む。
- 新しい acp 機能、builder、公開 API を設計したいだけで、既存の `acp.*` / `acp.builder.*` import surface の互換維持に関係しないとき。

## hash
- 932f4d41c84a22cb895f152d1f966c0eef5d207b5fa71ab91ee54d95715b354e

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
- cmoc の実行時共通 helper 群をまとめる領域。Codex 実行、設定、path、git、logging、state、doctor preprocess、INDEX 更新 preflight、Ollama 管理など、複数モジュールから共有される runtime 実装への入口になる。
- 集約 import 用の再公開モジュールと、責務別の runtime 実装モジュールが並び、個別の挙動や失敗時処理は対応する下位要素で確認する。

## Read this when
- cmoc の実行時処理で複数箇所から使う共通 helper、runtime API、永続状態、外部コマンド境界、Codex 実行境界を探すとき。
- Codex exec/TUI、Structured Output、quota/capacity retry、profile、CODEX_HOME、call log、indexing preflight の実装経路を確認したいとき。
- config 読み書き、runtime path、git 操作、doctor preprocess、Ollama 起動確認、subcommand logging、session/apply state の共有実装を確認・変更したいとき。
- runtime API の再公開対象や、呼び出し側が共通 runtime 機能をどの import 入口から参照するかを調べたいとき。

## Do not read this when
- CLI サブコマンド固有の引数、利用者向け workflow、業務処理だけを確認したいときは、該当する command 層や app spec を読む。
- oracle file にある正本仕様断片、prompt builder、path model、config 値の意味そのものを確認したいときは、対応する oracle 側の対象を読む。
- 個別の runtime helper の詳細が既に分かっている場合は、この領域全体ではなく、該当する下位要素を直接読む。
- テスト固有の期待値や外部挙動を確認したいだけのときは、対応する test 側の対象を読む。

## hash
- feea8c1eb5843e60d1486f94920387c3f9d0984b786392da70231e790d24eece

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
- CLI サブコマンド実装を領域別に束ねる階層。apply run、session lifecycle、review oracle、indexing、doctor、TUI、oracle 評価など、利用者向けコマンドの実行入口と orchestration 層へ進むための起点になる。
- 各対象は共通 runtime、git 操作、state、worktree、Codex 呼び出し、report 生成などを必要に応じて接続し、詳細な生成・判定・共通 helper 実装は下位または共通領域へ委譲する。

## Read this when
- CLI サブコマンドの実装入口を探し、どのコマンド領域または下位 module を読むべきか切り分けたいとき。
- apply run、session、review oracle、INDEX maintenance、doctor preprocess、TUI 起動、oracle 評価の実行フローや委譲先を確認または変更したいとき。
- サブコマンド固有の preflight、branch/worktree/state/process/report、失敗時処理、利用者向け出力がどこで束ねられているかを追いたいとき。

## Do not read this when
- CLI runtime、git wrapper、path model、state schema、Codex 実行 wrapper、INDEX 生成ロジックなどの共通処理そのものを調べたいときは、それぞれの共通実装へ直接進む。
- oracle file や realization file の定義、INDEX.md 生成規則、path model などの正本仕様を確認したいときは、対応する oracle doc または oracle src を読む。
- 特定サブコマンド内で対象列挙、prompt builder、report 描画、merge 処理など読むべき下位 module がすでに分かっているときは、その本文へ直接進む。

## hash
- c4a9130e8d8f76ddbb7193910439f5eeebf28090a0c0621f2e0850d481493767
