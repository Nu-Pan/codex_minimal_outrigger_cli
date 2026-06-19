# `fork`

## Summary

- この `<cmoc-root>/oracle/src/agent_call_parameter/apply/fork` ディレクトリのルーティング文書で、`file_audit_finding.py`、`fixing_point_refinement.py`、`fixing_point_application.py`、`change_summary.py` への入口です。
- `file_audit_finding.py` / `fixing_point_refinement.py` / `change_summary.py` は Structured Output schema を伴う読み取り中心の呼び出しを案内し、`fixing_point_application.py` は schema を使わず realization file を修正する書き込み中心の呼び出しを案内します。
- `cmoc apply fork` の 4 つの主要段階である、ファイル単位監査、要修正点の整理、要修正点 1 件の実装修正、変更要約生成の分岐先を整理する目次です。

## Read this when

- `cmoc apply fork` の各段階で、どの prompt と Structured Output schema が使われるかをまとめて確認したいとき。
- ファイル単位監査、要修正点リスト改善、要修正点 1 件の実装修正、作業レポート用変更要約のどれに進むべきか迷ったとき。
- `fork/INDEX.md` を追加・修正する前に、この階層の役割分担を整理したいとき。

## Do not read this when

- `cmoc apply fork` 以外のサブコマンドや、`review` / `indexing` / `session` 系の agent call parameter を探しているとき。
- 対象ファイルがすでに分かっていて、`file_audit_finding.py`、`file_audit_finding.json`、`fixing_point_refinement.py`、`fixing_point_refinement.json`、`fixing_point_application.py`、`change_summary.py`、`change_summary.json` を直接開くとき。
- この階層ではなく、`apply/` 全体の入口や `oracle` 全体の共通規約だけを確認したいとき。

## hash

- a175c279b19897d75f7614520aff0b5f11800414fd6be3e7a92edf2d7df7cb0a
