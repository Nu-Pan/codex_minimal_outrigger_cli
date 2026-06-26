# `fork`

## Summary
- `cmoc apply fork` のレビュー・修正・レポート生成で使う AI エージェント呼び出しパラメータと、その Structured Output schema をまとめた領域。
- フォーク適用後の差分要約、起点ファイルからの所見列挙、検出済み所見の修正依頼といった、apply fork 内の AI 支援工程への入口になる。

## Read this when
- `cmoc apply fork` が AI エージェントへどのような prompt、権限、model class、reasoning effort、Structured Output schema を渡しているかを確認・変更したいとき。
- apply fork のレビュー工程で、実装調査による所見列挙、所見対応作業、変更要約レポート生成のいずれかの呼び出し条件を追いたいとき。
- apply fork が扱う差分要約やレビュー所見の構造化出力契約と、その生成側の実装との対応を確認したいとき。

## Do not read this when
- fork の作成、ブランチ操作、git コマンド実行、差分適用など、apply fork 全体の実行制御や低レベル処理を調べたいとき。
- oracle standard や realization standard など、prompt に含まれる標準文書の本文そのものを確認したいとき。
- 汎用的な prompt 構築、markdown rendering、AgentCallParameter 型、repo root 解決など、apply fork 固有でない共通基盤を調べたいとき。

## hash
- dbd9e98ad05ec83c80ed9270504805e990b244274c969394ded93274f90a21a5
