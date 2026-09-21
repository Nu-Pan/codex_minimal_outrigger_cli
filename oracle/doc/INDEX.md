# `app_spec`

## Summary
- 対象ディレクトリ内の正本仕様文書が、アプリケーションの何を定義しているかを説明する。

## Read this when
- アプリケーションの正本仕様を確認したいとき。
- 実装ではなく、app_spec 配下の仕様文書から要求や挙動をたどり始めるとき。

## Do not read this when
- 具体的な実装コードやテストの挙動を直接確認したいとき。
- app_spec 配下の個別仕様文書が既に特定できており、その文書を直接読むべきとき。

## hash
- 55483d33df495282a09f6261bb22e9e73cdd693336bc5901a736554cad0d4097

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
- 採用しなかった設計案を記録する oracle 文書群。作業計画レビュー、並列所見調査、事後的なアクセス違反検査、.gitignore からの権限生成、AI 生成 kaizen の自動注入、oracle 網羅レビューの不採用理由を扱う。
- 現行仕様そのものではなく、代替案を退けた判断根拠や当時の設計上の懸念を確認するための補助的な参照先。

## Read this when
- 現在の設計判断について、過去に検討された代替方式とその不採用理由を確認するとき。
- 作業計画レビュー、並列ファイル調査、差分の事後検証、権限プロファイル動的生成、memory 自動注入、oracle review の採否を再評価するとき。
- 特定の代替案の詳細を読む前に、対象ディレクトリ内の関連する設計判断記録へ進むとき。

## Do not read this when
- 現行の仕様、状態遷移、処理ループ、権限規則、feedback 報告基準を確認したいときは、対応する正本仕様を直接読む。
- 実装やテストの現在の挙動、具体的な修正手順、実際の ignore 判定を調べたいときは、対応する realization file やリポジトリ設定へ直接進む。
- 過去の不採用理由や設計判断の背景を必要としない一般的な案内では、このディレクトリを読む必要はない。

## hash
- 5ce81f7165ac735106e8957743573558e46db4a633c9ffda405499cb4d50172c

# `dev_rule`

## Summary
- cmoc 開発における環境構築・依存関係管理、コード設計とコーディング規則、テスト規約および品質検査の実行手順を定める正本文書群への入口。
- Python 仮想環境や pip 操作の条件、CLI と共通機能の分割方針、型注釈・import・docstring・命名などの実装規約を確認できる。
- pytest による決定論的テストと、実在の CLI・実推論を使う実経路統合テストの要件、検査選択・完了判定・結果報告の手順を確認できる。

## Read this when
- cmoc の開発環境を新規構築する、依存関係を追加する、または pip を操作する必要があるとき。
- CLI の責務分割、共通機能の配置、Python の実装規約や識別子・型注釈・docstring の扱いを確認するとき。
- テストの意味上の要件、実経路統合テストの成立条件、focused test・品質検査の選択、fresh な完了ゲート、結果報告の方法を判断するとき。

## Do not read this when
- 構築済み環境で通常の test や品質検査を実行するだけで、実行手順の確認が目的でないときは、テスト対象に対応する手順へ直接進む。
- 特定のテスト実装の期待動作だけを確認する場合は、テスト実装規約へ直接進む。
- Python 環境の構築や pip 操作を伴わない、個別の実装内容・アプリケーション仕様・CLI 利用仕様の確認では、この開発規約群を入口にしない。

## hash
- 1aa3c6f1966d3cabd7997e77064ba0b8c9549b4a160462ca04745d9f60213b21
