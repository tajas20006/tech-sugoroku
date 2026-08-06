# 進捗

- [x] 実装コンテキストを確認
- [x] MVP仕様とタスク分割を作成
- [x] 失敗するルールテストを作成
- [x] ルールエンジンを実装
- [x] Flet GUIを実装
- [x] テスト・静的検査・起動確認
- [x] コミット

## 判断記録

- モードは auto。ユーザー指定に基づき、以後の実装判断は仕様に沿って自律的に進める。
- MVPは外部データ読み込みを後回しにし、UI動作を優先する。
- RED: `ModuleNotFoundError: No module named 'game'` を確認。
- GREEN: `uv run pytest -q` で9件のテストが通過。
- 静的検査: `uv run ruff check .` が成功。
- 起動確認: Flet Webサーバーが `http://127.0.0.1:8550` でHTTP 200を返した。
- コミット: `feat: add playable AWS sugoroku MVP`（ローカルコミット済み）
- Flet 0.86.5 の互換性修正: `ft.app` を `ft.run`、旧ボタンを `Button`、旧 alignment 定数を `ft.Alignment.CENTER`、`ImageFit` を `BoxFit` に置換。
- バランス調整: 初期クレジットを300に増やし、支払日を100/180/280/400へ緩和。通常クイズマスを12か所に増やした。
- 質問: `assets/quiz.md` と `assets/quiz-architecture.md` から56問を読み込み、カテゴリ別デッキを使い切るまで重複しない。
- 演出: サイコロを10フレーム切り替えてから最終出目を確定する。
- リッチ化: 固定マスとPNGトークンをStackで重ね、トークンを1マスずつ移動・バウンド。出目の拡大縮小とイベント結果バナーも追加。
- カットイン: 支払日、資格試験、AWS Summit、アイテム、クイズ、コスト発生で盤面全体を覆う短い演出を追加。
- 支払日: 着地時だけでなく通過時も支払結果をTurnResultで保持し、到着イベントより先にカットインを表示する。
