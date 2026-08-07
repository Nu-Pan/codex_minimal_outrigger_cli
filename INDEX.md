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
- 仮想環境内の Python を検証し、cmoc の Python CLI 本体へ委譲する起動ラッパーを含む。通常実行時のエラー表示、補完プローブ、ユーザー向けパスとコールスタック行番号の組み立てを扱う。cmoc の起動経路やラッパーの表示・エラー処理を確認する際の入口。

## Read this when
- cmoc の起動経路、仮想環境 Python の検証、補完プローブ、ラッパーのエラー出力や表示パスを確認・変更するとき。

## Do not read this when
- Python CLI 本体のコマンド挙動やドメインロジックを調べるときは、委譲先の実装を直接読む。開発環境の正本仕様を確認するときは、参照されている oracle 文書を読む。

## hash
- 2b049993c6378dede2a9d759c9dd13b8795479d1bc900a42c174e227e8ce2e0b

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
- oracle 配下の正本文書・正本ソース・正本テストを収める領域です。cmoc の人間所有の仕様、設計・開発規則、実装仕様や検証基準を確認するための入口で、下位の分野別文書・ソース・テストへ進む起点になります。

## Read this when
- cmoc の挙動、設計、制約、開発・テスト方針の正本を確認するとき
- 実装やテストを変更する前に、それが従うべき人間所有の仕様を特定するとき
- 下位領域のどの正本文書を読むべきか判断するとき

## Do not read this when
- 対象の仕様文書、正本ソース、正本テストがすでに特定でき、その本文を直接読むべきとき
- 現行 realization 実装や realization test の具体的な内容だけを調査するとき
- 通常の実装補助ファイルや作業メモを確認するとき

## hash
- bc44395fa80b13e8bebbea24fc8aaab33f83c5a17b1c6cccb38546936fd90050

# `pyproject.toml`

## Summary
- プロジェクトの Python パッケージ設定。依存関係、開発用依存関係、`cmoc` CLI エントリーポイント、パッケージ配置、pytest・Ruff・mypy の設定を定義する。

## Read this when
- 依存関係や Python バージョン要件を確認するとき
- `cmoc` コマンドのエントリーポイントやパッケージ構成を変更するとき
- pytest、Ruff、mypy のプロジェクト設定を確認・変更するとき

## Do not read this when
- 個別の CLI 処理や実装ロジックを確認するとき
- テストケースや oracle の正本仕様を確認するとき

## hash
- 62c23b5f8693844b19076cbd7c8e2cc4930ace5468300a33c0b5ae87e3886d9f

# `src`

## Summary
- cmoc の realization 実装をまとめるソースツリー。CLI 本体、サブコマンド、共通 runtime、ACP builder、互換 import shim、設定・基本型の公開入口を扱い、各機能の実装へ進むための入口となる。

## Read this when
- cmoc の CLI 構成やサブコマンドの実装入口を確認したいとき。
- 共通 runtime、ACP builder、互換 import path、設定公開経路の責務分担を調査したいとき。
- src 起動時の realization 側 package 構成や下位モジュールへの進み先を判断したいとき。

## Do not read this when
- 特定サブコマンドの詳細な挙動を確認・変更したいときは、対応する sub_commands 配下を直接読む。
- 共通 runtime、ACP builder、basic/config の個別実装を調査したいときは、対応する下位要素を直接読む。
- 正本仕様、oracle 側実装、利用側の具体的な参照を確認したいときは、それぞれの直接の対象を読む。

## hash
- 035d3e095c2a13750d73f70b6fae4813d6e9cc7b0d718e6235939031c311b660

# `test`

## Summary
- cmoc の realization test を集約するテストディレクトリ。CLI、Codex runtime、ACP builder、indexing、oracle review、session/run lifecycle、設定・状態永続化、Git/worktree、prompt、feedback、packaged import など、外部挙動と境界条件を pytest で検証する。各テストファイルが機能領域ごとの具体的な回帰・統合テストへの入口となる。

## Read this when
- cmoc の機能変更に対して、対応する外部契約・回帰テスト・統合テストの所在を特定するとき。
- CLI、Codex 実行、ACP builder、indexing、oracle review、session/run、設定、状態、worktree、feedback などの挙動をテスト観点から確認するとき。
- 共通するテスト fixture、fake command、Git repository、Ollama、Codex 実行環境の支援機能を確認するときは、該当する support module を読む。

## Do not read this when
- 正本仕様、schema、prompt 規範、設計意図そのものを確認・変更するときは、対応する oracle doc・oracle src・oracle schema を直接読む。
- 実装詳細の調査が目的で、テストによる期待挙動の確認が不要なときは、対応する src の実装を直接読む。
- テスト実行方法や品質検査の選択基準だけを確認するときは、repository local のテスト実行ルールを読む。

## hash
- db0ab8ace4d5fc576958f09c07572fe70fc2751f5b5ed191d39bf6f9bd10dd75
