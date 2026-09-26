# `basic.py`

## Summary
- エージェント呼び出しで共有するアクセスモード、文書検索範囲、呼び出しパラメータの型を定義する。各 call builder が共通設定を組み立てる際の入口。

## Read this when
- 複数の call builder に共通するパラメータ項目や任意設定を変更するとき。
- アクセスモードの区分や、呼び出し元が指定する文書検索範囲の表現を変更するとき。

## Do not read this when
- 特定の call の prompt やアクセスモード、検索範囲などの設定だけを変更するときは、その call の builder を確認する。
- アクセス制限や検索 routing の prompt 文面だけを変更するときは、該当する prompt builder を確認する。

## hash
- a39697df273e3f9c8effb0f64de20ec98a5d623d6ddb4b17ae6787134efe80a9

# `feedback`

## Summary
- feedback issue を扱う二種類の agent call の prompt と起動 parameter を構築する。構造化 observation と絞り込み済み候補の同一性を判定する処理と、正規化済み issue 一件を確認し、realization file の修正と検証を行う処理への入口。
- 前者は読み取り専用、後者は realization file の編集を許可する呼び出しとして定義されている。issue の同一性判定や修正時の作業範囲・検証結果の扱いを調べる際に参照する。

## Read this when
- 構造化 observation と絞り込み済み既存候補を比較する判定方法や、その呼び出しに渡す指示・参照範囲を変更または確認するとき。
- 正規化済み issue 一件の現在状態を確認し、安全な realization 修正と検証を依頼する方法を変更または確認するとき。

## Do not read this when
- 新しい observation の収集・提出や、既存候補の検索・絞り込みなど、これらの呼び出しに入力が渡る前の feedback 処理を調べるときは、その工程の担当箇所を直接読む。
- prompt の動作ではなく、feedback の意味仕様や出力形式の制約だけを確認するときは、それぞれの仕様または Structured Output schema を直接読む。

## hash
- bf99068d19b6939d934768ef3fe2c795cfaf4ebe36d2d861a51f859da676af79

# `indexing`

## Summary
- 対象の内容を追加文面として埋め込み、INDEX エントリー生成 agent 用の task と完全 prompt を組み立てる。
- 対象パスを call 固有の context で解決し、読み取り専用アクセスと構造化出力の設定を含む起動パラメータを作る専用 builder。

## Read this when
- INDEX エントリー生成 call に固有の指示、対象内容の渡し方、アクセスモード、構造化出力の設定を変更または調査するとき。
- この call の cwd と対象パス解決から、返される起動設定までを追うとき。

## Do not read this when
- 他の agent call にも共通する完全 prompt の合成、ファイルアクセス規定、パスモデル自体を変更するときは、それぞれの共通実装を直接読む。
- インデックス対象そのものの内容や振る舞いだけを確認・変更するときは、対象本文を直接読む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `oracle`

## Summary
- oracle向け agent call の prompt と起動パラメータを用途別に構築する領域です。編集、調査、レビュー関連の処理へ進む入口になります。

## Read this when
- oracle file の編集 call が使う指示、編集境界、差分確認の扱いを調べるとき。
- oracle file の調査 call が使う読み取り専用指示や TUI 起動設定を調べるとき。
- レビュー結果の列挙、検証、判断、統合に関する処理を調べるとき。

## Do not read this when
- oracle サブコマンドの選択、引数処理、実行の流れを調べるときは、コマンド側の実装から確認するとき。
- 複数の呼び出しで共有する ACP パラメータ型や prompt 組み立て規則そのものを調べるときは、共通ビルダーから確認するとき。
- oracle file の規範的な意図や要求を確認するときは、該当する仕様本文から確認するとき。

## hash
- 1e15ca1ae94e6bbcbdacdb6098d86e3de0efbcdbf16a324790f202c0673be8e5

# `quota_probe.py`

## Summary
- Codex CLI の quota 利用可能性確認 probe について、agent call の prompt と builder レベルの起動パラメータを組み立てる。
- probe の呼び出し構成を変更するときの入口であり、回復処理の判断規則そのものは定義しない。

## Read this when
- quota availability probe の prompt や read-only 実行、作業ディレクトリ、文書検索設定などを変更・確認するとき。
- quota probe 専用の呼び出しパラメータを調べ、他の agent-call builder と役割を切り分けるとき。

## Do not read this when
- probe の実行条件、成功判定、待機・再開など quota や一時障害の回復判断を変更するときは、回復規則の正本を読む。

## hash
- e7bce49198a9e6d20cffcc3a31c235a4b4e5f0018c9ccbebb34d82f5ba15f291

# `realization`

## Summary
- realization の apply と refactor fork に渡す agent call の prompt と起動条件を組み立てる。
- apply の差分に基づく realization 追従と、refactor の変更要約・ファイル単位の調査修正を扱うため、これらの call の指示や閲覧範囲を調べる入口となる。

## Read this when
- commit 範囲で指定した oracle の変更を realization 全体へ反映する call の構築条件を調べるとき。
- refactor fork の変更要約、または対象ファイルを起点に所見を調査・修正する call の指示や権限を調べるとき。

## Do not read this when
- oracle の編集・レビュー、feedback の処理、session の統合など別種の agent call を調べるときは、それぞれの call 構築箇所を直接確認する。
- fork や commit 範囲の準備、call の実行・結果処理を追うときは、これらの builder の呼び出し元を確認する。

## hash
- b2396faac73062045609b90ef95931319ba155f6cfd034a3a29b038c16292fde

# `run`

## Summary
- run のマージ競合解消 call を組み立てる入口。進行中の session worktree と呼び出し元が確定した閲覧範囲を使い、封印済み feedback 結果がある自動 join には追加の指示と参照を組み込む。

## Read this when
- run の成果を session に統合する call の構築や、適用される作業範囲を確認するとき。
- feedback 自動 join で、封印済み結果を call に渡す方法を確認するとき。

## Do not read this when
- run と session に共通する競合解消 prompt の構築や統合手順を確認するときは、共通 prompt builder を読む。
- 封印済み feedback 結果の分類や join 後の扱いに関する正本仕様を確認するときは、該当する oracle 文書を読む。

## hash
- 0464020a8c5a13458d30fc56d52a713016fc94f2992049a43a64c27fd9724afc

# `session`

## Summary
- session の変更を home branch に統合する際の、競合解消 agent call の構築を担う。
- home worktree を統合先として、session join 固有の commit、アクセス範囲、共通 prompt を組み合わせる実装への入口。

## Read this when
- session の変更を home branch に取り込む call の構築条件や、その調整箇所を調べるとき。

## Do not read this when
- run の成果を session に取り込む処理を調べるときは、run join 側の対象へ進む。
- 競合解消 prompt の共通内容や共通 policy を調べるときは、それぞれの共通定義を直接読む。

## hash
- 1b7676666d9372bc7e76cb4e102dd4da0d383287ed6e810b08587f7a69b86a58

# `tui`

## Summary
- 一般の `cmoc tui` 向けに、ユーザー入力と呼び出し側が確定した閲覧範囲から、cmoc の各種方針を含む完全プロンプトと Codex CLI TUI の起動設定を組み立てる。
- ユーザーの作業指示を受けて起動する TUI 呼び出しの入口であり、oracle file の調査に特化した読み取り専用 TUI 呼び出しとは目的とアクセス境界が異なる。

## Read this when
- 一般の `cmoc tui` に渡すユーザー入力のプロンプトへの組み込み方や、呼び出し側が選んだ閲覧範囲の反映を確認・変更するとき。
- 一般の TUI 呼び出しに適用するリポジトリ書き込み方針や、editor input handoff の設定を追うとき。

## Do not read this when
- oracle file に関する調査指示と読み取り専用の境界を持つ専用 TUI 呼び出しを調べる場合は、その調査用 builder へ進む。
- 呼び出しパラメータやファイルアクセスモードなど共通の型定義を確認する場合は、基礎型定義へ進む。
- 完全プロンプトの共通組み立てや各方針の文面を調べる場合は、共通 prompt builder や該当する方針定義へ進む。

## hash
- c26472d2c2eec14076c44546c8189b6af01f6f555f6f123be4d56e7c71a74c17
