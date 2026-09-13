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
- cmoc の oracle file に関する正本仕様、開発規約、branch model、設計上の代替案、および oracle 固有の agent call・prompt・パスモデル実装への入口。oracle と realization の責務分離、分類・列挙、oracle 編集／調査、呼び出し設定を担当対象へ切り分けて参照するための文書群。

## Read this when
- oracle file の責務、realization file との適合関係、分類・列挙規則を確認するとき。
- `cmoc oracle edit` や `cmoc oracle investigation` の実行目的、入力、完了条件、agent call の経路を調べるとき。
- oracle 固有の prompt builder、policy、path model、構造化入力、呼び出しパラメータの実装を確認するとき。
- oracle に関する開発・テスト規約、branch model、または採用・不採用となった設計判断を調査するとき。

## Do not read this when
- agent call 全体に共通する設定や prompt 構築だけを調べるときは、上位の共通実装入口を直接読む。
- feedback、realization、session、TUI など別領域の個別仕様や実装だけを確認したいときは、それぞれの対象を直接読む。
- 単一の oracle 文書や単一 builder の詳細な入力・出力・実装挙動だけを確認したいときは、oracle 配下の該当対象を直接読む。
- 機械的なファイル列挙やハッシュ計算だけを行い、oracle の意味仕様や責務分担を必要としないとき。

## hash
- 5d934eadb58979714c51a9c0785f9e0355f01a53eff110b25390887c833e7ca0

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
- src 配下の公開入口、CLI 起動経路、互換 shim、サブコマンド群、共有 runtime の構成を把握するための上位入口。
- トップレベル CLI から各処理領域へ進む際に、下位要素の担当範囲を選ぶための案内を提供する。

## Read this when
- src 配下の公開入口や CLI 階層の構成を最初に確認するとき。
- 個別のサブコマンドや runtime 実装へ進む前に、トップレベルの起動経路と下位領域の境界を判断するとき。

## Do not read this when
- 特定サブコマンドの具体的な挙動や runtime helper の内部実装が明確なときは、対応する下位要素を直接読む。
- 正本仕様、個別 workload の lifecycle、または特定 API の詳細だけを確認したいときは、この上位入口ではなく該当する下位要素や仕様を直接読む。

## hash
- 92c49d88b4920be6b54269aae95d8841e40a6dc5a0bfbe108f00b5e1e8227991

# `test`

## Summary
- test 配下のテスト群を、対象機能ごとの外部契約・回帰条件へ案内するインベントリ入口。CLI、runtime、Codex 実行、indexing、feedback、session、editor、構造化文書など、個別テストへ進む判断材料を提供する。

## Read this when
- テスト対象の外部挙動や回帰条件を調べる際に、まず test 配下のどのテストへ進むべきか判断したいとき。
- CLI・runtime・Codex・indexing・feedback・session・editor など複数領域にまたがる検証範囲や、専用テストへの入口を確認したいとき。

## Do not read this when
- 特定機能の実装仕様や正本仕様そのものを確認したいときは、対応する実装・oracle・仕様文書を直接読む。
- 個別テストの詳細な fixture、期待値、実行手順を確認したいときは、このインベントリではなく該当するテストファイルを直接読む。

## hash
- 1c58e8db67c6f802619fc3adbaf73fe26cbe5db9e7f9d3b106a18b43275a1898
