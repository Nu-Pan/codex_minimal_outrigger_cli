# `conflict_resolution.py`

## Summary
- `cmoc session join` が検出した merge conflict marker を解消するための AI エージェント呼び出しパラメータを構築する実装。対象パスを実パスへ解決し、conflict 解消に限定した役割・目標・追加アクセス規則を含む完了プロンプトを生成して返す。

## Read this when
- `cmoc session join` の conflict marker 解消用プロンプトや AgentCallParameter の内容を確認・変更したいとき。
- conflict 対象ファイルの一覧がどのようにプロンプトへ埋め込まれるか、また実パス解決や作業ルート解決の扱いを追いたいとき。
- merge conflict marker 解消時の許可範囲、禁止事項、oracle file への例外的編集許可、git add/git commit 禁止などのエージェント指示を確認したいとき。

## Do not read this when
- 通常の session join フロー全体、workspace 状態の統合、または conflict marker 検出処理を調べたいだけのとき。
- merge conflict の実際の解消アルゴリズムやファイル内容の自動編集処理を探しているとき。
- 汎用的なプロンプト部品、AgentCallParameter の型定義、パスモデルの仕様そのものを確認したいとき。

## hash
- d5cf6e98245985065e627071215cb070a4e415d761eabd0420b177e316242b1a
