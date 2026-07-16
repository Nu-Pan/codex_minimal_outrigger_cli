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
- cmoc のアプリケーション仕様断片を収める領域。CLI、サブコマンド、実行前処理、session・run の状態境界、ログ、agent call、provider、run isolation、利用手順、Python 実装・CLI・テスト規則などの詳細仕様へ進む入口。
- ACP builder と prompt builder、設定・ルートパス解決、規範文書・構造化 markdown 処理など、agent call と共通実行基盤の正本仕様を扱う領域。個別実装へ進む前に、共通基盤の仕様確認が必要な場合の入口。

## Read this when
- cmoc の CLI 挙動、サブコマンド、実行前処理、状態管理、ログ、agent call、Ollama provider、run isolation の仕様を調べるとき。
- session や run の branch・worktree 境界を確認するとき。
- 採用しなかった設計案、Python 実装、CLI 構成、テストの共通規則を確認するとき。
- agent call のモデル・推論強度・ファイルアクセス・Structured Output・作業ディレクトリ、prompt 構成、設定、パス解決、構造化 markdown 処理を確認するとき。
- 複数の仕様領域から、作業対象に直接関係する下位文書や共通基盤を選ぶ必要があるとき。

## Do not read this when
- INDEX.md の生成・更新規則だけを確認したいとき。
- git、branch、状態ファイルなどの基礎概念だけを確認したいとき。
- 特定仕様の詳細や個別実装が明らかな場合。
- 個別サブコマンドの実行フロー、CLI 入出力、ファイル探索、生成物保存の詳細だけを調べるとき。
- 特定の oracle file や realization file の具体的な仕様・実装だけを確認するとき。
- 採用しなかった設計案だけを確認したいとき。

## hash
- 0278044c1d0548ffb1b36734eab5eae1170a9e372170ef1341d6ac9ca97c4609

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
- cmoc の realization source tree。CLI の最上位入口、サブコマンド、共有 runtime、設定・基本 API の互換 import shim、oracle 名前空間への解決境界を扱い、各下位領域の実装へ進むための入口となる。

## Read this when
- cmoc CLI の起動経路、サブコマンド登録、共有 runtime、互換 import、または oracle 名前空間の解決方法を調査・変更するとき。
- apply、indexing、review、session、TUI などのサブコマンド実装や、それらが利用する共通処理の入口を探すとき。

## Do not read this when
- 特定サブコマンドや runtime helper の詳細を確認したいときは、対応する下位モジュールを直接読む。
- oracle の正本仕様・個別実装、または realization test の内容だけを確認したいとき。

## hash
- c41286120bec57043e6cdb188f552a91dd37fd81c5af7f066129f597999a5bc1

# `test`

## Summary
- テストコードと共通テスト補助を集約するディレクトリ。ACP builder、CLI サブコマンド、Codex runtime、Git/worktree、indexing、oracle review、session/apply state などの外部挙動・制御ロジックを検証する。各機能の回帰テストや関連 fixture・helper を探す入口。

## Read this when
- テストの追加・修正・失敗原因の調査で、対象機能の回帰テストや共通テスト補助を探すとき
- CLI、Codex 実行、indexing、oracle review、session/apply、Git/worktree、設定、Ollama の挙動をテストから確認したいとき

## Do not read this when
- 正本仕様や schema の内容を確認・変更するときは、対応する oracle ファイルを直接読む
- 実装の詳細や単体ロジックを確認するときは、対応する src ファイルを直接読む
- Codex CLI や LLM の出力品質そのものを評価したいとき

## hash
- 41cf128c7fd1834370bea8640f8c5c2375024b108d52dfec053dbcc0b34e779e
