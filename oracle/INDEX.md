# `doc`

## Summary
- cmoc の人間所有の正本仕様を集め、利用 workflow、機能やサブコマンドの挙動、共通する責務・状態・branch/run・ログ・エラー処理を定義する入口です。
- 開発環境、設計、コーディング、テストの規約と、採用しなかった案の判断理由も含みます。後者は現行仕様そのものではなく、判断の背景を説明します。

## Read this when
- cmoc の利用者向け挙動を追加・変更・確認するとき。該当する機能やサブコマンドの仕様から詳細を確認してください。
- oracle と realization の責務、仕様の優先関係、または仕様を agent 向けの指示へ反映する方法を確認するとき。
- 開発環境、実装設計、コーディング、テストの意味要件や実行手順を確認するとき。
- branch と run の lifecycle、状態管理、ログ、feedback、indexing など複数機能に関わる共通動作を確認するとき。
- 現行仕様に関係する採用判断の背景や、不採用にした案の理由を調べるとき。

## Do not read this when
- 実装やテストのソースを直接調査・変更するときは、該当する oracle/src、src、test の内容へ進んでください。
- 正確な prompt 文面、schema、algorithm、構築方法など、oracle src に委譲された詳細を確認するときは、その委譲先を読んでください。
- 対象が開発・検証規約だけ、または特定機能だけと明らかな場合は、その下位の文書群や該当仕様から読み始めてください。

## hash
- 6096c879aaee1c7ea641e0fd0d71d7a7860a2afee09ae5ce2642109ec28d73a6

# `src`

## Summary
- 自然言語の仕様から委譲された cmoc の正確な詳細を実装・データ定義として集約し、共通設定、パスと文書参照のモデル、構造化文書のレンダリングを定義する。
- 共通規定と作業別の指示を組み合わせて agent prompt と呼び出し条件を構築する。TUI、oracle 調査・編集、realization の適用・整理、join の競合解消、feedback、index 生成、quota probe が主な対象となる。
- editor input の handoff 文面、feedback の入力と処理、agent call の Structured Output 契約も含む。

## Read this when
- agent call の設定、root path と worktree の解決、文書参照、構造化文書の生成など、共通モデルの正確な挙動を変更・確認するとき。
- 共通 prompt の組み立て方や、アクセス制限・routing・oracle/realization などの規定文面を変更するとき。
- 特定の agent 作業の prompt、実行条件、handoff、feedback 処理、競合解消、または index 生成の入出力契約を変更するとき。

## Do not read this when
- 人間意図や cmoc の意味仕様を決める・変更する場合は、意味仕様の所有者である自然言語の oracle doc から確認する。ここは明示的に委譲された詳細の確認に進むときに読む。
- CLI の実行時処理やテストを変更するときは、実際の realization 実装・テストを確認する。この対象は oracle 側の詳細定義である。
- 一つの agent 作業だけが対象なら、対象作業の定義と必要な共通部品から確認する。全体を扱わない変更で、この配下すべてを読む必要はない。

## hash
- 2d6e5c4cec2e62e55920e86bcd6bf79ee97573076830d74af88e5063ec8e755a
