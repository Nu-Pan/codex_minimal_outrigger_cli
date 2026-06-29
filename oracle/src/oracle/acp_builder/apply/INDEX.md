# `fork`

## Summary
- `cmoc apply fork` における AI エージェント呼び出し用の正本断片をまとめる領域。差分要約、ファイル単位の所見列挙、所見適用依頼など、fork 適用フローのうち AI に渡す prompt・Structured Output schema・モデル選択・ファイルアクセス制約の契約を扱う。
- 実際の git 操作や fork 適用アルゴリズムそのものではなく、適用後の差分や仕様乖離を AI に調査・要約・修正させるための入力契約と出力契約を確認する入口となる。

## Read this when
- `cmoc apply fork` で、差分要約、実装所見の列挙、所見に基づく修正依頼を AI エージェントへどう渡すか確認したいとき。
- apply fork 系の prompt に含める role、summary、goal、補助入力、standard 群、placeholder、ファイルアクセスモードを確認または変更したいとき。
- apply fork 系の AI 呼び出しで使うモデルクラス、reasoning effort、Structured Output schema の選択根拠や境界を確認したいとき。
- fork 適用後の作業レポートやレビュー結果として、人間向け差分要約または修正所見リストの出力契約を確認したいとき。

## Do not read this when
- `cmoc apply fork` のブランチ作成、git diff 取得、実際のパッチ適用、commit 操作などの実行フローそのものを調べたいとき。
- oracle file、realization file、path keyword、AgentCallParameter、model class、file access mode などの共通概念の定義を確認したいとき。
- complete prompt の共通構築規則、markdown rendering、パス解決、構造化文書の汎用仕様を調べたいとき。
- apply fork 以外のサブコマンド用 prompt、一般的なルーティング文書、または実装・テスト変更種別ごとの個別判定ロジックを探しているとき。

## hash
- 28f66aa79cf3c48a0d66f247642a2aa7007c67983766b6344a9e0c304d6fd2ff
