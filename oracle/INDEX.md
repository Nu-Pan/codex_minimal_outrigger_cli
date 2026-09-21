# `doc`

## Summary
- cmoc の正本ドキュメント群。app_spec には CLI、セッション・run、agent 呼び出し、feedback、indexing などのプロダクト仕様、dev_rule には開発・設計・実装・テスト規約、considered_alternative には不採用案の判断記録、branch_model.md には Git branch・commit・worktree の用語と関係を収録する。各サブディレクトリの仕様や開発規約へ進むための入口。

## Read this when
- cmoc のプロダクト仕様、開発規約、ブランチモデル、または採用判断の根拠を確認するとき。
- 実装・テスト・サブコマンド・agent 呼び出しの正本を探す起点が必要なとき。

## Do not read this when
- 具体的な機能の詳細が特定できており、app_spec 内の該当仕様書を直接読む方が適切なとき。
- 開発環境・コーディング・テスト実行などの規約だけを確認したいときは dev_rule 以下へ、過去の不採用判断だけを確認したいときは considered_alternative 以下へ直接進む場合。

## hash
- dc3a25ce38ff5c6dfae4b59bc6b8d2db34c82ff25ff175b6206651ad4a3c525e

# `src`

## Summary
- cmoc の正本実装をまとめたディレクトリ。editor input handoff、feedback、prompt builder、ACP builder、共通データモデル・設定処理を扱い、各サブディレクトリから個別の実装仕様や起動パラメータ構築へ進む入口となる。

## Read this when
- cmoc の正本実装の責務分担を横断的に把握したいとき。
- サブコマンドの agent call、prompt、handoff、feedback、または共通モデルの実装を調査するとき。
- 対象となる実装領域が複数サブディレクトリにまたがり、最初に構成を確認する必要があるとき。

## Do not read this when
- 特定の prompt policy、サブコマンド起動処理、handoff 処理、feedback schema、または共通モデルの具体的な挙動を確認したいときは、該当サブディレクトリ内の実装ファイルを直接読む。
- 意味仕様そのものを確認したいときは、oracle/src ではなく対応する oracle/doc を読む。

## hash
- f3399a1025b495e9532879caa6e93029265c409304d9390cfff50f55762d416c
