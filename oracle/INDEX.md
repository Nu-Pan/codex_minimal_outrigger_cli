# `doc`

## Summary
- cmoc の個別アプリケーション仕様を機能別に選ぶ上位入口。CLI、agent call、ログ、feedback、prompt editor、run/session、通知などの責務と境界を確認できる。
- session と run を git branch・commit・worktree で隔離するモデルを定義する文書。分岐、統合、worktree、管理 branch の関係を確認できる。
- 採用しなかった設計・作業方式と不採用理由を記録する検討資料群。現行仕様や実装手順ではなく、設計判断の背景を調査できる。
- Python 実装、CLI の責務配置、開発環境、テスト要件、テスト実行手順へ振り分ける開発ルールの入口。

## Read this when
- cmoc のアプリケーション機能の挙動・責務・境界、または対応する個別仕様を選ぶとき。
- session fork、run の分岐・統合、worktree の作成、branch や commit の役割を確認するとき。
- 採用されなかった設計案や作業方式の理由を比較し、現行設計の判断背景を調査するとき。
- Python の記述規則、CLI 実装の配置、環境構築、テスト要件、またはテスト実行手順の入口を選ぶとき。

## Do not read this when
- 特定のアプリケーション機能の仕様が特定できている場合は、app_spec 配下の該当文書を直接読む。
- branch と run の具体的な CLI 入出力契約や個別処理を確認する場合は、対応する app_spec 文書を直接読む。
- 現行の仕様、実装方法、または操作手順を確認する場合は、considered_alternative ではなく正本仕様や開発ルールを読む。
- 特定のコーディング規則、設計責務、環境条件、テスト要件、またはテスト実行手順を確認する場合は、dev_rule 配下の該当文書を直接読む。

## hash
- 8e736d485e6959297814940fa85e90630d15ccbbf82939c16014aad94899a32c

# `src`

## Summary
- oracle 実装パッケージのルート。agent call 構築、prompt 構築、入力 handoff、feedback、設定・パス・構造化文書の機能領域を束ねる。
- agent call のパラメータや用途別 builder、session・TUI・review・realization の入口を調べる場合は `oracle/acp_builder` へ進む。
- 完全 prompt、prompt policy、prompt parts の構築規則を調べる場合は `oracle/prompt_builder` へ進む。
- editor input handoff や feedback の入力契約を調べる場合は、それぞれ `oracle/editor_input_handoff` または `oracle/feedback` へ進む。
- 設定モデル、パス解決、構造化文書の実装を調べる場合は `oracle/other` へ進む。

## Read this when
- oracle/src 配下の機能領域を特定し、調査対象の下位ディレクトリを選ぶとき。
- agent call、prompt、入力契約、設定・パス、構造化文書の複数領域にまたがる oracle 実装の入口を確認するとき。

## Do not read this when
- 特定の agent call builder、prompt policy、入力契約、設定モデル、パスモデル、または構造化文書の具体的な実装を確認したいときは、対応する下位ディレクトリを直接読む。
- session、TUI、review、realization、policy、parts など個別機能の挙動を調べるときは、該当する下位対象へ進む。

## hash
- 4307cf805748d8343d15f75cee2cd3dba18199117272e72e4dcd4575dc11c21d
