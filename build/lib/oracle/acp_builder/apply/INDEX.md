# `fork`

## Summary
- `cmoc apply fork` における agent 呼び出し用の正本 prompt 断片と、その呼び出し結果を受け渡す Structured Output schema を扱う領域。
- 差分要約生成、ファイル単位の所見列挙、所見対応修正の各 agent に渡す role・goal・制約・model class・reasoning effort・file access mode を確認する入口となる。
- 変更要約やレビュー所見を機械処理可能な JSON として受け渡すための出力契約もここから確認できる。

## Read this when
- `cmoc apply fork` が差分要約、ファイル単位レビュー、所見対応修正の agent call parameter をどう組み立てるか確認したいとき。
- 作業レポート向けの変更要約や、実装と oracle requirement の不一致を表すレビュー所見の Structured Output schema を確認したいとき。
- apply fork 系 agent に渡す readonly/write 権限、git 操作禁止、所見の扱い、placeholder、補助 prompt、model class、reasoning effort の正本を確認または変更したいとき。

## Do not read this when
- `cmoc apply fork` 全体の実行制御、fork 作成、branch 操作、git 操作、状態管理、所見統合の実装を調べたいとき。
- complete prompt の共通組み立て規則、Structured markdown 描画、path placeholder 解決の一般仕様を調べたいとき。
- 特定の realization file の実装内容、変更内容そのものの妥当性、または oracle file / realization file の基本定義やレビュー判断基準を確認したいとき。

## hash
- ce9a936961840e259ca6f74689b6aa0f087d34fd84080482b82f9a59c04a9a9e
