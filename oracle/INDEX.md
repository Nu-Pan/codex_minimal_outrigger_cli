# `doc`

## Summary
- cmoc の利用者向け挙動、サブコマンドの契約、複数機能に共通する規則、および session と run の Git 上の扱いを定める自然言語の正本仕様を収録する。
- 開発時のコード設計、コーディング、環境構築、テストの要件と実行手順、および採用しなかった設計案の判断記録も扱う。期待される挙動や開発規則を文書から確認する入口となる。
- 正確なプロンプト構築やデータ構造など、文書からソースへ明示的に委譲された詳細は oracle のソース側にある。

## Read this when
- cmoc の現在の利用者向け挙動、サブコマンドの契約、または複数機能に共通する規則を確認・変更するとき。
- session と run に関する Git branch、commit、worktree の用語や関係を確認するとき。
- 実装やテストに適用する設計・コーディング規則、テスト要件、既存環境での検査手順を確認するとき。
- 採用しなかった設計案の判断理由を調べるとき。現在の規則を決める場合は、記録中で参照される正本仕様も確認する。

## Do not read this when
- 確認対象が特定済みで、必要なのが正確なプロンプト構築、型や設定の定義などソース上の詳細だけであるときは、対応する oracle ソースを直接読む。
- 実際の oracle テストケースや assertion の内容を確認するだけであれば、対応する oracle test を直接読む。

## hash
- bdb58921a5bae113a52dd508d58be9a364f655435e207f36c4698d25d0e4fc00

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
