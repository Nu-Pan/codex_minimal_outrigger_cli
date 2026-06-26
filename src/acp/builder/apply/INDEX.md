# `fork`

## Summary
- `cmoc apply fork` のうち、フォーク適用後の調査・所見列挙・所見対応・変更要約を AI エージェントへ依頼するための prompt と呼び出し条件、および関連する構造化出力契約をまとめる領域。
- 差分要約、実装レビュー所見、所見対応依頼といった apply fork の補助エージェント工程について、どの標準・文脈・読み書き権限・モデル設定・出力 schema を渡すかを確認する入口になる。

## Read this when
- `cmoc apply fork` の実行中または実行後に、AI エージェントへ渡す調査依頼、修正依頼、変更要約依頼の prompt 内容や呼び出しパラメータを確認・変更したいとき。
- apply fork の所見列挙工程で、起点ファイルから関連する oracle file と realization file を調査させる条件、読み取り専用の扱い、標準文書の組み込み、出力 schema の対応を追いたいとき。
- 検出済み所見を realization file 修正担当へ渡す工程で、所見 JSON の埋め込み方、作業上の注意点、書き込み権限、参照標準、モデル設定を確認したいとき。
- apply fork の作業レポート向けに、git 差分を AI 要約担当へ渡してカテゴリ別の変更要約を生成する仕組みを確認したいとき。
- レビュー所見や変更要約の構造化出力について、報告単位、根拠情報、主要な変更パス、カテゴリ別要約などの出力契約を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体のコマンド実行フロー、fork の作成・適用・統合、ブランチ操作、git コマンド実行そのものを調べたいとき。
- oracle file、realization file、apply review standard、realization standard などの標準本文そのものを確認したいとき。
- 汎用的な AgentCallParameter 型、完全 prompt の共通構築、StructDoc の markdown rendering、repo root やパス解決 helper の詳細を調べたいとき。
- 個別カテゴリ名の網羅的な一覧、差分生成アルゴリズム、変更パス抽出の具体的な実装規則を探しているとき。
- INDEX.md 用エントリーや一般的なルーティング文書の書き方を確認したいだけのとき。

## hash
- dbd9e98ad05ec83c80ed9270504805e990b244274c969394ded93274f90a21a5
