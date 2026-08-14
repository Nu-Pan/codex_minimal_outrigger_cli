# `doc`

## Summary
- cmoc の正本仕様・開発ルール・検討記録を横断する oracle 文書群への入口。アプリケーション仕様、branch／commit／worktree モデル、不採用案の背景、実装・環境・テストの開発ルールへ、目的に応じて進むためのルーティング情報を提供する。

## Read this when
- cmoc のアプリケーションレベルの仕様や、複数サブコマンド・共通処理・状態管理の相互参照先を探すとき
- session fork、run の隔離、branch・commit・worktree の責務やライフサイクルを確認するとき
- realization refactor で採用しなかった作業方式や検査方式の理由を確認するとき
- Python 実装、CLI の責務配置、開発環境、テスト要件、テスト実行手順の参照先を判断するとき

## Do not read this when
- 特定の仕様書、開発ルール、テスト実行手順の詳細だけを確認する場合は、該当する個別ファイルまたは下位領域へ直接進む
- realization implementation や realization test の具体的な挙動を調査する場合は、対応する実装・テストまたは専用仕様へ進む
- INDEX.md の生成規則自体を確認する場合は、インデクシング仕様へ直接進む

## hash
- bed96d21f0d82569aef5547c801c33f358ebd6e17f1d2915713eea96bc3398fc

# `src`

## Summary
- cmoc の oracle 実装を構成する下位領域への入口。AI agent 呼び出しのパラメータ・用途別起動定義、feedback 入力の検証と正規化、共通設定・パス・構造化文書モデル、prompt の構築と標準定義を扱う。
- agent call のモデル・推論強度・ファイルアクセス・cwd などの起動パラメータや、oracle/realization の調査・編集・レビュー・適用フローを確認するときは acp_builder へ進む。
- feedback の入力検証・正規化や Structured Output 契約を確認するときは feedback へ進む。
- 設定、モデル指定、パスプレースホルダ、構造化文書、標準の共通モデルを確認するときは other へ進む。
- 完全な prompt の組み立て、prompt 部品、agent 向け標準・アクセス規則・ルーティング規則を確認するときは prompt_builder へ進む。

## Read this when
- oracle 実装の担当領域を特定し、acp_builder、feedback、other、prompt_builder のどこから調査または変更を始めるか判断するとき。
- agent call、feedback、共通モデル、prompt 構築の複数領域にまたがる変更や調査で、下位入口を選ぶとき。

## Do not read this when
- 対象となる下位領域や個別ファイルが明確で、そこへ直接進めるとき。
- oracle の正本仕様、realization の実装、または INDEX.md のルーティング規則そのものを確認するとき。

## hash
- eab64a844e6f21eb6ba0f257e89c743836544ab775cbb7de6c80fbb074e47989
