# `doc`

## Summary
- cmoc の正本仕様・設計判断・開発ルールを分類して置く上位文書ディレクトリ。
- アプリケーションの共通 lifecycle、実行境界、状態・ログ・feedback、サブコマンド固有契約への入口。
- 不採用となった設計・運用案と採否理由への入口。
- Python 実装、CLI 責務分担、開発環境、テスト規則・実行手順への入口。

## Read this when
- cmoc の仕様、設計判断、または開発ルールについて、どの文書群から確認を始めるか判断するとき。
- アプリケーション挙動、過去の代替案、Python/CLI 開発規約、環境、テスト手順のいずれかを調べるとき。

## Do not read this when
- 単一の実装、テスト、schema、状態データ、または個別文書の具体的内容だけを確認したいとき。
- 特定サブコマンドや個別ルールの詳細を確認するため、文書群全体を読む必要がないとき。
- INDEX.md の生成・更新規則そのものを確認したいとき。

## hash
- 1c302a7e45b505a98c9dac384bb8cbdba48442af21ddc97aa80a6768fd9bbbc8

# `src`

## Summary
- oracle の正本仕様のうち、プログラム・設定ファイルとして記述された詳細を扱う入口。
- agent call 構築、エディタ入力、フィードバック入力、共通モデル、prompt 構築の各領域へ進むための分類点。
- acp_builder は agent call パラメータと起動関連、editor_input_handoff はエディタ入力契約、feedback はフィードバック報告入力、other は設定・パス・構造化文書の共通モデル、prompt_builder は prompt と policy の構築定義を扱う。

## Read this when
- oracle/src 配下で、agent call の構築仕様、エディタ入力の入力契約、フィードバック報告の入力契約、共通モデル、または prompt 構築仕様の読み始める領域を判断するとき。
- 自然言語の意味仕様ではなく、oracle doc から委譲された実装・設定レベルの正確な詳細を確認するとき。

## Do not read this when
- oracle doc が所有する意味仕様や人間意図だけを確認したい場合は、対応する oracle/doc の仕様を直接読む。
- 特定の下位領域の詳細だけを確認したい場合は、acp_builder、editor_input_handoff、feedback、other、または prompt_builder の対象を直接読む。
- 実際の CLI ワークフローや realization の実装挙動だけを確認したい場合は、対応する realization 側の実装を読む。

## hash
- ccada7644a2477e1cbb46ced3efe2830744300a71d664378b085b909f483d087
