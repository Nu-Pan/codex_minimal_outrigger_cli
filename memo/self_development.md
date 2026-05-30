# `cmoc` による `cmoc` の自己開発のやり方

## 前提

- Ubuntu 24.04 LTS + bash 環境を想定
- cmoc を stage0, stage1 に分けて、 cmoc-stage0 を使って cmoc-stage1 の開発を行う

## セットアップ

1. Codex Minimal Outrigger CLI を `~/codex_minimal_outrigger_cli_stage0`, `~/codex_minimal_outrigger_cli_stage1` の二箇所に Clone する
2. stage0 の方で初期セットアップを行い `~/codex_minimal_outrigger_cli_stage0/bin/cmoc` が実行可能な状態にする
3. `~/bin/cmoc-stage0` を作成する
```bash
mkdir -p ~/bin
cat > ~/bin/cmoc-stage0 <<'EOF'
#!/bin/sh
exec "$HOME/codex_minimal_outrigger_cli_stage0/bin/cmoc" "$@"
EOF
chmod +x ~/bin/cmoc-stage0
```
4. `~/.bashrc` を手動で編集し、以下を追加する
```bash
# cmoc stage0 path
case ":$PATH:" in
  *":$HOME/bin:"*) ;;
  *) PATH="$HOME/bin:$PATH" ;;
esac
export PATH

# cmoc stage0 completion
_cmoc_stage0_completion() {
    local IFS=$'\n'
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _CMOC_COMPLETE=complete_bash cmoc-stage0 ) )
    return 0
}
complete -o default -F _cmoc_stage0_completion cmoc-stage0
```
5. `~/.bashrc` を再ロード (ターミナル再起動とかで良い)


## 基本的なワークフロー

1. `cmoc-stage0` を使って stage1 上で cmoc 開発フローを１周 (e.g. `cmoc-stage0 branch` から `cmoc-stage0-merge` まで) 回す
2. stage1 上で master branch を remote へ push
3. stage0 側で remote の master branch を pull
4. 先頭に戻る

## stage0 cmoc が動かなくなった場合

- stage0 上で Codex CLI を直接使って修正を行う

## 単一リポジトリ上での自己開発は却下した

- 自己開発で一番怖いのは「cmoc の作業中に cmoc が自身を編集・破壊してしまう」こと
- 次に怖いのは「使用する cmoc のバージョンが途中で変わってしまい、挙動・契約が一致しない」こと
- よって cmoc セッションを join するまでは、使用する cmoc のバージョンは固定し無ければならない
- もしも単一リポジトリで自己開発を行うと、 cmoc 開発ワークフローに従って `<cmoc-managed-branch>` 上での fork, merge が起こるごとに cmoc の挙動が変わってしまう
- よって、安全に開発するには stage0, stage1 に分けるしか無い
