# `apply`

## Summary
- 現在、apply サブコマンドの実装ファイルはありません。

## Read this when
- apply サブコマンドの実装が追加された後、その内容を確認するとき。

## Do not read this when
- apply 以外のサブコマンドを扱うとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `doctor.py`

## Summary
- `cmoc doctor` サブコマンドの実装。CLI ランタイム経由で doctor preprocess を 1 ステップ実行し、完了後に repo_root を表示する。doctor コマンドの実行経路と preprocess 呼び出しの入口として扱う。

## Read this when
- doctor サブコマンドの実装や実行手順を変更・調査するとき
- doctor preprocess の呼び出し位置、実行ステップ、表示内容を確認するとき

## Do not read this when
- doctor preprocess 自体の仕様や処理内容を確認したいときは、参照される oracle/doc/app_spec/doctor_preprocess.md を直接読む
- CLI ランタイム共通処理の仕様や実装だけを確認したいとき

## hash
- 48cc149773f0620f64d4650bed55bdb7b42dada088e55d312892186978176836

# `feedback`

## Summary
- feedback サブコマンドの実装をまとめたディレクトリ。feedback サブコマンドの処理を確認・変更するときの入口で、個別の report 処理や state・agent 契約の詳細へ進むための起点となる。

## Read this when
- feedback サブコマンドの挙動や実装を確認・変更するとき。
- report の publication、diagnostic、checkpoint 再開、candidate 変換、verification、generation 切替を調査するとき。

## Do not read this when
- feedback 以外のサブコマンドを扱うとき。
- feedback state の正本データ構造や永続化契約だけを確認する場合。
- normalization／verification agent の prompt、Structured Output schema、builder の契約だけを確認する場合。
- report の表示形式だけを確認する場合。

## hash
- 86ae1386fe29176843ea39d38e0bdd81a436d24385d32e09b07a2147b7873163

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
- oracle 系サブコマンドの実装をまとめるディレクトリ。oracle の編集・調査・レビューに関する各サブコマンドと、その実行フローを支える補助実装への入口となる。

## Read this when
- oracle 系サブコマンドの構成や、編集・調査・レビューの実行経路を確認するとき
- oracle review の対象列挙、レビュー loop、レポート生成、INDEX 差分の統合など、oracle review を支える実装の所在を確認するとき

## Do not read this when
- 特定の oracle サブコマンドの詳細な挙動を確認する場合は、該当する個別実装を直接読む
- oracle の編集・調査・レビューに関する契約やプロンプト内容そのものを確認する場合は、対応する oracle 仕様を直接読む
- 共通のプロンプト入力処理や Git・パス処理の詳細だけを確認する場合は、該当する専用実装を直接読む

## hash
- 5a5520709dac251611061fcc643f35d78201fea6dc38ea173acca29d5e77377f

# `realization`

## Summary
- realization workload サブコマンドのパッケージ入口で、配下の apply と refactor の処理へ進むための起点。apply workload の実行フローや refactor fork のライフサイクルを確認する際に対象を選ぶ。

## Read this when
- realization workload サブコマンドの実装構成や入口を確認するとき。
- apply workload または realization refactor の処理を調査・変更するとき。

## Do not read this when
- realization に関係しない処理を確認するとき。
- 共通ライフサイクル、CLI 契約、INDEX 更新規則など、より直接対応する共通実装や正本仕様を確認するとき。

## hash
- 69e98a3c5cc5c69a34276cc6e1e7368b204ef4f49af540303b1de06d598a2773

# `review`

## Summary
- review サブコマンドの realization 実装を配置するディレクトリ。現在は実装本文がなく、レビュー処理の具体的な入口として参照できる下位要素はない。

## Read this when
- review サブコマンドの実装ファイルを追加・変更する場所を確認するとき。

## Do not read this when
- oracle review の処理内容や仕様を調べるときは、対応する oracle 実装・仕様文書を直接読む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `run`

## Summary
- 編集 run の共通 lifecycle サブコマンドと、その実装・互換 shim へのルーティング入口。active run の停止・統合・cleanup、共通 lifecycle helper、report writer の責務を確認するために読む。
- active editing run を状態に応じて停止し、process、worktree、branch、state、tracking を cleanup する abandon 処理。停止失敗や cleanup 未完了時の資源保持、lifecycle report の生成も扱う。
- active run の差分を検査して session branch へ merge し、INDEX.md conflict の再生成、post-join hook、refactor state 同期、report 保存、失敗時 rollback、cleanup を行う join lifecycle。
- 共通 editing run lifecycle 実装を旧 import path から再公開する互換 shim。共通処理そのものではなく、旧参照との互換性や canonical 実装への移行を確認するときに読む。
- 共通 run report writer を旧 import path から再公開する互換 shim。lifecycle report または fork report の参照互換性を確認するときに読む。

## Read this when
- editing run の停止、統合、失敗復旧、cleanup、process tracking、state 同期、lifecycle report の挙動を調査または変更するとき
- run join における想定外差分、force-resolve、INDEX.md 限定 conflict 処理、post-join hook、refactor state 同期を確認するとき
- 旧 import path の lifecycle helper または report writer の互換性を確認するとき

## Do not read this when
- editing run 以外のサブコマンドを扱うとき
- 特定の共通 helper、Git 操作、state 管理、report writer の canonical 実装詳細だけを確認するときは、それぞれの commons 側実装を直接読む
- run の workload 固有処理や CLI 一般起動処理だけを調査するとき

## hash
- e2d8137bb96c1def3e634c2c07b2f4a61f95b3a1aede98383871042558d0b68c

# `session`

## Summary
- session サブコマンドの実装パッケージ。session の各ライフサイクル処理を確認・変更する際の入口であり、開始・継続・完了・破棄に相当する個別処理へ進むためのルーティングを担う。

## Read this when
- session サブコマンドの実装構成や、fork・join・abandon の各処理の入口を確認するとき。
- session の branch・state を扱うライフサイクル処理を確認・変更するとき。

## Do not read this when
- session 以外のサブコマンドを扱うとき。
- 特定の session 処理の詳細を確認する場合は、該当する個別サブコマンド実装を直接読む。
- session state の一般定義や共通 runtime の仕様だけを確認する場合は、それぞれの正本仕様・共通実装を直接読む。

## hash
- eca8a6509002c96e29d6832c8753e099c704b3a21f6823212b83ce7d5dc542ad

# `tui.py`

## Summary
- `cmoc tui` サブコマンドの実行入口と本体処理を担う。プロンプト編集用入力を準備・収集・確定し、固定パラメータで Codex TUI を起動する。

## Read this when
- `cmoc tui` の起動フロー、プロンプト編集、Codex TUI 起動処理を変更または調査するとき。
- TUI 実行前の indexing preflight、ログ前チェック、サブコマンド進捗管理の連携を確認するとき。

## Do not read this when
- TUI 起動パラメータの構築仕様だけを確認する場合は、パラメータ builder の実装を直接読む。
- プロンプト入力・保存・確定の詳細仕様だけを確認する場合は、prompt editor input 関連の実装または参照された正本仕様を直接読む。
- Codex TUI 自体の実行実装や共通 CLI ランタイムの挙動だけを確認する場合は、各ランタイム実装を直接読む。

## hash
- c544eb81e5f42cc514f3b4ffc390709325ed6cdb0cdd79ec833f4beff51e1ffa
