# AWS クイズバンク: アーキテクチャ編

4 択形式。通常問題は正解 `+80`／不正解 `-40`、資格試験問題は正解 `+250`／不正解 `-150` を基本値とする。

## ネットワーク・可用性

### A01: プライベートサブネットの外向き通信

- 問題: プライベートサブネットの EC2 からインターネットへ発信だけを許可したい。適切なサービスは？
- 選択肢: NAT Gateway / Internet Gateway のみ / Route 53 / AWS WAF
- 正解: NAT Gateway
- 解説: NAT Gateway は、外部から開始された接続を受けずに、プライベートサブネットから外部への接続を可能にします。

### A02: NAT の耐障害性

- 問題: 2 AZ 構成のプライベートサブネットからの外向き通信を高可用にしたい。推奨構成は？
- 選択肢: 各 AZ に NAT Gateway を配置 / NAT Gateway を 1 台だけ配置 / Internet Gateway を DB に接続 / NAT を使わない
- 正解: 各 AZ に NAT Gateway を配置
- 解説: NAT Gateway を各 AZ に置くと、1 AZ 障害時の影響を減らせます。

### A03: 負荷分散

- 問題: HTTP/HTTPS リクエストを複数のターゲットにルーティングしたい。適切なロードバランサーは？
- 選択肢: Application Load Balancer / Network Load Balancer のみ / NAT Gateway / VPC Peering
- 正解: Application Load Balancer
- 解説: ALB は HTTP/HTTPS のレイヤー 7 ルーティングを提供します。

### A04: DNS フェイルオーバー

- 問題: エンドポイントのヘルスチェック結果に応じて DNS 応答を切り替えたい。適切なサービスは？
- 選択肢: Route 53 ヘルスチェックとフェイルオーバールーティング / S3 Lifecycle / IAM ロール / AWS KMS
- 正解: Route 53 ヘルスチェックとフェイルオーバールーティング
- 解説: Route 53 はヘルスチェックに基づく DNS フェイルオーバーを設定できます。

### A05: 高度な DDoS 対策

- 問題: CloudFront を利用する公開サイトで、レート超過する送信元 IP を制限したい。適切な設定は？
- 選択肢: AWS WAF のレートベースルール / S3 バケットポリシー / KMS キー / EBS 暗号化
- 正解: AWS WAF のレートベースルール
- 解説: AWS WAF のレートベースルールは、定めたレートを超えるリクエスト送信元をブロックできます。

## セキュリティ・ガバナンス

### A06: ルートユーザー

- 問題: AWS アカウントの root user を日常運用で使うべき？
- 選択肢: 原則使わず、必要なタスクだけに限定する / 管理が楽なので毎日使う / 全員で共有する / アクセスキーを作る
- 正解: 原則使わず、必要なタスクだけに限定する
- 解説: root user は完全な権限を持つため、日常作業には別の IAM アイデンティティを使用します。

### A07: 一時的な認証情報

- 問題: EC2 上のアプリが S3 にアクセスする際、長期アクセスキーを置かずに権限を与える方法は？
- 選択肢: EC2 に IAM ロールを割り当てる / アクセスキーをソースコードへ書く / root user を使う / S3 を公開する
- 正解: EC2 に IAM ロールを割り当てる
- 解説: IAM ロールは一時的な認証情報を提供します。

### A08: 組織全体の制限

- 問題: 複数アカウントに対し、許可できるアクションの上限を組織単位で設定する機能は？
- 選択肢: Service Control Policy (SCP) / Security Group / Network ACL / S3 ACL
- 正解: Service Control Policy (SCP)
- 解説: SCP は Organizations 内のアカウントで利用可能な権限の上限を定義します。

### A09: 機密データの発見

- 問題: S3 内にある個人情報などの機密データを検出・分類したい。適切なサービスは？
- 選択肢: Amazon Macie / AWS WAF / Amazon CloudFront / Amazon SQS
- 正解: Amazon Macie
- 解説: Macie は S3 の機密データを検出・分類するサービスです。

### A10: 権限の検証

- 問題: 意図しない外部公開やクロスアカウントアクセスを見つける IAM 機能は？
- 選択肢: IAM Access Analyzer / CloudWatch Alarm / AWS Backup / AWS Shield
- 正解: IAM Access Analyzer
- 解説: IAM Access Analyzer は外部アクセスを分析し、ポリシーの検証にも使えます。

## データ・イベント駆動

### A11: ワークフロー

- 問題: 複数の Lambda 関数を、分岐・リトライ・待機を含むワークフローとして実行したい。適切なサービスは？
- 選択肢: AWS Step Functions / Amazon SQS / Amazon EFS / AWS KMS
- 正解: AWS Step Functions
- 解説: Step Functions は分散アプリケーションのワークフローを可視化・オーケストレーションします。

### A12: Pub/Sub

- 問題: 注文イベントを複数の処理システムへファンアウト配信したい。適切なサービスは？
- 選択肢: Amazon SNS / Amazon EBS / Amazon EC2 / Amazon RDS
- 正解: Amazon SNS
- 解説: SNS はメッセージを複数の購読者へ配信できます。

### A13: キャッシュ

- 問題: 読み取り負荷が高いアプリで、ミリ秒単位のインメモリキャッシュを使いたい。適切なサービスは？
- 選択肢: Amazon ElastiCache / Amazon S3 Glacier / Amazon EBS / AWS Backup
- 正解: Amazon ElastiCache
- 解説: ElastiCache は Redis や Memcached に対応するインメモリキャッシュです。

### A14: データウェアハウス

- 問題: 大規模な分析ワークロード用のクラウドデータウェアハウスはどれ？
- 選択肢: Amazon Redshift / Amazon Route 53 / AWS Lambda / Amazon Inspector
- 正解: Amazon Redshift
- 解説: Redshift は分析用途向けのデータウェアハウスサービスです。

### A15: ファイル共有

- 問題: 複数 EC2 インスタンスから同時にアクセスできる、Linux 向けの共有ファイルストレージは？
- 選択肢: Amazon EFS / Amazon EBS / Amazon S3 / Amazon DynamoDB
- 正解: Amazon EFS
- 解説: EFS は複数インスタンスからマウントできる伸縮自在なファイルシステムです。

## コスト・運用

### A16: 予算アラート

- 問題: コストまたは使用量が設定値を超えた時に通知を受けたい。適切なサービスは？
- 選択肢: AWS Budgets / AWS Artifact / Amazon Inspector / AWS KMS
- 正解: AWS Budgets
- 解説: AWS Budgets はコストや使用量の予算を設定し、しきい値でアラートできます。

### A17: コストの可視化

- 問題: AWS 利用額の傾向を確認し、将来コストの予測を見たい。適切なツールは？
- 選択肢: AWS Cost Explorer / AWS WAF / Amazon Route 53 / Amazon SQS
- 正解: AWS Cost Explorer
- 解説: Cost Explorer は支出の可視化、分析、予測を支援します。

### A18: リソース最適化

- 問題: EC2 などの利用状況を分析し、適切なリソースサイズの推奨を受けたい。適切なサービスは？
- 選択肢: AWS Compute Optimizer / AWS CloudTrail / Amazon Macie / AWS Shield
- 正解: AWS Compute Optimizer
- 解説: Compute Optimizer は利用状況を分析して最適化の推奨を提供します。

### A19: コンテナ管理

- 問題: Docker コンテナを起動、停止、管理するマネージドオーケストレーションサービスは？
- 選択肢: Amazon ECS / Amazon S3 / AWS IAM / Amazon Athena
- 正解: Amazon ECS
- 解説: ECS はコンテナ化されたアプリケーションを実行・管理するサービスです。

### A20: サーバーレスコンテナ

- 問題: ECS のタスクを、EC2 クラスターの管理なしで実行する起動タイプは？
- 選択肢: AWS Fargate / Dedicated Host / Spot Fleet / Elastic IP
- 正解: AWS Fargate
- 解説: Fargate は ECS タスクをサーバーレス基盤で実行できます。
