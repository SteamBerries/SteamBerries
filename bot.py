import discord
from discord import app_commands
from discord.ext import commands
import os

# ============================================
#  НАСТРОЙКИ — токен из переменной окружения
# ============================================
TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = 1527064860137885838  # ID канала для заявок

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Добавь переменную окружения.")

# ============================================
#  СОЗДАНИЕ БОТА
# ============================================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ============================================
#  ЗАПУСК БОТА
# ============================================
@bot.event
async def on_ready():
    print(f'✅ Бот {bot.user} запущен!')
    print(f'📍 Заявки будут приходить в канал ID: {CHANNEL_ID}')
    try:
        synced = await bot.tree.sync()
        print(f'✅ Синхронизировано {len(synced)} команд!')
    except Exception as e:
        print(f'❌ Ошибка синхронизации: {e}')

# ============================================
#  КОМАНДА !ping (для проверки)
# ============================================
@bot.command()
async def ping(ctx):
    await ctx.send('🏓 Pong! Бот работает!')

# ============================================
#  СЛЕШ-КОМАНДА /заявка
# ============================================
@bot.tree.command(name="заявка", description="Отправить заявку на покупку")
@app_commands.describe(
    nick="Ваш игровой ник",
    discord_name="Ваш Discord",
    pzv="Пункт выдачи (ПВЗ 1 или ПВЗ 2)",
    item="Что хотите заказать",
    price="Цена (необязательно)"
)
async def application(
    interaction: discord.Interaction,
    nick: str,
    discord_name: str,
    pzv: str,
    item: str,
    price: str = "Не указана"
):
    embed = discord.Embed(
        title="📦 Новая заявка!",
        color=0x8bc34a,
        timestamp=discord.utils.utcnow()
    )
    embed.add_field(name="👤 Ник", value=nick, inline=True)
    embed.add_field(name="💬 Discord", value=discord_name, inline=True)
    embed.add_field(name="📍 ПВЗ", value=pzv, inline=False)
    embed.add_field(name="📦 Товар", value=item, inline=True)
    embed.add_field(name="💰 Цена", value=price, inline=True)
    embed.set_footer(text="Нюхач | Магазин сервера")

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
        await interaction.response.send_message(
            f"✅ Заявка отправлена!\n"
            f"👤 Ник: {nick}\n"
            f"📦 Товар: {item}\n"
            f"📍 ПВЗ: {pzv}",
            ephemeral=True
        )
        print(f"✅ Заявка от {nick} отправлена в канал {CHANNEL_ID}")
    else:
        await interaction.response.send_message(
            "❌ Ошибка: канал не найден! Обратитесь к администратору.",
            ephemeral=True
        )

# ============================================
#  ЗАПУСК
# ============================================
if __name__ == "__main__":
    bot.run(TOKEN)
