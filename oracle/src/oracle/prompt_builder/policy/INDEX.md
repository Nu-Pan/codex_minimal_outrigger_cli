# `conflict_resolution.py`

## Summary
- join 系の競合解消 prompt に共通で渡す agent 規定を構築し、両 branch の意図を保つ統合、必要な付随編集と検証、未解消の判断・報告の境界を定める。

## Read this when
- join の競合解消 agent に渡す共通規定や、解消完了・未解消の報告条件を確認または変更するとき。
- 競合箇所の選択に加え、関連ファイルの編集や検証をどこまで agent に任せるか確認するとき。

## Do not read this when
- 競合解消の意味基準そのものを変更するときは、参照先の正本仕様を読む。
- join 固有の merge 入力取得、Git 状態の読み取り、commit の指定、prompt 全体の組み立てを調べるときは、その処理を担う prompt 構築側へ進む。

## hash
- 78feb169eaa2b114c8a6602cdf03b24437314d08747d725a323d2a599cf84440

# `editor_input_handoff.py`

## Summary
- 明示的に選ばれた editor input handoff 規定を、agent prompt 用の構造化 policy として組み立てる。
- active target が指定された場合のガイド取得から項目別依頼の送信までの手順、agent の成果責務、失敗時の対応、権限境界を伝える。
- この規定を完全 prompt に含めるかは、呼び出し側の選択に委ねられる。

## Read this when
- handoff の利用条件、agent に指示する手順、失敗時の対応や権限境界を変更・確認するとき。
- editor input handoff 規定が完全 prompt に含まれる条件を追うとき。

## Do not read this when
- handoff 機能の意味仕様を確認・変更するときは、正本の app spec を読む。
- MCP 入力項目や受理条件を確認するときは、該当する input schema を直接読む。
- ガイドの文面や完全 prompt の雛形を確認するときは、ガイド構築定義を直接読む。
- 生成本文の見出し・配置、送信元情報や参照値の構築・検査を確認するときは、本文 builder と参照モデルを直接読む。
- MCP の公開、target の登録・探索・無効化、editor input file の書き込み処理を確認するときは、該当する runtime 実装と意味仕様を読む。

## hash
- 588d0d4741adaf6b19b64eb136eead75ebf20491ffe92f79cc74fca0f8279199

# `feedback_reporting.py`

## Summary
- 全 agent call の基礎規定として挿入する、feedback observation の報告指示文を構築する。報告条件の意味仕様や reporter の収集処理ではなく、agent に渡す文面を担う。

## Read this when
- agent 向けの feedback observation 報告指示の文面や構造を調整するとき。

## Do not read this when
- 報告対象の意味上の判定基準や収集契約を確認・変更するときは、feedback observation の正本仕様を読む。
- 完全 prompt の組み立て順や、この指示文の呼び出し箇所を追うときは、完全 prompt の builder を直接読む。

## hash
- 203fbeb6ca169491ad48cfd61c5d95aeff6128d33632b7b0d70e95f9e3ddf1c5

# `file_access.py`

## Summary
- FileAccessMode に応じて、agent の直接ファイルアクセスに関する共通制限文面と path placeholder を構築する。NO_POLICY では共通制限を返さない。
- 完全 prompt に組み込まれる file-access policy 断片の構築箇所であり、mode の選択や他の prompt policy の統合は担当しない。

## Read this when
- 各アクセス mode で agent に伝える読み書き制限の文面を確認・変更するとき。
- 共通制限を prompt に含める条件や、path placeholder の受け渡しを調べるとき。

## Do not read this when
- アクセス mode の意味や Codex CLI sandbox との対応を確認するときは、正本仕様から確認する。
- 個別の agent call がどの mode を選ぶかを調べるときは、その call の builder から確認する。
- 完全 prompt の構成や各 policy の統合方法を調べるときは、完全 prompt の構築箇所を直接読む。

## hash
- 2024227edecd081482ba2bc22f0eace6067cc3c7a3d4df39292d91c4f77837ad

# `index_entry.py`

## Summary
- INDEX.md エントリー生成時に適用する、ルーティング情報の内容要件と禁止事項をプロンプトへ組み立てる。

## Read this when
- 生成するエントリーの Summary、Read this when、Do not read this when に課す意味上の要件を見直すとき。
- エントリー生成時のプロンプトに、どの内容上の制約が加わるかを確認するとき。

## Do not read this when
- 個別の対象についてエントリーを作るときは、その対象の本文を直接読む。生成時の規定を確認する必要がなければ、この定義を読む必要はない。
- 索引の配置、出力形式、ハッシュ、または生成手順を確認するときは、索引全体の仕様を参照する。
- 生成 call の組み立て方、対象の指定、または起動設定を確認するときは、call の構築を担う箇所を参照する。

## hash
- 6bf595b53b34a59a30230606ab87ee397ff028ac5e22c6136c02e9d6c7a62baa

# `oracle.py`

## Summary
- oracle file を扱う agent call に組み込む規定を定義し、oracle doc と oracle src の責務境界・優先関係や、正本仕様断片を扱う際の制約を定める。

## Read this when
- oracle file を扱う agent call の指示文を変更・レビューするとき。
- oracle doc と、そこから詳細を委譲された oracle src の責務や優先関係を確認するとき。

## Do not read this when
- 特定の oracle file が定める具体的な仕様を確認するときは、その oracle file を直接読む。
- realization file を扱う agent call の規定を確認するときは、realization file 用の規定を読む。

## hash
- 4e4de41de95647dfcd55ce5e4287127cd05c7c08f0e5a399c7ba06cf9b39419d

# `realization.py`

## Summary
- realization file を扱う agent call に渡す policy 文面と、参照用の root path placeholders を組み立てる。
- oracle file の要求に沿った具体化、必要な実装だけを保つ方針、検証、正本の非複製を prompt policy として示す。意味仕様そのものの正本ではない。

## Read this when
- realization file 編集用 agent call に注入する方針や文面を変更・調査するとき。
- この policy が利用する root path placeholders の供給を変更・調査するとき。

## Do not read this when
- realization file の意味上の責務や判断基準を定義・解釈するとき。正本の app spec を読む。
- prompt 全体でこの policy を有効にする条件や配置順を変更するとき。prompt assembly の定義を直接読む。
- oracle file の編集方針や realization の適合性レビュー方針を扱うとき。それぞれの専用 policy を読む。

## hash
- 36a10fbf5477337cdb240ee63c42952b7161f28c1d08a218325c8afe3881f510

# `realization_findings.py`

## Summary
- oracle file と realization file の適合性について、所見の判断基準を agent 向け文面として構築する定義。
- realization 作業全般の方針ではなく、適合性に関する所見の範囲を確認する入口。意味仕様は oracle doc が所有する。

## Read this when
- 適合性レビューで、oracle file の明示要求との不整合や realization file 内の明白な致命的問題を所見対象とする基準を確認するとき。
- oracle file 自体の問題や、要求として明示されていない事項、すでに解消された問題を所見に含めるか判断するとき。
- prompt builder がこの適合性 policy をどう構成・適用するか追うとき。

## Do not read this when
- oracle と realization の分類や realization 作業全般の実装・検証方針を調べる場合は、それぞれの分類定義または realization 全般の判断基準へ進む。
- 適合性基準の意味仕様を理解・改訂する場合は、意味仕様を所有する oracle doc の適合性に関する節を読む。
- この policy の prompt への追加条件や連結位置だけを調べる場合は、prompt の構成側を読む。

## hash
- b531825f8f44927871a9b987eb21d9d6aef981e1207d9d654edfe6030b464f3e

# `routing.py`

## Summary
- 目次情報からリポジトリ内の参照先を選び、実本文を判断根拠とするためのエージェント向け routing 規定文面を構築する。対象領域が不明な場合の起点や、目次と本文の内容が異なる場合の扱いを、パスの文脈とともに prompt へ渡す。

## Read this when
- 作業対象に応じて目次情報を使う起点や、目次と実本文の優先関係を変更するとき。
- リポジトリ起点の情報を routing 規定文面へ渡す方法を変更するとき。

## Do not read this when
- 個々の目次エントリーの生成規則を変更するときは、その生成規定や目次仕様を直接確認する。
- 完全 prompt 内で routing 規定を有効にする条件や配置を変更するときは、prompt の構成処理を直接確認する。
- 個別ファイルの意味や最新状態を判断するときは、その実本文を直接読む。

## hash
- dcaa865be45b4a4daf2a6c19e7e4706655ea8fd54e91ff1dff23acc0577c7118
