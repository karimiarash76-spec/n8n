# -*- coding: utf-8 -*-
import csv, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from articles import ARTICLES, CALENDAR, HOUSE, HERO_AR, INLINE_AR, NEGATIVE

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "package", "fonts", "ttf")
OUT = os.path.join(HERE, "..", "out")
os.makedirs(OUT, exist_ok=True)

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
def fa(x): return str(x).translate(FA)
def e(x): return html.escape(str(x))
SITE = "https://iransorang.com/"
BY_N = {a["n"]: a for a in ARTICLES}

def full_prompt(img):
    ar = HERO_AR if img["role"] == "hero" else INLINE_AR
    return f'{img["scene"]} {ar} {HOUSE}'

def file_name(a, img):
    suffix = {"hero": "hero", "inline1": "inline-1", "inline2": "inline-2"}[img["role"]]
    return f'{a["fslug"]}-{suffix}.webp'

def img_size(img):
    return "1200×675 (16:9)" if img["role"] == "hero" else "800×600 (4:3)"

ROLE_FA = {"hero": "تصویر شاخص", "inline1": "تصویر داخل متن ۱", "inline2": "تصویر داخل متن ۲"}

# ------------------------------------------------------------------ static report data
COMPETITORS = [
 ("torob.com · emalls.ir · basalam.com", "مقایسه‌گر قیمت / بازارچه",
  "«قیمت سرنگ ۵ سی سی کارتنی»، «سرنگ انسولین ۱۰۰ واحدی قیمت»، «لیست قیمت سرنگ»",
  "اعتبار دامنه، صدها فروشنده، به‌روزرسانی روزانه‌ی قیمت",
  "محتوای آموزشی ندارند. به‌جای رقابت، محصولات ایران سرنگ را در خود این پلتفرم‌ها ثبت کنید تا در SERP تراکنشی حضور داشته باشید."),
 ("minasorangonline.com", "تولیدکننده با فروش عمده‌ی مستقیم (رقیب مستقیم B2B)",
  "«خرید سرنگ با قیمت عمده ۱۴۰۵»، «سرنگ گاواژ»، «سرنگ سه تکه»، «انواع سرنگ تزریق (۹ مدل)»",
  "عنوان‌های سال‌دار، ارسال رایگان، تخفیف کارتنی، مقاله‌ی ستون «انواع سرنگ»",
  "فقط یک برند را می‌فروشد؛ ایران سرنگ چندبرندی است. مقایسه‌ی برندها و جدول‌های چندبرندی مزیتی است که این رقیب نمی‌تواند تکرار کند."),
 ("sohateb.com · samintebmehr.ir", "سایت خود برندها (هم تأمین‌کننده، هم رقیب SERP)",
  "«سایزهای سرنگ»، «میکروست»، «ماسک اکسیژن»",
  "اعتبار سازنده",
  "مقالات کوتاه و قدیمی. از این برندها لینک «نمایندگان/پخش‌کنندگان» بگیرید؛ بک‌لینکی مرتبط و طبیعی است."),
 ("tavanino.com · sedanmed.com · irantebco.com · tebtolid.com · mirzakhaniteb.com · arkanteb.ir", "فروشگاه/پخش تجهیزات پزشکی با فروش عمده",
  "صفحات دسته‌ی سرنگ؛ «ست سرم و میکروست»؛ «معرفی سرنگ لوئرلاک»؛ «تجهیز مطب»",
  "تنوع محصول بالا، صفحات دسته‌ی قوی",
  "مقالات عمومی بدون تعداد در کارتن، قیمت هر عدد یا کد IRC؛ دقیقاً همان داده‌ای که ایران سرنگ دارد."),
 ("hamyarmed.com · dermarozteb.com · tgamedico.com · zeemano.com · mosbatesabz.com · medkala.co · darmankala.com · timche360.com · imedtajhiz.com", "فروشگاه آنلاین با وبلاگ فعال",
  "«سرنگ لوئرلاک چیست»، «هر واحد سرنگ انسولین چند سی سی است»، «انواع سایز سرنگ»، «فرق ست سرم و ست خون»",
  "پوشش موضوعی گسترده و قدیمی‌بودن صفحات",
  "محتوای مشابه هم، بدون جدول داده‌ی واقعی و با تناقض در اعداد (فیلتر ست خون، درجه‌بندی سرنگ ۳۰ واحدی). عمق، جدول و منبع‌دهی آن‌ها را شکست می‌دهد."),
 ("aradbranding.com", "تولید انبوه صفحه",
  "ده‌ها صفحه‌ی «خرید/قیمت سرنگ انسولین/شیشه‌ای/زیرجلدی»",
  "تعداد زیاد صفحه",
  "محتوای کم‌عمق و تبلیغاتی. یک مقاله‌ی عمیق و داده‌محور معمولاً از چند صفحه‌ی سطحی جلو می‌زند."),
 ("doctoreto.com · salmandjan.ir · nabzeaval.com · globalclinic.online", "ناشر سلامت",
  "«انواع انسولین»، «انواع سرنگ انسولین (۱۲ مدل)»، «تنظیم قطرات سرم»",
  "اعتبار سلامت (E-E-A-T) و نگارش بیمارمحور",
  "دید خرید و کاتالوگ ندارند. ایران سرنگ با جدول مدل‌های موجود و مصرف ماهانه، پاسخ «حالا چه بخرم؟» را می‌دهد."),
 ("damyaran.com · vetshoop.ir · iranvet.ir · irandamdar.com · gohardam.com", "فروشگاه دامپزشکی",
  "«سرنگ دامپزشکی»، «سرنگ اتوماتیک»",
  "مخاطب دامدار",
  "راهنمای خرید سرنگ یکبار مصرف عمده برای دامداری وجود ندارد؛ بازار تازه برای انبارهای مشهد و بجنورد."),
 ("nhiso.com · hospexa.com · damirco.com · ghapple.com", "خدمات ثبت و مشاوره",
  "«کد IRC چیست»، «استعلام کد IRC»",
  "پوشش موضوع رگولاتوری",
  "تناقض در جزئیات و بدون مثال محصولی. ایران سرنگ می‌تواند با کد IRC واقعی محصولات خودش مثال بزند."),
]

GAPS = [
 ("جدول سایز گیج سوزن سرنگ رنگ", "جدول مته و گیج سیم؛ صفحه‌ی فارسی مرتبط نبود", "خالی", "بسیار زیاد", 4),
 ("سایز سوند معده NG tube", "فقط منابع انگلیسی", "خالی", "بسیار زیاد", 16),
 ("سرنگ گاواژ ۵۰ سی سی کاربرد", "فقط لیست‌های فروش emalls", "ضعیف", "زیاد", 19),
 ("استریل اتیلن اکساید / تاریخ انقضا سرنگ", "فقط مقالات علمی انگلیسی", "خالی", "زیاد", 25),
 ("تشخیص سرنگ BD اصل از تقلبی", "بلبرینگ، عطر، اسپیکر؛ فقط یک صفحه‌ی مرتبط", "ضعیف", "زیاد", 11),
 ("بهترین برند سرنگ ایرانی", "لوازم آرایشی، آبرنگ، قاشق؛ چند صفحه‌ی دسته‌ی فروشگاهی", "ضعیف", "زیاد", 23),
 ("کانولای بینی یا ماسک اکسیژن", "Wikipedia، UCSF و منابع انگلیسی", "ضعیف (برای فارسی)", "زیاد", 18),
 ("میکروست چیست", "در جستجوی ساده نتایج نامرتبط؛ در جستجوی دقیق چند وبلاگ فروشگاهی", "متوسط", "متوسط تا زیاد", 12),
 ("محاسبه قطرات سرم", "وبلاگ‌های پرستاری، یک کلینیک آنلاین، جزوه‌ی دانشگاهی", "متوسط؛ بدون ابزار تعاملی تمیز", "متوسط تا زیاد", 13),
 ("سرنگ لوئر لاک چیست / تفاوت با لوئر اسلیپ", "۶ تا ۸ وبلاگ فروشگاهی", "متوسط؛ تکراری", "متوسط", 2),
 ("هر واحد سرنگ انسولین چند سی سی است", "چند فروشگاه و ناشر سلامت", "خوب ولی متناقض", "متوسط", 9),
 ("استعلام کد IRC تجهیزات پزشکی", "سایت‌های خدمات ثبت", "متوسط؛ متناقض", "متوسط", 22),
 ("لیست تجهیزات مصرفی مطب", "لیست دستگاه‌ها، نه اقلام مصرفی", "متوسط", "متوسط", 21),
 ("خرید عمده سرنگ / قیمت سرنگ", "ترب، ایمالز، باسلام، صفحات دسته", "قوی (تراکنشی)", "کم برای وبلاگ؛ مخصوص صفحه‌ی فرود", None),
]

LANDINGS = [
 ("5963", "خرید عمده سرنگ", "خرید عمده سرنگ · قیمت عمده سرنگ", [1, 8, 20, 21, 23, 24]),
 ("5964", "سرنگ ۵ سی سی", "سرنگ ۵ سی سی", [2, 4, 5, 6]),
 ("5965", "سرنگ ۱۰ سی سی", "سرنگ ۱۰ سی سی", [2, 5, 6]),
 ("5966", "سرنگ ۳ سی سی", "سرنگ ۳ سی سی", [3, 5]),
 ("5967", "سرنگ ۲۰ سی سی", "سرنگ ۲۰ سی سی", [2, 5, 20]),
 ("5968", "سرنگ ۲ سی سی", "سرنگ ۲ سی سی", [3, 5, 6]),
 ("5969", "سرنگ ۵۰ سی سی", "سرنگ ۵۰ سی سی", [2, 5, 19, 20]),
 ("5970", "سرنگ انسولین", "سرنگ انسولین · قیمت سرنگ انسولین", [7, 9, 10, 11]),
 ("5971", "ست سرم", "ست سرم · قیمت ست سرم", [12, 13, 14]),
 ("5972", "میکروست", "میکروست · خرید میکروست", [12, 13]),
 ("5973", "ست خون", "ست خون · خرید ست خون", [14]),
 ("5974", "سرنگ گاواژ", "سرنگ گاواژ · قیمت سرنگ گاواژ", [16, 19, 20]),
 ("5975", "ماسک اکسیژن", "ماسک اکسیژن · خرید ماسک اکسیژن", [17, 18]),
 ("5976", "سوند نلاتون", "سوند نلاتون · خرید سوند نلاتون", [15]),
 ("5977", "سوند معده", "سوند معده · خرید سوند معده", [16]),
 ("5978", "لوله اکسیژن", "لوله اکسیژن · خرید کانولای بینی", [18]),
 ("5076–5089", "صفحات برندها", "نام هر برند", [11, 23]),
]

CLUSTERS = [
 ("A", "مبانی سرنگ", [1, 2, 3, 4, 5, 6], "صفحات سایز ۲ تا ۵۰ سی سی + خرید عمده (5963)"),
 ("B", "سرنگ انسولین و دوزهای کوچک", [7, 9, 10, 11], "سرنگ انسولین (5970) + برند BD (5089)"),
 ("C", "سرم‌درمانی و انتقال خون", [12, 13, 14], "ست سرم (5971)، میکروست (5972)، ست خون (5973)"),
 ("D", "سوندها، گاواژ و راه هوایی", [15, 16, 17, 18, 19], "سوند نلاتون، سوند معده، ماسک، لوله اکسیژن، سرنگ گاواژ"),
 ("E", "خرید سازمانی، کیفیت و اعتماد (B2B)", [8, 21, 22, 23, 24, 25], "خرید عمده (5963)، استعلام قیمت (6197)، صفحات برندها"),
 ("F", "بازارهای تازه", [20], "خرید عمده (5963)، سرنگ ۵۰ سی سی و گاواژ"),
]

SOURCES = [
 "https://minasorangonline.com/syringe/", "https://minasorangonline.com/types-of-syringes/", "https://torob.com/browse/3916/",
 "https://emalls.ir/", "https://basalam.com/", "https://tavanino.com/What-is-a-serum-and-microst-set", "https://sedanmed.com/",
 "https://www.irantebco.com/", "https://tebtolid.com/", "https://hamyarmed.com/blog/", "https://dermarozteb.com/how-many-cc-is-each-unit-of-insulin-syringe/",
 "https://dermarozteb.com/injection-set-vs-blood-injection-set/", "https://tgamedico.com/", "https://zeemano.com/", "https://mosbatesabz.com/",
 "https://medkala.co/different-syringe-sizes/", "https://sohateb.com/", "https://darmankala.com/blog/types-syringes/", "https://timche360.com/",
 "https://imedtajhiz.com/", "https://aradbranding.com/fa/", "https://salmandjan.ir/types-of-insulin-syringes/", "https://doctoreto.com/blog/types-of-insulin/",
 "https://globalclinic.online/home-care/setting-serum-drops-techniques-formulas/", "https://samintebmehr.ir/", "https://dibaexon.com/",
 "https://aspirin24.com/blog/what-is-micro-set/", "https://www.behnamteb.com/", "https://tebsho.com/", "https://www.taminsho.com/blog/post/57",
 "https://nhiso.com/what-is-the-meaning-of-irc-code/", "https://hospexa.com/medical-equipment-inquiry/", "https://damirco.com/blog/1660/medical-equipment-authenticity-verification-guide",
 "https://damyaran.com/", "https://vetshoop.ir/", "https://iranvet.ir/", "https://irandamdar.com/", "https://gohardam.com/",
 "https://sedanmed.com/blog/article/equip-the-policlinic", "https://www.sahraeimed.com/complete-list-of-general-practitioner-office-equipment/",
 "https://www.compat.com/ngt-selection/", "https://hospitalhandbook.ucsf.edu/12-oxygen-therapy/12-oxygen-therapy-0",
 "https://scielo.org.za/scielo.php?script=sci_arttext&pid=S1681-150X2014000400006", "https://bouali.mui.ac.ir/ (جزوه‌ی محاسبات دارویی)",
 "https://imed.ir/", "https://ttac.ir/", "https://ivo.ir/", "https://stayconnected.org/",
]

# ------------------------------------------------------------------ helpers
def tier_d(d):
    if d.startswith("زیاد") or d.startswith("متوسط تا زیاد"): return 0
    if d.startswith("متوسط"): return 1
    return 2
def tier_k(k):
    if k == "کم" or k.startswith("کم ("): return 0
    if k.startswith("کم تا متوسط"): return 1
    return 2

import re
def ltr_urls(t):
    return re.sub(r"(https?://[^\s؛،)]+)", r'<span dir="ltr">\1</span>', e(t))

def chip(t, cls=""): return f'<span class="chip {cls}">{e(t)}</span>'
def alink(n): return f'<a href="#a{n}">{fa(n)}</a>'

def url_of(a): return f'{SITE}{a["slug"]}/'

# ------------------------------------------------------------------ sections
def cover():
    return f'''
<section class="cover">
  <div class="cover-top">
    <div class="brandline">iransorang.com</div>
    <h1>تحقیق رقابتی سئو و نقشه‌ی محتوای ۲۵ مقاله‌ای ایران سرنگ</h1>
    <p class="lead">تحلیل رقبا و SERP فارسی، شکاف‌های محتوایی، کلمات کلیدی و URLهای پیشنهادی، بریف کامل هر مقاله برای رتبه‌گرفتن در گوگل و ۷۵ پرامپت تخصصی تصویر</p>
  </div>
  <div class="stats">
    <div class="stat"><b>{fa(25)}</b><span>بریف مقاله</span></div>
    <div class="stat"><b>{fa(75)}</b><span>پرامپت تصویر</span></div>
    <div class="stat"><b>{fa(6)}</b><span>خوشه‌ی موضوعی</span></div>
    <div class="stat"><b>{fa(13)}</b><span>هفته تقویم انتشار</span></div>
    <div class="stat"><b>{fa(30)}</b><span>کوئری SERP بررسی‌شده</span></div>
    <div class="stat"><b>+{fa(40)}</b><span>دامنه‌ی رقیب</span></div>
  </div>
  <div class="cover-foot">
    <div>تاریخ تهیه: ۴ آبان ۱۴۰۵ (۲۶ اکتبر ۲۰۲۶)</div>
    <div>بازار هدف: جستجوی فارسی گوگل در ایران · مخاطب: داروخانه‌ها، مطب‌ها، کلینیک‌ها، بیمارستان‌ها، دامداری‌ها و مصرف‌کننده‌ی نهایی</div>
  </div>
</section>'''

def toc():
    items = [("s1", "خلاصه‌ی مدیریتی"), ("s2", "روش تحقیق و محدودیت‌ها"), ("s3", "دارایی‌های فعلی سایت"),
             ("s4", "نقشه‌ی رقبا"), ("s5", "تحلیل شکاف SERP"), ("s6", "معماری خوشه‌های موضوعی"),
             ("s7", "نقشه‌ی جلوگیری از هم‌نوع‌خواری"), ("s8", "ماتریس اولویت"), ("s9", "تقویم انتشار ۱۳ هفته‌ای"),
             ("s10", "جدول کلمات کلیدی و URLها"), ("s11", "استاندارد نگارش و سئوی داخلی"), ("s12", "راهنمای تولید تصویر"),
             ("s13", "بریف ۲۵ مقاله"), ("s14", "اقدامات تکمیلی برای رتبه‌ی یک"), ("s15", "شاخص‌های پایش"), ("s16", "منابع")]
    lis = "".join(f'<li><a href="#{i}"><span class="num">{fa(k)}.</span> {e(t)}</a></li>' for k, (i, t) in enumerate(items, 1))
    arts = "".join(f'<li><a href="#a{a["n"]}"><span class="num">{fa(a["n"])}</span> {e(a["h1"])}</a></li>' for a in ARTICLES)
    return f'''
<section class="page" id="toc">
  <h2 class="sec">فهرست مطالب</h2>
  <ol class="toc">{lis}</ol>
  <h3 class="sub">بریف مقالات</h3>
  <ol class="toc-arts">{arts}</ol>
</section>'''

def summary():
    return f'''
<section class="page" id="s1">
  <h2 class="sec">۱. خلاصه‌ی مدیریتی</h2>
  <div class="callout">
    <b>جمع‌بندی در یک جمله:</b> جستجوی فارسی سرنگ و ملزومات تزریقی دو لایه دارد. کلمات «قیمت/خرید» در اختیار مقایسه‌گرهای قیمت و صفحات دسته‌ی فروشگاه‌هاست. کلمات آموزشی و مقایسه‌ای در اختیار وبلاگ‌هایی است که محتوای مشابه و گاه متناقض دارند. ایران سرنگ با داده‌ی زنده‌ی کاتالوگ (قیمت هر عدد، تعداد در کارتن، کد IRC و ۱۲ برند) می‌تواند در لایه‌ی دوم جایگاه اول را بگیرد و ترافیک را به صفحات فرود تجاری خودش برساند.
  </div>
  <h3 class="sub">یافته‌های کلیدی</h3>
  <ol class="nice">
    <li><b>شش شکاف خالی در SERP فارسی:</b> جدول گیج سرسوزن، سایز سوند معده، محتوای آموزشی سرنگ گاواژ، تاریخ انقضا و انبارداری سرنگ، تشخیص اصالت سرنگ BD و «بهترین برند سرنگ ایرانی». برای این عبارت‌ها یا نتیجه‌ی فارسی مرتبطی در صدر نبود یا نتایج نامرتبط بودند. این‌ها سریع‌ترین مسیر رتبه‌ی یک هستند.</li>
    <li><b>رقیب مستقیم B2B:</b> سایت مینا سرنگ آنلاین با صفحات «قیمت عمده ۱۴۰۵»، ارسال رایگان و مقاله‌ی ستون «انواع سرنگ». این سایت فقط یک برند دارد. مقایسه‌ی چندبرندی مزیتی است که این رقیب نمی‌تواند تکرار کند.</li>
    <li><b>برندها هم رقیب SERP هستند:</b> سایت سها طب و وبلاگ ثمین طب مهر در کلمات «سایز سرنگ»، «میکروست» و «ماسک اکسیژن» دیده می‌شوند. این برندها تأمین‌کننده‌ی ایران سرنگ‌اند و می‌توانند منبع بک‌لینک مرتبط باشند.</li>
    <li><b>کیفیت محتوای رقبا پایین و تکراری است.</b> درباره‌ی منافذ فیلتر ست خون، درجه‌بندی سرنگ ۳۰ واحدی و تعداد رقم کد IRC، منابع رتبه‌دار با هم تناقض دارند. مقاله‌ای که این تناقض‌ها را با استناد به استاندارد ISO یا سامانه‌ی رسمی حل کند، «افزوده‌ی اطلاعاتی» واقعی دارد؛ همان چیزی که گوگل پاداش می‌دهد.</li>
    <li><b>بخش تازه‌ی بازار:</b> دامداری‌ها و مرغداری‌ها. فروشگاه‌های دامی سرنگ اتوماتیک می‌فروشند، اما راهنمای خرید سرنگ یکبار مصرف عمده برای دامدار وجود ندارد. این بخش با انبارهای مشهد و بجنورد هم‌خوانی دارد.</li>
  </ol>
  <h3 class="sub">پیشنهاد اصلی</h3>
  <ul class="nice">
    <li>۲۵ مقاله در ۶ خوشه و ۲ مقاله در هفته، در مجموع ۱۳ هفته. شروع با مقاله‌ی ستون «انواع سرنگ» و برد‌های سریع.</li>
    <li>هر مقاله کلمه‌ی کلیدی «خودش» را دارد و دست‌کم به یک صفحه‌ی فرود تجاری لینک می‌دهد. هیچ مقاله‌ای کلمه‌ی کلیدی یک صفحه‌ی فرود را هدف نمی‌گیرد (بخش ۷).</li>
    <li>هر مقاله یک جدول HTML از داده‌ی واقعی کاتالوگ، یک جدول معکوس («اگر مصرف شما X است…») و یک بخش «چه وقت نخرید» دارد. این سه عنصر را رقبا ندارند.</li>
    <li>دارایی‌های لینک‌گیر: ماشین‌حساب قطرات سرم، جدول گیج سرسوزن، چک‌لیست‌های دانلودی کیفیت و ملزومات مطب.</li>
  </ul>
  <div class="warn">
    <b>پیش‌شرط فنی پیش از هر انتشار:</b> اگر حالت تعمیر (Maintenance) سایت هنوز روشن است، هیچ صفحه‌ای قابل ایندکس و رتبه‌گیری نیست. وضعیت <span dir="ltr">mtnc-options → status</span> را بررسی و خاموش کنید. همچنین صفحه‌ی قوانین (6200) با پیشنهاد ارسال صفحه‌ی 5963 تناقض دارد و یک جای خالی «[مهلت مرجوعی را تعیین کنید]» دارد؛ پیش از انتشار مقالات B2B اصلاح شود.
  </div>
</section>'''

def method():
    return f'''
<section class="flowsec" id="s2">
  <h2 class="sec">۲. روش تحقیق و محدودیت‌ها</h2>
  <table class="grid">
    <tr><th>بخش</th><th>روش</th><th>محدودیت و نحوه‌ی جبران</th></tr>
    <tr><td>تحلیل SERP</td><td>۳۰ جستجوی فارسی در ۴ آبان ۱۴۰۵ برای عبارت‌های تجاری، آموزشی و مقایسه‌ای حوزه‌ی سرنگ، ست سرم، سوند، ماسک، کد IRC و بازار دامپزشکی؛ ثبت دامنه‌ها و نوع صفحات رتبه‌دار.</td><td>نتایج از دید جستجوگری خارج از ایران گرفته شده و ممکن است با نتایج داخل ایران کمی فرق کند. پیش از نگارش هر مقاله، SERP کلمه‌ی اصلی و دو کلمه‌ی فرعی را از داخل ایران دوباره بررسی کنید.</td></tr>
    <tr><td>حجم و سختی کلمات</td><td>سطح‌بندی تخمینی (زیاد/متوسط/کم) بر پایه‌ی تعداد و کیفیت رقبای رتبه‌دار، وجود مقایسه‌گرهای قیمت و تنوع عبارت‌های پیشنهادی.</td><td>Ahrefs و بیشتر ابزارهای حجم جستجو پایگاه داده‌ی ایران را پشتیبانی نمی‌کنند (درخواست با کشور IR رد شد). به همین دلیل در این سند عدد حجم ساختگی نمی‌آید. پس از ۴ تا ۶ هفته با Google Search Console و Google Trends (منطقه‌ی ایران) کالیبره شود.</td></tr>
    <tr><td>محتوای رقبا</td><td>نوع صفحه، عنوان‌ها و زاویه‌ی محتوا از نتایج جستجو.</td><td>دریافت مستقیم صفحات رقبا و خود iransorang.com از محیط تحلیل ممکن نبود (خطای DNS/دسترسی شبکه برای دامنه‌های ایرانی). ساختار سایت از مستندات داخلی پروژه گرفته شده است: شناسه‌ی صفحات فرود، برندها، انبارها و پیش‌نویس مقاله‌ی ۶۲۵۸.</td></tr>
    <tr><td>داده‌ی محصول</td><td>تمام اعداد قیمت و تعداد در کارتن در مقالات باید از ووکامرس و به‌صورت توکن زنده (isbp) بیایند.</td><td>این سند عمداً هیچ قیمتی ذکر نمی‌کند. وزن و ابعاد کارتن در سایت ثبت نشده است؛ اگر مقاله‌ای به آن نیاز داشت از مدیر سایت پرسیده شود، تخمین زده نشود.</td></tr>
    <tr><td>محتوای پزشکی</td><td>مقالات مشخصات و منطق خرید را می‌گویند.</td><td>توصیه‌ی پزشکی نیستند. در موضوعات تزریق و دوز، جمله‌ی «دوز و روش تزریق فقط طبق دستور پزشک معالج» الزامی است. روش جایگذاری سوند یا تکنیک تزریق آموزش داده نمی‌شود.</td></tr>
  </table>
  <h3 class="sub">راهنمای خواندن سطح‌ها</h3>
  <p><b>تقاضا (تخمینی):</b> زیاد = عبارت پرتکرار با چند صفحه‌ی رقیب قوی؛ متوسط = عبارت تخصصی با تقاضای پایدار؛ کم = عبارت دنباله‌دار یا B2B با حجم کم ولی ارزش تبدیل بالا. <b>سختی (تخمینی):</b> کم = SERP فارسی خالی یا نامرتبط؛ متوسط = چند وبلاگ فروشگاهی با محتوای متوسط. <b>اولویت:</b> P1 = ماه اول؛ P2 = ماه دوم و سوم؛ P3 = تکمیل خوشه.</p>
</section>'''

def assets():
    rows = "".join(f'<tr><td class="c">{e(i)}</td><td>{e(t)}</td><td>{e(k)}</td></tr>' for i, t, k, _ in LANDINGS)
    return f'''
<section class="flowsec" id="s3">
  <h2 class="sec">۳. دارایی‌های فعلی سایت (مبنای لینک‌سازی داخلی)</h2>
  <p>ایران سرنگ یک فروشگاه ووکامرس عمده‌فروشی است با صفحات فرود تجاری برای هر گروه محصول، صفحات برند، انبار در تهران، اصفهان، مشهد و بجنورد، و یک دسته‌ی وبلاگ (شناسه‌ی ۴۵۵). این صفحات مقصد لینک‌های داخلی مقالات‌اند و کلمه‌ی کلیدی تجاری‌شان فقط متعلق به خودشان است.</p>
  <table class="grid">
    <tr><th>شناسه</th><th>صفحه‌ی فرود</th><th>کلمه‌ی کلیدی رزروشده برای صفحه‌ی فرود</th></tr>
    {rows}
    <tr><td class="c">6197</td><td>استعلام قیمت</td><td>مقصد CTA مقالات B2B</td></tr>
    <tr><td class="c">5598 / 5599</td><td>درباره‌ی ما / تماس با ما</td><td>سیگنال اعتماد (E-E-A-T)</td></tr>
    <tr><td class="c">6258</td><td>پیش‌نویس «تعداد سرنگ در کارتن»</td><td>از قبل نوشته شده؛ هیچ‌کدام از ۲۵ مقاله‌ی این پلن آن را هدف نمی‌گیرند. فقط به آن لینک می‌دهند.</td></tr>
  </table>
  <p class="muted">برندهای کاتالوگ: آوا پزشک (5076)، ورید (5077)، سها (5078)، مینا سرنگ (5079)، مارون (5080)، هما سرنگ (5081)، حلما طب (5082)، آیمد (5083)، تری مد (5084)، شفا سرنگ (5085)، ثمین طب مهر (5086) و BD (5089).</p>
</section>'''

def competitors():
    rows = "".join(f'<tr><td class="dom" dir="ltr">{e(d)}</td><td>{e(t)}</td><td>{e(k)}</td><td>{e(s)}</td><td>{e(o)}</td></tr>' for d, t, k, s, o in COMPETITORS)
    return f'''
<section class="flowsec" id="s4">
  <h2 class="sec">۴. نقشه‌ی رقبا</h2>
  <p>رقبا بر اساس نوع کسب‌وکار و کلماتی که در جستجوها برایشان دیده شد گروه‌بندی شده‌اند. ستون آخر می‌گوید ایران سرنگ از کجا می‌تواند جلو بزند.</p>
  <table class="grid small">
    <tr><th style="width:17%">دامنه‌ها</th><th style="width:13%">نوع</th><th style="width:22%">عبارت‌هایی که در SERP دیده شد</th><th style="width:16%">نقطه‌ی قوت</th><th>نقطه‌ی ضعف و فرصت ایران سرنگ</th></tr>
    {rows}
  </table>
  <h3 class="sub">الگوهای مشترک در صفحات رتبه‌دار</h3>
  <ul class="nice">
    <li><b>سال در عنوان صفحات تجاری</b> («قیمت عمده ۱۴۰۵») برای CTR. برای صفحات فرود ایران سرنگ هم توصیه می‌شود، برای مقالات آموزشی نه.</li>
    <li><b>عنوان‌های عددی</b> («۹ مدل»، «۱۲ مدل + جدول»). عنوان سئوی همه‌ی ۲۵ مقاله‌ی این پلن یک عدد لاتین دارد.</li>
    <li><b>نبود داده‌ی واقعی:</b> تقریباً هیچ رقیبی قیمت هر عدد، تعداد در کارتن یا کد IRC محصول را در محتوای آموزشی نمی‌آورد. این مزیت انحصاری ایران سرنگ است.</li>
    <li><b>جدول به‌صورت تصویر یا بدون جدول:</b> جدول‌های HTML واقعی شانس اسنیپت جدولی و استناد در پاسخ‌های هوش مصنوعی را بالا می‌برند.</li>
  </ul>
</section>'''

def gaps():
    rows = ""
    for q, top, qual, opp, n in GAPS:
        tgt = alink(n) if n else "صفحه‌ی فرود"
        rows += f'<tr><td>{e(q)}</td><td>{e(top)}</td><td>{e(qual)}</td><td>{e(opp)}</td><td class="c">{tgt}</td></tr>'
    return f'''
<section class="flowsec" id="s5">
  <h2 class="sec">۵. تحلیل شکاف SERP</h2>
  <p>هرچه کیفیت پاسخ فعلی ضعیف‌تر باشد، شانس رتبه‌ی یک با یک مقاله‌ی عمیق و داده‌محور بیشتر است. ردیف آخر یادآوری می‌کند که کلمات تراکنشی مال صفحات فرودند، نه وبلاگ.</p>
  <table class="grid">
    <tr><th style="width:24%">عبارت جستجو</th><th style="width:26%">آنچه در صدر دیده شد</th><th style="width:14%">کیفیت پاسخ فعلی</th><th style="width:16%">فرصت</th><th>مقاله</th></tr>
    {rows}
  </table>
</section>'''

def clusters():
    rows = ""
    for code, name, ns, land in CLUSTERS:
        arts = "، ".join(f'{alink(n)} {e(BY_N[n]["kw"])}' for n in ns)
        rows += f'<tr><td class="c"><b>{code}</b></td><td>{e(name)}</td><td>{arts}</td><td>{e(land)}</td></tr>'
    return f'''
<section class="flowsec" id="s6">
  <h2 class="sec">۶. معماری خوشه‌های موضوعی</h2>
  <p>هر خوشه یک مقاله‌ی هاب دارد که به همه‌ی مقالات خوشه لینک می‌دهد. هر مقاله به هاب، به ۲ تا ۳ مقاله‌ی هم‌خوشه و به صفحه‌ی فرود تجاری خوشه لینک می‌دهد. این ساختار اعتبار موضوعی (Topical Authority) را به صفحات فرود می‌رساند.</p>
  <div class="flow">
    <div class="node land">صفحات فرود تجاری<br><small>5963 · 5964–5978 · برندها</small></div>
    <div class="arrow">▲ لینک با انکر دقیق</div>
    <div class="row3">
      <div class="node hub">هاب‌ها: {alink(1)} انواع سرنگ · {alink(21)} لیست مصرفی مطب · {alink(23)} برندها</div>
    </div>
    <div class="arrow">▲ لینک دوطرفه</div>
    <div class="node leaf">۲۲ مقاله‌ی خوشه‌ای: پاسخ به یک پرسش مشخص + جدول داده + «چه وقت نخرید»</div>
  </div>
  <table class="grid">
    <tr><th>کد</th><th>خوشه</th><th>مقالات (شماره و کلمه‌ی کلیدی)</th><th>صفحه‌ی فرود مقصد</th></tr>
    {rows}
  </table>
</section>'''

def cannibal():
    rows = ""
    for i, t, k, ns in LANDINGS:
        arts = "، ".join(f'{alink(n)} «{e(BY_N[n]["kw"])}»' for n in ns)
        rows += f'<tr><td class="c">{e(i)}</td><td>{e(t)}</td><td>{e(k)}</td><td>{arts}</td></tr>'
    return f'''
<section class="flowsec" id="s7">
  <h2 class="sec">۷. نقشه‌ی جلوگیری از هم‌نوع‌خواری (Anti-Cannibalisation)</h2>
  <p>قاعده: کلمه‌ی کلیدی تجاری هر صفحه‌ی فرود فقط در عنوان، H1 و URL همان صفحه می‌آید. مقالات پشتیبان آن را فقط به‌عنوان <b>انکر لینک</b> به صفحه‌ی فرود به کار می‌برند و کلمه‌ی کلیدی خودشان پرسشی، مقایسه‌ای یا راهنمایی است.</p>
  <table class="grid small">
    <tr><th style="width:10%">شناسه</th><th style="width:14%">صفحه‌ی فرود</th><th style="width:20%">کلمه‌ی رزرو</th><th>مقالات پشتیبان و کلمه‌ی کلیدی متمایز آن‌ها</th></tr>
    {rows}
  </table>
  <h3 class="sub">دروازه‌ی کنترل پیش از انتشار (طبق مهارت blog سایت)</h3>
  <ul class="nice">
    <li>هم‌پوشانی متن مقاله با هر صفحه‌ی هم‌موضوع (شینگل ۵ کلمه‌ای) کمتر از <b>۲۵٪</b> و تیترهای H2 یکسان کمتر از <b>۴۰٪</b>. بیشترین عدد و جفت صفحه را گزارش کنید.</li>
    <li>کلمه‌ی کلیدی هر مقاله با کلمه‌ی هیچ صفحه‌ی فرود و هیچ مقاله‌ی دیگری یکسان نیست. مقاله‌ی ۱ («انواع سرنگ») وارد جزئیات انسولین نمی‌شود و برای آن به مقاله‌ی ۱۰ لینک می‌دهد.</li>
    <li>اگر Search Console نشان داد مقاله‌ای برای کلمه‌ی یک صفحه‌ی فرود بالاتر از خود آن صفحه آمده، H2 مربوط را از کلمه پاک کنید و یک لینک متنی با انکر دقیق به صفحه‌ی فرود اضافه کنید.</li>
  </ul>
</section>'''

def priority():
    grid = [[[] for _ in range(3)] for _ in range(3)]
    for a in ARTICLES:
        grid[tier_d(a["demand"])][tier_k(a["kd"])].append(a["n"])
    rlab = ["تقاضای زیاد", "تقاضای متوسط", "تقاضای کم / B2B"]
    clab = ["سختی کم", "سختی کم تا متوسط", "سختی متوسط"]
    body = ""
    for r in range(3):
        cells = ""
        for c in range(3):
            ns = grid[r][c]
            hot = " hot" if (r <= 1 and c == 0) else ""
            cells += f'<td class="pm{hot}">' + " ".join(f'<span class="pill">{alink(n)} {e(BY_N[n]["kw"])}</span>' for n in ns) + '</td>'
        body += f'<tr><th>{rlab[r]}</th>{cells}</tr>'
    return f'''
<section class="flowsec" id="s8">
  <h2 class="sec">۸. ماتریس اولویت (تقاضا × سختی، هر دو تخمینی)</h2>
  <p>خانه‌های رنگی بهترین نسبت شانس به تلاش را دارند. مقالات تقاضای زیاد با سختی متوسط («انواع سرنگ» و «هر واحد سرنگ انسولین») زودتر منتشر می‌شوند، چون رسیدن به رتبه‌ی یک در آن‌ها زمان و لینک بیشتری می‌خواهد.</p>
  <table class="grid pmx">
    <tr><th></th>{"".join(f"<th>{c}</th>" for c in clab)}</tr>
    {body}
  </table>
</section>'''

def calendar():
    rows = ""
    for w, ns, note in CALENDAR:
        arts = "<br>".join(f'{alink(n)} {e(BY_N[n]["h1"])}' for n in ns)
        rows += f'<tr><td class="c">{fa(w)}</td><td>{arts}</td><td>{e(note)}</td></tr>'
    return f'''
<section class="flowsec" id="s9">
  <h2 class="sec">۹. تقویم انتشار ۱۳ هفته‌ای (۲ مقاله در هفته)</h2>
  <p class="muted">هر مقاله ابتدا به‌صورت پیش‌نویس ساخته می‌شود و پس از تأیید منتشر می‌شود. پس از هر ۴ هفته، دو مقاله‌ی قبلی بر اساس داده‌ی Search Console بازبینی می‌شوند: کلمات فرعی جدید، پرسش‌های تازه و رفع افت جایگاه.</p>
  <table class="grid">
    <tr><th style="width:8%">هفته</th><th>مقالات</th><th style="width:30%">منطق</th></tr>
    {rows}
  </table>
</section>'''

def kwtable():
    rows = ""
    for a in ARTICLES:
        rows += (f'<tr><td class="c">{alink(a["n"])}</td><td><b>{e(a["kw"])}</b><div class="tiny">{e("، ".join(a["kw2"][:3]))}</div></td>'
                 f'<td class="url" dir="ltr">{e(url_of(a))}</td><td>{e(a["intent"])}</td><td>{e(a["demand"])}</td><td>{e(a["kd"])}</td><td class="c">{e(a["prio"].split()[0])}</td></tr>')
    return f'''
<section class="flowsec" id="s10">
  <h2 class="sec">۱۰. جدول کلمات کلیدی و URLهای پیشنهادی</h2>
  <p>اسلاگ‌ها فارسی و شامل کلمه‌ی کلیدی‌اند (ساختار پیوند یکتای سایت <span dir="ltr">/%postname%/</span> است). اسلاگ فارسی تنها راه پاس‌شدن آزمون «کلمه‌ی کلیدی در URL» در Rank Math است و در وردپرس به‌صورت درصدی ذخیره و درست نمایش داده می‌شود. نام فایل تصاویر لاتین است.</p>
  <table class="grid small">
    <tr><th>#</th><th style="width:22%">کلمه‌ی کلیدی اصلی و فرعی‌ها</th><th>URL پیشنهادی</th><th>نیت</th><th>تقاضا</th><th>سختی</th><th>اولویت</th></tr>
    {rows}
  </table>
</section>'''

def standards():
    return f'''
<section class="flowsec" id="s11">
  <h2 class="sec">۱۱. استاندارد نگارش و سئوی داخلی (برای همه‌ی ۲۵ مقاله)</h2>
  <table class="grid">
    <tr><th style="width:26%">مورد</th><th>هدف</th></tr>
    <tr><td>طول</td><td>۱٬۴۰۰ تا ۳٬۲۰۰ کلمه بسته به مقاله (در هر بریف آمده). عدد را اندازه بگیرید، تخمین نزنید.</td></tr>
    <tr><td>چگالی کلمه‌ی کلیدی</td><td>۱ تا ۲.۵ درصد. جای طبیعی کلمه: یک H2، دو پرسش FAQ (H3)، همه‌ی کپشن‌ها، پاراگراف «خلاصه‌ی جواب» و جمع‌بندی. اگر سقف طبیعی کمتر از ۱٪ بود، عدد واقعی را گزارش کنید و متن را با کلمه پر نکنید.</td></tr>
    <tr><td>عنوان سئو</td><td>۱۵ تا ۷۰ نویسه، کلمه‌ی کلیدی در ابتدای عنوان، یک عدد لاتین (آزمون عدد Rank Math فقط رقم ASCII را می‌شناسد).</td></tr>
    <tr><td>توضیحات متا</td><td>۱۱۰ تا ۱۶۵ نویسه، شامل کلمه‌ی کلیدی. همه‌ی ۲۵ متای این سند این شرط را دارند.</td></tr>
    <tr><td>تیترها</td><td>۱۰ تا ۱۵ تیتر H2 و ۵ تا ۷ تیتر H3. کلمه‌ی کلیدی در دست‌کم یک H2 و یک H3.</td></tr>
    <tr><td>لینک‌ها</td><td>دست‌کم ۵ لینک داخلی (ترجیحاً به صفحات فرود) و دست‌کم ۱ لینک خارجی معتبر (<span dir="ltr">imed.ir</span> یا استاندارد ISO).</td></tr>
    <tr><td>جدول</td><td>دست‌کم یک جدول HTML واقعی، هرگز تصویر جدول.</td></tr>
    <tr><td>اسکیما</td><td>BlogPosting از طریق Rank Math با مقادیر متنی واقعی، بدون متغیرهای %…%. FAQPage دستی اضافه نشود؛ FAQ به‌صورت H3 در متن بیاید.</td></tr>
    <tr><td>ZWNJ (نیم‌فاصله)</td><td>کلمه‌ی کلیدی باید با فاصله‌ی معمولی و دقیقاً یکسان نوشته شود؛ «۵ سی سی» نه «۵ سی‌سی».</td></tr>
    <tr><td>اعداد قیمت و کارتن</td><td>همیشه توکن زنده (<span dir="ltr">&lt;span class="isbp" data-isbp="…"&gt;</span>) یا نام برند، سایز و ساختار کنار عدد تا افزونه‌ی autolive آن را زنده کند.</td></tr>
  </table>
  <h3 class="sub">قالب محتوا که از رقبا متمایزتان می‌کند</h3>
  <ol class="nice">
    <li><b>شروع با یک ناهنجاری عددی از داده‌ی واقعی</b>، نه تعریف. مثال: «چرا کارتن سرنگ ۳ سی سی یک برند از کارتن ۵ سی سی همان برند گران‌تر است؟».</li>
    <li><b>«خلاصه‌ی جواب»</b> بلافاصله پس از مقدمه: سه خط پاسخ مستقیم. این بخش نامزد اسنیپت ویژه و پاسخ‌های هوش مصنوعی است.</li>
    <li><b>جدول داده‌ی کاتالوگ + جدول معکوس</b> («اگر مصرف ماهانه‌ی شما X است…»).</li>
    <li><b>یک بخش که می‌تواند فروش را از دست بدهد</b> («چه وقت نخرید») با محاسبه. برای هر مقاله متفاوت است و در بریف آمده. قوی‌ترین سیگنال تجربه و اعتماد (E-E-A-T).</li>
    <li><b>۵ تا ۷ پرسش FAQ</b> با همان لحنی که کاربر تایپ می‌کند.</li>
    <li><b>جمع‌بندی با سه اقدام بعدی مشخص</b>، نه تکرار متن.</li>
  </ol>
  <p class="muted">از این عبارت‌ها پرهیز شود: «در نهایت»، «به طور کلی»، «لازم به ذکر است»، «در دنیای امروز». خواننده را «شما» خطاب کنید و هر جا ممکن است به جای صفت، عدد اندازه‌گیری‌شده بیاورید.</p>
  <div class="note"><b>محدودیت‌های شناخته‌شده‌ی Rank Math در فارسی:</b> آزمون‌های Power Word و Title Sentiment با دیکشنری انگلیسی کار می‌کنند و در فارسی پاس نمی‌شوند. امتیاز ۱۰۰ دست‌یافتنی نیست و ۹۰ به بالا هدف واقع‌بینانه است. امتیاز در مرورگر محاسبه می‌شود؛ پس از ذخیره، نوشته را باز کنید و «به‌روزرسانی» بزنید.</div>
</section>'''

def imgguide():
    return f'''
<section class="flowsec" id="s12">
  <h2 class="sec">۱۲. راهنمای تولید تصویر (۷۵ تصویر)</h2>
  <table class="grid">
    <tr><th style="width:24%">مورد</th><th>استاندارد</th></tr>
    <tr><td>ابزار</td><td>Nano Banana Pro (Gemini) از طریق مهارت <span dir="ltr">ax</span>. پرامپت‌ها انگلیسی‌اند چون دقت مدل‌های تصویر با انگلیسی بیشتر است. متن جایگزین (alt) و کپشن فارسی‌اند.</td></tr>
    <tr><td>زبان بصری ثابت</td><td>نور نرم و پخش از بالا-چپ؛ سفید، پلاستیک شفاف پزشکی، فولاد جراحی و فقط یک رنگ تأکیدی فیروزه‌ای ملایم (<span dir="ltr">#3E8E87</span>)؛ بالینی و خلوت. این بخش در انتهای همه‌ی پرامپت‌ها آمده است.</td></tr>
    <tr><td>ممنوعیت‌ها</td><td>هیچ متن، حرف، عدد، لوگو یا بسته‌بندی واقعی یک برند. درجه‌بندی سرنگ فقط خط بدون عدد. هیچ سوزنی در تماس با پوست، بدون خون و بدون چهره‌ی انسان (برای نمایش روی صورت از مانکن استفاده شده).</td></tr>
    <tr><td>اندازه و فرمت</td><td>تصویر شاخص ۱۲۰۰×۶۷۵ (۱۶:۹)؛ تصاویر داخل متن ۸۰۰×۶۰۰ (۴:۳)؛ خروجی WebP.</td></tr>
    <tr><td>نام فایل</td><td>لاتین و خط‌تیره، مثل <span dir="ltr">syringe-types-hero.webp</span> (برای هر تصویر در بریف آمده). در پوشه‌ی کاری: <span dir="ltr">hero.png · inline1.png · inline2.png</span>.</td></tr>
    <tr><td>متن جایگزین (alt)</td><td>alt تصویر شاخص شامل کلمه‌ی کلیدی اصلی است. alt تصاویر داخل متن کلمات فرعی را دارد.</td></tr>
    <tr><td>کپشن</td><td>هر تصویر داخل متن یک <span dir="ltr">&lt;figcaption&gt;</span> متفاوت از alt دارد که شامل کلمه‌ی کلیدی است. تصویر شاخص داخل متن تکرار نمی‌شود.</td></tr>
    <tr><td>پس‌پردازش</td><td>هر سه تصویر پیش از آپلود با مهارت <span dir="ltr">watermark</span> واترمارک می‌شوند؛ درج با <span dir="ltr">wp_get_attachment_image</span> و <span dir="ltr">loading="lazy"</span> تا srcset ساخته شود.</td></tr>
    <tr><td>اسکرین‌شات‌ها</td><td>در مقاله‌ی ۲۲ (استعلام IRC)، تصاویر مراحل سامانه باید اسکرین‌شات واقعی باشند، نه تصویر ساختگی.</td></tr>
  </table>
  <h3 class="sub">پرامپت منفی سراسری (برای ابزارهایی که فیلد Negative دارند)</h3>
  <div class="prompt" dir="ltr">{e(NEGATIVE)}</div>
  <p class="muted">Nano Banana Pro فیلد منفی جداگانه ندارد؛ ممنوعیت‌ها داخل متن هر پرامپت آمده‌اند. در Midjourney همین فهرست را بعد از <span dir="ltr">--no</span> بگذارید و در Stable Diffusion در فیلد Negative.</p>
</section>'''

def brief(a):
    kv = [
        ("عنوان سئو (Title tag)", f'<b>{e(a["title"])}</b> <span class="tiny">({fa(len(a["title"]))} نویسه)</span>'),
        ("توضیحات متا", f'{e(a["meta"])} <span class="tiny">({fa(len(a["meta"]))} نویسه)</span>'),
        ("کلمه‌ی کلیدی اصلی", f'<span class="kw">{e(a["kw"])}</span>'),
        ("کلمات کلیدی فرعی", e("، ".join(a["kw2"]))),
        ("کلمات مرتبط معنایی (LSI)", e("، ".join(a["lsi"]))),
        ("URL پیشنهادی", f'<span class="url" dir="ltr">{e(url_of(a))}</span>'),
        ("نیت جستجو / قیف", f'{e(a["intent"])} · {e(a["funnel"])}'),
        ("تقاضا / سختی (تخمینی) / اولویت", f'{e(a["demand"])} · {e(a["kd"])} · <b>{e(a["prio"])}</b>'),
        ("طول هدف", e(a["words"])),
        ("هدف اسنیپت / پاسخ AI", e(a["snippet"])),
    ]
    kvh = "".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in kv)
    outline = "".join(f"<li>{e(h)}</li>" for h in a["outline"])
    faq = "".join(f"<li>{e(q)}</li>" for q in a["faq"])
    imgs = ""
    for img in a["images"]:
        imgs += f'''
    <div class="imgcard">
      <div class="imghead"><span class="role">{ROLE_FA[img["role"]]}</span><span>{e(img["place"])}</span><span class="dim">{img_size(img)}</span></div>
      <table class="kv2">
        <tr><th>نام فایل</th><td dir="ltr" class="fn">{e(file_name(a, img))}</td></tr>
        <tr><th>متن جایگزین (alt)</th><td>{e(img["alt"])}</td></tr>
        <tr><th>کپشن (figcaption)</th><td>{e(img["cap"])}</td></tr>
      </table>
      <div class="plabel">Prompt — Nano Banana Pro</div>
      <div class="prompt" dir="ltr">{e(full_prompt(img))}</div>
    </div>'''
    return f'''
<section class="article" id="a{a["n"]}">
  <div class="ahead">
    <span class="anum">مقاله {fa(a["n"])} از ۲۵</span>
    <span class="acl">{e(a["cluster"])}</span>
  </div>
  <h2 class="atitle">{e(a["h1"])}</h2>
  <table class="kv">{kvh}</table>
  <div class="two">
    <div class="box"><h4>وضعیت SERP و رقبای فعلی</h4><p>{e(a["serp"])}</p></div>
    <div class="box accent"><h4>زاویه‌ی برتری (افزوده‌ی اطلاعاتی)</h4><p>{e(a["angle"])}</p></div>
  </div>
  <div class="two">
    <div class="box"><h4>داده‌ی اختصاصی لازم از سایت</h4><p>{e(a["data"])}</p></div>
    <div class="box warnbox"><h4>بخش الزامی «چه وقت نخرید»</h4><p>{e(a["lose"])}</p></div>
  </div>
  <div class="two">
    <div class="box"><h4>ساختار تیترها (H2)</h4><ol class="ol">{outline}</ol></div>
    <div class="box"><h4>پرسش‌های FAQ (H3)</h4><ol class="ol">{faq}</ol></div>
  </div>
  <div class="linksrow">
    <div class="box"><h4>لینک‌ها، تبدیل و انتشار</h4>
      <p><b>داخلی:</b> {e(a["links_in"])}</p>
      <p><b>خارجی:</b> {ltr_urls(a["links_out"])}</p>
      <p><b>CTA:</b> {e(a["cta"])}</p>
      <p><b>اسکیما و انتشار:</b> BlogPosting (Rank Math)، دسته‌ی وبلاگ (۴۵۵)، وضعیت پیش‌نویس، robots: index, follow.</p>
    </div>
  </div>
  <h3 class="imgsec">سه تصویر مقاله</h3>
  {imgs}
</section>'''

def extras():
    return f'''
<section class="page" id="s14">
  <h2 class="sec">۱۴. اقدامات تکمیلی برای رتبه‌ی یک (فراتر از محتوا)</h2>
  <table class="grid">
    <tr><th style="width:22%">محور</th><th>اقدام</th></tr>
    <tr><td>کلمات تراکنشی</td><td>محصولات را در ترب و ایمالز ثبت کنید. SERP «قیمت سرنگ…» را این پلتفرم‌ها گرفته‌اند و حضور در آن‌ها سریع‌تر از رقابت مستقیم است. عنوان صفحات فرود را با سال (۱۴۰۵) و قیمت زنده به‌روز نگه دارید.</td></tr>
    <tr><td>بک‌لینک مرتبط</td><td>(۱) صفحه‌ی «نمایندگان/پخش‌کنندگان» در سایت برندهای تأمین‌کننده؛ (۲) معرفی ماشین‌حساب قطرات سرم و جدول گیج سرسوزن به کانال‌ها و انجمن‌های دانشجویان پرستاری؛ (۳) چک‌لیست‌های دانلودی کیفیت و ملزومات مطب برای دایرکتوری‌های تجهیزات پزشکی؛ (۴) رپورتاژ داده‌محور (مثلاً «قیمت هر عدد سرنگ در ۱۲ برند») در رسانه‌های اقتصادی حوزه‌ی سلامت.</td></tr>
    <tr><td>سئوی محلی</td><td>ثبت چهار انبار تهران، اصفهان، مشهد و بجنورد در نقشه‌های نشان و بلد (و Google Maps در صورت امکان) با نام و شماره‌ی یکسان. برای عبارت‌هایی مثل «پخش سرنگ مشهد»، یک بخش کوتاه شهرمحور در صفحه‌ی 5963 کافی است. صفحه‌ی جدا برای هر شهر فقط وقتی ساخته شود که محتوای واقعاً متفاوتی دارد.</td></tr>
    <tr><td>اعتماد (E-E-A-T)</td><td>یک بازبین متخصص (داروساز یا کارشناس تجهیزات پزشکی) با نام و سمت در انتهای مقالات؛ مجوزها و گواهی‌ها در «درباره‌ی ما» (5598)؛ تاریخ به‌روزرسانی قابل مشاهده؛ منبع‌دهی به ISO، <span dir="ltr">imed.ir</span> و <span dir="ltr">ttac.ir</span>.</td></tr>
    <tr><td>لینک داخلی برگشتی</td><td>هر صفحه‌ی فرود در پایین صفحه بخش «راهنمای انتخاب» داشته باشد و به ۱ تا ۲ مقاله‌ی مرتبط لینک دهد (مثلاً 5974 به مقاله‌ی ۱۹ و 5970 به مقاله‌های ۹ و ۱۰).</td></tr>
    <tr><td>دیده‌شدن در هوش مصنوعی (GEO)</td><td>بلوک «خلاصه‌ی جواب»، تعریف‌های ۴۰ کلمه‌ای، جدول‌های HTML و FAQ احتمال استناد در AI Overviews گوگل و پاسخ‌های ChatGPT/Gemini را بالا می‌برند. نام برند «ایران سرنگ» در جمله‌های تعریفی بیاید.</td></tr>
    <tr><td>فنی</td><td>خاموش‌بودن حالت تعمیر؛ ارسال نقشه‌ی سایت و IndexNow پس از هر انتشار؛ تصاویر WebP با lazy-load؛ بررسی Core Web Vitals موبایل؛ اصلاح تناقض‌های صفحه‌ی قوانین (6200).</td></tr>
    <tr><td>تازگی</td><td>جدول‌های قیمت با توکن زنده خودکار به‌روز می‌شوند. هر ۳ ماه، SERP پنج مقاله‌ی پربازدید را دوباره بررسی کنید و پرسش‌های تازه را به FAQ اضافه کنید.</td></tr>
  </table>
</section>'''

def kpis():
    return f'''
<section class="flowsec" id="s15">
  <h2 class="sec">۱۵. شاخص‌های پایش (Google Search Console و GA4)</h2>
  <table class="grid">
    <tr><th style="width:16%">زمان</th><th>چه چیزی را بسنجیم</th><th style="width:34%">اقدام اگر عقب بود</th></tr>
    <tr><td>هفته‌ی ۲ پس از انتشار هر مقاله</td><td>ایندکس‌شدن (URL Inspection)، نخستین ایمپرشن‌ها</td><td>درخواست ایندکس، لینک داخلی از هاب و صفحه‌ی فرود</td></tr>
    <tr><td>روز ۳۰</td><td>میانگین جایگاه کلمه‌ی اصلی و فرعی‌ها؛ CTR؛ پرسش‌های جدید در گزارش Queries</td><td>اگر جایگاه ۸ تا ۲۰ بود: افزودن پرسش‌های جدید به FAQ و تقویت جدول. اگر CTR زیر میانگین بود: بازنویسی عنوان و متا.</td></tr>
    <tr><td>روز ۶۰</td><td>کلیک از مقاله به صفحات فرود (رویداد GA4)، فرم‌های استعلام قیمت (6197)</td><td>جابه‌جایی CTA به بالای جدول اصلی، افزودن لینک متنی در «خلاصه‌ی جواب»</td></tr>
    <tr><td>روز ۹۰</td><td>سهم مقالات در جایگاه ۱ تا ۳، تعداد دامنه‌های ارجاع‌دهنده به دارایی‌های لینک‌گیر</td><td>به‌روزرسانی عمیق مقالات زیر جایگاه ۱۰ و برنامه‌ی لینک‌سازی برای مقالات ستون</td></tr>
  </table>
  <p class="muted">رتبه‌ی یک گوگل قابل تضمین نیست. شانس آن برای عبارت‌هایی که SERP فارسی خالی یا ضعیفی دارند (بخش ۵) بیشتر است. عبارت‌های رقابتی مثل «انواع سرنگ» و «هر واحد سرنگ انسولین» به لینک‌سازی و به‌روزرسانی مستمر نیاز دارند.</p>
</section>'''

def sources():
    lis = "".join(f'<li dir="ltr">{e(s)}</li>' for s in SOURCES)
    return f'''
<section class="flowsec" id="s16">
  <h2 class="sec">۱۶. منابع و صفحات بررسی‌شده در SERP</h2>
  <p>نشانی‌هایی که در جستجوهای ۴ آبان ۱۴۰۵ در نتایج دیده شدند یا در بریف‌ها به‌عنوان منبع خارجی پیشنهاد شده‌اند.</p>
  <ol class="src">{lis}</ol>
</section>'''

CSS = f'''
@font-face {{ font-family: Vazirmatn; src: url("file://{FONT}/Vazirmatn-Regular.ttf"); font-weight: 400; }}
@font-face {{ font-family: Vazirmatn; src: url("file://{FONT}/Vazirmatn-Medium.ttf"); font-weight: 500; }}
@font-face {{ font-family: Vazirmatn; src: url("file://{FONT}/Vazirmatn-Bold.ttf"); font-weight: 700; }}
@font-face {{ font-family: Vazirmatn; src: url("file://{FONT}/Vazirmatn-ExtraBold.ttf"); font-weight: 800; }}
:root {{ --teal:#2E7D76; --teal-d:#1E5B56; --teal-l:#E7F2F1; --ink:#1C2B33; --muted:#5B6B73; --line:#D3E1DF; --warn:#B4532A; --warn-l:#FBEFE8; --bg:#FFFFFF; }}
@page {{ size: A4; margin: 15mm 13mm 17mm 13mm; }}
* {{ box-sizing: border-box; }}
html, body {{ background: var(--bg); color: var(--ink); }}
body {{ font-family: Vazirmatn, sans-serif; font-size: 9.6pt; line-height: 1.75; direction: rtl; margin: 0; }}
a {{ color: var(--teal-d); text-decoration: none; }}
b {{ font-weight: 700; }}
p {{ margin: 4px 0 8px; }}
.page, .article {{ break-before: page; }}
.cover {{ height: 262mm; display: flex; flex-direction: column; justify-content: space-between; padding: 18mm 8mm 6mm; background: linear-gradient(160deg, #F2F8F7 0%, #FFFFFF 55%); border-right: 6px solid var(--teal); }}
.brandline {{ font-family: Vazirmatn; direction: ltr; text-align: right; color: var(--teal); font-weight: 700; letter-spacing: .5px; font-size: 12pt; }}
.cover h1 {{ font-size: 25pt; line-height: 1.5; font-weight: 800; margin: 14mm 0 6mm; color: var(--ink); }}
.cover .lead {{ font-size: 12pt; color: var(--muted); max-width: 150mm; }}
.stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm; }}
.stat {{ background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 5mm; }}
.stat b {{ display: block; font-size: 22pt; color: var(--teal); font-weight: 800; line-height: 1.2; }}
.stat span {{ color: var(--muted); font-size: 10pt; }}
.cover-foot {{ color: var(--muted); font-size: 9.5pt; border-top: 1px solid var(--line); padding-top: 4mm; }}
h2.sec {{ font-size: 16pt; font-weight: 800; color: var(--teal-d); margin: 0 0 6px; padding-bottom: 4px; border-bottom: 2px solid var(--teal); }}
h2, h3, h4 {{ break-after: avoid; }}
ol {{ list-style-type: persian; }}
ol.src {{ list-style-type: decimal; }}
.ol.cols {{ columns: 2; column-gap: 18px; }}
.flowsec {{ margin-top: 16px; }}
.linksrow {{ margin-top: 8px; }}
.article {{ font-size: 8.8pt; line-height: 1.6; }}
h3.imgsec {{ break-before: page; }}
h3.sub {{ font-size: 11.5pt; font-weight: 700; color: var(--ink); margin: 12px 0 4px; }}
.toc, .toc-arts {{ margin: 0; padding: 0; list-style: none; }}
.toc li {{ margin: 0; font-size: 9.8pt; line-height: 1.6; }}
.toc-arts {{ list-style: none; padding: 0; columns: 1; }}
.toc-arts li {{ padding: 1px 0; border-bottom: 1px dashed var(--line); font-size: 8.6pt; line-height: 1.55; }}
.num {{ display: inline-block; min-width: 22px; color: var(--teal); font-weight: 700; }}
.callout {{ background: var(--teal-l); border-right: 4px solid var(--teal); padding: 8px 12px; border-radius: 6px; margin: 6px 0 10px; }}
.warn {{ background: var(--warn-l); border-right: 4px solid var(--warn); padding: 8px 12px; border-radius: 6px; margin-top: 10px; }}
.note {{ background: #F6F8F9; border: 1px solid var(--line); padding: 8px 12px; border-radius: 6px; margin-top: 8px; }}
.muted {{ color: var(--muted); font-size: 9pt; }}
.tiny {{ color: var(--muted); font-size: 8pt; }}
ol.nice, ul.nice {{ padding-right: 18px; margin: 4px 0; }}
ol.nice li, ul.nice li {{ margin: 3px 0; }}
table {{ border-collapse: collapse; width: 100%; }}
table.grid {{ margin: 6px 0 10px; }}
table.grid th, table.grid td {{ border: 1px solid var(--line); padding: 5px 7px; vertical-align: top; text-align: right; }}
table.grid th {{ background: var(--teal-l); color: var(--teal-d); font-weight: 700; }}
table.grid tr {{ break-inside: avoid; }}
table.small td, table.small th {{ font-size: 8.4pt; line-height: 1.6; }}
td.c {{ text-align: center !important; white-space: nowrap; }}
td.dom {{ text-align: left !important; font-size: 8pt; color: var(--teal-d); word-break: break-word; }}
.url {{ font-size: 8.2pt; color: var(--teal-d); word-break: break-all; }}
td.url {{ text-align: left !important; }}
.flow {{ display: flex; flex-direction: column; align-items: center; gap: 4px; margin: 8px 0 12px; }}
.node {{ border-radius: 8px; padding: 7px 14px; text-align: center; width: 78%; }}
.node.land {{ background: var(--teal); color: #fff; font-weight: 700; }}
.node.land small {{ color: #DDEFEC; font-weight: 400; }}
.node.hub {{ background: var(--teal-l); border: 1px solid var(--teal); }}
.node.leaf {{ background: #fff; border: 1px dashed var(--teal); }}
.row3 {{ width: 100%; display: flex; justify-content: center; }}
.arrow {{ color: var(--teal); font-size: 8.5pt; }}
table.pmx td.pm {{ width: 30%; height: 38mm; }}
table.pmx td.hot {{ background: #F0F8F6; }}
table.pmx th {{ text-align: center; }}
.pill {{ display: inline-block; background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: 1px 8px; margin: 2px; font-size: 8.3pt; }}
.ahead {{ display: flex; justify-content: space-between; align-items: center; background: var(--teal); color: #fff; padding: 5px 10px; border-radius: 6px 6px 0 0; }}
.anum {{ font-weight: 800; }}
.acl {{ font-size: 8.6pt; color: #E3F1EF; }}
h2.atitle {{ font-size: 12.6pt; font-weight: 800; color: var(--ink); margin: 6px 0 6px; line-height: 1.55; }}
table.kv th, table.kv td {{ border-bottom: 1px solid var(--line); padding: 2px 6px; text-align: right; vertical-align: top; }}
table.kv th {{ width: 27%; color: var(--teal-d); font-weight: 700; background: #F7FBFA; }}
.kw {{ background: var(--teal); color: #fff; padding: 1px 8px; border-radius: 10px; font-weight: 700; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7px; margin-top: 7px; }}
.box {{ border: 1px solid var(--line); border-radius: 6px; padding: 6px 10px; break-inside: avoid; }}
.box h4 {{ margin: 0 0 3px; font-size: 9.8pt; color: var(--teal-d); }}
.box p {{ margin: 1px 0; font-size: 8.5pt; line-height: 1.6; }}
.box.accent {{ background: var(--teal-l); border-color: #BFD9D5; }}
.box.warnbox {{ background: var(--warn-l); border-color: #EBC9B8; }}
.box.warnbox h4 {{ color: var(--warn); }}
ol.ol {{ margin: 0; padding-right: 18px; font-size: 8.4pt; line-height: 1.55; }}
h3.imgsec {{ font-size: 11pt; color: var(--teal-d); margin: 10px 0 4px; border-bottom: 1px solid var(--line); padding-bottom: 2px; }}
.imgcard {{ border: 1px solid var(--line); border-radius: 6px; padding: 5px 9px; margin: 5px 0; break-inside: avoid; }}
.imghead {{ display: flex; gap: 10px; align-items: center; font-size: 8.8pt; color: var(--muted); margin-bottom: 3px; }}
.imghead .role {{ background: var(--teal-l); color: var(--teal-d); font-weight: 700; padding: 0 8px; border-radius: 10px; }}
.imghead .dim {{ margin-right: auto; direction: ltr; }}
table.kv2 th, table.kv2 td {{ padding: 2px 5px; font-size: 8.8pt; text-align: right; vertical-align: top; }}
table.kv2 th {{ width: 22%; color: var(--teal-d); font-weight: 500; }}
td.fn {{ text-align: left !important; color: var(--teal-d); }}
.plabel {{ direction: ltr; text-align: left; font-size: 7.6pt; color: var(--muted); margin-top: 3px; letter-spacing: .3px; }}
.prompt {{ direction: ltr; text-align: left; font-family: Vazirmatn, sans-serif; font-size: 7.7pt; line-height: 1.5; background: #F6F9F9; border: 1px solid var(--line); border-left: 3px solid var(--teal); border-radius: 4px; padding: 5px 8px; color: #23343B; }}
ol.src {{ font-size: 8pt; line-height: 1.6; padding-left: 22px; padding-right: 0; text-align: left; columns: 2; column-gap: 20px; direction: ltr; }}
'''

def build_html():
    parts = [cover(), toc(), summary(), method(), assets(), competitors(), gaps(), clusters(), cannibal(), priority(),
             calendar(), kwtable(), standards(), imgguide(),
             '<section class="page" id="s13"><h2 class="sec">۱۳. بریف ۲۵ مقاله</h2><p>هر بریف شامل عنوان و متای آماده‌ی Rank Math، کلمات کلیدی، URL، تحلیل SERP، زاویه‌ی برتری، داده‌ی لازم از سایت، بخش الزامی «چه وقت نخرید»، ساختار تیترها، FAQ، لینک‌ها و سه تصویر با نام فایل، alt، کپشن و پرامپت کامل است. ترتیب بریف‌ها بر اساس خوشه است؛ ترتیب انتشار در بخش ۹ آمده است.</p>'
             + "".join(f'<div class="mini"><b>{fa(a["n"])}.</b> {e(a["kw"])} — <span class="tiny">{e(a["cluster"])}</span></div>' for a in ARTICLES) + '</section>']
    parts += [brief(a) for a in ARTICLES]
    parts += [extras(), kpis(), sources()]
    return f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<title>تحقیق سئو و پلن ۲۵ مقاله‌ای ایران سرنگ</title><style>{CSS} .mini{{font-size:9pt;border-bottom:1px dashed var(--line);padding:2px 0}}</style></head>
<body>{"".join(parts)}</body></html>'''

def build_prompts_txt():
    L = []
    L.append("IRAN SORANG — 75 IMAGE PROMPTS FOR 25 BLOG ARTICLES (Nano Banana Pro)")
    L.append("=" * 78)
    L.append("Global negative prompt (for tools with a negative field):")
    L.append(NEGATIVE)
    L.append("")
    for a in ARTICLES:
        L.append("=" * 78)
        L.append(f'ARTICLE {a["n"]:02d} | {a["h1"]}')
        L.append(f'Focus keyword: {a["kw"]}')
        L.append(f'URL: {url_of(a)}')
        for img in a["images"]:
            L.append("-" * 78)
            L.append(f'[{img["role"]}] file: {file_name(a, img)}  size: {img_size(img)}')
            L.append(f'alt: {img["alt"]}')
            L.append(f'caption: {img["cap"]}')
            L.append(f'placement: {img["place"]}')
            L.append("PROMPT:")
            L.append(full_prompt(img))
        L.append("")
    return "\n".join(L)

def build_csv(path):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["#", "cluster", "h1", "seo_title", "meta_description", "focus_keyword", "secondary_keywords", "url",
                    "intent", "funnel", "demand_est", "difficulty_est", "priority", "target_words", "week"])
        week_of = {n: wk for wk, ns, _ in CALENDAR for n in ns}
        for a in ARTICLES:
            w.writerow([a["n"], a["cluster"], a["h1"], a["title"], a["meta"], a["kw"], " | ".join(a["kw2"]), url_of(a),
                        a["intent"], a["funnel"], a["demand"], a["kd"], a["prio"], a["words"], week_of[a["n"]]])

if __name__ == "__main__":
    doc = re.sub(r'(<table class="grid[^"]*"[^>]*>\s*)(<tr>.*?</tr>)', r'\1<thead>\2</thead>', build_html(), flags=re.S)
    open(os.path.join(OUT, "report.html"), "w", encoding="utf-8").write(doc)
    open(os.path.join(OUT, "iransorang-image-prompts-75.txt"), "w", encoding="utf-8").write(build_prompts_txt())
    build_csv(os.path.join(OUT, "iransorang-keyword-map-25.csv"))
    print("written")
