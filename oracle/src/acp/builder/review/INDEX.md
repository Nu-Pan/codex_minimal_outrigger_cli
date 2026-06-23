# `oracle`

## Summary
- `cmoc review oracle` の AI 呼び出し境界を定義する oracle src 群。レビュー対象の oracle file から新規所見を列挙し、所見の妥当性を支持・反証する理由を追加調査し、人間提示の採否を判定し、複数所見の重複や矛盾を整理する各段階の prompt 構築と Structured Output 契約を扱う。
- 各段階で agent に渡す役割、目的、補助文脈、oracle file だけを根拠にする制約、既知情報との重複排除、空結果の扱い、モデル種別、reasoning effort、file access mode、出力 schema への接続を確認する入口になる。

## Read this when
- `cmoc review oracle` のレビュー所見生成から検証、採否判定、所見整理までの AI 呼び出しパラメータや出力契約を確認したいとき。
- レビュー対象 oracle file、関連 oracle file、既知所見、既知の擁護理由・反証理由、入力済み所見リストを、各 review oracle prompt がどの意味で補助文脈として扱うか確認したいとき。
- 新規所見や新規理由を、既知情報と重複しない単位で返す境界、該当するものがない場合に空の一覧を返す境界を実装・検証したいとき。
- レビュー所見について、妥当だと言える理由、妥当ではないと言える理由、人間へ提示すべきかの判断理由、重複・矛盾整理後に残す理由をどの段階で扱うか切り分けたいとき。
- oracle review 系サブコマンドで、標準 prompt 部品、oracle/review oracle 標準、Structured Output schema、モデル設定、純粋 oracle 読み取りモードの組み込み経路を追いたいとき。

## Do not read this when
- oracle file と realization file の基本定義、パスキーワード、oracle 標準、review oracle 標準そのものの本文を確認したいとき。
- 通常の実装担当 agent 向け prompt、INDEX.md 生成 prompt、または oracle review 以外のサブコマンド prompt を確認したいとき。
- レビュー所見の保存、集約、CLI 表示、編集操作の適用、後続処理など、AI 呼び出しパラメータや応答 schema 以外の実装を調べたいとき。
- 個別の oracle file 本文を読んで、所見や理由の具体的な根拠材料を探したいとき。
- 共通 prompt 組み立て、構造化 Markdown 描画、path 解決、AgentCallParameter の一般仕様、file access mode の共通仕様だけを確認したいとき。

## hash
- b9df6a1f0c8b4688f4e34a0f2c7c879e7aa97a68dee6b9a24258feb001c1aa6e
