# `doc`

## Summary
- cmoc の自然言語による正本仕様ドキュメント群。ブランチモデル、アプリケーション仕様、開発規約、および採用しなかった設計案の記録を、カテゴリ別の下位文書への入口として提供する。

## Read this when
- cmoc の仕様全体から確認を始めるとき。
- サブコマンド、状態管理、ファイル分類、ログ、フィードバック、開発・テスト規約などの正本ドキュメントを探すとき。
- 現在の仕様に加えて、過去に検討したが採用しなかった設計判断の理由を確認するとき。

## Do not read this when
- 特定の仕様内容が分かっており、該当する下位の Markdown 文書を直接読めるとき。
- 実装コードの具体的な挙動を確認したいとき。
- テストコードや実行成果物を確認したいとき。

## hash
- 503724d55ffb90f47222b9428eacdfd484103d837bf015d41949314fc4ce1d4b

# `src`

## Summary
- cmoc の正本実装を収めるディレクトリで、agent call のパラメータ・パスモデル、入力 handoff、設定・文書参照・構造化文書、prompt の構築と各種 policy を扱う。
- 正本仕様から委譲された正確な実装詳細を確認する入口であり、agent 呼び出し、prompt 生成、ファイルアクセス制約、oracle/realization の扱い、routing や findings の挙動を調べる際に利用する。
- 領域ごとに acp_builder、prompt_builder、other などへ分かれているため、具体的な責務が判明している場合は対応する下位ディレクトリを直接読む。

## Read this when
- oracle の自然言語仕様から委譲された実装詳細を確認したいとき
- agent call の構築、prompt の組み立て、path placeholder、設定モデル、入力 handoff、構造化文書処理の実装を調べたいとき
- realization が参照する正本実装の挙動や、実装と oracle/doc の対応を確認したいとき

## Do not read this when
- 自然言語の意味仕様や要件そのものを確認したいときは oracle/doc を読む
- テストケースや期待結果を確認したいときは oracle/test を読む
- 特定の実装領域が明確な場合は、このディレクトリ全体ではなく該当する下位ディレクトリまたはファイルを直接読む
- 生成・運用側の実装の挙動だけを調べる場合は src を読む

## hash
- da529287cb232b0fbe2a2898ebf478bfc20295ccb546e289563d7fdaee3b9b8b
