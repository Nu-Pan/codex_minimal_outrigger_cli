# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消時に、AI エージェントへ渡す呼び出しパラメータを構築する領域。
- conflict 対象パスを作業ルート基準の実パスへ解決し、解消対象一覧、編集範囲、禁止事項、oracle file 例外を含む完了用プロンプトを組み立てる。
- 返却する呼び出しパラメータには、mainstream モデル、中程度 reasoning、realization write のファイルアクセスモード、生成済み markdown prompt、編集対象パス集合を設定する。

## Read this when
- `cmoc session join` の conflict marker 解消作業で、AI 呼び出しに渡す role、goal、file access rule、対象ファイル一覧を確認または変更したいとき。
- merge conflict marker 解消時に、oracle file の編集を例外的に許可する条件や、git add / git commit を禁止する制約を確認したいとき。
- conflict 対象パスの解決方法、プロンプトへの対象ファイル一覧の埋め込み方、AgentCallParameter の構成を追いたいとき。

## Do not read this when
- 通常の `cmoc session join` の join 処理全体、branch 操作、merge 実行、conflict 検出の流れを調べたいだけのとき。
- merge conflict marker の実際の解消アルゴリズムや、対象ファイル本文をどう編集するかを調べたいとき。
- 汎用的なプロンプト構築部品、markdown rendering、パスモデルの詳細仕様を調べたいとき。

## hash
- b050422df4bfe54a741aaf35e8b86dc75747466de5d590917394b6a16fa4d607
