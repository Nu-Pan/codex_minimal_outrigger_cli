# `apply`

## Summary
- `cmoc realization apply fork` における realization 追従処理の起動パラメータ構築を担う実装入口です。oracle file の差分、対象コミット範囲、linked worktree 情報を codex exec 用プロンプトと AgentCallParameter に組み立てます。

## Read this when
- `cmoc realization apply fork` の追従用 AgentCallParameter や codex exec prompt の構築方法を確認したいとき。
- oracle file の変更差分や対象コミット範囲、linked worktree 情報が追従プロンプトへ組み込まれる流れを調べたいとき。
- fork 起動時の実行モデル、推論設定、ファイルアクセス権限の対応関係を確認したいとき。

## Do not read this when
- `cmoc realization apply fork` 以外の用途の prompt 構築を調べるとき。各用途に対応する prompt builder を直接確認してください。
- realization file の具体的な変更処理やテスト内容を確認したいとき。対応する realization implementation または realization test を直接確認してください。

## hash
- 849c654d79ee29fb9c2b380bf1700480db1701f4387ce9586d56ddcde68a85bb

# `refactor`

## Summary
- refactor fork における変更差分の人間向け要約処理と、ファイル単位の実装レビュー・修正処理を構築する。変更要約およびレビュー結果の Structured Output スキーマ、関連 prompt、実行時のモデル・権限・作業ディレクトリ設定を扱う。
- 変更要約処理は、与えられた refactor 差分を意味論的なカテゴリ、要約、変更 path に分類する AgentCallParameter を生成する。
- ファイルレビュー・修正処理は、指定された oracle または realization file を起点に必要な調査、realization file の修正、修正後検証を行う AgentCallParameter を生成し、所見・根拠・変更 path・対応結果を返す。

## Read this when
- refactor fork の変更差分要約の prompt、出力契約、または AgentCallParameter 構築を確認・変更するとき
- refactor fork のファイル単位レビュー、修正、検証の prompt、作業条件、または出力契約を確認・変更するとき
- 変更要約やレビュー結果の Structured Output の項目と対応条件を確認するとき

## Do not read this when
- 実際にレビューされる個別の oracle file や realization file の内容を調査するとき
- 通常の realization 実装・テストの挙動を確認するとき
- refactor fork を呼び出す上位の運用や、別の prompt builder の責務を調査するとき

## hash
- 2af6a11f95412b14b5db372fb0a83f12d315f5fe10f04a867111547a8e741469
