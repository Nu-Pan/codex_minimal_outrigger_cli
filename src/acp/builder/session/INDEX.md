# `join`

## Summary
- `cmoc session join` で merge conflict marker が検出された後、解消担当 AI エージェントへ渡す呼び出しパラメータを組み立てる領域。
- 解消対象パスを実パスへ解決し、作業範囲、編集禁止事項、oracle file の例外的編集許可、`git add` / `git commit` 禁止を含む complete prompt を生成する。
- 返却するエージェント設定は、主流モデル、中程度 reasoning、conflict 解消用の書き込み権限、生成済み Markdown prompt に固定される。

## Read this when
- `cmoc session join` の merge conflict marker 解消用エージェント呼び出しで、prompt・権限・モデル設定がどう決まるかを確認または変更したいとき。
- conflict 解消対象ファイル一覧、oracle file の例外的編集許可、対象外ファイル編集禁止、`git add` / `git commit` 禁止が prompt にどう埋め込まれるかを追いたいとき。
- conflict 解消対象として渡されたパスが、作業ルートや実パス解決を経て prompt 内の対象一覧になる流れを確認したいとき。

## Do not read this when
- 通常の `cmoc session join` の合流処理全体、git 操作、conflict 検出、join 後の状態更新を調べたいだけのとき。
- complete prompt の共通構築、構造化 Markdown レンダリング、パスモデル、ACP の基礎型そのものを調べたいとき。
- merge conflict の具体的な解消アルゴリズムや、対象ファイル本文の編集方針を探しているとき。

## hash
- 1f946d5dd918f49686c94d756cd73f07f2b173dfbe9da9d3dbace8d5d2590f08
