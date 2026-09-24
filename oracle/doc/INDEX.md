# `app_spec`

## Summary
- cmoc のアプリケーション仕様を構成する正本文書群。CLI の共通動作、セッション・run 状態、oracle/realization の責務、Codex 呼び出し、ログ・エラー・feedback、ファイル列挙などの横断契約を扱う。
- `sub_command` 配下には、各サブコマンドの引数、事前条件、処理手順、状態遷移、agent call 委譲、report、終了結果を定義する個別仕様がまとまっている。

## Read this when
- cmoc 全体の挙動や複数サブコマンドにまたがる契約を確認するとき。
- サブコマンドの仕様を調べる際に、まず共通契約と個別仕様の入口を把握するとき。
- oracle file と realization file、session/run、feedback、Codex CLI、ログ出力の責務境界を確認するとき。

## Do not read this when
- 特定の共通機能の詳細だけを確認したい場合は、直下の対応する仕様ファイルを直接読む。
- 特定サブコマンドの処理だけを確認したい場合は、`sub_command` 配下の該当ファイルを直接読む。
- 実装の具体的な構造や field の正確な型を確認したい場合は、仕様から委譲されている `oracle/src` の対象を読む。

## hash
- c6e34239134bd29925b67f3a009e0a2ad9e5bfe46fd07d979008ec5f1d6bf4cd

# `branch_model.md`

## Summary
- cmoc が session と run を隔離・統合するための branch、commit、worktree の正本モデルを定義する。session/run branch の作成元・命名・対応関係、fork/join commit、run worktree の配置と no-op join の扱いを確認する入口である。

## Read this when
- session fork や run の開始・join・apply における branch、commit、worktree の関係を確認したいとき。
- run の差分検査や report がどの fork commit を基準にすべきか確認したいとき。
- session branch と run branch の命名、分岐元、merge 先を確認したいとき。

## Do not read this when
- 個別サブコマンドの実装手順や CLI 入出力を確認したいとき。
- run state や report の項目定義そのものを確認したいときは、それらを直接定義する仕様へ進むべきである。

## hash
- d043bb04484e4c8b1c47fbaf83d5e776f1c0e1a2d180e01ee2788e2fb23251aa

# `considered_alternative`

## Summary
- 代替案を採用しなかった理由と、その代わりに現行仕様で採用された方針への参照をまとめる正本文書群。
- 作業計画レビュー、oracle review、事後検証、自動改善記憶、permission profile 動的生成など、過去に検討・断念した設計判断の個別記録への入口。

## Read this when
- 現行仕様に至った設計上の不採用理由や、検討された代替方式との比較を確認したいとき。
- 特定の代替案に関する判断記録を探すとき。

## Do not read this when
- 現行の仕様や実装手順を確認したいときは、各文書が参照する oracle/doc/app_spec 配下の正本を直接読むべきです。
- 代替案の採否理由ではなく、実装の現在の挙動や通常の作業手順だけを調べたいとき。

## hash
- 8f1609bbacffd65e7eedc6cffe9ac52710be176773c393d128c0f025f82ba759

# `dev_rule`

## Summary
- cmoc 開発における環境構築、設計、コーディング、テスト実装、テスト実行と品質検査の正本規則をまとめた文書群。
- 実装方針と共通のコーディング制約を確認する入口であり、テストの意味要件と実行・完了判定は分担された個別文書へ案内する。

## Read this when
- cmoc の開発環境や Python 仮想環境、依存関係の扱いを確認するとき。
- CLI・共通機能の設計方針、型注釈・docstring・命名・import・コメントなどの実装規則を確認するとき。
- テストの目的・非目的、実経路統合テストの要件、または品質検査の選択・実行・完了判定・報告方法を確認するとき。

## Do not read this when
- 具体的な機能の正本仕様や外部 CLI 呼び出し規約を確認したい場合は、対応する app_spec の文書を直接読むとき。
- 個別の実装・テストコードの挙動や詳細を確認したい場合は、src・test の対象を直接読むとき。
- 既に構築済み環境で通常のテスト実行だけを行う場合に、環境構築規則だけを確認したいとき。

## hash
- cd7d23c93d085767e759f358baa2c54a3fe075d0b4d1f0a1418d18cc3074c443
