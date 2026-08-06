# DDD リファクタリング: コンテキストとドメイン分析

## 目的と範囲

既存 MVP の振る舞いと Flet 演出を維持しながら、ゲームルール、ユースケース構築、外部データ取得、表示を明確に分離する。モードは auto とし、判断は本書と `progress.md` に記録する。

## 現状分析

- `game.py` はドメインモデル、盤面設定、ゲーム進行、ランダムメッセージ、Markdown パーサーを同時に担当している。
- `main.py` は Flet 表示と演出を担当する一方、クイズファイルの場所と `Game` の生成方法も知っている。
- `tests/test_game.py` は主要ルールを 18 ケース、`tests/test_main.py` は Flet API と演出要素を 1 ケースで固定している。
- ベースラインは `pytest` 19 件成功、`ruff` 成功。作業開始時の Git ワークツリーはクリーン。
- Python 3.14 / Flet 0.86.5 以上。追加依存は不要。

## ユビキタス言語

| 用語 | 意味 |
| --- | --- |
| 対戦セッション | 2 人分の状態、現在ターン、未解決クイズ、勝者を含む 1 ゲーム |
| プレイヤー | 位置、クレジット、所持品、認定バッジ、一時効果を持つ主体 |
| ターン | 能動アイテムを最大 1 個使用し、サイコロ移動と停止イベントを解決する単位 |
| 盤面 | 0〜59 の位置、マス種別、支払日の配置を定義する不変ルール |
| 支払日 | 停止・通過の双方で支払いを要求し、不足時に直前チェックポイントへ戻す境界 |
| 問題デッキ | 通常／資格試験ごとに、使い切るまで同じ問題を出さない集合 |
| アイテム | 能動効果または自動防御を 1 回提供する所持物 |
| ターン結果 | UI が演出するための、出目、停止マス、文言、問題、支払結果のスナップショット |

## サブドメインと境界づけられたコンテキスト

### Game Play（中心ドメイン）

勝敗を生む中核。`Game` 集約がコマンド（ターン実行、回答、アイテム使用）を受け、状態遷移と不変条件を管理する。`Player` は集約内エンティティ、`Question` と `TurnResult` は値オブジェクト、`Board` は盤面ルールを表すドメインサービス／不変設定として扱う。

### Learning Content（支援サブドメイン）

問題の永続化・取得を担当する。アプリケーション層に `QuestionRepository` ポートを定義し、Markdown 実装をインフラストラクチャ層へ置く。ゲーム本体はファイル形式やパスを知らない。

### Presentation（汎用サブドメイン）

Flet の画面、カメラ、アニメーション、入力イベントを担当する。`TurnResult` を表示へ変換するが、支払い・勝利・アイテム効果を再計算しない。

## 集約と不変条件

```text
Game（集約ルート）
├─ players: Player × 2
├─ current_player_index
├─ pending_question / pending_player_index
├─ winner_index
├─ Board
└─ QuestionDeck（通常・資格試験）
```

- クレジットは常に 0 以上。
- ランダム獲得によるアイテム所持数は最大 3。
- 未回答問題がある間は移動も能動アイテム使用もできない。
- 能動アイテムは 1 ターン 1 個まで。
- 支払日は停止時・通過時の両方で順番に処理する。
- 最終支払日を通過して支払い済みのプレイヤーだけが勝者になれる。
- 通常問題と資格試験問題は、それぞれのデッキを使い切るまで重複しない。

## 目標依存関係

```text
main.py (presentation)
  -> techsugoroku.application.game_factory
       -> QuestionRepository port
       -> techsugoroku.domain.Game

techsugoroku.infrastructure.markdown_question_repository
  -> QuestionRepository port
  -> techsugoroku.domain.Question

game.py (compatibility facade)
  -> domain / application / infrastructure public APIs
```

ドメイン層から Flet、`pathlib.Path` による読み込み、Markdown 形式への依存を排除する。メッセージはゲーム結果の一部であり、現 MVP ではドメイン設定として残す。

## 移行上の判断

- 全面書き換えではなく、既存 API を保つストラングラーパターンを使う。これにより GUI と外部利用の回帰を避ける。
- 過度な抽象化を避け、永続化ポートは現時点で必要な `list()` のみにする。
- `random.Random` の直接注入を追加し、従来の `rng_seed` も互換性のため維持する。
- `main.py` は既定ファクトリーを利用し、資産パスとリポジトリ構築を UI から除去する。

## 不確実性

`overview.md` と現行 MVP 仕様には報酬値や一部アイテム効果の差がある。今回の正本は `specs/mvp-game/spec.md` と既存テストであり、ゲームバランスは変更しない。
