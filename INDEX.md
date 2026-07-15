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
- cmoc のアプリケーション仕様断片を集約する oracle ディレクトリ。CLI 共通基盤、実行環境、ログ、状態管理、prompt、session/run、branch、設計判断、Python 開発規則などの正本文書と、ACP builder・設定・パス・構造化文書・prompt 合成に関する正本ソースを扱う。doc と src は、機能別の仕様や正本定義へ進むための入口。

## Read this when
- cmoc のアプリケーション仕様や、対象機能の正本文書を探すとき。
- CLI 共通基盤、session/run、branch、設計判断、Python 開発規則など横断的な仕様を確認するとき。
- ACP builder の呼び出し設定、Structured Output 契約、設定・パス・構造化文書モデル、prompt の正本定義を確認するとき。
- 採用仕様だけでなく、不採用案の理由や prompt に組み込まれる規範文面を確認するとき。

## Do not read this when
- 実装コードやテストコードの具体的な挙動を確認するときは、対応する src または test 配下へ進む。
- 対象機能の仕様が明確な場合は、このディレクトリ全体ではなく doc または src 配下の該当する個別ファイルへ直接進む。
- oracle／realization の一般定義・記述標準や INDEX.md の生成・更新規則だけを確認するときは、各専用文書へ進む。

## hash
- 7e65eeaa260bf2336a8eff27fd983223199ebcbcbaa592dec9321076d8d6c786

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
- `src` 配下の実体実装への入口。CLI 本体、共通 runtime、互換公開面、各サブコマンド、正本側 `oracle` への橋渡しをまとめて見分けるためのルーティング層で、まず読むと下位のどの責務へ進むべきかを切り分けられる。

## Read this when
- `src` 全体で、まずどの責務の実装へ進むべきかを判断したいとき。
- CLI 入口、共通 runtime、互換公開面、サブコマンド群、正本側 `oracle` への参照先を整理したいとき。
- 既存の公開名や移行導線を保ったまま、読むべき下位モジュールを絞り込みたいとき。

## Do not read this when
- 個別機能の具体的な挙動やアルゴリズムを知りたいときは、対応する下位モジュールを直接読む。
- 互換入口の存続判断ではなく、特定の実装本体だけを変えたいときはここではない。
- `src` の配下構成ではなく、`oracle` 側の正本仕様そのものを確認したいときは正本側を読む。

## hash
- d0aedd15be6858f6c0c37279e0dff176a3f3770060f321211131c4f2c3110ed1

# `test`

## Summary
- `test/` 配下の回帰・統合テストと、複数テストで共有する補助モジュールを収める。ACP builder、CLI、Codex runtime、apply/session/review oracle、indexing、Git/worktree、設定、権限、Ollama などの外部挙動・制御契約を確認する入口。

## Read this when
- 実装や正本仕様の変更が、対応する CLI・runtime・builder・state・worktree・report・権限・indexing の外部挙動に影響する可能性があるとき。
- 変更対象に対応する個別テスト、または複数テストで共有する `_support` 補助の責務を特定したいとき。
- Codex 実行の retry、quota、subprocess、path、permission、TUI、設定、preflight の回帰を確認するとき。

## Do not read this when
- 正本仕様そのもの、実装内部の詳細、または schema・prompt・state の定義だけを確認したいときは、対応する `oracle/` や `src/` を直接読む。
- 対象が明確に単一のテストファイルまたは補助モジュールに限定されている場合は、このディレクトリ全体を読む必要はない。
- テスト対象と無関係なサブコマンド、runtime 領域、または共通補助の挙動を調べる場合。

## hash
- 72a970071f64afe4ad2878f8a653830ae6a35be67a69168cafae7844e7aa7f6d
