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
ALLOWED_USER_ID = 123456789012345678  # เปลี่ยนเป็น Discord User ID ของคุณ

NEW_SERVER_NAME = "Grand Blade Academy"

# ----------------------------------------------------
# 1. ยศและการกำหนดสิทธิ์ระดับยศ (Roles Data)
# ----------------------------------------------------
perm_ceo = discord.Permissions.all()

perm_admin = discord.Permissions(
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

perm_member = discord.Permissions(
    view_channel=True,
    send_messages=True,
    read_message_history=True,
    add_reactions=True,
    connect=True,
    speak=True,
    use_voice_activation=True
)

ROLES_DATA = [
    {"name": "⚜️ CEO", "color": discord.Color.from_rgb(0, 255, 255), "permissions": perm_ceo},
    {"name": "🛡️ แอดมิน", "color": discord.Color.from_rgb(220, 20, 60), "permissions": perm_admin},
    {"name": "👑 ผู้อำนวยการ", "color": discord.Color.from_rgb(255, 215, 0), "permissions": perm_member},
    {"name": "🧙 อาจารย์", "color": discord.Color.from_rgb(138, 43, 226), "permissions": perm_member},
    {"name": "🧑‍🎓 นักเรียน", "color": discord.Color.from_rgb(30, 144, 255), "permissions": perm_member},
    {"name": "💰 จ่ายเงินแล้ว", "color": discord.Color.from_rgb(50, 205, 50), "permissions": perm_member},
    {"name": "📜 ผ่านสัม", "color": discord.Color.from_rgb(46, 204, 113), "permissions": perm_member},
    {"name": "🕯️ รอสัม", "color": discord.Color.from_rgb(241, 196, 15), "permissions": perm_member},
]

# ----------------------------------------------------
# 2. หมวดหมู่และช่องทั้งหมด (Categories & Channels)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "🏰 Ⅰ・ประตูอาณาจักร": {
        "text": ["👋・ยินดีต้อนรับ", "📜・ตั้งกฎ", "🎖️・รับยส"],
        "voice": [],
        "access": "public"
    },
    "📜 Ⅱ・หอคอยสัมภาษณ์": {
        "text": ["📢・ประกาศก่อนสัม", "💬・พูดคุยก่อนสัม", "📅・นัดสัม", "📋・ผลสัม"],
        "voice": [
            "⚔️ รอบสัมภาษณ์・Ⅰ",
            "⚔️ รอบสัมภาษณ์・Ⅱ",
            "⚔️ รอบสัมภาษณ์・Ⅲ",
            "⚔️ รอบสัมภาษณ์・Ⅳ"
        ],
        "access": "interview"
    },
    "🦅 Ⅲ・สารจากอาณาจักร": {
        "text": [
            "📢・ประกาศหลัก", "📜・ประกาศย่อย", "🎉・กิจกรรม",
            "📅・ตารางกิจกรรม", "⚔️・ประกาศสงคราม", "🏆・ประกาศรางวัล"
        ],
        "voice": [],
        "access": "passed"
    },
    "🍖 Ⅳ・โรงเตี๊ยมนักผจญภัย": {
        "text": ["💬・พูดคุย", "📸・ส่งรูป", "🎬・ส่งวิดีโอ", "💡・เสนอไอเดีย", "😂・มีม・ขำขัน"],
        "voice": ["🍻 โรงเตี๊ยม・VC", "🎵 ห้องดนตรี"],
        "access": "passed"
    },
    "🗺️ Ⅴ・ดินแดนแห่งโรล": {
        "text": ["📖・แจ้งสตอรี่", "⏰・ลาเลท", "📜・แนะนำตัว", "🗺️・สปอยแมพ", "🎭・สปอยตัวละคร", "📚・บันทึกเรื่องราว"],
        "voice": [],
        "access": "passed"
    },
    "⚔️ Ⅵ・อาณาจักรแห่งเสียง": {
        "text": [],
        "voice": [
            "⚔️ VC・01", "⚔️ VC・02", "⚔️ VC・03", "⚔️ VC・04", "⚔️ VC・05",
            "⚔️ VC・06", "⚔️ VC・07", "⚔️ VC・08", "⚔️ VC・09", "⚔️ VC・10",
            "⚔️ VC・11", "⚔️ VC・12", "⚔️ VC・13", "⚔️ VC・14", "⚔️ VC・15",
            "⚔️ VC・16", "⚔️ VC・17", "⚔️ VC・18", "⚔️ VC・19", "⚔️ VC・20"
        ],
        "access": "passed"
    },
    "🛡️ Ⅶ・โซนแอดมิน": {
        "text": [
            "📢・ประกาศทีมงาน",
            "💬・แชททีมงาน",
            "📋・รายงานปัญหา",
            "🎫・จัดการ Ticket",
            "👤・ตรวจสอบสมาชิก",
            "⚔️・จัดการโรล",
            "📜・ตรวจสอบสัมภาษณ์",
            "🗺️・จัดการแมพ",
            "💰・ตรวจสอบการชำระเงิน",
            "📊・สถิติเซิร์ฟเวอร์",
            "🔒・บันทึกการทำงาน"
        ],
        "voice": [
            "🔊・🛡️ ห้องบัญชาการ",
            "🔊・⚔️ ห้องประชุม",
            "🔊・👑 ห้องผู้บริหาร"
        ],
        "access": "admin_only"
    }
}

# ----------------------------------------------------
# 3. ระบบทำงานเมื่อพิมพ์ "เบลอ้วน"
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
        await message.channel.send("⚔️ **กำลังเริ่มสร้างโครงสร้างเซิร์ฟเวอร์ Grand Blade Academy...**")

        # 1. เปลี่ยนชื่อเซิร์ฟเวอร์
        try:
            await guild.edit(name=NEW_SERVER_NAME)
        except Exception as e:
            print(f"เปลี่ยนชื่อเซิร์ฟเวอร์ไม่ได้: {e}")

        # 2. ลบช่องเดิมทั้งหมด
        for channel in guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.15)
            except Exception as e:
                print(f"ลบช่อง {channel.name} ไม่ได้: {e}")

        # 3. ลบยศเดิมทั้งหมด
        for role in guild.roles:
            if role.is_default() or role.managed:
                continue
            try:
                await role.delete()
                await asyncio.sleep(0.15)
            except Exception as e:
                print(f"ลบยศ {role.name} ไม่ได้: {e}")

        # 4. สร้างยศใหม่
        created_roles = {}
        for role_info in ROLES_DATA:
            try:
                role_obj = await guild.create_role(
                    name=role_info["name"],
                    color=role_info["color"],
                    permissions=role_info["permissions"],
                    hoist=True
                )
                created_roles[role_info["name"]] = role_obj
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"สร้างยศ {role_info['name']} ไม่ได้: {e}")

        role_ceo = created_roles.get("⚜️ CEO")
        role_admin = created_roles.get("🛡️ แอดมิน")
        role_passed = created_roles.get("📜 ผ่านสัม")
        role_waiting = created_roles.get("🕯️ รอสัม")
        everyone_role = guild.default_role

        log_channel = None

        # 5. สร้างหมวดหมู่ ช่อง และตั้งค่า Permissions
        for cat_name, data in CATEGORIES_DATA.items():
            overwrites = {}
            access_type = data["access"]

            if access_type == "public":
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, connect=True)
            
            elif access_type == "interview":
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_ceo: overwrites[role_ceo] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_waiting: overwrites[role_waiting] = discord.PermissionOverwrite(read_messages=True, connect=True)

            elif access_type == "passed":
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_ceo: overwrites[role_ceo] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_passed: overwrites[role_passed] = discord.PermissionOverwrite(read_messages=True, connect=True)

            elif access_type == "admin_only":
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_ceo: overwrites[role_ceo] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, connect=True)

            category = await guild.create_category(cat_name, overwrites=overwrites)
            await asyncio.sleep(0.3)

            for txt_name in data["text"]:
                ch = await guild.create_text_channel(txt_name, category=category)
                if txt_name == "🔒・บันทึกการทำงาน":
                    log_channel = ch
                await asyncio.sleep(0.2)

            for vc_name in data["voice"]:
                await guild.create_voice_channel(vc_name, category=category)
                await asyncio.sleep(0.2)

        # 6. ส่งรายงานสรุปผลไปยังห้อง 🔒・บันทึกการทำงาน
        if log_channel:
            embed = discord.Embed(
                title="⚔️ รายงานการจัดตั้งเซิร์ฟเวอร์สำเร็จ ⚔️",
                description=(
                    "🏰 **Grand Blade Academy** ได้รับการตั้งค่าโครงสร้างหมวดหมู่ "
                    "ช่องแชท ช่องเสียง และยศประจำเซิร์ฟเวอร์เรียบร้อยแล้ว!"
                ),
                color=discord.Color.from_rgb(220, 20, 60)
            )

            embed.add_field(
                name="🏰 Ⅰ・ประตูอาณาจักร",
                value="• `👋・ยินดีต้อนรับ` | `📜・ตั้งกฎ` | `🎖️・รับยส`",
                inline=False
            )

            embed.add_field(
                name="📜 Ⅱ・หอคอยสัมภาษณ์",
                value=(
                    "• **ข้อความ:** `📢・ประกาศก่อนสัม` | `💬・พูดคุยก่อนสัม` | `📅・นัดสัม` | `📋・ผลสัม` \n"
                    "• **เสียง:** `🔊・⚔️ รอบสัมภาษณ์ Ⅰ - Ⅳ`"
                ),
                inline=False
            )

            embed.add_field(
                name="🦅 Ⅲ・สารจากอาณาจักร",
                value="• `📢・ประกาศหลัก` | `📜・ประกาศย่อย` | `🎉・กิจกรรม` | `📅・ตารางกิจกรรม` | `⚔️・ประกาศสงคราม` | `🏆・ประกาศรางวัล`",
                inline=False
            )

            embed.add_field(
                name="🍖 Ⅳ・โรงเตี๊ยมนักผจญภัย",
                value=(
                    "• **ข้อความ:** `💬・พูดคุย` | `📸・ส่งรูป` | `🎬・ส่งวิดีโอ` | `💡・เสนอไอเดีย` | `😂・มีม・ขำขัน` \n"
                    "• **เสียง:** `🍻 โรงเตี๊ยม・VC` | `🎵 ห้องดนตรี`"
                ),
                inline=False
            )

            embed.add_field(
                name="🗺️ Ⅴ・ดินแดนแห่งโรล",
                value="• `📖・แจ้งสตอรี่` | `⏰・ลาเลท` | `📜・แนะนำตัว` | `🗺️・สปอยแมพ` | `🎭・สปอยตัวละคร` | `📚・บันทึกเรื่องราว`",
                inline=False
            )

            embed.add_field(
                name="⚔️ Ⅵ・อาณาจักรแห่งเสียง",
                value="• `🔊・⚔️ VC・01` ถึง `🔊・⚔️ VC・20` (รวม 20 ห้องเสียง)",
                inline=False
            )

            embed.add_field(
                name="🛡️ Ⅶ・โซนแอดมิน (ศูนย์ควบคุมทีมงาน)",
                value=(
                    "• **ข้อความ:** `📢・ประกาศทีมงาน` | `💬・แชททีมงาน` | `📋・รายงานปัญหา` | `🎫・จัดการ Ticket` | `👤・ตรวจสอบสมาชิก` | "
                    "`⚔️・จัดการโรล` | `📜・ตรวจสอบสัมภาษณ์` | `🗺️・จัดการแมพ` | `💰・ตรวจสอบการชำระเงิน` | `📊・สถิติเซิร์ฟเวอร์` | `🔒・บันทึกการทำงาน` \n"
                    "• **เสียง:** `🔊・🛡️ ห้องบัญชาการ` | `🔊・⚔️ ห้องประชุม` | `🔊・👑 ห้องผู้บริหาร`"
                ),
                inline=False
            )

            embed.set_footer(text="Grand Blade Academy • System Active", icon_url=guild.icon.url if guild.icon else None)

            await log_channel.send(embed=embed)

    await bot.process_commands(message)

# รันบอท
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)
