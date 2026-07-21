---
name: run-cmoc-tests
description: cmoc リポジトリ固有のテスト実行環境を準備し、focused test、full pytest、Ruff、mypy の対象を選び、通常の検査は sandbox 内、GPU integration test だけは限定した sandbox escalation で検証する。cmoc の実装・テスト変更後にテストや品質検査を実行するとき、test-local Ollama cache を維持したまま pytest の一時領域を隔離するとき、または cmoc のテスト失敗を再現・診断するときに使用する。
---

# cmoc のテストと品質検査を実行する

## 正本と責務を確認する

- 最初に `oracle/doc/dev_rule/development_environment.md` と `oracle/doc/dev_rule/test_rule.md` を読む。
- Python 共通の品質ゲートには `python-dev-skill` を併用し、その skill を編集しない。
- テストの正しさ、test-local Ollama、cache、timeout、および backend の要件は oracle file を正本とする。この skill から要件を補完または変更しない。
- この skill では cmoc 固有の実行対象、一時領域の準備、および実行時アクセスだけを扱う。

## 検査対象を選ぶ

- repository root を cwd とする。
- focused test は `test/INDEX.md` から変更対象に対応する test file を選ぶ。
- Ruff の first-party 検査対象には `src`、`oracle/src`、`test` を渡す。
- mypy の検査対象には `src`、`oracle/src` を渡す。pytest の import path を前提とする `test` は、project の mypy 対象へ追加しない。
- `gpu_integration` marker は test-local Ollama による GPU-only 実推論を必要とする test だけを選択する。
- full pytest は `test -ra -m "not gpu_integration"` と `test -ra -m gpu_integration` の和集合とし、どちらも fresh に実行する。

## pytest の一時領域と cache を準備する

- pytest の隔離だけを目的として run 固有の `TMPDIR` を設定せず、pytest の case/session 用一時領域を使用する。
- run 固有の `TMPDIR` が既に設定されているか、別の理由で必要な場合は、pytest 起動前に `test_rule.md` が定義する cache root override 環境変数へ、run に依存しない system temporary directory 上の path を設定する。
- system temporary directory の基準を取得してから `TMPDIR` を設定する。既に上書き済みなら、開発環境規則が指定する Python を `TMPDIR`、`TMP`、`TEMP` なしで起動し、`tempfile.gettempdir()` の値を取得する。
- cache path は `test_rule.md` の安定性と namespacing の要件に従って選び、この skill 独自の命名規則を設けない。
- archive や model を手動で事前配置せず、cache hit と cache miss の処理を realization test の helper に任せる。

## GPU integration test だけを sandbox 外で実行する

- `gpu_integration` 以外の pytest、Ruff、および mypy は repository 所定の sandbox 内で実行する。
- `gpu_integration` を選択する pytest command は sandbox 内で試行せず、最初の実行から shell/exec tool の command 単位 sandbox escalation を要求する。
- Codex の unified exec tool では、対象 command に `sandbox_permissions=require_escalated` を指定し、test-local Ollama が WSL GPU device を使用するために必要だと justification に明記する。
- escalation は pytest command とその descendant process だけへ限定する。agent call 全体へ `danger-full-access` を指定せず、prefix allow rule の作成または永続化を要求しない。
- escalation が利用不能、拒否、または review 失敗になった場合は同じ test を sandbox 内で代替実行せず、GPU test と full test が未完了だと報告する。
- sandbox 外で起動した test が host の GPU 利用不能を理由に skip した場合は、skip と具体的な理由を報告する。

## system temporary directory へのアクセスを限定する

- この repository 所定の test・品質検査を実行している間だけ、その test・tool が作成したか明示的に割り当てられた system temporary directory 上の一時ファイルと cache を読み書きしてよい。
- escalated GPU test の間だけ、test-local Ollama が GPU device を使用してよい。関係のない device や host file を探索または操作しない。
- この例外を、関係のない一時ファイルの探索・読み書き、または repository 外への作業成果物の配置に使用しない。
- file access mode ごとの oracle file と realization file の読み書き境界は変更しない。

## 検証を実行する

1. 開発環境規則どおりに interpreter と依存関係を確認する。
2. 変更中は、選択した focused test と変更した first-party path に対する品質検査を `python-dev-skill` の方法で実行する。
3. focused test が `gpu_integration` の場合も、その test を選択する最初の command から sandbox escalation を要求する。
4. 完了時は、上記の tool ごとの対象、sandbox 内の非 GPU pytest、および escalated GPU pytest を使い、`python-dev-skill` の完了ゲートを fresh に実行する。
5. cache 状態や sandbox 内の GPU 可視性の事前判定を実行手順に加えず、選択した test command から realization test の helper を起動する。

## 結果を報告する

- 実行した command、終了状態、skip、失敗した検査を報告する。
- sandbox 内の非 GPU pytest と escalated GPU pytest の結果を分けて報告する。
- full pytest を実行していない場合や、Real Codex CLI を使う test が skip された場合は、その事実と理由を明記する。
