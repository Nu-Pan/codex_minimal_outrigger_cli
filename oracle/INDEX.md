# `doc`

## Summary
- cmoc の製品動作と各サブコマンドの契約を定める正本文書群。Codex 呼び出しやファイルアクセス、状態・run、feedback、ログ・通知などの横断仕様も含む。
- branch・commit・worktree の用語と関係、開発環境・設計・コーディング・テストの規約、不採用案の判断理由を扱う文書も収録する。

## Read this when
- cmoc の外部動作やサブコマンドの要求を調べたり変更したりするとき。
- branch・commit・worktree の関係、または開発・コーディング・テストの規約を確認するとき。
- 採用されなかった案の判断理由を確認するとき。

## Do not read this when
- 特定のサブコマンドの契約だけが必要なら、その個別仕様と必要な横断仕様を直接読む。
- 正確な prompt、schema、構築方法や実装・テストの具体的な内部構造だけが必要なら、それらを定義・実装するソースやテストを直接読む。
- 現行仕様の根拠だけで足り、過去の判断理由が不要なら、不採用案の記録は読まない。

## hash
- 23cbe775c36a5faa492d9ef4afbb87faff6ab962a9e4e960a82b3c531a5d0b43

# `src`

## Summary
- `oracle/src` は、cmoc のプロンプトや agent call の構築、共通モデルを定義する正本の Python コードと JSON Schema をまとめています。
- 下位には call ごとの構築定義のほか、パス・設定・構造化文書のモデル、editor input handoff、feedback の定義があります。

## Read this when
- agent に渡すプロンプトやポリシー、agent call のパラメータやデータ契約の定義を確認・変更するとき。
- 共通モデルや handoff、feedback の source-level の振る舞いを調べるとき。

## Do not read this when
- 機能の意図や要件だけを確認する場合は、該当する `oracle/doc` の仕様から読むとき。
- 通常の実現コードやテストだけを調査・変更する場合は、それぞれの realization の実装やテストへ直接進むとき。

## hash
- f5f1902625efa2a97dd7975cbb55f8636a4d1d55006128469e7a887b79c6e313
