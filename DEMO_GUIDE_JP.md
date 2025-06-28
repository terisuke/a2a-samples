# A2A デモを動かしてみよう

このガイドでは、AIエージェント同士が会話するデモを実際に動かす方法を説明します。

## 必要なもの

1. **パソコン** (Windows、Mac、Linux のいずれか)
2. **Python 3.12以上** がインストールされていること
3. **Google Gemini API キー** (無料で取得可能)

### Windows環境の推奨事項
- **PowerShell** または **Windows Terminal** の使用を推奨
- **Git for Windows** がインストールされていること
- コマンドプロンプトよりPowerShellの方が扱いやすいです

## APIキーの取得方法

### Google Gemini API キー（無料枠あり）

1. https://makersuite.google.com/app/apikey にアクセス
2. Googleアカウントでログイン
3. 「APIキーを作成」をクリック
4. 表示されたキーをコピーして保存

**無料枠の制限：**
- 15 RPM（1分間に15リクエスト）
- 1日100万トークン
- Flashモデルのみ利用可能（Pro不可）
- このデモはすべて無料枠で動作します

### OpenAI API キー

1. https://platform.openai.com/api-keys にアクセス
2. アカウントを作成またはログイン
3. 「Create new secret key」をクリック
4. 表示されたキーをコピーして保存（一度しか表示されません）

### Anthropic (Claude) API キー

1. https://console.anthropic.com/ にアクセス
2. アカウントを作成またはログイン
3. 「API Keys」セクションで新しいキーを作成
4. 表示されたキーをコピーして保存

## デモの実行手順（簡易版）

Google Gemini API無料枠のみを使った最小構成で始める場合は、[実践例セクション](#実践例factsagentとcurrencyagentで作る旅行情報システム)へジャンプしてください。

### 1. プロジェクトをダウンロード

ターミナル（コマンドプロンプト）を開いて以下を実行：

```bash
git clone https://github.com/terisuke/a2a-samples.git
cd a2a-samples
```

### 2. uvツールをインストール

#### Mac/Linuxの場合：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windowsの場合：
```powershell
# PowerShellを管理者として実行
irm https://astral.sh/uv/install.ps1 | iex
```

または、[uv公式サイト](https://github.com/astral-sh/uv)から直接ダウンロード

### 3. Google Gemini APIキーを取得

[APIキーの取得方法](#google-gemini-api-キー無料枠あり)を参照してください。



## 実践例：Facts AgentとCurrency Agentで作る旅行情報システム

### Google Gemini API無料枠だけで実現するA2A連携デモ

このセクションでは、2つのエージェントを連携させて、東京の観光情報収集から費用計算まで行う実践例を紹介します。すべてGemini API無料枠（Flashモデル）で動作します。

#### 使用するエージェント

1. **ADK Facts Agent** - Google検索による観光情報収集（ポート10003）
   - 使用モデル：Gemini 2.5 Flash Lite Preview（無料枠対応）
2. **LangGraph Currency Agent** - 通貨変換（ポート10000）
   - 使用モデル：Gemini 2.0 Flash（無料枠対応）

### 📋 実行手順（順番通りに実行してください）

#### ステップ1: 各エージェントを起動

**ターミナル1: LangGraph Currency Agent（通貨変換）**

Mac/Linuxの場合：
```bash
cd samples/python/agents/langgraph
uv sync
echo "GOOGLE_API_KEY=あなたのGemini APIキー" > .env
uv run app
```

Windowsの場合（PowerShell）：
```powershell
cd samples\python\agents\langgraph
uv sync
echo "GOOGLE_API_KEY=あなたのGemini APIキー" > .env
uv run app
```

**ターミナル2: ADK Facts Agent（情報収集）**

Mac/Linuxの場合：
```bash
cd samples/python/agents/adk_facts
uv sync
echo "GOOGLE_API_KEY=あなたのGemini APIキー" > .env
uv run python __main__.py --port 10003
uv run . --port 10003
```

Windowsの場合（PowerShell）：
```powershell
cd samples\python\agents\adk_facts
uv sync
echo "GOOGLE_API_KEY=あなたのGemini APIキー" > .env
uv run python __main__.py --port 10003
```

#### ステップ2: デモUIを起動

**ターミナル3: デモUI**

Mac/Linuxの場合：
```bash
cd demo/ui
echo "GOOGLE_API_KEY=あなたのGemini APIキー" > .env
PYTHONPATH=../../samples/python:$PYTHONPATH uv run main.py
```

Windowsの場合（PowerShell）：
```powershell
cd demo\ui
echo "GOOGLE_API_KEY=あなたのGemini APIキー" > .env
$env:PYTHONPATH = "..\..\samples\python;$env:PYTHONPATH"
uv run main.py
```

Windowsの場合（コマンドプロンプト）：
```cmd
cd demo\ui
set PYTHONPATH=..\..\samples\python;%PYTHONPATH%
uv run main.py
```

#### ステップ3: エージェントを登録

1. ブラウザで `http://localhost:12000/agents` にアクセス
2. 以下のエージェントを追加：
   - Currency Agent: `localhost:10000`
   - Facts Agent: `localhost:10003`
3. メインページ（`http://localhost:12000`）に戻る

### 🎯 Host Agent機能について

**重要**: デモUIにはHost Agent機能が内蔵されています。これは、複数のエージェントを自動的に連携させる仕組みです。

- **手動連携（エージェント登録前）**: 各エージェントを個別に選択して質問
- **自動連携（エージェント登録後）**: Host Agentが適切なエージェントを自動選択

Host Agent機能を使うと、「日本の観光地の入場料をユーロで教えて」のような複合的な質問に対して、自動的に複数のエージェントが連携して回答します。

### 🖥️ スタンドアロンHost Agentの起動方法

デモUI以外にも、独立したHost Agentを起動する方法がいくつかあります：

#### 1. CLI Host Agent（最も簡単）

コマンドライン上で動作するシンプルなHost Agent：

```bash
# Host Agentの起動（任意のA2Aエージェントに接続）
cd samples/python/hosts/cli
uv sync
uv run . --agent http://localhost:10000

# 複数のエージェントに接続する場合
uv run . --agent http://localhost:10000 --agent http://localhost:10003
```

#### 2. Multiagent Orchestrator Host

Google ADKベースの高度なHost Agent：

```bash
cd samples/python/hosts/multiagent
uv sync
echo "GOOGLE_API_KEY=あなたのAPIキー" > .env
uv run host_agent.py
```

#### 3. 特定用途のHost Agent（例：旅行プランナー）

Airbnb検索と天気情報を組み合わせた旅行プランナー：

```bash
# 必要なエージェントを起動
# ターミナル1: 天気エージェント
cd samples/python/agents/airbnb_planner_multiagent/weather_agent
uv sync
uv run .

# ターミナル2: Airbnbエージェント
cd samples/python/agents/airbnb_planner_multiagent/airbnb_agent
uv sync
uv run .

# ターミナル3: Host Agent（Gradio UI付き）
cd samples/python/agents/airbnb_planner_multiagent/host_agent
uv sync
uv run .
# http://localhost:8083 でアクセス
```

### 💬 使い方

#### 手動連携モード（エージェント登録前）

左側のリストから個別にエージェントを選択して質問：

**例1: Facts Agentで情報収集**
```
質問: "What is the average daily tourist expense in Tokyo"
回答: 約$194（¥28,087）/日
```

**例2: Currency Agentで通貨変換**
```
質問: "How much is 28087 JPY in EUR"
回答: 約€188
```

#### 自動連携モード（エージェント登録後 - Host Agent使用）

エージェントを登録すると、デモUIがHost Agentとして機能し、自動的に適切なエージェントを選択：

**複合的な質問の例：**
- 「日本のニッチな観光スポットを教えて」→「入場料は？」→「それは何ユーロ？」
- 「東京ディズニーランドのチケット価格を米ドルで教えて」
- 「築地市場の朝食の平均価格をユーロで知りたい」

### 🔧 トラブルシューティング

#### エージェントがデモUIに表示されない場合

1. エージェントが正常に起動しているか確認：
   
   Mac/Linuxの場合：
   ```bash
   curl http://localhost:10000/.well-known/agent.json
   curl http://localhost:10003/.well-known/agent.json
   ```
   
   Windowsの場合（PowerShell）：
   ```powershell
   Invoke-WebRequest -Uri http://localhost:10000/.well-known/agent.json
   Invoke-WebRequest -Uri http://localhost:10003/.well-known/agent.json
   ```

2. `http://localhost:12000/agents` でエージェントを手動登録

#### Facts Agentが "I do not have access to real-time information" と返す場合

- 質問を具体的にする（例：「Tokyo tourist spots」→「interesting facts about Tokyo」）
- エージェントのログを確認：
  - Mac/Linux: `tail -f adk_facts_10003.log`
  - Windows (PowerShell): `Get-Content adk_facts_10003.log -Tail 20 -Wait`

#### Currency Agentがエラーを返す場合

- 日付形式を確認（YYYY-MM-DD または "latest"）
- 通貨コードが正しいか確認（USD, EUR, JPY など）

#### ポートが既に使用されている場合

```bash
# 別のポートで起動
uv run app --port 10004  # Currency Agent用
uv run python __main__.py --port 10005  # Facts Agent用
```

#### Windows固有の問題

##### PowerShellで実行ポリシーエラーが出る場合

```powershell
# 管理者権限でPowerShellを開いて実行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

##### 文字化けが発生する場合

```powershell
# UTF-8エンコーディングを設定
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### 🎯 Host Agent連携の実例

デモUIのHost Agent機能を使った実際の会話例：

**ユーザー**: 「日本のニッチな観光スポットを教えて」
→ Host AgentがFacts Agentを選択し、裏砂漠（伊豆大島）などを提案

**ユーザー**: 「日本民家集落博物館の料金は？」
→ Host AgentがFacts Agentから「大人800円」という情報を取得

**ユーザー**: 「800円は何ユーロになるの？」
→ Host AgentがCurrency Agentを選択し、「4.728ユーロ」と自動変換

このように、ユーザーは個別のエージェントを意識することなく、自然な会話で情報を得ることができます。

## 🚀 次のステップ

### 1. 他のエージェントを試す

```bash
# HelloWorld Agent（シンプルな応答）
# Mac/Linux
cd samples/python/agents/helloworld
uv sync
echo "GOOGLE_API_KEY=あなたのAPIキー" > .env
uv run app

# Windows (PowerShell)
cd samples\python\agents\helloworld
uv sync
echo "GOOGLE_API_KEY=あなたのAPIキー" > .env
uv run app
```

### 2. 独自のエージェントを作成

`samples/python/agents/` のサンプルを参考に、独自のエージェントを作成してみましょう。

### 3. 本格的なHost Agentシステムの構築

複数のエージェントを管理する独自のHost Agentを実装して、より複雑なワークフローを実現できます。

## ⚠️ 注意事項

- APIキーは他人と共有しないでください
- 無料枠には利用制限があります（15 RPM、100万トークン/日）
- 本番環境での使用前に、セキュリティ対策を確認してください

## 📚 参考資料

- [A2Aプロトコル仕様](https://google.github.io/agent-to-agent-protocol/)
- [Google Gemini API](https://ai.google.dev/)
- [サンプルコード（オリジナル）](https://github.com/googlesamples/a2a-samples)
- [このガイド用のリポジトリ](https://github.com/terisuke/a2a-samples)

## 🆘 サポート

問題が解決しない場合は、GitHubのIssuesで質問してください：
- [このガイドに関する問題](https://github.com/terisuke/a2a-samples/issues)
- [A2Aサンプル全般の問題](https://github.com/googlesamples/a2a-samples/issues)
