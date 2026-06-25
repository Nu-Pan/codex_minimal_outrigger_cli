# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出された merge conflict marker の解消を AI エージェントへ依頼するための呼び出しパラメータを組み立てる実装。
- 解消対象パスを実パスへ解決し、作業範囲・禁止事項・例外的に編集可能な oracle file の扱いを含む complete prompt を生成する。
- 返却するエージェント設定は、主流モデル、中程度 reasoning、conflict 解消用の書き込み権限、生成済み Markdown prompt に固定されている。

## Read this when
- `cmoc session join` の conflict marker 解消用エージェント呼び出しで、どの prompt・権限・モデル設定が渡されるかを確認または変更したいとき。
- merge conflict marker 解消時に、対象ファイル一覧、oracle file の例外的編集許可、`git add` / `git commit` 禁止などの作業制約が prompt にどう埋め込まれるかを追いたいとき。
- conflict 解消対象として渡されたパスが、作業ルートや実パス解決を経て prompt 内の対象一覧になる流れを確認したいとき。

## Do not read this when
- 通常の `cmoc session join` の合流処理全体、git 操作、conflict 検出、または join 後の状態更新を調べたいだけのとき。
- complete prompt の共通構築仕様、構造化 Markdown レンダリング、パスモデル、または ACP の基礎型そのものを調べたいとき。
- merge conflict の具体的な解消アルゴリズムや、対象ファイル本文の編集方針を実装として探しているとき。

## hash
- cadb5c60a3f4ce22d84f429857cc2b2b6d482d74588306a76f9cae3b057a19fa
