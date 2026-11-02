"""Generate the public, searchable two-page resume (requires reportlab)."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
FONT_ROOT=Path("/usr/share/fonts/truetype/dejavu")
pdfmetrics.registerFont(TTFont("Resume",str(FONT_ROOT/"DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Resume-Bold",str(FONT_ROOT/"DejaVuSans-Bold.ttf")))
pdfmetrics.registerFontFamily("Resume",normal="Resume",bold="Resume-Bold",italic="Resume",boldItalic="Resume-Bold")
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'output/pdf/Muhammad_Umar_Amin_Resume.pdf'
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
INK=colors.HexColor('#182a27'); GREEN=colors.HexColor('#275c45'); MUTED=colors.HexColor('#485b53')
styles={
'name':ParagraphStyle('Name',fontName='Resume-Bold',fontSize=23,leading=27,textColor=INK,spaceAfter=5),
'headline':ParagraphStyle('Headline',fontName='Resume-Bold',fontSize=11,leading=15,textColor=GREEN,spaceAfter=7),
'contact':ParagraphStyle('Contact',fontName='Resume',fontSize=9,leading=13,textColor=MUTED,spaceAfter=3),
'section':ParagraphStyle('Section',fontName='Resume-Bold',fontSize=10.5,leading=15,textColor=GREEN,spaceBefore=10,spaceAfter=7),
'role':ParagraphStyle('Role',fontName='Resume-Bold',fontSize=10.3,leading=14,textColor=INK,spaceAfter=2),
'meta':ParagraphStyle('Meta',fontName='Resume',fontSize=9.2,leading=13,textColor=MUTED,spaceAfter=5),
'body':ParagraphStyle('Body',fontName='Resume',fontSize=10,leading=13.5,textColor=INK,spaceAfter=6),
'bullet':ParagraphStyle('Bullet',fontName='Resume',fontSize=10,leading=13.3,textColor=INK,leftIndent=11,firstLineIndent=0,bulletIndent=0,spaceAfter=3),
}
story=[]
def para(text,style='body'):return Paragraph(text,styles[style])
def section(text):story.append(para(text.upper(),'section'))
def bullet(text):story.append(Paragraph(escape(text),styles['bullet'],bulletText='-'))
def role(title,company,dates,location,bullets):
 story.append(KeepTogether([para(escape(title+' | '+company),'role'),para(escape(dates+' | '+location),'meta')]))
 for b in bullets:bullet(b)
 story.append(Spacer(1,5))
def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#d5ddd6'));canvas.line(43,39,569,39)
 canvas.setFont('Resume',8);canvas.setFillColor(MUTED);canvas.drawString(43,26,'Muhammad Umar Amin | E-commerce & Analytics')
 canvas.drawRightString(569,26,f'{doc.page} / 2');canvas.restoreState()
story += [para('MUHAMMAD UMAR AMIN','name'),para('E-commerce Manager | Marketplace Strategy & Data Analytics','headline'),para('San Antonio, Texas | <a href="mailto:mamin14@lamar.edu" color="#275c45">mamin14@lamar.edu</a> | +1 409 333 5341','contact'),para('<a href="https://www.linkedin.com/in/muhammad-umar-amin-0a6795257/" color="#275c45">LinkedIn</a> | <a href="https://github.com/Muhammadumaramin" color="#275c45">GitHub</a> | <a href="https://muhammadumaramin.github.io/portfolio/" color="#275c45">muhammadumaramin.github.io/portfolio/</a>','contact')]
section('Professional summary')
story.append(para('E-commerce manager leading a six-person team across Amazon 1P/3P, Walmart, and multi-channel operations. Connects inventory, fulfillment, and customer experience with business analytics. M.S. Computational &amp; Quantitative Methods, Lamar University; GPA 4.00.'))
section('Core expertise')
for t in [
'<b>Marketplaces:</b> Amazon 1P/3P, Walmart WFS, eBay, Newegg, Shopify, Target Plus, Amazon International',
'<b>Operations:</b> FBA/WFS/FBM, Fishbowl, inventory reconciliation, listing QA, returns, account health, SOPs',
'<b>Analytics:</b> Excel, SQL, Power BI, Tableau, Python, R, forecasting, regression, A/B testing',
'<b>Commercial:</b> Buyer presentations, vendor negotiations, promotions, DTC journeys, CRM, subscriptions, SEO/GEO/AEO']:
 story.append(para(t))
section('Professional experience')
role('E-commerce Manager','Haifa Wholesale LLC','Jun 2026 - Present','San Antonio, TX',[
'Lead a six-person team across listings, fulfillment, returns, and account health in consumer electronics.',
'Manage Amazon 1P/3P, Walmart, eBay, Newegg, and other channels; support launches and catalog quality.',
'Coordinate FBA, WFS, and merchant fulfillment; investigate Fishbowl and marketplace inventory discrepancies.',
'Prepare weekly reviews and buyer presentations with Excel, SQL, and Power BI; support line reviews, planning, and annual vendor negotiations.',
'Support DTC customer journeys, CRM automation, subscriptions, and SEO/GEO/AEO.'])
role('Business Analyst - Data & Operations','ELAN RGV Wireless LLC','Jan 2026 - Jun 2026','Corpus Christi, TX',[
'Built operational reports and KPI summaries with Excel, SQL, and Power BI to support business reviews.',
'Tracked workflows in Asana and translated sales and operations data into practical updates.'])
role('Data Analytics Intern','Storied Data Inc.','Jun 2025 - Jul 2025','Remote',[
'Created credit spending and eye cancer dashboards and supported data reconciliation and reporting.',
'Used Excel, SQL, Power BI, and later Python and Streamlit to make analytical findings easier to explore.'])
story.append(PageBreak())
story += [para('MUHAMMAD UMAR AMIN','role'),para('E-commerce Manager | Additional experience, education & selected projects','meta')]
section('Additional professional experience')
role('Graduate Teaching Assistant','Lamar University','Fall 2024 - Dec 2025','Beaumont, TX',[
'Tutored pre-algebra through Calculus III, linear algebra, differential equations, and statistics in the Math Shop.',
'Supported MATH 2312 and MATH 1316 instruction; adapted explanations to different learning needs.'])
role('E-commerce Marketplace & Operations Lead','Ahmad Traders','Jul 2020 - Jul 2024','Wazirabad, Pakistan',[
'Managed marketplace and retail operations spanning Amazon, Walmart, eBay, Etsy, and Shopify.',
'Coordinated listings, inventory, customer service, and fulfillment across more than 1,200 SKUs and 200 monthly orders.',
'Used sales reporting and workflow improvements to support stock availability, order accuracy, and customer service.'])
section('Education')
story += [para('M.S. Computational &amp; Quantitative Methods | Lamar University','role'),para('2024 - 2025 | Completed December 2025 | GPA: 4.00 / 4.00','meta'),para('Coursework: time series analysis, regression, design of experiments, data mining, and statistical inference.'),para('B.S. Mathematics | University of Central Punjab','role'),para('2018 - 2022 | GPA: 3.66 / 4.00','meta'),para('DAE Electrical Technology | Faran Group of Institutes','role'),para('2014 - 2017 | A+ | 87.52%','meta')]
section('Selected academic projects')
for title,desc,url in [
('Walmart Weekly Sales Forecasting','Compared ARIMA and ARIMAX models to examine weekly sales patterns, seasonality, and external drivers.','Time_Series_Forecasting_of_Walmart_Sales'),
('Hydrocarbon Emissions Analysis','Examined temperature and pressure variables using regression, transformations, and model diagnostics.','Analysis_of_Hydrocarbon_Emissions'),
('Cirrhosis Death Rates','Explored skewness, outliers, and transformations as a basis for statistical inference.','Statistical-Cirrhosis-Death-Rates')]:
 story.append(para(f'<b>{title}:</b> {desc} <a href="https://github.com/Muhammadumaramin/{url}" color="#275c45">Repository</a>'))
section('Recognition & communication')
story.append(para('Phi Kappa Phi (2025) | Graduate panelist, Texas Undergraduate Mathematics Conference (2025)'))
story.append(para('Languages: English and Urdu.'))
doc=SimpleDocTemplate(str(OUTPUT),pagesize=letter,rightMargin=43,leftMargin=43,topMargin=37,bottomMargin=51,title='Muhammad Umar Amin - E-commerce Manager Resume',author='Muhammad Umar Amin',subject='Marketplace strategy, operations and quantitative analytics')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUTPUT)
