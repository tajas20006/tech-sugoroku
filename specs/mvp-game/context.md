# 実装コンテキスト

## 対象

AWS 学習すごろくのローカル2人対戦 MVP を実装する。

## 現在の構成

- Python 3.14 以上、Flet 0.86 以上。
- 実装開始前の `main.py` は `Hello from tech-sugoroku!` を表示するだけ。
- 画像は `assets/images/` に配置済み。
- クイズとメッセージは `assets/` 配下の Markdown で管理済みだが、MVP はまず組み込みの代表問題を使用する。

## 実装方針

- ルールは UI から独立した `game.py` に置き、pytest で検証する。
- `main.py` は Flet の画面とイベント処理だけを担当する。
- 追加ライブラリは導入しない。既存の Flet と pytest で完結する。
- Flet は Apache-2.0 ライセンスであり、商用利用可能な既存依存として使用する。

## 依存関係

```text
main.py (Flet GUI)
  └─ game.py (盤面、プレイヤー、ターン、クイズ、アイテム)
       └─ tests/test_game.py
```
