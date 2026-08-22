# `oracle`

## Summary
- cmoc の正本仕様・共通モデル・agent call 構築定義を扱うソースディレクトリ。agent call パラメータ、quota probe、prompt 構築、パスと設定のモデル、構造化 Markdown 文書、feedback reporter 入力契約など、下位の用途別定義へ進むための入口を提供する。
- `acp_builder`、`prompt_builder`、`other`、`feedback` に分かれ、agent 呼び出し契約、完全 prompt と policy の組み立て、root path・設定・文書ノードの共通モデル、問題報告入力スキーマをそれぞれ扱う。

## Read this when
- agent call の共通パラメータ、quota availability probe、prompt の構造や policy 統合、path context・root placeholder、cmoc 設定、構造化 Markdown 文書、feedback reporter 入力契約を調査または変更するとき。
- 用途別の正本モデルや prompt 構築定義の所在を特定し、`acp_builder`、`prompt_builder`、`other`、`feedback` の下位要素へ進む必要があるとき。

## Do not read this when
- 既存 INDEX.md のルーティング情報だけを確認したいとき。
- Codex CLI のバックエンド固有実装、通常の realization・session・TUI 実行処理、collector の保存・集約処理、個別 issue やレビュー所見の内容を直接確認したいときは、対応する実装・仕様・データ定義を読む。

## hash
- cd97037170d661f94a1da579c4311ccdeda085686cc411f83eb4a163cb8c17ef
