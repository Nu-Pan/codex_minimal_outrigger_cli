# `doc`

## Summary
- cmoc の正本文書群への入口。アプリケーション仕様、開発ルール、session/run の branch model、採用しなかった代替案など、実装や調査の前提となる文書領域を目的別に案内する。
- 個別機能の挙動仕様、開発・テスト規則、git による隔離モデル、設計上の不採用理由を、それぞれ担当する下位文書群へ進むための起点として扱う。

## Read this when
- cmoc の正本仕様や開発ルールを調査し、どの文書領域から確認を始めるべきか判断するとき。
- アプリケーション挙動、実装・テスト規則、session/run の git 隔離、または採用しなかった設計案に関する文書を探すとき。

## Do not read this when
- 特定機能の仕様本文、開発環境やテスト実行の詳細、branch model の具体的契約など、担当する下位文書が明らかな場合。
- 実装ファイルやテストの具体的な挙動だけを調べる場合。

## hash
- a4b2ea5984a7d12c6204039c42d72a891898726463b68a3fe8bb09ba5e30fee7

# `src`

## Summary
- agent call の起動パラメータ、prompt 構築、Structured Output 契約、feedback 処理、oracle／realization の編集・レビュー、INDEX.md 生成を担う実装群の入口。
- agent call の共通設定、prompt policy、パス・設定・構造化文書モデルなど、各 builder が利用する基盤要素を確認するための領域。

## Read this when
- agent call の種類ごとの起動パラメータ、cwd、ファイルアクセスモード、Structured Output schema、indexing preflight の設定を調べるとき。
- 完全な prompt の組み立て、oracle／realization、routing、feedback、所見判定に関する policy の構築を調べるとき。
- oracle file や realization file の編集・調査・レビュー、feedback issue の正規化・検証、INDEX.md エントリー生成の処理を変更・確認するとき。
- 設定モデル、パスコンテキスト、placeholder 解決、構造化文書の Markdown 化など、builder の共通基盤を確認するとき。

## Do not read this when
- 実際の Codex CLI 起動や TUI の実行制御だけを調べる場合は、該当する実行処理の対象へ直接進むとき。
- 意味仕様や運用ルールの正本を確認する場合は、oracle/src の実装詳細ではなく対応する oracle doc を読むとき。
- 個別の agent call の出力項目や JSON Schema の詳細だけを確認する場合は、対象の schema または個別 builder を直接読むとき。
- 既存の INDEX.md のルーティング内容だけを確認する場合は、この実装領域全体を読む必要はないとき。

## hash
- 95f12ad58d63052dfe8deb01198215f1681dd9396afa46e1870f015ad4468952
