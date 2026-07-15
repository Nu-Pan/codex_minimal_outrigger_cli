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
- cmoc アプリケーション仕様断片と設計・開発規則をまとめる正本文書群への入口。CLI 補完、Codex 呼び出し、ログ、前処理、プロンプト、実行隔離、session 状態、branch/run 境界、サブコマンドなどの仕様を扱う。
- ACP builder、prompt builder、設定・ルートパス解決、規範文書や構造化 markdown を扱う共通 oracle src への入口。

## Read this when
- cmoc の個別機能やサブコマンドの正本仕様を確認・変更するとき。
- CLI 補完、Codex 呼び出し、ログ、前処理、プロンプト生成、実行隔離、session 状態、branch/run 境界を調べるとき。
- agent call のパラメータ、prompt の組み立て、設定、ルートパス、構造化 markdown の検査・レンダリングを確認するとき。
- 個別対象へ進む前に、仕様文書または共通 oracle src の入口を選ぶ必要があるとき。

## Do not read this when
- INDEX.md の自動生成・更新規則だけを確認したいとき。
- リポジトリ全体の共通運用前提だけを確認したいとき。
- 特定文書や実装の詳細が明らかで、個別対象を直接読める単純な作業のとき。
- 個別サブコマンドの実行フローや生成物保存処理だけを調査し、共通基盤を確認する必要がないとき。

## hash
- 56ab59fb93d7b5c88f13da1832c75d3079139818b5bef3e859fbb1ccda00133e

# `pyproject.toml`

## Summary
- プロジェクトの配布・インストール・テスト実行に関わる設定の正本。依存関係、`cmoc` のエントリポイント、`src` と `oracle/src` のパッケージ配置、pytest の import パスを確認・変更したいときに読む。

## Read this when
- 新しい依存を追加・更新したい。
- `cmoc` の起動方法や公開エントリポイントを変えたい。
- `src` / `oracle/src` のパッケージ配置や配布対象を確認したい。
- pytest から `src` と `oracle/src` を import できる前提を変えたい。

## Do not read this when
- 個別の CLI 挙動やサブコマンド仕様を確認したい場合は、各サブコマンド側の文書や実装を先に読む。
- 実装ロジックやテストケースの詳細を追いたい場合は、`src` や `test` の該当ファイルを直接読む。
- 配布メタデータではなく利用手順を知りたい場合は、README を読む。

## hash
- d01948ab1730e2747d529d49d8c8ca10b84bd6a86e19d7b2810ee87c95ccb904

# `src`

## Summary
- cmoc の実装入口をまとめる階層。CLI 起動とサブコマンド接続、共有 runtime、`acp`・`basic`・`config`・`oracle` の互換 import 経路を扱う。
- `commons` は設定・状態・Git・パス・ログ・Codex 実行などの共有 runtime、`sub_commands` は apply・review・session・doctor・TUI・indexing の処理、`acp` と `basic` と `config` は既存公開名を保つ互換入口、`oracle.py` は正本側 namespace への解決入口である。

## Read this when
- cmoc CLI の公開入口、サブコマンド構成、起動時の引数処理を確認したいとき。
- 共有 runtime の責務から、設定・状態・Git・パス・ログ・Codex 実行などの実装先を切り分けたいとき。
- apply、review、session、doctor、TUI、indexing の処理入口を確認したいとき。
- 既存の `acp.*`、`basic.*`、`config.*` import や `oracle` namespace の解決経路を維持・変更したいとき。

## Do not read this when
- 特定のサブコマンドや runtime helper の詳細な入出力・失敗時挙動を調べたいときは、対応する下位モジュールを直接読む。
- `acp`・`basic`・`config` の正本型や機能仕様を確認したいときは、互換入口ではなく `oracle` 側の実体を読む。
- CLI の公開構成ではなく、個別の prompt、report、Git 操作、状態管理の実装詳細だけを確認したいとき。

## hash
- a9dfbd6b69969ac024142303d4666a61f1069beab9508fb0d272d8ba1e238882

# `test`

## Summary
- テスト群を、ACP builder、CLI サブコマンド、Codex runtime、indexing、review oracle、session/apply、共通 runtime などの責務別に整理した検証領域。各テストは対応する実装や正本仕様の外部挙動・制御契約を確認する入口となる。

## Read this when
- 実装または正本仕様を変更し、その外部挙動・状態遷移・エラー処理・公開契約を回帰確認するとき。
- 対象が ACP builder、CLI、Codex 実行、indexing、review oracle、session/apply、runtime、設定、Ollama のいずれかに関係するとき。
- 対応する実装や oracle 文書を確認したうえで、既存の受け入れ条件を調べるとき。

## Do not read this when
- テスト対象と直接関係する実装や oracle file の内容そのものだけを確認したいとき。
- テスト領域に含まれない機能や、内部実装の分割・配置だけを調査するとき。
- Codex CLI や LLM の出力品質自体を評価したいとき。

## hash
- 501aeb8bf5f9c93a331fc7867489d1f955c349587754d3209721f5cde6583ca7
