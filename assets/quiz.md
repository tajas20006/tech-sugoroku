# AWS クイズバンク

4 択形式。選択肢の順番はゲームごとにランダム化し、不正解時にも解説を表示する。

## 通常クイズ

### Q01: オブジェクトストレージ

- 問題: 画像、バックアップ、静的ファイルなどを保存する AWS のオブジェクトストレージサービスはどれ？
- 選択肢: Amazon S3 / Amazon EBS / Amazon RDS / Amazon EC2
- 正解: Amazon S3
- 正解メッセージ: `S3 バケットにきれいに保存できた！ +80 Credits`
- 不正解メッセージ: `EBS に画像を詰め込み始めた。-40 Credits`
- 解説: Amazon S3 は、オブジェクトを保存・取得するストレージサービスです。

### Q02: 仮想サーバー

- 問題: AWS 上で仮想サーバーを起動するサービスはどれ？
- 選択肢: Amazon EC2 / AWS Lambda / Amazon CloudFront / Amazon Route 53
- 正解: Amazon EC2
- 正解メッセージ: `EC2 を適切なサイズで起動！ +80 Credits`
- 不正解メッセージ: `DNS にサーバーを期待してしまった。-40 Credits`
- 解説: Amazon EC2 は、必要な台数・性能の仮想サーバーを提供します。

### Q03: アクセス権限

- 問題: AWS リソースへのアクセス権限を安全に管理するサービスはどれ？
- 選択肢: IAM / Amazon Inspector / AWS Shield / Amazon Cognito
- 正解: IAM
- 正解メッセージ: `IAM の最小権限を守った！ +80 Credits`
- 不正解メッセージ: `全員に AdministratorAccess を付けそうになった。-40 Credits`
- 解説: IAM はユーザー、ロール、ポリシーで AWS へのアクセスを制御します。

### Q04: サーバーレス実行

- 問題: サーバー管理をせず、イベントに応じてコードを実行できるサービスはどれ？
- 選択肢: AWS Lambda / Amazon EC2 / Amazon ECS / AWS Elastic Beanstalk
- 正解: AWS Lambda
- 正解メッセージ: `Lambda が軽やかに実行された！ +80 Credits`
- 不正解メッセージ: `小さな処理のためにサーバーを一晩中待機させた。-40 Credits`
- 解説: AWS Lambda はイベント駆動でコードを実行するサーバーレスサービスです。

### Q05: 高可用性のDB

- 問題: Amazon RDS の可用性を高め、障害時のフェイルオーバーを自動化する構成はどれ？
- 選択肢: Multi-AZ 配置 / リードレプリカのみ / 単一 AZ の大きなインスタンス / 手動バックアップのみ
- 正解: Multi-AZ 配置
- 正解メッセージ: `Multi-AZ が静かにフェイルオーバー！ +80 Credits`
- 不正解メッセージ: `DB が 1 台だけ。祈りの運用になった。-40 Credits`
- 解説: Multi-AZ は別 AZ のスタンバイへ自動フェイルオーバーします。

### Q06: DDoS 対策

- 問題: Web アプリケーションへの不正な HTTP(S) リクエストをルールでブロックするサービスはどれ？
- 選択肢: AWS WAF / Amazon GuardDuty / AWS KMS / Amazon Macie
- 正解: AWS WAF
- 正解メッセージ: `WAF が怪しいリクエストをブロック！ +80 Credits`
- 不正解メッセージ: `WAF なしでインターネットの荒波へ。-40 Credits`
- 解説: AWS WAF は Web ACL のルールで HTTP(S) リクエストをフィルタリングします。

### Q07: 非同期処理

- 問題: 処理を疎結合にし、メッセージを一時的に保持するキューサービスはどれ？
- 選択肢: Amazon SQS / Amazon SNS / AWS Step Functions / Amazon EventBridge
- 正解: Amazon SQS
- 正解メッセージ: `SQS で処理をきれいに疎結合化！ +80 Credits`
- 不正解メッセージ: `ピーク時の処理を全部同期でつないだ。-40 Credits`
- 解説: Amazon SQS はコンポーネント間のメッセージを保持するマネージドキューです。

### Q08: コスト最適化

- 問題: 長期間、安定して稼働する EC2 の料金を抑える選択肢として適切なのはどれ？
- 選択肢: Savings Plans またはリザーブドインスタンス / 常にオンデマンドのみ / 使わないインスタンスも停止しない / 最大サイズに統一する
- 正解: Savings Plans またはリザーブドインスタンス
- 正解メッセージ: `コミット利用でコストを最適化！ +80 Credits`
- 不正解メッセージ: `オンデマンド一本足打法で請求額が伸びた。-40 Credits`
- 解説: 利用量が予測可能なワークロードでは、コミット型の割引が有効です。

### Q09: メトリクスとアラーム

- 問題: リソースのメトリクスを監視し、しきい値超過時に通知するサービスはどれ？
- 選択肢: Amazon CloudWatch / AWS CloudTrail / AWS Config / AWS Artifact
- 正解: Amazon CloudWatch
- 解説: CloudWatch はメトリクス、ログ、アラームを扱います。

### Q10: 監査ログ

- 問題: AWS アカウント内で「誰が、いつ、何をしたか」を記録するサービスはどれ？
- 選択肢: AWS CloudTrail / Amazon CloudWatch / Trusted Advisor / Compute Optimizer
- 正解: AWS CloudTrail
- 解説: CloudTrail は AWS API アクティビティを記録します。

### Q11: コンテンツ配信

- 問題: 世界中の利用者へコンテンツを低遅延で配信する CDN サービスはどれ？
- 選択肢: Amazon CloudFront / Amazon VPC / AWS Direct Connect / Elastic Load Balancing
- 正解: Amazon CloudFront
- 解説: CloudFront はエッジロケーションを利用してコンテンツを配信します。

### Q12: NoSQL データベース

- 問題: サーバーレスでスケーラブルなキーバリュー／ドキュメント型 DB はどれ？
- 選択肢: Amazon DynamoDB / Amazon RDS / Amazon Aurora / Amazon Redshift
- 正解: Amazon DynamoDB
- 解説: DynamoDB はフルマネージドな NoSQL データベースです。

### Q13: 自動スケーリング

- 問題: EC2 の負荷に合わせてインスタンス数を自動調整する機能はどれ？
- 選択肢: EC2 Auto Scaling / Amazon CloudFront / AWS Backup / Amazon SQS
- 正解: EC2 Auto Scaling
- 解説: EC2 Auto Scaling は定義した条件に基づき台数を調整します。

### Q14: 暗号化キー

- 問題: AWS サービスで使用する暗号化キーを作成・管理するサービスはどれ？
- 選択肢: AWS KMS / AWS Secrets Manager / Amazon Cognito / IAM
- 正解: AWS KMS
- 解説: AWS KMS は暗号化キーの作成、管理、利用を容易にします。

### Q15: ネットワーク分離

- 問題: インターネットから直接アクセスさせたくない DB を置くサブネットはどれ？
- 選択肢: プライベートサブネット / パブリックサブネット / インターネットゲートウェイ / NAT Gateway
- 正解: プライベートサブネット
- 解説: 外部公開不要な DB は通常プライベートサブネットに配置します。

### Q16: シークレット管理

- 問題: DB 認証情報を安全に保管し、定期的にローテーションしたい。適切なサービスはどれ？
- 選択肢: AWS Secrets Manager / 公開 S3 バケット / ソースコード / 平文のメモ
- 正解: AWS Secrets Manager
- 解説: Secrets Manager はシークレットの保管とローテーションを支援します。

### Q17: イベント連携

- 問題: AWS サービスや SaaS のイベントをルールで振り分けるサービスはどれ？
- 選択肢: Amazon EventBridge / Amazon EBS / AWS Direct Connect / Amazon EFS
- 正解: Amazon EventBridge
- 解説: EventBridge はイベントバスとルールによりイベント駆動連携を構築します。

### Q18: バックアップ

- 問題: 複数 AWS サービスのバックアップポリシーを一元管理するサービスはどれ？
- 選択肢: AWS Backup / AWS WAF / Amazon Inspector / AWS Shield
- 正解: AWS Backup
- 解説: AWS Backup はバックアップを一元的に設定・監視できます。

### Q19: コンテナ実行

- 問題: コンテナ化したアプリケーションをサーバー管理なしで実行する選択肢はどれ？
- 選択肢: AWS Fargate / Amazon EC2 の手動構築のみ / Amazon S3 / Route 53
- 正解: AWS Fargate
- 解説: Fargate は ECS や EKS 向けのサーバーレスコンテナ実行基盤です。

### Q20: DNS

- 問題: ドメイン名と IP アドレスなどを名前解決する AWS サービスはどれ？
- 選択肢: Amazon Route 53 / Amazon CloudFront / Amazon VPC / AWS IAM
- 正解: Amazon Route 53
- 解説: Route 53 は高可用性の DNS サービスです。

### Q21: 脅威検出

- 問題: AWS アカウントやワークロードの悪意ある活動を継続的に検出するサービスはどれ？
- 選択肢: Amazon GuardDuty / AWS WAF / AWS KMS / Amazon SQS
- 正解: Amazon GuardDuty
- 解説: GuardDuty はログや脅威インテリジェンスを分析して脅威を検出します。

### Q22: インフラのコード化

- 問題: AWS リソースをテンプレートで定義し、再現可能に構築するサービスはどれ？
- 選択肢: AWS CloudFormation / AWS CloudTrail / Amazon CloudWatch / AWS Config
- 正解: AWS CloudFormation
- 解説: CloudFormation はインフラストラクチャをコードとして管理します。

### Q23: 通知

- 問題: メール、SMS、HTTP エンドポイントなどへメッセージを配信するサービスはどれ？
- 選択肢: Amazon SNS / Amazon SQS / AWS Step Functions / Amazon MQ
- 正解: Amazon SNS
- 解説: SNS は発行者から複数の購読者へ通知を配信します。

### Q24: 設定の評価

- 問題: AWS リソースの設定変更を記録し、ルール準拠を評価するサービスはどれ？
- 選択肢: AWS Config / AWS CloudTrail / Amazon CloudWatch / AWS Artifact
- 正解: AWS Config
- 解説: AWS Config はリソース設定の履歴とコンプライアンス評価を提供します。

## 資格試験クイズ

正解時は `+250 Credits` と認定バッジ、不正解時は `-150 Credits`。

### Q09: 可用性と運用負荷

- 問題: Web アプリを高可用性にしつつ、サーバー管理の負担を最小化したい。最も適切な構成はどれ？
- 選択肢: 複数 AZ の ALB 配下に AWS Fargate サービスを配置 / 1 台の EC2 にすべて配置 / オンプレミスを手動増設 / 1 AZ に EC2 を複数台配置
- 正解: 複数 AZ の ALB 配下に AWS Fargate サービスを配置
- 解説: ALB、複数 AZ、Fargate により可用性と運用負荷の低減を両立できます。

### Q10: S3 の長期保管

- 問題: S3 データを、最初の 30 日間は頻繁に利用し、その後数年間はほぼ参照しない。コストを抑える方法はどれ？
- 選択肢: S3 ライフサイクルルールでストレージクラスを移行 / 常に S3 Standard / 毎月手動削除 / EBS にコピー
- 正解: S3 ライフサイクルルールでストレージクラスを移行
- 解説: アクセス頻度に合わせてストレージクラスを移行することでコストを抑えられます。

### Q11: アカウント分離

- 問題: 複数チームの AWS 環境を分離しながら、請求、ガバナンス、アクセス管理を一元化したい。適切なサービスはどれ？
- 選択肢: AWS Organizations / Amazon Cognito / AWS WAF / Amazon Route 53
- 正解: AWS Organizations
- 解説: AWS Organizations は複数アカウントの請求統合とガバナンスを支援します。

### Q12: DDoS 対策の組み合わせ

- 問題: 公開 Web アプリを一般的な DDoS 攻撃から保護し、HTTP(S) リクエストの細かな制御もしたい。適切な組み合わせはどれ？
- 選択肢: AWS Shield Standard と AWS WAF / AWS KMS と IAM / GuardDuty と CloudTrail / Macie と S3
- 正解: AWS Shield Standard と AWS WAF
- 解説: Shield Standard は一般的な DDoS 対策、WAF は Web リクエストのルール制御を担います。

### Q13: 変動する DynamoDB 負荷

- 問題: DynamoDB の読み込みが予測不能に変動する。運用負荷を下げつつスロットリングを避けるには？
- 選択肢: オンデマンドキャパシティモード / EC2 を増やす / 読み込みを禁止 / RDS に無条件で移行
- 正解: オンデマンドキャパシティモード
- 解説: オンデマンドモードは変動するトラフィックに応じて自動でスケールします。

### Q14: リージョン障害対策

- 問題: リージョン規模の障害に備え、DB の復旧時間を短くしたい。適切な選択肢は？
- 選択肢: 別リージョンへのレプリケーションまたはリードレプリカ / 同一 AZ のみでバックアップ / 単一インスタンスの大型化 / ローカル PC にだけ保存
- 正解: 別リージョンへのレプリケーションまたはリードレプリカ
- 解説: リージョン障害には別リージョンへのデータ複製と復旧手順が必要です。

### Q15: 最小権限

- 問題: 開発者に必要最小限の S3 読み取りだけを許可する最もよい方法は？
- 選択肢: 対象バケットの読み取りのみを許可する IAM ポリシー / AdministratorAccess / ルートユーザーの共有 / アクセスキーを全員で共有
- 正解: 対象バケットの読み取りのみを許可する IAM ポリシー
- 解説: IAM は職務に必要な最小権限を付与します。

### Q16: 大容量データ分析

- 問題: S3 上のログをサーバー管理なしで SQL 分析したい。最適なサービスは？
- 選択肢: Amazon Athena / Amazon EC2 / Amazon Route 53 / AWS WAF
- 正解: Amazon Athena
- 解説: Athena は S3 上のデータを標準 SQL で分析できるサーバーレスサービスです。

### Q17: 信頼性の設計原則

- 問題: AWS Well-Architected の信頼性設計で、単一障害点の影響を下げるために推奨される考え方はどれ？
- 選択肢: 水平スケールで複数の小さなリソースへ分散する / 1 台の最大インスタンスに集約する / 復旧手順をテストしない / 容量を推測で固定する
- 正解: 水平スケールで複数の小さなリソースへ分散する
- 解説: 信頼性の設計原則には、複数の小さなリソースに分散して単一障害の影響を減らすことが含まれます。

### Q18: S3 ライフサイクル

- 問題: S3 に保存したログを 30 日後に低コストなストレージクラスへ自動移行する機能はどれ？
- 選択肢: S3 Lifecycle ルール / S3 バケットポリシー / CloudTrail イベント / Route 53 ヘルスチェック
- 正解: S3 Lifecycle ルール
- 解説: S3 Lifecycle はオブジェクトのストレージクラス移行、アーカイブ、期限切れ削除を自動化できます。

### Q19: DDoS 耐性の強化

- 問題: CloudFront 配信の Web アプリで、アプリケーションレイヤーのリクエストフラッド対策を追加したい。最も適切な追加サービスはどれ？
- 選択肢: AWS WAF の Web ACL とレートベースルール / AWS KMS / Amazon EFS / AWS Artifact
- 正解: AWS WAF の Web ACL とレートベースルール
- 解説: AWS WAF のレートベースルールは、許容値を超えるリクエストを送る送信元をブロックできます。

### Q20: 計画停止と障害

- 問題: Aurora Global Database で、計画メンテナンスのためにプライマリリージョンを変更する。データ損失を避ける操作はどれ？
- 選択肢: スイッチオーバー / 障害時フェイルオーバー / スナップショット削除 / 読み取り停止
- 正解: スイッチオーバー
- 解説: 健全な状態で行うスイッチオーバーは、セカンダリを同期してからプライマリを変更するため RPO 0 です。
