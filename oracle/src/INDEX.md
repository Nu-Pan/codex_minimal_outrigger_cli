# `oracle`

## Summary
- AI エージェント呼び出しのパラメータモデルと、用途別の prompt・Structured Output・アクセスモード・cwd・モデル設定を構築する実装群の入口。
- agent call の共通データ型、indexing・quota probe・session などの起動定義、prompt の統合、パスモデル、設定モデル、構造化 Markdown の処理を扱う。
- 配下の用途別定義や共通モデルへ進む前に、エージェント呼び出し構築全体の責務分担を確認するための対象。

## Read this when
- AI エージェント呼び出しの共通パラメータ、モデル・推論設定、ファイルアクセスモード、cwd、preflight の扱いを調査・変更するとき。
- 用途別 agent call の prompt、Structured Output schema、起動条件を確認するとき。
- 完全 prompt の構築、placeholder、標準規則、routing 規則の統合方法を調査するとき。
- cmoc の設定、agent call 用パスコンテキスト、構造化 Markdown のモデルやレンダリングを確認するとき。
- indexing、quota availability probe、session などの用途別起動定義へ進む入口を判断するとき.

## Do not read this when
- 特定用途の prompt や Structured Output の詳細が明らかで、該当する下位定義を直接確認できるとき。
- 個別の feedback 入力契約や検証処理だけを調査するときは、feedback の対象を直接読む。
- oracle・realization の具体的な処理、通常の session join、または対象ファイルの仕様だけを確認するときは、該当する下位実装や仕様を直接読む。
- Codex CLI の利用可能性確認だけを行うときは、quota probe の定義を直接読む。

## hash
- 43f56f1be4556f2473d5502787d0778aff7676c0f68996d96f20327ad7af96b5
