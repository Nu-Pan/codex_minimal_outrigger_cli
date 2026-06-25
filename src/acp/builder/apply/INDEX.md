# `fork`

## Summary
- 適用・分岐処理のうち、AI エージェントへ渡す呼び出しパラメータと、その呼び出しが返す構造化出力の契約を扱う領域。変更要約、ファイル単位の所見列挙、検出済み所見への修正依頼など、`cmoc apply fork` の各段階で使う prompt、schema、model class、reasoning effort、ファイルアクセス権限の入口になる。
- 実際の分岐作成や Git 操作の制御フローではなく、差分・所見・修正依頼を AI にどう読ませ、どの Structured Output として返させるかを確認するための下位要素を束ねている。

## Read this when
- `cmoc apply fork` で、変更要約、所見列挙、所見対応作業のいずれかに使う AI 呼び出し条件や prompt 構成を調べたいとき。
- 差分本文、起点ファイル、所見リストなどの入力が、AI 向け prompt にどのように埋め込まれるかを確認したいとき。
- `cmoc apply fork` の各 AI 呼び出しで使う Structured Output schema、model class、reasoning effort、ファイルアクセス権限の参照先を探したいとき。
- レビュー所見や変更要約を、どのような人間向けカテゴリ・根拠位置・修正方針として構造化して返すかを確認したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、branch 作成、差分取得、Git コマンド実行など、実行フロー本体を調べたいとき。
- oracle standard、realization standard、apply review standard、path keyword など、prompt に参照される共通仕様や共通概念の本文を確認したいとき。
- 汎用的な AgentCallParameter、path 解決、完全 prompt 生成、markdown rendering などの共通部品そのものを調べたいとき。
- 個別の変更対象ファイルやテストの内容を直接確認したいだけで、変更要約・所見列挙・所見適用の AI 呼び出し契約を変更しないとき。

## hash
- 5271faab99ff0ab2b1969a0d189eb54f62226ecc1395e045d39b0822e5f8d123
