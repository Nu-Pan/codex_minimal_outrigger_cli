# `doc`

## Summary
- cmoc の開発規約、設計方針、開発環境、テスト実行およびテスト実装の正本ドキュメント群。実装・テストの変更方針や検証手順を確認する入口。
- cmoc のアプリケーション仕様、状態管理、ブランチ・run 隔離、Codex CLI 呼び出し、ログ、フィードバック、ファイル分類、インデクシング、および各サブコマンドの正本ドキュメント群。利用者向け挙動や実装要件を確認する入口。
- 採用しなかった設計案と、その判断理由を記録した文書群。現行仕様や実装手順ではなく、設計上の背景や代替案を調べるための資料。

## Read this when
- cmoc 全体の仕様、開発規約、運用方針、サブコマンドの挙動を調べるとき。
- 実装やテストの変更前に、対応する正本仕様または開発規約の入口を探すとき。
- 現行仕様ではなく、過去に検討された代替案や設計判断の背景を確認したいとき。

## Do not read this when
- 対象の実装コードやテストコードの具体的な挙動を直接確認する場合。
- 特定の仕様文書やサブコマンド文書がすでに特定できている場合。
- 現行仕様ではなく、単に設計上の代替案の背景だけを確認したい場合は、`considered_alternative` 配下を直接読む方が適切。

## hash
- 53090747d0b04e5b167acb99c2ac2339e10d94483049660bbb5c519b9f66bcef

# `src`

## Summary
- cmoc の oracle 側実装をまとめるディレクトリで、共有モデル、設定、パス解決、構造化文書の生成を扱う。
- agent に渡す完全 prompt と、ファイルアクセス、oracle・realization、routing、INDEX エントリー、feedback などの共通 policy を構築する。
- 各種 agent call のパラメータを定義し、indexing、oracle 編集・調査、realization の適用・リファクタリング、feedback 処理、session join、quota probe などの処理単位を構成する。
- エディタ入力の handoff や外部 feedback 入力など、agent call に付随する入出力処理の定義も提供する。

## Read this when
- oracle 側の共有データモデル、設定、パス placeholder、文書構造の実装を確認するとき。
- agent prompt の組み立て方や、ファイルアクセス・oracle/realization・routing・INDEX entry などの共通規定を確認するとき。
- cmoc の特定操作がどの agent call、prompt、schema、cwd、アクセスモードを使うか確認するとき。
- indexing、oracle 操作、realization 操作、feedback、session join、エディタ handoff の起動定義を確認するとき。

## Do not read this when
- 単一処理の具体的な挙動だけを確認したい場合は、該当する下位の acp_builder・prompt_builder・other ファイルを直接読む。
- 正本仕様や利用者向けの動作説明を確認したい場合は、ここではなく対応する oracle/doc を読む。
- 実際の realization 実装やテストの挙動を確認したい場合は、ここではなく src または test の該当箇所を読む。

## hash
- a4f530a1e12791a0d8c43c55ffa71046b31f0842787ef97dafaae24a8de6339d
