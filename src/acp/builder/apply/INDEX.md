# `__init__.py`

## Summary
- oracle 側の apply builder package と対応する互換 package であることだけを示す package 初期化要素。実処理や公開 API の定義ではなく、同領域を package として扱うための入口に位置づけられる。

## Read this when
- apply builder 領域が oracle 側の package 構造と対応しているかを確認したいとき。
- package 初期化部分に実装意図や互換性メモがあるかを確認したいとき。

## Do not read this when
- apply builder の具体的な処理、変換、適用ロジックを調べたいとき。その場合は同 package 内の実装本体を読む。
- 公開関数、クラス、入出力仕様、エラー処理を確認したいとき。この対象にはそれらの定義は含まれない。

## hash
- a6df93a5897c266e6f48287739c8bf8192733ea9fb19e2f6eb05a302f4165b06

# `fork`

## Summary
- apply fork 向け agent call parameter builder の realization 側実装をまとめる領域。oracle 側 builder への委譲入口と、その委譲に必要な oracle src import 準備、repo root 由来の fallback、oracle parameter から realization 側型への適合処理を扱う。
- 変更要約、ファイル単位所見列挙、所見適用など、apply fork の各 agent 呼び出し用 parameter 構築は個別 builder が担い、共通の import・型変換境界は共有 helper に集約されている。

## Read this when
- apply fork の各 agent 呼び出しで、realization 側が oracle 側 builder をどの入口から呼び出しているか確認したいとき。
- oracle 側 builder の戻り値を realization 側の agent call parameter として扱う変換境界を調べたいとき。
- oracle パッケージを通常 import できない配置で、repo root 由来の候補から oracle src を import path に追加する fallback を確認したいとき。
- 変更要約、ファイル単位所見列挙、所見適用のどの parameter builder を読むべきか、この領域内で入口を選びたいとき。

## Do not read this when
- apply fork のプロンプト内容、出力条件、agent call parameter の正本仕様そのものを確認したいとき。この領域は realization 側の薄い委譲実装なので、対応する oracle 側の本文を読む。
- apply fork 全体の CLI 制御、fork 適用処理、git 操作、作業レポート生成フローを調べたいとき。この領域は agent call parameter 構築の入口と共通境界に限られる。
- repo root 解決そのものの仕様、ACP 型の定義・フィールド・検証規則、または oracle 側 builder 本体の詳細を確認したいとき。それぞれの定義元や委譲先を読む。

## hash
- 776bf75f4f272d2e5c153e34de033989cc8d5e54f37f42e94f91dd7b307650c4
