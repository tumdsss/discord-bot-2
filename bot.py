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

NEW_SERVER_NAME = "Makaitachi Academy : สถาบันแห่งโลกปีศาจ"

# ----------------------------------------------------
# 1. ยศและการกำหนดสิทธิ์ระดับยศ (Roles Data)
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
# 2. หมวดหมู่และช่องทั้งหมด (รวมโซน 7)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "🏰 1. 「 魔界・โถงต้อนรับ 」": {
        "text": ["👋・ยินดีต้อนรับ", "📜・กฎโรงเรียน", "🎖️・รับยศ", "📌・วิธีเข้าโรล"],
        "voice": [],
        "access": "public"  # ไม่จำกัดยศ
    },
    "🎓 2. 「 面接・ห้องสัมภาษณ์ 」": {
        "text": ["📢・ประกาศก่อนสัม", "💬・พูดคุยก่อนสัม", "📅・นัดสัม", "📋・ผลสัม"],
        "voice": ["🎙️・สัมภาษณ์ รอบที่ 01", "🎙️・สัมภาษณ์ รอบที่ 02", "🎙️・สัมภาษณ์ รอบที่ 03", "🎙️・สัมภาษณ์ รอบที่ 04"],
        "access": "interview"  # CEO, แอดมิน, รอสัม
    },
    "📜 3. 「 告知・กระดานประกาศ 」": {
        "text": ["📢・ประกาศหลัก", "📜・ประกาศย่อย", "🔔・แจ้งเตือนสำคัญ", "📰・ข่าวสารโรงเรียน", "⚜️・ประกาศจากสภานักเรียน"],
        "voice": [],
        "access": "passed"  # CEO, แอดมิน, ผ่านสัม
    },
    "🌙 4. 「 集会・ห้องโถงกลาง 」": {
        "text": ["💬・พูดคุยทั่วไป", "📸・ส่งรูป", "🎬・ส่งวิดีโอ", "💡・เสนอแนะ"],
        "voice": [],
        "access": "passed"  # CEO, แอดมิน, ผ่านสัม
    },
    "🐉 5. 「 魔界劇・เขตโรลเพลย์ 」": {
        "text": ["📖・แจ้งสตอรี่", "⏳・ลาเลท", "🪪・แนะนำตัว", "🗺️・สปอยแมพ", "👿・สปอยตัวละคร", "🔮・ข้อมูลตัวละคร"],
        "voice": [],
        "access": "passed"  # CEO, แอดมิน, ผ่านสัม
    },
    "🔮 6. 「 ROLEPLAY・โลกแห่งการโรล 」": {
        "text": [],
        "voice": [
            "🔊・VC 01", "🔊・VC 02", "🔊・VC 03", "🔊・VC 04", "🔊・VC 05",
            "🔊・VC 06", "🔊・VC 07", "🔊・VC 08", "🔊・VC 09", "🔊・VC 10",
            "🔊・VC 11", "🔊・VC 12", "🔊・VC 13", "🔊・VC 14", "🔊・VC 15",
            "🔊・VC 16", "🔊・VC 17", "🔊・VC 18", "🔊・VC 19", "🔊・VC 20"
        ],
        "access": "passed"  # CEO, แอดมิน, ผ่านสัม
    },
    "🔐 7. 「 管理者・โซนแอดมิน 」": {
        "text": [
            "📋・จัดการสมาชิก", "🎓・จัดการนักเรียน", "📚・จัดการอาจารย์",
            "📢・ประกาศสำหรับทีมงาน", "📝・บันทึกการทำงาน", "⚠️・แจ้งปัญหาภายใน",
            "💰・ตรวจสอบการชำระเงิน", "🎫・จัดการตั๋ว", "📖・จัดการสตอรี่", "🛠️・จัดการเซิร์ฟเวอร์"
        ],
        "voice": ["🔊・ห้องประชุมทีมงาน", "🔊・ห้อง Staff", "🔒・ห้องลับผู้บริหาร"],
        "access": "admin_only"  # CEO, แอดมิน
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
        await message.channel.send("⚠️ **กำลังเริ่มรีเซ็ต กำหนดสิทธิ์ และสร้าง Makaitachi Academy...**")

        # 1. เปลี่ยนชื่อดิสคอร์ด
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

        # 4. สร้างยศใหม่ และเก็บ Reference ไว้ใช้ตั้ง Permissions
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

        # ดึงยศหลักๆ มาใช้งาน
        role_ceo = created_roles.get("💎 CEO")
        role_admin = created_roles.get("🛡️ แอดมิน")
        role_passed = created_roles.get("🩸 ผ่านสัม")
        role_waiting = created_roles.get("⏳ รอสัม")
        everyone_role = guild.default_role

        log_channel = None  # เก็บห้องที่จะส่งสรุปผล

        # 5. สร้างหมวดหมู่ ช่อง และตั้งค่า Permissions ของแต่ละโซน
        for cat_name, data in CATEGORIES_DATA.items():
            overwrites = {}
            access_type = data["access"]

            if access_type == "public":
                # โซน 1: ให้คนทั่วไปดูได้ปกติ
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=True, connect=True)
            
            elif access_type == "interview":
                # โซน 2: ปิดคนทั่วไป, เปิดให้ CEO, แอดมิน, รอสัม
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_ceo: overwrites[role_ceo] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_waiting: overwrites[role_waiting] = discord.PermissionOverwrite(read_messages=True, connect=True)

            elif access_type == "passed":
                # โซน 3-6: ปิดคนทั่วไป, เปิดให้ CEO, แอดมิน, ผ่านสัม
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_ceo: overwrites[role_ceo] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_passed: overwrites[role_passed] = discord.PermissionOverwrite(read_messages=True, connect=True)

            elif access_type == "admin_only":
                # โซน 7: ปิดคนทั่วไป, เปิดให้เฉพาะ CEO, แอดมิน
                overwrites[everyone_role] = discord.PermissionOverwrite(read_messages=False, connect=False)
                if role_ceo: overwrites[role_ceo] = discord.PermissionOverwrite(read_messages=True, connect=True)
                if role_admin: overwrites[role_admin] = discord.PermissionOverwrite(read_messages=True, connect=True)

            # สร้าง Category พร้อม Overwrites สิทธิ์
            category = await guild.create_category(cat_name, overwrites=overwrites)
            await asyncio.sleep(0.3)

            # สร้าง Text Channels
            for txt_name in data["text"]:
                ch = await guild.create_text_channel(txt_name, category=category)
                if txt_name == "📝・บันทึกการทำงาน":
                    log_channel = ch
                await asyncio.sleep(0.2)

            # สร้าง Voice Channels
            for vc_name in data["voice"]:
                await guild.create_voice_channel(vc_name, category=category)
                await asyncio.sleep(0.2)

        # 6. ส่งสรุปผลไปยังห้อง 📝・บันทึกการทำงาน
        if log_channel:
            embed = discord.Embed(
                title="⚙️ บันทึกการติดตั้งระบบสถาบัน",
                description=(
                    "🏰 **Makaitachi Academy : สถาบันแห่งโลกปีศาจ** 🩸\n"
                    "ระบบได้ทำการรีเซ็ตเซิร์ฟเวอร์ สร้างห้อง ยศ และกำหนดสิทธิ์การเข้าถึงเรียบร้อยแล้ว!"
                ),
                color=discord.Color.from_rgb(220, 20, 60)
            )

            embed.add_field(
                name="🏰 1. 「 魔界・โถงต้อนรับ 」 (สาธารณะ)",
                value="• ทุกคนเห็นได้ทั่วไป สำหรับต้อนรับ แจ้งกฎ รับยศ และสอนวิธีเข้าโรล",
                inline=False
            )
            embed.add_field(
                name="🎓 2. 「 面接・ห้องสัมภาษณ์ 」 (เฉพาะ รอสัม / Admin / CEO)",
                value="• สำหรับประกาศ นัดหมาย สัมภาษณ์สด และแจ้งผลสัมภาษณ์เข้าสถาบัน",
                inline=False
            )
            embed.add_field(
                name="📜 3. 「 告知・กระดานประกาศ 」 (เฉพาะ ผ่านสัม / Admin / CEO)",
                value="• กระดานประกาศหลัก ประกาศย่อย ข่าวสาร และการแจ้งเตือนสำคัญ",
                inline=False
            )
            embed.add_field(
                name="🌙 4. 「 集会・ห้องโถงกลาง 」 (เฉพาะ ผ่านสัม / Admin / CEO)",
                value="• พื้นที่พูดคุยทั่วไป ส่งรูป วิดีโอ และเสนอแนะความคิดเห็น",
                inline=False
            )
            embed.add_field(
                name="🐉 5. 「 魔界劇・เขตโรลเพลย์ 」 (เฉพาะ ผ่านสัม / Admin / CEO)",
                value="• แจ้งสตอรี่ ลาเลท แนะนำตัว และดูข้อมูล/สปอยตัวละครและแผนที่",
                inline=False
            )
            embed.add_field(
                name="🔮 6. 「 ROLEPLAY・โลกแห่งการโรล 」 (เฉพาะ ผ่านสัม / Admin / CEO)",
                value="• ห้องเสียง VC 01 - VC 20 สำหรับใช้พูดคุยเล่นโรลเพลย์",
                inline=False
            )
            embed.add_field(
                name="🔐 7. 「 管理者・โซนแอดมิน 」 (เฉพาะ Admin / CEO)",
                value="• ศูนย์บริหารจัดการสมาชิก นักเรียน อาจารย์ สตอรี่ ตั๋ว ระบบ และบันทึกการทำงาน",
                inline=False
            )

            embed.set_footer(text="ระบบทำงานเสร็จสมบูรณ์ • Makaitachi Academy", icon_url=guild.icon.url if guild.icon else None)

            await log_channel.send(embed=embed)

    await bot.process_commands(message)

# รันบอท
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)
