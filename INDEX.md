# `AGENTS.md`

## Summary
- cmoc 自己開発時に、仕様文・agent への指示文・現在の agent への指示文を区別するための注意事項と、agent 向け指示文を単独で理解可能かつ仕様定義を含まない形に保つための基準。

## Read this when
- cmoc 自身のリポジトリを cmoc で開発しており、同じ文面が異なる情報レイヤーに現れる場合の解釈を確認するとき。
- cmoc が呼び出す agent への指示文を作成・確認し、仕様への暗黙の依存や仕様定義の混入を避けるとき。

## Do not read this when
- cmoc の仕様そのものを調べる必要があるとき。
- 具体的な実装、設定、CLI 挙動を確認する必要があり、レイヤー区別や agent 向け指示文の独立性が関係しないとき。

## hash
- da4f29cd7f635f81ead991302bf0b25e687760e47096c1c5efe20318b8c9a8f2

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
- cmoc の正本仕様・開発規則・branch model・設計検討資料と、仕様を実装する oracle 側コード・構造化入力を、文書群と実装群に分けて参照する入口。

## Read this when
- cmoc の現行仕様、開発ルール、branch 関係、または採用しなかった設計案を確認するときは doc 配下へ進む。
- oracle・realization・feedback・indexing・prompt 構築などの正本データ形式や agent call 構築コードを調べるときは src 配下へ進む。
- 仕様とその実装の対応を横断して調査するとき。

## Do not read this when
- 対象の仕様文書、開発規則、設計検討資料、または src 配下の個別モジュールがすでに特定できているとき。
- 実装コード全体ではなく、特定の oracle／realization file の保存内容だけを確認したいとき。

## hash
- 80c46483ee37fc83a4e2332e99156cf9e109ec0903b0a7214679b758eea7a9ea

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
- cmoc の CLI 起動入口とコマンドツリーを構成し、共通 runtime および各サブコマンドへ接続する。
- acp、basic、config、oracle、cmoc_runtime の互換 import 入口と、commons の共通 runtime 実装をまとめる。
- sub_commands 配下に doctor、tui、feedback、indexing、oracle、realization、run、session のサブコマンド実装を配置する。

## Read this when
- cmoc の CLI コマンド構成、起動処理、Typer／Click 境界を確認するときは main.py を読む。
- 互換 import の公開面や oracle 側実装への接続経路を確認するときは acp、basic、config、cmoc_runtime、oracle.py を読む。
- 複数の実行経路で共有される runtime、状態管理、エラー処理、Git、ログ、feedback、report、lifecycle を確認するときは commons を読む。
- サブコマンドの配置や、目的の command 実装への入口を確認するときは sub_commands を読む。

## Do not read this when
- 個別サブコマンドの業務処理や利用者向け仕様だけを確認したいときは、sub_commands 配下の対応する実装を直接読む。
- 互換入口の詳細な API、正本側 oracle 実装、または個別 runtime helper の仕様だけを確認したいときは、対応する下位要素や正本実装を直接読む。
- INDEX.md のルーティング規則や CLI・feedback・editing run の正本仕様を確認したいときは、対応する仕様文書を直接読む。

## hash
- 85418cdb60cae7f34c88d704ef1258e993935ec45637b1aa7d6be34c302aa1e3

# `test`

## Summary
- `test` 配下のテスト群と共有ヘルパーを、実装された外部挙動・runtime 境界・CLI lifecycle・Codex 実行・Git/state・feedback などの回帰検証入口として案内する。
- 個別テストは、対象機能の外部契約や回帰条件を確認するための入口であり、正本仕様・実装詳細・schema 内容そのものは対応する oracle、realization、実装、または schema を直接読む。

## Read this when
- `test` 配下で、共有 fixture/helper、CLI の末端 command と lifecycle、doctor・indexing・TUI・oracle・realization・session・feedback の統合挙動を調査または変更するとき。
- Codex runtime の subprocess、JSONL、quota/retry、path、権限、TUI、process tracking、設定、state、Git ignore、file access、prompt editor、通知などの回帰テスト入口を探すとき。
- 実際の Codex CLI・独立 process・PTY を使う本番経路や、外部から観測できる report・state・Git・call log の受け入れ挙動を確認するとき。
- INDEX 更新、Structured Output builder、prompt rendering、editor input handoff、構造化文書 renderer、skill metadata など、テストで検証される横断的な契約を確認するとき。

## Do not read this when
- 正本仕様、oracle schema、realization 実装、builder 実装、runtime 実装などの内容自体を確認・変更する場合は、対応する正本または実装対象を直接読む。
- 単一サブコマンドや単一 runtime 関数の内部仕様だけを調べる場合で、テストの期待挙動や回帰例を必要としないとき。
- Codex 推論・PTY・独立 process を使う受け入れ試験が不要で、通常の単体テストや個別 fixture の範囲だけを確認するとき。
- `INDEX.md` の構造・hash・ファイル所在など機械的情報だけを確認するとき。

## hash
- db9d29b92a0b7ff33bf500195c63ab46cfc342a51b9c00b5d0b610116afdcacb
