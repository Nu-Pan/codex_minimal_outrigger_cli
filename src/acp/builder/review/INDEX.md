# `__init__.py`

## Summary
- oracle.acp_builder.review と互換の package であることだけを示す、review builder 領域の package 初期化用ファイル。実装ロジックや詳細な仕様ではなく、互換名前空間としての位置づけを確認する入口になる。

## Read this when
- review builder 領域で、oracle 側の同名 package と対応する realization package が存在するかを確認したいとき。
- package としての互換性や import 経路の成立だけを確認したいとき。

## Do not read this when
- review builder の具体的な処理、関数、クラス、出力、制御フローを調べたいとき。
- 正本仕様断片としての review builder の要求を調べたいとき。
- package 初期化以外の実装変更先を探しているとき。

## hash
- adf6124f1c3a49a136159186b6a58b39f4321e0113527b60e85d8b1e3205484e

# `oracle`

## Summary
- review oracle 周辺で、正本側実装への互換 import 経路と、一部の AgentCallParameter 生成結果に対する最小限の prompt 補正をまとめる realization 側の入口。
- 多くの対象は実体ロジックを持たず、旧来の呼び出し元を正本側経路へ移行するまで残す再公開層として機能する。
- finding merge と finding advocate validation では、正本側 builder の出力を保持しつつ、oracle root 表記に関する既知の静的 typo だけを局所補正する wrapper を持つ。

## Read this when
- review oracle の旧来 import 経路がなぜ残っているか、また削除できる条件を確認したいとき。
- review finding enumeration、judgment、challenger validation が realization 側に実装本体を持つのか、正本側へ委譲しているだけなのかを切り分けたいとき。
- review oracle の finding merge または finding advocate validation で渡される AgentCallParameter の生成経路を確認したいとき。
- 生成 prompt 内の oracle root 表記に対する一時的な互換補正がどこで行われ、どの動的入力を変更しない前提なのかを確認したいとき。

## Do not read this when
- review oracle の検出仕様、判定仕様、prompt 正本、structured output schema の本来の定義を確認したいときは、正本側の対応する oracle 実装や仕様文書を読む。
- 新しい finding の列挙、判定、検証ロジックを追加・変更したいときは、この互換層ではなく委譲先の実装本体を読む。
- AgentCallParameter 型、model class、reasoning effort、file access mode などの共通構造を調べたいときは、共通の parameter 定義へ進む。
- review oracle と無関係な CLI 表示、テスト方針、INDEX.md 生成仕様、oracle file と realization file の一般的な責務境界を調べているときは、より直接その責務を持つ対象へ進む。

## hash
- 6cc02d64fda77f8230d1b6ff12f6bcfc1c44b5fc8782501b880043954d509966
