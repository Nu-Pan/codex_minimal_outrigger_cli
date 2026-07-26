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
- Codex Minimal Outrigger CLI（cmoc）の概要、初期セットアップ、基本ワークフロー、ターミナルロック対策を案内するプロジェクト入口。詳細な開発指示は AGENTS.md、運用手順は oracle/doc/app_spec/usage.md へ進むための起点。

## Read this when
- cmoc の目的や略称を確認したいとき
- 初期セットアップや PATH 設定の手順を確認したいとき
- 基本ワークフローの参照先を知りたいとき
- Ctrl+S によるターミナルロックを防ぎたいとき

## Do not read this when
- 詳細な開発規約や恒常的なリポジトリ指示を確認したいときは AGENTS.md を読む
- 基本ワークフローの具体的な運用手順を確認したいときは oracle/doc/app_spec/usage.md を直接読む

## hash
- aee9654cfb1c4d0d9aa963e9f03b8a56f4e5b6cdc7aac1ebeeb478b914f88f11

# `bin`

## Summary
- cmoc コマンドの実行ラッパー。仮想環境の Python を検証し、通常実行では CLI 本体へ引数を渡す。仮想環境が使えない場合の案内と、シェル補完プローブ時の実行可能性確認を扱う。

## Read this when
- cmoc の起動経路、仮想環境 Python の検証、起動失敗時のエラー表示、シェル補完プローブの挙動を確認するとき。

## Do not read this when
- cmoc のサブコマンドや CLI 本体の処理内容を確認するときは、CLI 本体の実装を直接読む。
- Python 仮想環境の作成、依存関係、開発環境の正本仕様を確認するときは、対応する oracle ドキュメントを読む。

## hash
- 9a9a99329708cba2a6d2e35d6a087d2b5b3f3a130027abbf4b6a5fa0696e1e35

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
- cmoc の正本仕様ファイルを集約するディレクトリ。CLI 自動補完、Codex CLI 呼び出し、ログ、doctor preprocess、プロンプト、run・session lifecycle、サブコマンドなど、複数機能にまたがる仕様確認の入口を提供する。
- 下位の doc は自然言語による仕様、src は正本ソースを扱う。特定機能の詳細や個別定義を調べる場合は、該当する下位ディレクトリまたはファイルへ進む。

## Read this when
- cmoc の正本仕様を横断的に探すとき
- CLI 起動、Codex CLI 呼び出し、ログ、プロンプト、run・session lifecycle、サブコマンドなどの仕様の入口を確認するとき
- 正本ソースの責務分担や、エージェント呼び出し・設定・パス・構造化文書・プロンプト関連の下位領域を確認するとき

## Do not read this when
- 特定機能の詳細仕様や個別定義が明らかなとき
- realization の実装・テスト詳細だけを調査するとき
- cmoc の一般的な利用手順だけを確認するとき

## hash
- 6877728871b1241f4ff9e1a35daadd176707bd10caacf4aeefb6c43e9b318157

# `pyproject.toml`

## Summary
- プロジェクトの Python パッケージメタデータ、依存関係、CLI エントリーポイント、ビルド設定を定義する設定ファイル。pytest・Ruff・mypy の実行対象や Python バージョン要件も確認できる。

## Read this when
- 依存関係、対応 Python バージョン、`cmoc` コマンドのエントリーポイント、パッケージ探索、ビルド設定を確認するとき。
- pytest・Ruff・mypy のプロジェクト共通設定や GPU integration テストのマーカーを確認するとき。

## Do not read this when
- CLI の具体的な処理や実装責務を確認したいときは、`src` 配下の実装を直接読む。
- 正本仕様や開発環境・テスト手順を確認したいときは、`oracle` 配下の該当文書を読む。

## hash
- b2f7a17a58e3aa7aac375d93ebf50b342e13e74c4e9bc5ba3b6e8fd88b78edd4

# `src`

## Summary
- ACP互換層の公開入口と、`acp.builder.*` の互換入口・realization adapterをまとめるディレクトリ。canonicalなoracle実装への接続や、builder adapterの下位要素へ進む起点となる。
- `basic.*` の互換importを維持する公開入口群。ACP型、path model、構造化文書APIを実体定義から再公開する。
- `commons.cmoc_runtime` の公開名を互換的に再公開する薄いimport shim。`cmoc_runtime`公開名からruntime moduleへ移行するための入口。
- 複数のCLIサブコマンドで共有するruntime helperを集約するcommonsパッケージ。Codex実行、CLI lifecycle、設定、Git/worktree、path、logging、state、error、report、INDEX更新などの共通実行基盤を扱う。
- 設定モジュールの互換入口を提供するディレクトリ。`config.*`参照を成立させ、設定型をrealization側から再公開する。
- Typerを用いたcmoc CLIの主要エントリーポイント。doctor、tui、indexing、session、oracle、realization、runなどのサブコマンドを登録し、対応する実装へ委譲する。
- `src`起動時に正本側`oracle.*`パッケージを解決するための互換用package shim。正本ソースのパッケージパスを再公開する。
- CLIサブコマンド実装をまとめるディレクトリ。doctor、indexing、oracle、realization、run、session、tuiなどの実装への入口を提供する。

## Read this when
- ACP公開名の互換維持、builder adapter、canonical実装への接続、またはprompt補正・workload・command・TUI・session関連の実装を調査するとき。
- `basic.*`経由の公開名や互換import、またはACP型・path model・構造化文書APIの再公開関係を確認するとき。
- `cmoc_runtime`の互換import pathやruntime moduleへの移行状況を確認するとき。
- 複数のCLIサブコマンドにまたがる共通runtime機能、Codex exec/TUI起動、設定、Git/worktree、path、logging、state、error、run lifecycle、report、INDEX更新を調査・変更するとき。
- `config`または`config.cmoc_config`の参照経路や設定型の互換入口を確認するとき。
- cmocのCLIコマンド、サブコマンド、option、Typer/Click引数解析、エラー変換、自動補完、またはCLIからの委譲先を調査・変更するとき。
- `src`起動時の`oracle.*`パッケージ解決や互換importの挙動を確認するとき。
- CLIサブコマンドの実装構成やdoctor、indexing、oracle、realization、run、session、tuiの実行フローを確認・変更するとき。

## Do not read this when
- 個別のbuilder、TUI、session、oracle、realization実装の詳細だけを確認したいときは、対応する下位実体を直接読む。
- 利用側の参照や利用者向け公開面だけを調査するときは、各参照元を直接読む。
- ACP APIの正本仕様や実装本体を確認したいときは、対応するoracle側または実体モジュールを直接読む。
- runtimeの詳細実装や責務別moduleを確認するときは、`commons.cmoc_runtime`または該当runtime moduleを直接読む。
- 設定定義の内容や仕様そのものを確認するときは、oracle側の設定定義を直接読む。
- 個別サブコマンドの処理内容、永続化、worktree操作の詳細を確認するときは、`sub_commands`配下の該当実装を直接読む。
- 正本側`oracle.*`の実装内容を確認するときは、`oracle/src/oracle`配下を直接読む。
- 特定サブコマンドの限定された共通処理や詳細実装だけを確認するときは、該当する下位実装を直接読む。
- applyまたはreviewの具体的な実装を確認するときは、実装追加後に該当箇所を読む。

## hash
- fce6f07b42d6aa5183bab69d1d1b2797387c041fefb300c8e6e41d276959dd14

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。共通テスト支援、ACP builder、Codex runtime、CLI、indexing、oracle review、session、state、設定などの外部挙動・制御ロジックを検証する各テストへの入口となる。

## Read this when
- 複数のサブコマンドや runtime 領域にまたがるテスト対象を探すとき
- 対象機能の realization test の候補を選び、個別テストへ進むとき

## Do not read this when
- 実装の詳細を確認する場合は、対応する src ファイルを直接読む
- 正本仕様や schema の内容を確認する場合は、対応する oracle ファイルを直接読む
- テスト実行手順や共通の開発環境を確認する場合は、対応する開発・テスト手順を直接読む

## hash
- 6ac4e1750dc0abbc17261775a29ebabb9f50e23554965359573f4e552aa48b0d
