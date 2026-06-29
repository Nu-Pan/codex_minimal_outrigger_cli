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
- realization 側の review oracle builder から、finding の列挙・判定・結合・検証処理を oracle 側実装へ到達させるための互換 import 境界。大半は正本側実装の再公開で、advocate 検証パラメータ生成だけは oracle 側結果を包み、prompt 内の oracle root placeholder 表記を補正する。

## Read this when
- realization 側の review oracle builder で、finding 列挙・判定・結合・検証機能がどの公開経路から参照されるか確認したいとき。
- この階層が独自ロジックを持つ実装なのか、oracle 側実装を再公開する互換境界なのかを切り分けたいとき。
- finding advocate 検証パラメータ生成で、oracle 側実装と異なる prompt 文字列が返る理由や placeholder 表記補正の位置を確認したいとき。
- 互換 import 経路を変更・削除してよいか判断するために、review oracle 関連機能の入口としての役割を確認したいとき。

## Do not read this when
- finding 列挙・判定・結合・検証の具体的なアルゴリズム、入出力、判定基準、prompt 構成を理解したいとき。その場合は委譲先の oracle 側実装や仕様断片を読む。
- review workflow 全体、CLI 入出力、builder 全体の責務分担、または finding 以外の review 処理を調べたいとき。より上位または該当責務の本文へ進む。
- Structured Output schema、model class、reasoning effort、file access mode などの共通定義を調べたいとき。この階層ではなく、それらを定義する oracle 側または共通定義を読む。
- 公開 API の詳細や再公開先の実装内容そのものを確認したいとき。この階層は主に互換入口であり、処理本体の説明場所ではない。

## hash
- 84e36a37b06c2a67a4784c4bb04f88a46eb30c6ad62175e184038a14a9a1aff1
