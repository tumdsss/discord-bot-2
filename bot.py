import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------------------------------
# 📌 ID ผู้ใช้ที่ได้รับอนุญาตให้ใช้คำสั่งได้คนเดียว
# ----------------------------------------------------
ALLOWED_USER_ID = 933529869487321161  # เปลี่ยนเป็น Discord User ID ของคุณ

# ----------------------------------------------------
# 1. ข้อมูลชื่อเซิร์ฟเวอร์ใหม่
# ----------------------------------------------------
NEW_SERVER_NAME = "Makaitachi Academy : สถาบันแห่งโลกปีศาจ"

# ----------------------------------------------------
# 2. ยศใหม่และการกำหนดสิทธิ์ (Roles & Permissions)
# ----------------------------------------------------
perm_ceo = discord.Permissions.all()  # ขั้นผู้จัดการ

perm_admin = discord.Permissions(     # ขั้นผู้ดูแล
    manage_roles=True,
    manage_channels=True,
    kick_members=True,
    ban_members=True,
    manage_messages=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
    view_channel=True,
    send_messages=True,
    connect=True,
    speak=True
)

perm_member = discord.Permissions(    # ขั้นสมาชิกทั่วไป
    view_channel=True,
    send_messages=True,
    read_message_history=True,
    add_reactions=True,
    connect=True,
    speak=True,
    use_voice_activation=True
)

ROLES_DATA = [
    {"name": "💎 CEO", "color": discord.Color.from_rgb(0, 255, 255), "permissions": perm_ceo},
    {"name": "👑 ผอ.", "color": discord.Color.from_rgb(255, 215, 0), "permissions": perm_member},
    {"name": "🛡️ แอดมิน", "color": discord.Color.from_rgb(220, 20, 60), "permissions": perm_admin},
    {"name": "📚 อาจารย์", "color": discord.Color.from_rgb(138, 43, 226), "permissions": perm_member},
    {"name": "🎓 นักเรียน", "color": discord.Color.from_rgb(30, 144, 255), "permissions": perm_member},
    {"name": "🩸 ผ่านสัม", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member},
    {"name": "⏳ รอสัม", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member},
    {"name": "💰 จ่ายเงินแล้ว", "color": discord.Color.from_rgb(50, 205, 50), "permissions": perm_member},
]

# ----------------------------------------------------
# 3. หมวดหมู่และช่อง (Categories & Channels)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "🏰 1. 「 魔界・โถงต้อนรับ 」": {
        "text": [
            "👋・ยินดีต้อนรับ",
            "📜・กฎโรงเรียน",
            "🎖️・รับยศ",
            "📌・วิธีเข้าโรล"
        ],
        "voice": []
    },
    "🎓 2. 「 面接・ห้องสัมภาษณ์ 」": {
        "text": [
            "📢・ประกาศก่อนสัม",
            "💬・พูดคุยก่อนสัม",
            "📅・นัดสัม",
            "📋・ผลสัม"
        ],
        "voice": [
            "🎙️・สัมภาษณ์ รอบที่ 01",
            "🎙️・สัมภาษณ์ รอบที่ 02",
            "🎙️・สัมภาษณ์ รอบที่ 03",
            "🎙️・สัมภาษณ์ รอบที่ 04"
        ]
    },
    "📜 3. 「 告知・กระดานประกาศ 」": {
        "text": [
            "📢・ประกาศหลัก",
            "📜・ประกาศย่อย",
            "🔔・แจ้งเตือนสำคัญ",
            "📰・ข่าวสารโรงเรียน",
            "⚜️・ประกาศจากสภานักเรียน"
        ],
        "voice": []
    },
    "🌙 4. 「 集会・ห้องโถงกลาง 」": {
        "text": [
            "💬・พูดคุยทั่วไป",
            "📸・ส่งรูป",
            "🎬・ส่งวิดีโอ",
            "💡・เสนอแนะ"
        ],
        "voice": []
    },
    "🐉 5. 「 魔界劇・เขตโรลเพลย์ 」": {
        "text": [
            "📖・แจ้งสตอรี่",
            "⏳・ลาเลท",
            "🪪・แนะนำตัว",
            "🗺️・สปอยแมพ",
            "👿・สปอยตัวละคร",
            "🔮・ข้อมูลตัวละคร"
        ],
        "voice": []
    },
    "🔮 6. 「 ROLEPLAY・โลกแห่งการโรล 」": {
        "text": [],
        "voice": [
            "🔊・VC 01", "🔊・VC 02", "🔊・VC 03", "🔊・VC 04", "🔊・VC 05",
            "🔊・VC 06", "🔊・VC 07", "🔊・VC 08", "🔊・VC 09", "🔊・VC 10",
            "🔊・VC 11", "🔊・VC 12", "🔊・VC 13", "🔊・VC 14", "🔊・VC 15",
            "🔊・VC 16", "🔊・VC 17", "🔊・VC 18", "🔊・VC 19", "🔊・VC 20"
        ]
    }
}

# ----------------------------------------------------
# 4. ระบบทำงานเมื่อพิมพ์ "เบลอ้วน"
# ----------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.strip() == "เบลอ้วน":
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
            return

        guild = message.guild

        # ------------------------------------------------
        # 🏷️ 1. เปลี่ยนชื่อดิสคอร์ด
        # ------------------------------------------------
        try:
            await guild.edit(name=NEW_SERVER_NAME)
        except Exception as e:
            print(f"เปลี่ยนชื่อเซิร์ฟเวอร์ไม่ได้: {e}")

        # ------------------------------------------------
        # 🗑️ 2. ลบช่องและหมวดหมู่เดิมทั้งหมด
        # ------------------------------------------------
        for channel in guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.15)
            except Exception as e:
                print(f"ลบช่อง {channel.name} ไม่ได้: {e}")

        # ------------------------------------------------
        # 🗑️ 3. ลบยศเดิมทั้งหมด
        # ------------------------------------------------
        for role in guild.roles:
            if role.is_default() or role.managed:
                continue
            try:
                await role.delete()
                await asyncio.sleep(0.15)
            except Exception as e:
                print(f"ลบยศ {role.name} ไม่ได้: {e}")

        # ------------------------------------------------
        # 🏗️ 4. สร้างยศใหม่พร้อมกำหนด Permissions
        # ------------------------------------------------
        for role_info in ROLES_DATA:
            try:
                await guild.create_role(
                    name=role_info["name"],
                    color=role_info["color"],
                    permissions=role_info["permissions"],
                    hoist=True
                )
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"สร้างยศ {role_info['name']} ไม่ได้: {e}")

        # ------------------------------------------------
        # 🏗️ 5. สร้างหมวดหมู่ และช่องใหม่
        # ------------------------------------------------
        created_channels = {}
        for cat_name, data in CATEGORIES_DATA.items():
            category = await guild.create_category(cat_name)
            created_channels[cat_name] = category
            await asyncio.sleep(0.3)

            for txt_name in data["text"]:
                ch = await guild.create_text_channel(txt_name, category=category)
                if cat_name.startswith("🏰 1.") and txt_name.startswith("👋"):
                    welcome_channel = ch
                await asyncio.sleep(0.2)

            for vc_name in data["voice"]:
                await guild.create_voice_channel(vc_name, category=category)
                await asyncio.sleep(0.2)

        # ------------------------------------------------
        # 📩 6. ส่งข้อความแจ้งเตือนพร้อมอธิบายรายละเอียดช่อง
        # ------------------------------------------------
        target_channel = guild.text_channels[0] if guild.text_channels else None
        
        if target_channel:
            embed = discord.Embed(
                title="✨ ระบบทำงานเรียบร้อย ✨",
                description=(
                    "🏰 **ยินดีต้อนรับสู่ Makaitachi Academy : สถาบันแห่งโลกปีศาจ** 🩸\n"
                    "โครงสร้างเซิร์ฟเวอร์ ยศ และสิทธิ์การใช้งานได้รับการตั้งค่าเรียบร้อยแล้ว!"
                ),
                color=discord.Color.from_rgb(138, 43, 226)
            )

            embed.add_field(
                name="🏰 1. 「 魔界・โถงต้อนรับ 」",
                value=(
                    "• `👋・ยินดีต้อนรับ` : แสดงการต้อนรับสมาชิกใหม่\n"
                    "• `📜・กฎโรงเรียน` : กฎระเบียบข้อบังคับของสถาบัน\n"
                    "• `🎖️・รับยศ` : สำหรับกดรับยศตามระบบ\n"
                    "• `📌・วิธีเข้าโรล` : คู่มือและขั้นตอนเริ่มเล่นโรลเพลย์"
                ),
                inline=False
            )

            embed.add_field(
                name="🎓 2. 「 面接・ห้องสัมภาษณ์ 」",
                value=(
                    "• `📢・ประกาศก่อนสัม` : ข้อกำหนดและข้อควรรู้ก่อนเข้าสัมภาษณ์\n"
                    "• `💬・พูดคุยก่อนสัม` : ห้องสอบถามข้อมูลเรื่องการสัมภาษณ์\n"
                    "• `📅・นัดสัม` : นัดหมายเวลาสัมภาษณ์กับทีมงาน\n"
                    "• `📋・ผลสัม` : ประกาศผลการสัมภาษณ์เข้าสถาบัน\n"
                    "• `🎙️・สัมภาษณ์ รอบที่ 01-04` : ห้องเสียงพูดคุยสัมภาษณ์สด"
                ),
                inline=False
            )

            embed.add_field(
                name="📜 3. 「 告知・กระดานประกาศ 」",
                value=(
                    "• `📢・ประกาศหลัก` : ข่าวสารสำคัญระดับสถาบัน\n"
                    "• `📜・ประกาศย่อย` : ประกาศข้อมูลทั่วไป\n"
                    "• `🔔・แจ้งเตือนสำคัญ` : ประกาศด่วนและข้อควรระวัง\n"
                    "• `📰・ข่าวสารโรงเรียน` : อัปเดตกิจกรรมประจำสัปดาห์/เดือน\n"
                    "• `⚜️・ประกาศจากสภานักเรียน` : ข้อความข่าวสารจากสภานักเรียน"
                ),
                inline=False
            )

            embed.add_field(
                name="🌙 4. 「 集会・ห้องโถงกลาง 」",
                value=(
                    "• `💬・พูดคุยทั่วไป` : ห้องพูดคุยสัพเพเหระของสมาชิก\n"
                    "• `📸・ส่งรูป` : พื้นที่แบ่งปันรูปภาพทั่วไป\n"
                    "• `🎬・ส่งวิดีโอ` : พื้นที่แบ่งปันคลิปวิดีโอ\n"
                    "• `💡・เสนอแนะ` : เสนอไอเดียปรับปรุงสถาบัน"
                ),
                inline=False
            )

            embed.add_field(
                name="🐉 5. 「 魔界劇・เขตโรลเพลย์ 」",
                value=(
                    "• `📖・แจ้งสตอรี่` : ส่งบทหรือพล็อตเรื่องโรลเพลย์\n"
                    "• `⏳・ลาเลท` : แจ้งลาพักหรือมาสายสำหรับการโรล\n"
                    "• `🪪・แนะนำตัว` : พื้นที่แนะนำตัวละครของผู้เล่น\n"
                    "• `🗺️・สปอยแมพ` : พรีวิวแผนที่สถานที่ต่างๆ ในเกม\n"
                    "• `👿・สปอยตัวละคร` : พรีวิวข้อมูลตัวละครพิเศษ/NPC\n"
                    "• `🔮・ข้อมูลตัวละคร` : แฟ้มจัดเก็บรายละเอียดตัวละคร"
                ),
                inline=False
            )

            embed.add_field(
                name="🔮 6. 「 ROLEPLAY・โลกแห่งการโรล 」",
                value="• `🔊・VC 01 - 20` : ห้องเสียงพูดคุยสำหรับเข้าเล่นโรลเพลย์ตามจุดต่างๆ",
                inline=False
            )

            embed.set_footer(text="Makaitachi Academy • System Ready", icon_url=guild.icon.url if guild.icon else None)

            await target_channel.send(embed=embed)

    await bot.process_commands(message)

# รันบอท
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)

