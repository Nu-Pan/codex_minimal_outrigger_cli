# `acp_builder`

## Summary
- 個々の agent call に渡す prompt と実行パラメータを組み立てる。共通の呼び出し情報とファイルアクセスモードを定義し、作業ディレクトリ、構造化出力の利用、インデクシング事前処理、エディター入力の受け渡しなどを呼び出し種別に応じて設定する。
- quota 利用確認、目次エントリー生成、feedback issue の判定と修復、session join の衝突解消、TUI 起動、oracle の調査と編集、realization の追従や fork の要約・レビューに対応する builder 群への入口。

## Read this when
- これらの呼び出し種別について、agent に渡す作業内容や対象範囲、アクセスモード、作業ディレクトリ、構造化出力や事前処理の設定を調べる・変更するとき。
- 共通の呼び出しパラメータ定義、または特定操作向け builder の責務を確認するとき。

## Do not read this when
- Codex CLI の起動処理、実行時設定、または個別サブコマンドの入力取得・制御順序を調べるときは、呼び出し側の処理や実行設定を確認する。
- 共通 prompt policy の本文や組み立て方を調べるときは、各 builder が選択する共通 prompt 構築・policy 定義を確認する。
- サブコマンドの意図や業務上の手順そのものを確認するときは、その意味仕様を記述する oracle 文書を直接確認する。

## hash
- 0781e495a5330d8e854e6c252d0d48e9d64d26d3a163700b22cc842730efa045

# `editor_input_handoff`

## Summary
- editor input handoff の MCP 入出力契約と、handoff 本文・ガイドの構築定義を担う正本ソースの入口です。
- handoff 全体の運用仕様から参照される、契約と生成内容の詳細を確認する場所です。

## Read this when
- handoff MCP の入力説明や受理条件、結果形式を確認・変更するとき。
- 項目別入力と送信元情報からの本文生成や、受信先ガイドの構築を確認・変更するとき。

## Do not read this when
- target の登録・有効期間、処理手順、失敗時の扱いなど、handoff 機能全体の仕様を確認するときは、その機能の仕様書を直接読んでください。
- agent に渡す handoff instruction の利用条件・送信手順・責務を確認するときは、その instruction の文面定義を直接読んでください。

## hash
- a2a1263148e18bfbd7bc09d014034824d810a0f333b5cb8c958c0676e6ec0ee8

# `feedback`

## Summary
- 定義するのは feedback observation の agent 提出入力契約で、tool discovery と受け入れ検査が共通して参照する。

## Read this when
- feedback observation の提出データが満たす構造や制約を確認・変更するとき。
- reporter と collector で共有する入力検査の契約を確認するとき。

## Do not read this when
- 報告対象の判断基準や収集・保存の動作を確認するときは、feedback observation の正本仕様を読む。
- agent 向け報告指示の文面や prompt への配置を確認するときは、その生成を担う prompt builder を読む。

## hash
- 709d2b0ca7660b1772a43fe8fdaed710d40142564511ba28a435a49b6776aa67

# `other`

## Summary
- agent call の作業起点と Git worktree 情報からルートパスを導出し、プレースホルダー表記を解決する共通モデルを提供する。
- 階層文書、参照ブロック、コードブロック、規定文などを Markdown に描画するヘルパーを提供する。
- 文書参照のパスと参照箇所を保持し、単独または一覧形式の Markdown 表現へ変換する。
- リポジトリごとの並列数や Codex provider・call の設定値モデルと初期値を定義する。

## Read this when
- agent call の cwd や Git worktree から `repo-root`、`work-root`、`run-root` をどう決定・解決するか確認または変更するとき。
- 構造化された文書要素を Markdown に描画する方法を確認または変更するとき。
- 文書参照の保持方法や Markdown 表現を確認または変更するとき。
- リポジトリごとの設定モデルや、並列数・Codex provider・call 設定の初期値を確認または変更するとき。

## Do not read this when
- 特定の呼び出しがどの cwd を選ぶか、または個別コマンドの実行手順を調べるときは、その値や手順を決める呼び出し側へ進む。
- 設定の読み込み・検証・保存や、設定が実際の呼び出しに与える影響を調べるときは、それらを担う設定処理へ進む。
- 文書参照が agent handoff で持つ意味や使われ方を調べるときは、参照モデルではなく受け渡しの意味仕様へ進む。

## hash
- 265e7ab16ce97da75528f16976200e0f149bfec0d5cc8d000792a520a178f834

# `prompt_builder`

## Summary
- agent 向け構造化 prompt を組み立て、共通規定や選択された規定、呼び出し固有の依頼文面を集約する。
- 規定ごとの生成文面と placeholder の扱いに加え、エディタ起動前に人間へ表示する入力案内も定義する。

## Read this when
- agent call に渡す prompt の構成や、規定・依頼文面の組み込み方を調べる、または変更するとき。
- 生成される規定文、placeholder の扱い、エディタ起動前の案内の挙動を調べる、または変更するとき。

## Do not read this when
- 個々の規定の正本上の意味や優先関係を判断するときは、規定の意味仕様を直接確認する。
- どの呼び出しがどの prompt 構成を選ぶかを追うときは、呼び出し側の選択や制御を担う箇所から確認する。

## hash
- 8b52d93dc0305b481c83f78a1dc2d855eafb7d4fd2b5b7526c53bba7fe695609
