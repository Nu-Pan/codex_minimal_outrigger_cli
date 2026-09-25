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
- cmoc が agent 呼び出しに渡す prompt、共通規定、タスク別の呼び出しパラメータを組み立てるコードと設定を収める。oracle 編集、realization の追従・整理、変更の統合、feedback、索引生成などの呼び出し構築が対象。
- 呼び出し設定、アクセス区分、root path の解決、構造化文書の Markdown 描画、文書参照を扱う共通モデルも含む。editor input handoff と feedback などで使う入力・出力の検証定義もここにある。
- ここにあるコードと設定は、agent 呼び出しの正確な構築内容を確認・変更するための参照先。意味仕様を担う文書や、生成された realization の実装とは役割が異なる。

## Read this when
- agent に渡す prompt の組み立て、共通規定の選択、または oracle 編集・realization 追従・統合・feedback・索引生成などの呼び出し構築を変更・追跡するとき。
- 呼び出し設定、root path の解決、構造化文書の描画、文書参照など、複数の呼び出しで共有される処理を変更・確認するとき。
- editor input handoff のガイドや本文の生成、または agent 呼び出しの入力・出力検証定義を調べるとき。

## Do not read this when
- 人間意図や製品・サブコマンドの意味仕様を知りたいときは、意味仕様を担う oracle 文書から読む。ここは文書から明示的に委譲された正確な構築詳細が必要な場合に参照する。
- oracle のテスト上の期待や検証を調べるときは、対応する oracle test を直接読む。
- 生成物である realization の実装やテストを変更するときは、対応する realization 側の実装・テストを直接読む。

## hash
- 27518ebbb0868e4ede32c2a05eb9b09a785f2a3cc60d9312dc0875d045e14e46
