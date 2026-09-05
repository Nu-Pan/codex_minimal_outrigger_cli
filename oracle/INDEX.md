# `doc`

## Summary
- cmoc の正本ドキュメント群を、アプリケーション仕様、開発ルール、設計上の不採用案などの領域別に案内する上位入口。外部挙動、実装・テスト規約、設計判断の背景を確認する際に、適切な下位文書を選ぶために使う。

## Read this when
- cmoc の仕様・開発ルール・設計判断に関する文書群から、調査対象の領域や下位文書を特定するとき
- CLI の挙動、session・run の管理、Python 実装、テスト、環境構築、または過去の代替案のどの文書を読むべきか判断するとき

## Do not read this when
- 特定の仕様、実装規約、テスト手順、設計案の本文を確認したい場合は、ここで領域を絞った後に該当する下位文書を直接読む
- 実装・テストの具体的なコードや状態ファイルの内容だけを調べる場合は、対応する realization または state ファイルを直接読む

## hash
- fbabaebc9593c9e5cb51b459913b55d4ad02def9c58e6421d01f22bd6f1de62e

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
