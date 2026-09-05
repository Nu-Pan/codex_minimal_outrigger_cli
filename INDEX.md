# `AGENTS.md`

## Summary
- cmoc 自己開発で恒常的に適用するリポジトリ固有の補足指示を定義する文書。動的生成プロンプトの権限・作業範囲は変更せず、Python 環境、設計、テスト、テスト実行に関する oracle file の参照先を案内する。

## Read this when
- cmoc リポジトリ自身の開発に関する作業を行うとき
- Python 環境や依存関係、realization implementation、realization test、品質検査の標準参照先を確認するとき
- 動的生成プロンプトとリポジトリ固有指示の関係を確認するとき

## Do not read this when
- 動的生成プロンプトが定める作業範囲・ファイルアクセス・oracle/realization 規則だけを確認したいとき
- 特定の実装やテストの詳細仕様を確認する必要があり、案内された oracle file を直接読むべきとき
- cmoc 自己開発に関係しない一般的な作業を行うとき

## hash
- 89bee9d7c2af278bbd665139abcc639290db77ce14190f9d84c74505d635448d

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
- Codex Minimal Outrigger CLI の概要、初期セットアップ、基本ワークフローへの入口、運用上の注意点を案内するプロジェクトの導入文書。リポジトリを初めて使う場合や開発環境を構築する場合の起点となる。

## Read this when
- プロジェクトの目的や略称を確認したいとき
- 初期セットアップ手順を確認したいとき
- 基本ワークフローの参照先を知りたいとき
- ターミナルロックなどの運用上の注意を確認したいとき

## Do not read this when
- 基本ワークフローの具体的な仕様や操作手順を確認したいときは、リンク先の仕様文書を直接読む
- 恒常的なリポジトリ開発ルールを確認したいときは、開発指示文書を直接読む

## hash
- 6b9b1484c0f145d96180325067b4b8552f696e6ed12e84990ab90ed87d713cb6

# `bin`

## Summary
- cmoc の CLI 起動用シェルラッパー。仮想環境 Python の存在・実行可能性を確認し、通常起動では不足時の標準エラー報告後に `src/main.py` を実行する。補完プローブ時は Python が利用可能な場合のみ転送する。CLI の起動経路、Python 検証、起動失敗時のエラー形式、補完時の挙動を確認・変更するときの入口。

## Read this when
- cmoc コマンドの起動処理や、仮想環境 Python の検証・エラー報告を調査するとき
- シェルラッパーから `src/main.py` への転送条件や、自動補完プローブ時の分岐を変更・確認するとき

## Do not read this when
- CLI の実際の引数処理やアプリケーション動作を調査するときは、直接 `src/main.py` または対応する仕様を読む
- エラー内容の正本仕様や初回セットアップ手順を確認するときは、参照されているエラー処理・開発環境の文書を直接読む

## hash
- 70422bb34b7732bfa99d94d395b5c91f9aba3302293f0edba8366c10e7645dfe

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
- cmoc の正本仕様・設計判断・開発ルールを分類した文書群への上位入口。アプリケーション挙動、代替案の採否、Python/CLI 開発規約、環境、テスト手順を確認するための起点。

## Read this when
- cmoc の仕様・設計判断・開発ルールについて、最初に確認すべき文書群を判断するとき。
- アプリケーションの共通挙動、過去の代替案、Python/CLI 開発、開発環境、テスト手順の正本領域を探すとき。

## Do not read this when
- 単一の実装・テスト・schema・状態データ・個別文書の具体的内容だけを確認したいとき。
- 特定サブコマンドや個別ルールの詳細へ直接進めるとき。
- INDEX.md の生成・更新規則自体を確認したいとき。

## hash
- 49712aacf2eefa8ff73ee52b40e7cac313561336468cf0774bfd79320b571326

# `pyproject.toml`

## Summary
- Pythonプロジェクトのパッケージ metadata、依存関係、CLIエントリーポイント、ビルド・配布設定、およびpytest・Ruff・mypyの開発ツール設定を定義する。

## Read this when
- Pythonのバージョン要件、実行時・開発時依存関係、`cmoc`コマンドのエントリーポイント、パッケージ探索や配布内容を確認するとき。
- pytest、Ruff、mypyの共通設定を確認・変更するとき。

## Do not read this when
- CLIの具体的な処理やランタイム挙動を確認するとき。
- 個別テストの内容やテスト実行手順を確認するとき。

## hash
- 3a783c008041cc5d2791af2abb3cfe1c24d8231f77689b906b36f62158c77455

# `src`

## Summary
- cmoc の CLI 起動入口と、互換 import、共通 runtime、サブコマンド実装を含む src 配下の最上位ルーティング入口。
- main.py によるコマンドツリーと起動時互換処理、oracle.py・cmoc_runtime.py などの互換入口、basic・config・commons・acp・sub_commands の下位構成へ進むための起点。

## Read this when
- cmoc の CLI 全体構成、console script の起動経路、またはトップレベルのコマンド委譲先を確認するとき。
- src 起動時の oracle・runtime・basic・config 互換 import の入口や、共通 runtime とサブコマンド実装の配置を横断して判断するとき。

## Do not read this when
- 特定コマンドの処理、個別 runtime helper、互換 API の定義、acp builder の詳細を確認したい場合は、対応する下位モジュールやパッケージを直接読む。
- 正本 oracle 実装、正本仕様、INDEX.md 生成規則だけを確認したい場合は、src の入口ではなく、それぞれの正本対象を直接読む。

## hash
- 015b7af3c6f4aa0fe08e0501754866974ecc6fc67673c43029013811aef300b2

# `test`

## Summary
- `test` ディレクトリは、cmoc の runtime・CLI・Codex 実行・prompt・Git/worktree・session/run state・feedback・通知などの外部挙動を検証する回帰テスト群と、共有 fixture/helper をまとめたテスト入口です。
- 個別機能の単体契約から、doctor・indexing・oracle・session・editing run の CLI lifecycle、実 Codex/PTY を含む統合経路まで、実装変更時の対応テストを探すための上位ルーティング先です。

## Read this when
- cmoc の実装や正本仕様を変更・検証する際に、対象機能の外部契約を確認するテスト、統合 lifecycle、または共有テスト fixture/helper の入口を探すとき。
- CLI command tree、Codex runtime、indexing、prompt editor、session/run state、feedback、Git/worktree、primary report、Windows toast などの回帰挙動を確認するとき。
- 実 Codex CLI・独立 process・PTY を含む受け入れ経路、または通常の mock/単体テストで検証される境界を確認するとき。

## Do not read this when
- 正本仕様、schema、または実装の責務・内部処理そのものを確認することが目的で、対応する oracle 文書や実装ファイルを直接読むべきとき。
- テスト対象の機能領域が明確で、その個別テストまたは共有 helper に直接進めるとき。
- テスト実行手順や Python 環境の規約だけを確認したいとき。

## hash
- 28d0355ed6f8483af5a751037732f9b74aeeb295ea23f372c8dab01ffb71148c
