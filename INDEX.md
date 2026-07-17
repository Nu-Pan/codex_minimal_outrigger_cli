# `AGENTS.md`

## Summary
- cmoc 自己開発時に恒常的に適用するリポジトリ固有の指示を定める補足文書。動的生成プロンプトの権限や作業範囲は変更せず、Python 環境、設計、テストの判断時に参照すべき oracle file への入口を提供する。

## Read this when
- cmoc リポジトリ固有の開発ルールや、動的生成プロンプトとの関係を確認するとき
- Python の実行環境・環境構築・pip の扱いを判断するとき
- realization implementation の配置・責務境界を判断するとき
- realization test の実装・実行・変更後の検証方法を判断するとき

## Do not read this when
- 具体的な Python 環境手順を確認する場合は、直接 development_environment.md を読むとき
- 実装の設計責務を確認する場合は、直接 design_rule.md を読むとき
- テスト手順を確認する場合は、直接 test_rule.md を読むとき
- 動的生成プロンプトで指定された作業範囲や権限を確認する場合

## hash
- b168e9259b1693105309f460d4ef248fd19978f0bae5fab8e1617b0f3aeac112

# `LICENSE`

## Summary
- This file is the repository's license grant and warranty disclaimer. Read it when you need to confirm redistribution rights, attribution obligations, or liability terms for using the project in another codebase or release.
- It is the right place to consult for legal permission questions about copying, modifying, sublicensing, or distributing the software.

## Read this when
- You need to know whether the project can be reused, copied, modified, merged, published, sublicensed, or redistributed.
- You need to confirm whether attribution or the license notice must be preserved in derived or distributed copies.
- You need the warranty and liability terms that apply to use of the software.

## Do not read this when
- You are looking for implementation behavior, CLI usage, configuration, or development workflow.
- You need repository structure or routing guidance; a different `INDEX.md` is the better entry point.
- You need project-specific legal exceptions or additional terms, which would have to be stated in another file.

## hash
- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary
- この文書はリポジトリ全体の入口で、cmoc の概要、初期セットアップ、最初に押さえるべき使い方を短く案内する。新規導入時や、まず全体像と実行開始手順を確認したいときに読む。
- 詳細な運用手順はここではなく、基本ワークフローを定義する正本へ進むための起点として扱う。

## Read this when
- このリポジトリを初めてセットアップするとき。
- cmoc の役割と、最初に何を行うかを短く把握したいとき。
- 基本的な使い方の入口を探していて、詳細仕様へ進む前段階にいるとき。

## Do not read this when
- 個別コマンドの詳細な振る舞いを知りたいだけのときは、該当する仕様文書を直接読む。
- リポジトリ固有の開発ルールや補助規約だけを確認したいときは、この文書ではなくそれらの正本を読む。
- すでにセットアップ済みで、目的の操作手順も分かっているときは再読しなくてよい。

## hash
- e4571c78602bbcf0bc912efbea8f14f9fd0494760f2a334e3affef69cb32741b

# `bin`

## Summary
- `cmoc` の起動ラッパー。仮想環境の Python を確認し、補完要求か通常起動かを切り替えて `src/main.py` へ渡す。

## Read this when
- `cmoc` の実行前提、特に `.venv` の存在確認と、欠落時に出す案内を確認したいとき。
- シェル補完のときだけ別経路で起動する条件を確認したいとき。
- `cmoc` から実際の CLI 実装へどう入るかを追いたいが、各サブコマンドの処理本体までは不要なとき。

## Do not read this when
- 各サブコマンドの引数解釈や業務ロジックを知りたいときは `src/main.py` や該当サブコマンド実装を読む。
- 仮想環境のセットアップ手順そのものや、利用者向けの運用説明だけが目的なら、このラッパーではなく上位の利用案内を読む。

## hash
- ca144e1b915722cdfe8a460aa67f416f69bc3eac2aea5de84869eaa1f907025e

# `codex_minimal_outrigger_cli.code-workspace`

## Summary
- VS Code のワークスペース設定を確認・変更するときに読む。ここには、このリポジトリを開いたときの既定インタプリタ、Python の解析対象、エディタ既定設定、非表示対象の方針がまとまっている。
- 日常的な実装変更やテスト追加では通常読まない。そうした作業は各実装・テスト・関連 `INDEX.md` を優先し、このファイルはエディタ環境やワークスペース構成に関する判断が必要なときだけ参照する。

## Read this when
- このリポジトリを VS Code のワークスペースとして開くとき
- Python の実行環境や解析対象の既定を確認したいとき
- エディタ側でどのファイルを見せるか・隠すかの方針を変えたいとき

## Do not read this when
- アプリケーションの挙動や CLI の仕様を確認したいとき
- 実装やテストの変更先を探したいとき
- 既存の各領域の `INDEX.md` や本文を読むべき作業をしているとき

## hash
- 1938307f70f255710d75d39c07d860ecb381acbb031ca19b2f2b6e565ac41acb

# `oracle`

## Summary
- cmoc の正本仕様と共通実装を収める oracle の入口。アプリケーション仕様は `doc`、ACP builder・prompt builder・設定・パス解決・構造化文書基盤は `src` へ進む。

## Read this when
- cmoc の正本仕様や共通 oracle src の所在を確認するとき。
- アプリケーション仕様と共通基盤のどちらを読むべきか判断するとき。

## Do not read this when
- INDEX.md の自動生成・更新規則だけを確認するとき。
- Python 実行環境、設計ルール、テスト手順などの開発規則だけを確認するとき。
- 対象機能が明らかで、`doc` または `src` の下位対象を直接読めるとき。

## hash
- 157dac4912ece0467ddc624911775416001678918766d5f404ebdab319494417

# `pyproject.toml`

## Summary
- Python プロジェクトのパッケージ metadata、依存関係、CLI エントリポイント、ビルド設定、パッケージ探索、pytest・Ruff・mypy の設定を定義する。プロジェクトの実行・配布・開発ツール設定への入口。

## Read this when
- 依存関係、対応 Python バージョン、`cmoc` CLI のエントリポイント、パッケージ配置やビルド設定を確認・変更するとき
- pytest、Ruff、mypy のプロジェクト共通設定を確認・変更するとき

## Do not read this when
- CLI の具体的な処理や実装を確認するときは `src` 配下を直接読む
- 正本仕様や oracle 側の実装・テストを確認するときは `oracle` 配下を直接読む

## hash
- 41be0de2208bc52d124bffe4dc0a086623184f709aa1d049d18a22ce5601aae2

# `src`

## Summary
- cmoc の realization 実装における Python パッケージ領域。互換 import 入口、共有 runtime、CLI 最上位入口、サブコマンド、正本 oracle への接続を扱い、各機能の実装・公開面・委譲関係を下位要素へ案内する。

## Read this when
- cmoc の realization 側で、CLI 起動経路、サブコマンド登録、互換 import、共有 runtime、または oracle 名前空間への接続先を確認・変更するとき。
- apply、indexing、review、session、TUI、doctor、eval-oracle などの実装入口や担当領域を特定するとき。

## Do not read this when
- 特定機能の詳細な仕様や本体実装だけを確認したいときは、対応する下位モジュールまたは oracle 側を直接読む。
- CLI と無関係な正本仕様、利用者向け手順、個別テストの詳細だけを調べたいとき。

## hash
- 5965be03e4d15e642b989d0947aab8ac47b3b3229d790401e9cf53e8a2919276

# `test`

## Summary
- ACP builder、CLI、Codex runtime、apply/session、indexing、review oracle、doctor、Git/worktree などの pytest テスト群を収録するテスト領域。各テストファイルは対応する機能の外部挙動・制御ロジック・回帰条件を確認する入口となる。

## Read this when
- 対象機能の回帰テスト、外部契約、失敗条件、状態遷移、CLI 統合挙動を確認・変更するとき
- どのテストが特定の runtime、subcommand、ACP builder、indexing、review oracle の挙動を検証するかを探すとき
- 共通テスト補助や packaged layout、実 Codex/Ollama を使う受け入れテストの構成を確認するとき

## Do not read this when
- 正本仕様や prompt・schema の内容自体を確認するときは、対応する oracle 文書・schema・実装を直接読む
- テスト対象の実装詳細だけを追うときは、対応する src ファイルを先に読む
- 対象機能と無関係なテストや、LLM の回答品質そのものを評価するとき

## hash
- aaffcdfaec20f4162fb995b0896af954b464ab9739a6f289b265e52d14d9cf23
