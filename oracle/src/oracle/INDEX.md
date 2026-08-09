# `acp_builder`

## Summary
- oracle 向け ACP 呼び出しのサブコマンド別ビルダーを配置する領域です。oracle review の所見列挙・採否判定・統合・妥当性検証と、oracle investigation の調査起動設定を扱います。各実装の prompt、出力契約、起動条件を確認する入口です。

## Read this when
- oracle review の所見列挙、採否判定、重複・矛盾の統合、妥当性検証に関する ACP 呼び出し契約や prompt 構築を確認・変更するとき。
- oracle investigation の調査用 ACP 起動設定、調査 prompt、モデル、アクセスモード、作業ディレクトリを確認・変更するとき。
- この領域にある oracle 向け ACP builder の用途や呼び出し条件を確認するとき。

## Do not read this when
- oracle file の編集内容や realization 側の実装だけを確認する場合。
- サブコマンドに依存しない共通 prompt 構築ロジックを確認する場合は、共通 prompt builder を直接読むべきです。
- 個別のレビュー所見や、その根拠となる oracle 仕様を確認する場合は、該当する対象を直接確認すべきです。

## hash
- d4f87b365ec1edf55d4f89d6df57ac7c9e7a79028a648d05826e12fc08b53820

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- cmoc の oracle src にある基盤モデル群をまとめたディレクトリ。リポジトリ設定、root・worktree パス解決、規範モデル、構造化文書のデータ構造と Markdown 変換を扱い、これらの共通モデル実装を確認する入口となる。

## Read this when
- cmoc のリポジトリ固有設定、root placeholder や agent call のパス導出、Standard・Requirement のモデル、または StructDoc の構造化・Markdown 変換を調査・変更するとき。
- 複数の共通モデルの責務分担や、これらを利用する oracle src の実装へ進む前に基盤定義を確認するとき。

## Do not read this when
- 永続化された設定 JSON の生成・同期や doctor の具体的な挙動だけを確認するときは、対象の設定ファイルや doctor 実装を直接読む。
- 個別の列挙型定義、個別の規範本文、StructDoc の正本仕様、または CLI・agent call などの利用側処理だけを調査するときは、それぞれの直接の定義・仕様・呼び出し側へ進む。

## hash
- 0925ecd2af76345af3913b3a776af54e93ab0a72ce1ae7bd6212c95be3b3daf3

# `prompt_builder`

## Summary
- エージェント呼び出し用プロンプトを構成する実装群。プレースホルダ型、完全なプロンプトの組み立て、エディタ初期入力、oracle・realization・アクセス制御・ルーティングなどの共通規範を扱う。各機能の詳細を確認する際の入口となる。

## Read this when
- エージェント呼び出し用プロンプトの構成や統合規則を調査・変更するとき。
- プレースホルダの型、エディタ入力の初期文面、共通規範の注入条件を確認するとき。
- 複数の prompt builder 部品から調査対象を選ぶ必要があるとき。

## Do not read this when
- 特定の静的プロンプト本文や個別規則だけを確認したいときは、対応する下位部品を直接読む。
- prompt builder の呼び出し元や session・CLI 処理を調査するとき。
- プロンプト構築と無関係な機能や、構造化文書の一般的な実装を確認するとき。

## hash
- 3fd75b4b70d43dfa3b0512a6417f033323e81676d3f16aba8ea9d953fc047ece
