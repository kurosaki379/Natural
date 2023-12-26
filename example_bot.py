import discord
from discord.ext import commands
import re
from discord import Embed

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 1. ようわからんやつ
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


# 2. ログの自動解析システム(RagePluginHook.log)
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.attachments and "RagePluginHook.log" in message.attachments[0].filename:
        # バイトオブジェクトを文字列にデコード
        log_content = (await message.attachments[0].read()).decode("utf-8")

        # 正規表現を使用してログから情報を抽出
        gtav_version_match = re.search(r"Product version: (.+)", log_content)
        rage_version_match = re.search(r"Version: RAGE Plugin Hook (.+?) for", log_content)
        lspdfg_version_match = re.search(r"LSPD First Response (.+?) \((.+?)\)", log_content)
        crash_status_match = re.search(r"Crash (.+)", log_content)

        # 各情報を取得し、もし該当する情報がない場合は"Unknown"とする
        gtav_version = gtav_version_match.group(1) if gtav_version_match else "不明"
        rage_version = rage_version_match.group(1) if rage_version_match else "不明"
        lspdfg_version = lspdfg_version_match.group(2) if lspdfg_version_match else "不明"
        crash_status = crash_status_match.group(1) if crash_status_match else "No"

        # 結果のメッセージを作成
        result_message = (
            f"GTAV バージョン: {gtav_version} {'最新' if gtav_version.strip() == '1.0.3095.0' else '使用しているファイルは旧バージョンのものです。GTA5フォルダーから「GTA5.exe」を削除してファイルの整合性チェックを行い、ファイルを最新にしてください。'}\n"
            f"RAGE Plugin Hook バージョン: {rage_version} {'最新' if rage_version == 'v1.107.1334.16527' else '導入されているファイルは旧バージョンのものです。最新のRAGE Plugin Hookに導入し直してください。'}\n"
            f"LSPDFR バージョン: {lspdfg_version} {'最新' if lspdfg_version == '0.4.8748.23994' else '導入されているファイルは旧バージョンのものです。最新のLSPDFRに導入し直してください。'}\n"
            f"クラッシュの有無: {crash_status}\n"
        )

        # 結果のメッセージを送信
        result_message = await message.channel.send(result_message)

        # デバッグメッセージ
        print(f"gtav_version: {gtav_version}")
        print(f"rage_version: {rage_version}")
        print(f"lspdfg_version: {lspdfg_version}")
        print("Debug Message: Reached this point successfully.")

        # 埋め込みメッセージを作成
        embed = Embed(
            title='NaturalのRagePluginHook.logの自動解析システムをご利用いただきありがとうございます。',
            description='GTA5フォルダー内にある『RagePluginHook.log』というファイルをチャンネルに1つ送信してください。するとNaturalが自動的に解析をして結果を送信します。',
            color=discord.Color(int('ff92b4', 16))
        )

        # フィールドを追加 (オプション)
        embed.add_field(name='注意事項', value='現在は、RagePluginHook.logにしか対応しておりません。RagePluginHook.log以外のログファイルを送ったとしても自動解析されません。\nNaturalがオフラインの時や取り込み中などの時は、使用しないでください。\n場合によっては、手動でRagePluginHook.logを確認する場合があります。ご了承ください。\n現在は、試験段階です。一応皆様のdiscordサーバーに導入できますが不具合等が起こった際は、大変お手数をおかけしますがNatural開発者チームまでお問い合わせを願います。', inline=True)
        embed.add_field(name='NaturalのRagePluginHook.log自動解析システムとは？', value='NaturalがGTA5のバージョン、RagePluginHookのバージョン、LSPDFRバージョンが最新化を確認しクラッシュがあるのかを解析してメッセージを送ります。', inline=True)

        # フッターを追加 (オプション)
        embed.set_footer(text='Natural', icon_url='https://media.discordapp.net/attachments/1188159632187850914/1188161081785458719/2023-12-21_204844.png?ex=6599843c&is=65870f3c&hm=052c8387113bbb631e994f9c51d55d9c12d33df52920eb7c28be532346d7219c&=&format=webp&quality=lossless')

        # 埋め込みメッセージを送信
        await message.channel.send(embed=embed)

# 3. ステータス (ステータスの処理)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await update_status()

async def update_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='使用可能中'))

# Botのトークンを設定して起動
token = "YOUR_DISCORD_BOT_TOKEN"
bot.run("MTE4NjY1MDE3MzIwNDU5ODk0Ng.GuXAdA.DczOP--2TNqEW9iTHx3YujG7NWVTJeMC4Ey9nA")