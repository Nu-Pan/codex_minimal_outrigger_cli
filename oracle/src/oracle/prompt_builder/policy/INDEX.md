# `conflict_resolution.py`

## Summary
- join の内容競合を解消する agent 向け共通方針を構築する。統合・検証の判断基準、管理操作との境界、完了報告の内容を定める。

## Read this when
- run join または session join の競合解消で、両側の意図を保つ統合や付随編集、検証、未解消時の報告に関する共通指示を確認・変更するとき。
- 完全 prompt に組み込まれる競合解消方針の文面を調べるとき。

## Do not read this when
- 統合の意味上の判断基準を確認するときは、参照先の正本仕様を読む。
- 各 join 固有の編集範囲や、commit 参照入力を含む競合解消 prompt の構築を確認するときは、それぞれを定める仕様または prompt 構築定義へ進む。
- 一般的な realization の扱い方針やアクセスモード別の制限を確認するときは、それぞれの共通方針を読む。

## hash
- 968850dfd80be0562fe8f61355ec99e024e6e1251edd5b9d1f0097a0d281dfb0

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
- FileAccessMode とパス文脈に応じて、エージェント向けのファイルアクセス制限をプロンプト用に組み立てる。共通禁止事項に mode 別の追加制限を加え、規定のない mode では何も返さない。
- アクセス規定の文面や mode ごとの適用内容を変更するときに確認する実装箇所。

## Read this when
- プロンプトに含める直接ファイルアクセスの共通制限や、各 mode での oracle file・realization file のアクセス制限を変更するとき。
- 制限規定を出さない mode の扱い、または規定に付けるパス置換情報やプロンプト上の見出しを変更するとき。

## Do not read this when
- ファイルアクセス mode の正本上の意味や sandbox との責務境界を変更するときは、ファイルアクセス制限を定める正本仕様を読む。
- 完全なプロンプトへの規定の組み込み方を変更するときは、プロンプト全体を組み立てる箇所を読む。個別の呼び出しでどの mode を選ぶかを変更するときは、その呼び出しのパラメータを構築する箇所を読む。

## hash
- 9edb86dd8a944a72920dbb83935ae4bc8c426b20e376fa26e6a800cbfc5e7e83

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
- agent call 向けの routing 規定文面と work-root placeholder を構築する。
- 文書検索の利用可否に応じて案内を切り替え、検索手段の選び方、現在原文の確認、閲覧制限の維持、検索失敗と正常なゼロ件の区別を伝える。
- 検索結果を参照先選びの手掛かりとして扱い、oracle/src と oracle/test は直接参照または既存の文字列検索で確認するよう案内する。

## Read this when
- agent call に利用可能な検索手段や、検索結果と現在原文の扱いを伝える routing 規定の構築・変更を調べるとき。
- 文書検索が有効な場合と無効な場合で、agent 向けの案内がどう切り替わるか確認するとき。

## Do not read this when
- 検索対象や閲覧範囲の意味仕様、索引同期、検索結果の生成を調べる場合。agent 向け文面の構築ではなく、文書検索の仕様または検索実装へ進む。
- 直接ファイルアクセス制限や oracle・realization の取扱い規定を調べる場合。routing 文面の責務外なので、それぞれの policy へ進む。
- routing 規定を完全 prompt に含める条件や配置を調べる場合。prompt 全体を組み立てる箇所へ進む。

## hash
- a7535416b2a7feba073d107a085ff32f0e9e2b6e7a53e15510704c5b75172696
