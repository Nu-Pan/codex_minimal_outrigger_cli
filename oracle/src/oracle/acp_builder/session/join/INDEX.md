# `conflict_resolution.py`

## Summary
- `cmoc session join` における Git merge conflict 解消用エージェント呼び出しパラメータを構築する関数。対象パスを実体パスへ解決し、conflict 対象を埋め込んだ prompt と、最高品質・リポジトリ書き込み権限・事前 indexing 無効などの起動設定をまとめて返す。

## Read this when
- `cmoc session join` の merge conflict marker 解消処理を変更・調査するとき。
- conflict 解消用 prompt の内容、対象ファイルのパス解決、または AgentCallParameter のモデル・推論・アクセス設定を確認するとき。

## Do not read this when
- 通常の session join 処理や conflict 解消以外の prompt 構築を確認するとき。
- AgentCallParameter の共通定義や prompt の一般的な組み立て規則そのものを確認するときは、それぞれの共通実装を直接読む。

## hash
- 250f05f1e71333741def1f7eead1cc886e3aaf0f6f7c356df8ab0481868d3d58
