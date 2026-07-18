# `apply`

## Summary
- apply サブコマンドの実装パッケージ。abandon、fork、fork report、join の処理を扱い、apply run の開始からレビュー・修正、差分 commit、merge、report 保存、state 更新、process・worktree・branch cleanup までの実装入口となる。

## Read this when
- apply サブコマンドの実装を確認または変更するとき。
- apply run の lifecycle、state・process tracking、worktree・branch 操作、差分処理、report 生成、join・abandon の挙動を調査するとき。

## Do not read this when
- apply 以外のサブコマンドだけを扱うとき。
- 共通 runtime、Git、worktree、Codex 実行基盤の実装だけを変更・調査するときは、対応する共通実装を直接読む。
- apply fork 内のレビュー・修正プロンプト生成や report 内容だけを扱うときは、対応する下位実装を直接読む。

## hash
- 5f2275d9b011172ec29ff2fb2afa5fe73a6fa692c5de562481b35860e11e2fa4

# `doctor.py`

## Summary
- doctor サブコマンドの実装。CLI runtime を介して doctor 用の preprocess 処理を明示的に実行する。

## Read this when
- doctor サブコマンドの動作や preprocess 呼び出しを確認・変更するとき。

## Do not read this when
- doctor 以外のサブコマンドを扱うとき。preprocess の共通実装自体を確認するときは、共通 runtime preprocess command の実装を直接読む。

## hash
- 9324a8b1f2f1bbd3a83adfb61690e64ff7e1f6502e165e208c84e2cefbd35980

# `eval_oracle.py`

## Summary
- want を書き出した oracle を、oracle review と同じ評価経路へ渡す実装。評価対象の scope を受け取り、oracle review 実装へ委譲する。

## Read this when
- oracle に記述した want の評価経路や、oracle review と同じ評価処理を確認・変更するとき。

## Do not read this when
- oracle review 自体の評価ロジックを変更するときは、直接 oracle review の実装を読む。
- oracle の検討方針や評価基準を確認するときは、対応する oracle 文書を直接読む。

## hash
- 4a5d221c70ba607bc460b99a70f7d0c385eb3115c40668c54aeecd7cf6820461

# `indexing.py`

## Summary
- `cmoc indexing` サブコマンドの CLI 実行入口。worktree の安全条件を確認し、ロック下で INDEX.md の更新と差分 commit を実行する。

## Read this when
- `cmoc indexing` の実行フロー、worktree 前提条件、インデックス更新・commit 処理を変更または調査するとき。

## Do not read this when
- インデックス更新の具体的な処理や commit の実装自体を調査するときは、`commons.indexing` の実装を直接読む。
- 他のサブコマンドの CLI 実行フローだけを調査するとき。

## hash
- 648fe512e7039f2060fbe5969945f9992a0b8b3697e92d2cbbf949083d8804ce

# `oracle`

## Summary
- oracle 系サブコマンドをまとめる package。oracle 編集・レビューの CLI 実装と、レビュー対象列挙、ループ制御、パス解決、レポート生成、INDEX 更新などの下位処理への入口を提供する。

## Read this when
- oracle 系サブコマンドの package 構成や、編集・レビュー機能の実行入口を確認するとき。
- oracle review の対象列挙、レビュー制御、パス解決、レポート生成、INDEX 更新の担当モジュールを特定するとき。

## Do not read this when
- 特定の oracle サブコマンドや下位処理の詳細だけを確認・変更するときは、該当する個別モジュールを直接読む。
- oracle file の内容やレビュー対象そのものの仕様を確認するとき。

## hash
- 7b0f992e63ab6481d9a385d1f5fe6ead3e7d9ead7b8b22036b5c8739de62dfd5

# `review`

## Summary
- review サブコマンドの realization 実装を配置するディレクトリ。現在は実装本文がなく、レビュー処理の具体的な入口として参照できる下位要素はない。

## Read this when
- review サブコマンドの実装ファイルを追加・変更する場所を確認するとき。

## Do not read this when
- oracle review の処理内容や仕様を調べるときは、対応する oracle 実装・仕様文書を直接読む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `session`

## Summary
- session サブコマンドの実装パッケージ。fork、join、abandon の各 session 操作に関する CLI 実装を確認する入口。

## Read this when
- session サブコマンドの実装や構成を確認・変更するとき。
- session branch、session state、cleanup、merge、rollback など session 操作の挙動を調査するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- 共通の git 操作、state 操作、Codex 実行規則、session データモデル自体を直接確認するとき。

## hash
- fd4b0da87a48090397a866c729c2b89e9e18e7a38833e92107be89c7220385bd

# `tui.py`

## Summary
- `cmoc tui` の CLI 実行経路を担当する実装。プロンプト入力、実行パラメータ解決、TUI 用 AgentCallParameter の構築、Codex TUI 起動までを統合する。TUI のパラメータ解決や起動処理の流れを確認・変更するときの入口。

## Read this when
- `cmoc tui` の実行フロー、プロンプト編集入力、解決済みパラメータからの TUI 起動パラメータ構築を確認するとき
- TUI で許可するファイルアクセスモードや、設定された oracle・realization standard の反映を変更するとき
- TUI 起動前後の CLI runtime、ログ、作業ルートの扱いを確認するとき

## Do not read this when
- TUI の低レベルな起動パラメータ生成だけを変更する場合は、TUI builder の実装を直接確認する
- TUI 用パラメータ解決のプロンプトや許可モード定義だけを変更する場合は、resolve parameter 側を直接確認する
- プロンプト編集そのものの入力処理だけを変更する場合は、prompt editor input 側を直接確認する

## hash
- bc6c3be08640a1000dcead34a380e970ba103be1b1fd792bea3cc1579a1db2d3
